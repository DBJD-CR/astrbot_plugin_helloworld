// AstrBot 会在返回 HTML 时自动注入 bridge SDK，无需手动引入。
const bridge = window.AstrBotPluginPage;
const output = document.getElementById("output");

function render() {
  document.getElementById("heading").textContent = bridge.t(
    "pages.demo.heading",
    "Plugin Page Demo",
  );
  document.getElementById("ping").textContent = bridge.t(
    "pages.demo.ping",
    "Ping",
  );
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
