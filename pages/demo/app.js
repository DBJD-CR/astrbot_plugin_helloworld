// AstrBot 会在返回 HTML 时自动注入 bridge SDK，无需手动引入。
const bridge = window.AstrBotPluginPage;
const output = document.getElementById("output");

// 页面初始文案（英文 locale 下的回退文本）。
const PAGE_DEFAULTS = {
  heading: "Plugin Page Demo",
  desc: "A minimal plugin Page talking to the plugin backend via the AstrBotPluginPage bridge.",
  ping: "Ping",
  loading: "Loading...",
};

function render() {
  const locale = bridge.getLocale() || "zh-CN";
  document.documentElement.lang = locale;
  document.title = bridge.t("pages.demo.title", PAGE_DEFAULTS.heading);
  document.getElementById("heading").textContent = bridge.t(
    "pages.demo.heading",
    PAGE_DEFAULTS.heading,
  );
  document.getElementById("desc").textContent = bridge.t(
    "pages.demo.desc",
    PAGE_DEFAULTS.desc,
  );
  document.getElementById("ping").textContent = bridge.t(
    "pages.demo.ping",
    PAGE_DEFAULTS.ping,
  );
  if (!output.textContent || output.textContent === PAGE_DEFAULTS.loading) {
    output.textContent = bridge.t("pages.demo.loading", PAGE_DEFAULTS.loading);
  }
}

// 等待 bridge 就绪并获取初始上下文（插件名、Page 名、locale、isDark 等）。
await bridge.ready();
render();

// 响应 WebUI 语言 / 主题切换。
bridge.onContext(render);

document.getElementById("ping").addEventListener("click", async () => {
  try {
    // endpoint 为插件内相对路径，Dashboard 会转发到插件注册的后端 API。
    const result = await bridge.apiGet("ping", { limit: 20 });
    output.textContent = JSON.stringify(result, null, 2);
  } catch (error) {
    output.textContent = `Error: ${error.message}`;
  }
});
