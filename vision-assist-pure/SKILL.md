 ---
 name: vision-assist-pure
 description: >
   Analyze images and answer visual questions (pure skill version, no MCP).
   Use PROACTIVELY whenever the user's message contains an image file path (any extension:
   .jpg, .jpeg, .png, .gif, .webp, .bmp, etc.), an image URL, or a base64 data URI —
   regardless of what language the user writes in or how they phrase the request.
   Do not read images with file tools; always use this skill instead.
 ---
 
 # Vision Assist (Pure Skill)
 
 This is the standalone skill version of Vision Assist. It runs as a regular CLI script
 instead of an MCP server. Use it in environments where MCP is not available.
 
 ## Usage
 
 > **IMPORTANT**: `scripts/vision_assist.py` is a relative path inside this skill's directory.
 > When this skill is invoked, use the base directory shown by the system and `cd` into it
 > before calling the script.
 
 ```bash
 cd "<base_dir>"
 python scripts/vision_assist.py ask -p "Describe everything visible." -i /path/to/image.jpg
 ```
 
 Examples:
 
 ```bash
 # Describe image contents
 python scripts/vision_assist.py ask -p "Describe everything visible in this image in detail." -i /path/to/image.jpg
 
 # OCR
 python scripts/vision_assist.py ask -p "Transcribe every line of visible text verbatim." -i sign.jpg
 
 # Compare two images
 python scripts/vision_assist.py ask -p "Image 1 is the reference, Image 2 is the candidate. List every difference." -i a.png b.png
 
 # Image URL
 python scripts/vision_assist.py ask -p "Describe" -i https://example.com/pic.jpg
 
 # Base64 data URI
 python scripts/vision_assist.py ask -p "Describe" -i "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mP8z8BQDwAEhQGAhKmMIQAAAABJRU5ErkJggg=="
 
 # Retry and proxy options
 python scripts/vision_assist.py ask -p "..." -i img.png --retry 3 --no-proxy
 ```
 
 | Flag | Default | Description |
 |---|---|---|
 | `--prompt` / `-p` | required | What you want to know about the image(s) |
 | `--image` / `-i` | required | One or more image paths, `http(s)://` URLs, or base64 data URIs |
 | `--retry` | `1` | Max attempts with exponential backoff |
 | `--no-proxy` | off | Bypass system proxy (SSL fixes) |
 | `--provider` | active | Override active provider for this call |
 | `--model` | configured | Override configured model for this call |
 
 ## Configuration
 
 Copy `scripts/config.example.json` to `scripts/config.json` and fill in your API key, or use the CLI:
 
 ```bash
 python scripts/vision_assist.py config --set openai.api_key YOUR_KEY
 python scripts/vision_assist.py config --use openai
 python scripts/vision_assist.py config --check-key
 ```
 
 Run `python scripts/vision_assist.py config --help` for the full configuration surface.
 
 ## How to construct the prompt
 
 **Never pass the user's words directly as the prompt.** Infer intent from context and write a focused vision-model prompt.
 
 | User intent | Prompt to use |
 |---|---|
 | General viewing / "look at this" | `"Describe everything visible: scene, people, objects, actions, and all text."` |
 | Verify or fact-check claims in an image | `"Describe the full scene and transcribe all visible text verbatim."` |
 | Specific question about the image | Translate the user's question into a focused vision-model prompt |
 | OCR only | `"Transcribe every line of visible text verbatim, preserving line breaks."` |
 | Compare images | `"Image 1 is the reference, Image 2 is the candidate. List every visual difference."` |
 
 **Default when unsure**: ask for both scene description and all visible text.
 
 ## Security: never read config.json directly
 
 `scripts/config.json` contains API keys in plaintext. To check whether a key is configured,
 use the CLI commands above; they mask key values. Never expose the raw file contents.
 
 ## If you hit "api_key not configured"
 
 The user hasn't set up a provider yet. Ask them to run:
 
 ```bash
 python scripts/vision_assist.py config --set <provider>.api_key YOUR_KEY
 python scripts/vision_assist.py config --use <provider>
 ```
