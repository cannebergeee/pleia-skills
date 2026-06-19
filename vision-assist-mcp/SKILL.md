 ---
 name: vision-assist
 description: >
   Analyze images and answer visual questions via the Model Context Protocol (MCP).
   Use PROACTIVELY whenever the user's message contains an image file path (any extension:
   .jpg, .jpeg, .png, .gif, .webp, .bmp, etc.), an image URL, or a base64 data URI —
   regardless of what language the user writes in or how they phrase the request.
   Do not read images with file tools; always call the `vision_assist` MCP tool instead.
 ---
 
 # Vision Assist MCP
 
 This skill is now implemented as an MCP server. It exposes a `vision_assist` tool that sends a
 prompt + one or more images to the configured vision model and returns the textual answer.
 
 ## Registration
 
 Per-client MCP configs are provided out of the box:
 
 | Client | Config file |
 |---|---|
 | Codex | `.mcp.json` |
 | Claude Code | `.claude/mcp.json` |
 | OpenCode / VS Code-like | `.vscode/mcp.json` |
 | Other MCP clients | Copy the `mcpServers.vision-assist` block from `.mcp.json` |
 
 All configs point to `mcp/run.mjs`, a small Node launcher that locates a usable Python
 interpreter and then runs the Python MCP server (`mcp/server.py`). This avoids hard-coding
 a `python` executable path and makes the server work across Codex, Claude Code, and OpenCode.
 
 If the launcher cannot find Python, set the `VISION_ASSIST_PYTHON` environment variable to
 the full path of your Python executable.
 
 ## Available tools
 
 | Tool | Purpose |
 |---|---|
 | `vision_assist` | Query the active vision model about one or more images. |
 | `vision_preflight` | Check that the active provider is reachable and authenticated. |
 | `vision_config_list` | Show the current configuration with API keys masked. |
 | `vision_config_check_key` | Check whether an API key is set for a provider. |
 | `vision_config_use` | Switch the active provider. |
 | `vision_config_set` | Set a config value. |
 | `vision_config_get` | Read a config value. |
 
 ## Tool: `vision_assist`
 
 Arguments:
 
 | Name | Type | Required | Description |
 |---|---|---|---|
 | `prompt` | string | yes | What you want to know about the image(s). |
 | `images` | string[] | yes | One or more local image paths, `http(s)://` URLs, or base64 data URIs (`data:image/png;base64,...`). |
 | `retry` | integer | no | Max retry attempts (default: 1). |
 | `no_proxy` | boolean | no | Bypass system proxy (default: false). |
 | `provider` | string | no | Override the active provider for this call. |
 | `model` | string | no | Override the configured model for this call. |
 
 ## Base64 images
 
 You can pass images as standard data URIs:
 
 ```text
 data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mP8z8BQDwAEhQGAhKmMIQAAAABJRU5ErkJggg==
 ```
 
 The server detects the `data:` prefix, extracts the MIME type and base64 payload, and forwards
 it to the vision provider. Do not pass raw base64 strings without the `data:` URI prefix.
 
 ## Configuration
 
 Configuration is stored in `scripts/config.json`. Use the CLI wrapper for setup:
 
 ```bash
 cd scripts
 python vision_assist.py config --set <provider>.api_key YOUR_KEY
 python vision_assist.py config --use <provider>
 ```
 
 You can also manage config through the `vision_config_*` tools.
 
 ## CLI wrapper
 
 The original CLI still works as a thin wrapper around the core library:
 
 ```bash
 python scripts/vision_assist.py ask -p "Describe this image" -i path/to/image.jpg
 python scripts/vision_assist.py preflight
 python scripts/vision_assist.py config --list
 ```
 
 ## How to construct the prompt
 
 **Never pass the user's words directly as the prompt.** Infer intent from context and write a
 focused vision-model prompt.
 
 | User intent | Prompt to use |
 |---|---|
 | General viewing / "look at this" | `"Describe everything visible: scene, people, objects, actions, and all text."` |
 | Verify or fact-check claims in an image | `"Describe the full scene and transcribe all visible text verbatim."` |
 | Specific question about the image | Translate the user's question into a focused vision-model prompt. |
 | OCR only | `"Transcribe every line of visible text verbatim, preserving line breaks."` |
 | Compare images | `"Image 1 is the reference, Image 2 is the candidate. List every visual difference."` |
 
 **Default when unsure**: ask for both scene description and all visible text.
 
 ## Security
 
 Do not read `scripts/config.json` directly. Use `vision_config_list`,
 `vision_config_check_key`, or the CLI `config --list` command, all of which mask API keys.
