#!/usr/bin/env python3
"""Vision Assist MCP server - stdio JSON-RPC."""

import json
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)

import scripts.vision_core as core

SERVER_NAME = "Vision Assist MCP"
SERVER_VERSION = "1.0.0"
PROTOCOL_VERSION = "2024-11-05"

METHOD_NOT_FOUND = -32601
INVALID_PARAMS = -32602
INTERNAL_ERROR = -32603


def send(message):
   line = json.dumps(message, ensure_ascii=False)
   sys.stdout.buffer.write((line + "\n").encode("utf-8"))
   sys.stdout.buffer.flush()


def send_result(request_id, result):
   send({"jsonrpc": "2.0", "id": request_id, "result": result})


def send_error(request_id, code, message):
   send({"jsonrpc": "2.0", "id": request_id, "error": {"code": code, "message": message}})


def tool_result(text, is_error=False):
   return {
       "content": [{"type": "text", "text": text}],
       "isError": is_error,
   }


def handle_vision_assist(args):
   prompt = args.get("prompt")
   images = args.get("images")
   if not prompt or not isinstance(prompt, str):
       raise ValueError("'prompt' is required and must be a string")
   if not images or not isinstance(images, list) or not all(isinstance(i, str) for i in images):
       raise ValueError("'images' is required and must be a list of strings")
   retry = int(args.get("retry", 1))
   no_proxy = bool(args.get("no_proxy", False))
   provider = args.get("provider") or None
   model = args.get("model") or None
   return core.ask(
       prompt=prompt,
       image_paths=images,
       retry=retry,
       no_proxy=no_proxy,
       override_provider=provider,
       override_model=model,
   )


def handle_preflight(args):
   result = core.preflight(
       quick=bool(args.get("quick", False)),
       no_proxy=bool(args.get("no_proxy", False)),
       override_provider=args.get("provider") or None,
   )
   return json.dumps(result, indent=2, ensure_ascii=False)


def handle_config_list(_args):
   return json.dumps(core.config_list(masked=True), indent=2, ensure_ascii=False)


def handle_config_check_key(args):
   info = core.config_check_key(args.get("provider") or None)
   return json.dumps(info, indent=2, ensure_ascii=False)


def handle_config_use(args):
   provider = args.get("provider")
   if not provider:
       raise ValueError("'provider' is required")
   return core.config_use(provider)


def handle_config_set(args):
   key = args.get("key")
   value = args.get("value")
   if key is None or value is None:
       raise ValueError("'key' and 'value' are required")
   return core.set_config_value(key, value)


def handle_config_get(args):
   key = args.get("key")
   if not key:
       raise ValueError("'key' is required")
   val = core.get_config_value(key)
   return f"{key}: {val}"


