 # Vision Assist MCP 部署说明
 
 ## 1. 环境要求
 
 - Python 3.8+
 - `requests` 包：`pip install -r requirements.txt`
 - 一个可用的 vision provider API key（OpenAI / Gemini / Anthropic 或兼容 OpenAI 格式的服务）
 - Node.js（Codex、Claude Code、OpenCode 自身都基于 Node，所以通常已自带）
 
 ## 2. 配置 API key
 
 用 CLI 配置（推荐）：
 
 ```powershell
cd <SKILL_DIR>
python scripts\vision_assist.py config --set openai.api_key YOUR_KEY
python scripts\vision_assist.py config --use openai
python scripts\vision_assist.py config --check-key
 ```
 
 也可以直接编辑 `scripts/config.json`（注意保密，不要上传到仓库）。
 
 ## 3. 在各客户端中启用
 
 项目里已经按不同客户端的约定放好了配置文件：
 
 | 客户端 | 配置文件 |
 |---|---|
 | Codex | `.mcp.json` |
 | Claude Code | `.claude/mcp.json` |
 | OpenCode / VS Code 类 | `.vscode/mcp.json` |
 | 其他 MCP 客户端 | 复制 `.mcp.json` 里的 `mcpServers.vision-assist` 块到对应配置 |
 
 所有配置文件都使用 `mcp/run.mjs` 作为入口。`run.mjs` 会自动寻找可用的 Python 解释器，
 所以只要 Node 在 PATH 里，就能直接启动 server。
 
 如果找不到 Python，可以设置环境变量：
 
 ```powershell
 $env:VISION_ASSIST_PYTHON = "C:\Path\To\python.exe"
 ```
 
 加载成功后，发送包含图片路径、URL 或 base64 数据 URI 的消息时，模型会自动调用 `vision_assist` tool。
 
 示例消息：
 
 ```text
 请描述一下 project/assets/screenshot.png 里的内容
 ```
 
 也支持直接传 base64 数据 URI：
 
 ```text
 data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mP8z8BQDwAEhQGAhKmMIQAAAABJRU5ErkJggg==
 ```
 
 如果客户端没有自动识别，尝试重新加载窗口或重启客户端。
 
 ## 4. 验证 server 是否正常
 
 手动启动 server 并发送 JSON-RPC 测试：
 
 ```powershell
 $init = '{"jsonrpc":"2.0","id":1,"method":"initialize","params":{"protocolVersion":"2024-11-05"}}'
 $tools = '{"jsonrpc":"2.0","id":2,"method":"tools/list"}'
 "$init`n$tools" | node mcp/run.mjs
 ```
 
 能看到 `vision_assist` 等 tools 列表即表示 server 正常。
 
 ## 5. 在其他 MCP 客户端使用
 
 把 `.mcp.json` 里的 `mcpServers.vision-assist` 块复制到对应客户端的 MCP 配置里即可。例如 Claude Desktop 的 `claude_desktop_config.json`：
 
 ```json
 {
   "mcpServers": {
     "vision-assist": {
       "command": "node",
       "args": [
          "C:/Users/pleia/OneDrive/PROJECT/pleia-skills/vision-assist-mcp/mcp/run.mjs"
       ]
     }
   }
 }
 ```
 
 ## 6. 常见问题
 
 - **提示找不到 `python`**：`run.mjs` 会按 PATH、常见安装路径、Codex 自带 runtime 的顺序查找 Python。如果仍找不到，设置 `VISION_ASSIST_PYTHON` 环境变量。
 - **报 `No module named requests`**：运行 `pip install -r requirements.txt`。
 - **调用图片失败/路径不存在**：server 以仓库根目录为工作目录，图片路径建议写相对路径或完整绝对路径。
 - **API key 校验失败**：用 `python scripts/vision_assist.py config --check-key` 或 `vision_preflight` tool 检查。
 - **base64 图片被当成路径**：确保使用标准 data URI 格式 `data:image/png;base64,XXXX`，不要只传裸 base64 字符串。
