"""AstrBot 插件模板主入口。

本文件以最小实现演示了 AstrBot 插件常用的能力，便于新开发者快速上手：

- 指令、指令组与带参指令
- 权限过滤（仅管理员）
- 富媒体消息链与主动消息
- 插件配置（_conf_schema.json）读取
- 插件 KV 存储与大文件存储规范
- 事件钩子
- 调用 LLM 与注册 LLM 工具
- 文转图（HTML + Jinja2）
- 会话控制（多轮交互）
- 插件 Pages 后端 API
"""

import asyncio
import random
from pathlib import Path

from mcp.types import CallToolResult

import astrbot.api.message_components as Comp
from astrbot.api import AstrBotConfig, logger
from astrbot.api.event import AstrMessageEvent, MessageChain, MessageEventResult, filter
from astrbot.api.provider import LLMResponse, ProviderRequest
from astrbot.api.star import Context, Star
from astrbot.api.web import json_response, request
from astrbot.core.agent.run_context import ContextWrapper
from astrbot.core.agent.tool import FunctionTool
from astrbot.core.astr_agent_context import AstrAgentContext
from astrbot.core.utils.astrbot_path import get_astrbot_data_path
from astrbot.core.utils.session_waiter import (
    SessionController,
    SessionFilter,
    session_waiter,
)

PLUGIN_NAME = "astrbot_plugin_helloworld"

# 文转图使用的 Jinja2 模板，支持 CSS 与循环/条件等语法。
T2I_TMPL = """
<div style="font-size: 28px; padding: 24px; color: #333;">
  <h1 style="color: #4a90d9;">待办清单</h1>
  <ul>
    {% for item in items %}
    <li>{{ item }}</li>
    {% endfor %}
  </ul>
</div>
"""