TOOLS = [
   {
       "name": "vision_assist",
       "title": "Vision Assist",
       "description": (
           "Analyze images and answer visual questions. Use PROACTIVELY whenever the user's message "
           "contains an image file path (any extension: .jpg, .jpeg, .png, .gif, .webp, .bmp, etc.) "
           "or an image URL - regardless of language or phrasing. Images may also be supplied as "
           "base64 data URIs (data:image/png;base64,...). Do not read image files directly; always "
           "call this tool instead. Handles describing image contents, transcribing visible text, "
           "comparing multiple images, verifying visual details, and answering any question about what an image shows."
       ),
       "inputSchema": {
           "type": "object",
           "properties": {
               "prompt": {
                   "type": "string",
                   "description": "What to ask the vision model about the image(s).",
               },
               "images": {
                   "type": "array",
                   "items": {"type": "string"},
                   "description": "One or more local image paths, http(s) URLs, or base64 data URIs (data:image/...;base64,...).",
               },
               "retry": {
                   "type": "integer",
                   "default": 1,
                   "description": "Max retry attempts with exponential backoff.",
               },
               "no_proxy": {
                   "type": "boolean",
                   "default": False,
                   "description": "Bypass system proxy.",
               },
               "provider": {
                   "type": "string",
                   "description": "Override the active provider for this call.",
               },
               "model": {
                   "type": "string",
                   "description": "Override the configured model for this call.",
               },
           },
           "required": ["prompt", "images"],
       },
       "annotations": {
           "readOnlyHint": False,
           "destructiveHint": False,
           "idempotentHint": True,
           "openWorldHint": True,
       },
   },
   {
       "name": "vision_preflight",
       "title": "Vision Assist Preflight",
       "description": "Check that the active vision provider is reachable and authenticated.",
       "inputSchema": {
           "type": "object",
           "properties": {
               "quick": {"type": "boolean", "default": False},
               "no_proxy": {"type": "boolean", "default": False},
               "provider": {"type": "string"},
           },
       },
       "annotations": {
           "readOnlyHint": True,
           "destructiveHint": False,
           "idempotentHint": True,
           "openWorldHint": False,
       },
   },
   {
       "name": "vision_config_list",
       "title": "Vision Assist Config List",
       "description": "Show the current configuration with API keys masked.",
       "inputSchema": {"type": "object"},
       "annotations": {
           "readOnlyHint": True,
           "destructiveHint": False,
           "idempotentHint": True,
           "openWorldHint": False,
       },
   },
   {
       "name": "vision_config_check_key",
       "title": "Vision Assist Check API Key",
       "description": "Check whether the configured API key is set for a provider.",
       "inputSchema": {
           "type": "object",
           "properties": {
               "provider": {"type": "string", "description": "Provider name (defaults to active provider)."},
           },
       },
       "annotations": {
           "readOnlyHint": True,
           "destructiveHint": False,
           "idempotentHint": True,
           "openWorldHint": False,
       },
   },
   {
       "name": "vision_config_use",
       "title": "Vision Assist Use Provider",
       "description": "Switch the active provider.",
       "inputSchema": {
           "type": "object",
           "properties": {
               "provider": {"type": "string"},
           },
           "required": ["provider"],
       },
       "annotations": {
           "readOnlyHint": False,
           "destructiveHint": False,
           "idempotentHint": False,
           "openWorldHint": False,
       },
   },
   {
       "name": "vision_config_set",
       "title": "Vision Assist Config Set",
       "description": "Set a config value. KEY may be 'active_provider', '<provider>.<field>', or '<field>' (writes to active provider).",
       "inputSchema": {
           "type": "object",
           "properties": {
               "key": {"type": "string"},
               "value": {"type": "string"},
           },
           "required": ["key", "value"],
       },
       "annotations": {
           "readOnlyHint": False,
           "destructiveHint": False,
           "idempotentHint": False,
           "openWorldHint": False,
       },
   },
   {
       "name": "vision_config_get",
       "title": "Vision Assist Config Get",
       "description": "Read a config value. KEY rules are the same as vision_config_set.",
       "inputSchema": {
           "type": "object",
           "properties": {
               "key": {"type": "string"},
           },
           "required": ["key"],
       },
       "annotations": {
           "readOnlyHint": True,
           "destructiveHint": False,
           "idempotentHint": True,
           "openWorldHint": False,
       },
   },
]


HANDLERS = {
   "vision_assist": handle_vision_assist,
   "vision_preflight": handle_preflight,
   "vision_config_list": handle_config_list,
   "vision_config_check_key": handle_config_check_key,
   "vision_config_use": handle_config_use,
   "vision_config_set": handle_config_set,
   "vision_config_get": handle_config_get,
}


def handle_tool_call(request_id, params):
   name = params.get("name")
   arguments = params.get("arguments", {})
   if name not in HANDLERS:
       send_error(request_id, INVALID_PARAMS, f"Unknown tool: {name}")
       return
   try:
       text = HANDLERS[name](arguments)
       send_result(request_id, tool_result(str(text), is_error=False))
   except (core.ConfigError, core.VisionError, ValueError) as e:
       send_result(request_id, tool_result(str(e), is_error=True))
   except Exception as e:
       send_result(request_id, tool_result(f"Internal error: {e}", is_error=True))


def handle_request(msg):
   request_id = msg.get("id")
   method = msg.get("method")
   params = msg.get("params", {})

   if method == "initialize":
       send_result(request_id, {
           "protocolVersion": params.get("protocolVersion", PROTOCOL_VERSION),
           "capabilities": {"tools": {}},
           "serverInfo": {
               "name": SERVER_NAME,
               "version": SERVER_VERSION,
           },
           "instructions": (
               "You have access to the vision_assist tool. "
               "Use it proactively whenever the user's message contains an image file path or URL and they want to "
               "view, describe, transcribe, compare, verify, or ask anything about the image. "
               "Do not read image files directly with file tools; route them through vision_assist."
           ),
       })
       return

   if method == "ping":
       send_result(request_id, {})
       return

   if method == "tools/list":
       send_result(request_id, {"tools": TOOLS})
       return

   if method == "tools/call":
       handle_tool_call(request_id, params)
       return

   if request_id is not None:
       send_error(request_id, METHOD_NOT_FOUND, f"Method not found: {method}")


def main():
   try:
       for raw in sys.stdin.buffer:
           line = raw.decode("utf-8").strip()
           if not line:
               continue
           try:
               msg = json.loads(line)
           except json.JSONDecodeError:
               continue
           handle_request(msg)
   except KeyboardInterrupt:
       pass


if __name__ == "__main__":
   main()