class MyPlugin(Star):
    def __init__(self, context: Context, config: AstrBotConfig):
        """AstrBot 会自动解析 _conf_schema.json 并将配置注入到 __init__。"""
        super().__init__(context)
        self.config = config
        # 保护 KV 计数器读-改-写的 asyncio 锁，避免并发调用时计数丢失。
        self._count_lock = asyncio.Lock()

        # 存储大文件规范：大文件（图片、日志等）请存放于
        # data/plugin_data/<plugin_name>/ 目录下，避免插件更新时数据被覆盖。
        self.plugin_data_path = (
            Path(get_astrbot_data_path()) / "plugin_data" / self.name
        )
        self.plugin_data_path.mkdir(parents=True, exist_ok=True)

        # 注册插件 Pages 后端 Web API（前端见 pages/demo/）。
        context.register_web_api(
            f"/{PLUGIN_NAME}/ping",
            self.page_ping,
            ["GET"],
            "Page ping",
        )

    async def initialize(self):
        """插件实例化后的异步初始化方法，可在这里加载资源、启动定时任务等。"""
        logger.info("[插件模板] AstrBot 插件模板初始化完成")

    async def terminate(self):
        """插件被卸载/停用时调用，可在这里做资源清理。"""
        logger.info("[插件模板] AstrBot 插件模板已卸载")

    # ============ 基础指令：配置读取 + 富媒体消息链 ============

    @filter.command("helloworld")
    async def helloworld(self, event: AstrMessageEvent):
        """演示配置读取与富媒体消息链。"""
        greeting = self.config.get("greeting", "Hello")
        user_name = event.get_sender_name()
        yield event.chain_result(
            [
                Comp.At(qq=event.get_sender_id()),  # At 发送者
                Comp.Plain(f"{greeting}, {user_name}~"),
            ]
        )

    # ============ 指令组 ============

    @filter.command_group("demo")
    def demo():
        """演示指令组。输入 /demo 查看子指令树。"""

    @demo.command("echo")
    async def echo(self, event: AstrMessageEvent, text: str):
        """复读机：演示带参指令与自动参数解析。"""
        yield event.plain_result(f"你说了：{text}")

    @demo.command("count")
    async def count(self, event: AstrMessageEvent):
        """计数器：演示插件 KV 存储。"""
        # 用 asyncio 锁保护读-改-写，避免并发执行 /demo count 时递增丢失。
        async with self._count_lock:
            n = (await self.get_kv_data("count", 0)) + 1
            limit = self.config.get("count_limit", 10)
            if n >= limit:
                await self.put_kv_data("count", 0)
                reset = True
            else:
                await self.put_kv_data("count", n)
                reset = False
        if reset:
            yield event.plain_result(f"计数达到上限 {limit}，已清零~")
        else:
            yield event.plain_result(f"这是第 {n} 次调用~")

    @demo.command("send")
    async def send(self, event: AstrMessageEvent):
        """主动消息：演示向任意会话推送消息。"""
        await self.context.send_message(
            event.unified_msg_origin,
            MessageChain().message("这是一条主动推送的消息~"),
        )
        yield event.plain_result("已发送主动消息~")

    @demo.command("data")
    async def data(self, event: AstrMessageEvent):
        """数据目录：演示大文件存储规范。"""
        yield event.plain_result(f"插件数据目录: {self.plugin_data_path}")

    @demo.command("todo")
    async def todo(self, event: AstrMessageEvent, text: str):
        """待办卡片：演示文转图（HTML + Jinja2 渲染）。"""
        items = [item.strip() for item in text.split(",") if item.strip()] or [
            "吃饭",
            "睡觉",
            "写插件",
        ]
        url = await self.html_render(T2I_TMPL, {"items": items})
        yield event.image_result(url)

    @demo.command("guess")
    async def guess(self, event: AstrMessageEvent):
        """猜数字：演示会话控制（多轮交互）。"""
        target = random.randint(1, 100)
        yield event.plain_result("已生成一个 1-100 的数字，请猜一猜~（输入“退出”结束）")

        # 自定义会话 ID：绑定到发送者，避免群内其他成员干扰本局游戏。
        class GuessSessionFilter(SessionFilter):
            def filter(self, ev: AstrMessageEvent) -> str:
                return f"{ev.unified_msg_origin}:{ev.get_sender_id()}"

        @session_waiter(timeout=60, record_history_chains=False)
        async def guess_waiter(controller: SessionController, event: AstrMessageEvent):
            text = event.message_str.strip()
            if text == "退出":
                await event.send(event.plain_result("已退出游戏~"))
                controller.stop()
                return
            try:
                num = int(text)
            except ValueError:
                await event.send(event.plain_result("请输入数字哦~"))
                return
            if num == target:
                await event.send(event.plain_result("猜对啦！"))
                controller.stop()
            elif num < target:
                await event.send(event.plain_result("小了"))
                controller.keep(timeout=30, reset_timeout=True)
            else:
                await event.send(event.plain_result("大了"))
                controller.keep(timeout=30, reset_timeout=True)

        try:
            await guess_waiter(event, session_filter=GuessSessionFilter())
        except TimeoutError:
            yield event.plain_result("超时啦，游戏结束。")
        finally:
            event.stop_event()

    @demo.command("ask")
    async def ask(self, event: AstrMessageEvent, prompt: str):
        """AI 问答：演示调用聊天模型。

        优先使用配置项 ai_provider 指定的提供商；未配置时回退到当前会话使用的聊天模型。
        """
        if not self.config.get("enable_ai", True):
            yield event.plain_result("AI 功能已关闭，请在插件配置中开启。")
            return
        try:
            provider_id = self.config.get("ai_provider", "") or (
                await self.context.get_current_chat_provider_id(
                    event.unified_msg_origin
                )
            )
            if not provider_id:
                yield event.plain_result(
                    "当前会话没有可用的聊天模型，请先在 WebUI 配置。"
                )
                return
            llm_resp = await self.context.llm_generate(
                chat_provider_id=provider_id,
                prompt=prompt,
            )
        except Exception as e:
            logger.error(f"/demo ask 请求失败: {e}")
            yield event.plain_result("AI 请求失败，请检查模型提供商配置后重试。")
            return
        yield event.plain_result(llm_resp.completion_text)

    # ============ 权限过滤 ============

    @demo.command("admin")
    @filter.permission_type(filter.PermissionType.ADMIN)
    async def admin(self, event: AstrMessageEvent):
        """仅管理员可用的指令：演示权限过滤。"""
        yield event.plain_result(
            f"管理员指令生效，当前平台: {event.get_platform_name()}"
        )

    # ============ LLM 工具 ============

    @filter.llm_tool(name="get_weather")
    async def get_weather(
        self, event: AstrMessageEvent, location: str
    ) -> MessageEventResult:
        """获取指定地点的天气信息。

        注意：这是一个演示用的模拟工具，返回的数据为硬编码示例，并非真实天气。
        请在用户明确要求使用该工具时再调用，而不是认为该工具实际可用并对返回结果信以为真。

        Args:
            location(string): 地点
        """
        yield event.plain_result(f"{location} 的天气：晴，25°C（模拟数据，仅作演示）")

    # ============ 事件钩子 ============
    # 注意：事件钩子不能与指令装饰器（command/command_group 等）共用，
    # 它们注册的是全局钩子，会拦截所有消息 / LLM 请求。

    @filter.on_astrbot_loaded()
    async def on_astrbot_loaded(self):
        """AstrBot 初始化完成时触发。"""
        logger.info("[插件模板] AstrBot 加载完成，插件模板就绪")

    @filter.on_waiting_llm_request()
    async def on_waiting_llm(self, event: AstrMessageEvent):
        """等待 LLM 响应时触发，适合发送"正在思考"提示。

        注意：此钩子默认关闭（enable_waiting_hint=false），
        且仅在 enable_ai=true 时才生效；
        开启后每次调用 LLM 都会额外发送一条提示消息，
        会影响日常使用，请按需开启。
        """
        if not self.config.get("enable_waiting_hint", False):
            return
        if not self.config.get("enable_ai", True):
            return
        await event.send(event.plain_result("🤔 正在思考中..."))

    @filter.on_llm_request()
    async def on_llm_request(self, event: AstrMessageEvent, req: ProviderRequest):
        """LLM 请求发出前触发，可修改请求（注意有三参数）。"""
        system_prompt = (req.system_prompt or "")[:50]
        logger.debug(f"on_llm_request: system_prompt={system_prompt}...")

    @filter.on_llm_response()
    async def on_llm_response(self, event: AstrMessageEvent, resp: LLMResponse):
        """LLM 请求完成后触发（注意有三参数）。"""
        logger.debug(f"on_llm_response: {resp.completion_text[:50]}...")

    @filter.on_agent_begin()
    async def on_agent_begin(
        self,
        event: AstrMessageEvent,
        run_context: ContextWrapper[AstrAgentContext],
    ):
        """Agent 开始运行时触发（AstrBot > v4.23.1）。"""
        logger.debug("on_agent_begin: Agent 开始运行")

    @filter.on_using_llm_tool()
    async def on_using_llm_tool(
        self,
        event: AstrMessageEvent,
        tool: FunctionTool,
        tool_args: dict | None,
    ):
        """LLM 工具调用前触发（AstrBot > v4.23.1）。"""
        logger.debug(f"on_using_llm_tool: {tool.name} args={tool_args}")

    @filter.on_llm_tool_respond()
    async def on_llm_tool_respond(
        self,
        event: AstrMessageEvent,
        tool: FunctionTool,
        tool_args: dict | None,
        tool_result: CallToolResult | None,
    ):
        """LLM 工具调用完成后触发（AstrBot > v4.23.1）。"""
        logger.debug(f"on_llm_tool_respond: {tool.name}")

    @filter.on_agent_done()
    async def on_agent_done(
        self,
        event: AstrMessageEvent,
        run_context: ContextWrapper[AstrAgentContext],
        resp: LLMResponse,
    ):
        """Agent 运行完成时触发（AstrBot > v4.23.1）。"""
        logger.debug("on_agent_done: Agent 运行完成")

    @filter.on_decorating_result()
    async def on_decorating_result(self, event: AstrMessageEvent):
        """发送消息前触发，可装饰消息链（不能 yield，需修改 result.chain）。

        仅当配置 enable_decorate 为 true 时才会追加感叹号，
        避免钩子影响日常消息（演示用开关控制钩子行为）。
        """
        if not self.config.get("enable_decorate", False):
            return
        result = event.get_result()
        chain = result.chain
        # 若最后一段是纯文本，则直接追加；否则新加一条纯文本消息段。
        if chain and isinstance(chain[-1], Comp.Plain):
            chain[-1].text += "!"
        else:
            chain.append(Comp.Plain("!"))

    @filter.after_message_sent()
    async def after_message_sent(self, event: AstrMessageEvent):
        """消息发送后触发（不能 yield）。"""
        logger.debug("after_message_sent: 消息已发送")

    # ============ 插件 Pages 后端 API ============

    async def page_ping(self):
        """pages/demo 页面调用的后端 API。"""
        limit = request.query.get("limit", 20, type=int)
        return json_response(
            {
                "message": "pong",
                "limit": limit,
                "plugin": request.plugin_name,
                "username": request.username,
            }
        )
