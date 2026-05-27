#!/usr/bin/env python3
"""Call Xiaomi MiMo web_search through chat completions and emit JSON."""

from __future__ import annotations

import argparse
import json
import os
import sys
import urllib.error
import urllib.request


DEFAULT_BASE_URL = "https://api.xiaomimimo.com/v1"
DEFAULT_MODEL = "mimo-v2.5-pro"


def parse_location(raw: str | None) -> dict[str, str] | None:
    if not raw:
        return None
    try:
        value = json.loads(raw)
    except json.JSONDecodeError as exc:
        raise SystemExit(f"--location must be JSON: {exc}") from exc
    if not isinstance(value, dict):
        raise SystemExit("--location must be a JSON object")
    if "type" not in value:
        value["type"] = "approximate"
    return value


def extract_message(data: dict) -> dict:
    choices = data.get("choices") or []
    if not choices:
        return {}
    first = choices[0] or {}
    return first.get("message") or {}


def normalize_citations(message: dict) -> list[dict]:
    citations = []
    for item in message.get("annotations") or []:
        if not isinstance(item, dict):
            continue
        citations.append(
            {
                "type": item.get("type"),
                "title": item.get("title"),
                "url": item.get("url"),
                "site_name": item.get("site_name"),
                "publish_time": item.get("publish_time"),
                "summary": item.get("summary"),
                "logo_url": item.get("logo_url"),
            }
        )
    return citations


def build_payload(args: argparse.Namespace) -> dict:
    tool = {
        "type": "web_search",
        "max_keyword": args.max_keyword,
        "force_search": args.force_search,
        "limit": args.limit,
    }
    location = parse_location(args.location)
    if location:
        tool["user_location"] = location

    messages = []
    if args.system:
        messages.append({"role": "system", "content": args.system})
    messages.append({"role": "user", "content": args.query})

    return {
        "model": args.model,
        "messages": messages,
        "tools": [tool],
        "tool_choice": "auto",
        "max_completion_tokens": args.max_completion_tokens,
        "temperature": args.temperature,
        "top_p": args.top_p,
        "stream": False,
        "stop": None,
        "frequency_penalty": 0,
        "presence_penalty": 0,
        "thinking": {"type": "disabled"},
    }


def post_json(url: str, api_key: str, payload: dict, timeout: int) -> dict:
    body = json.dumps(payload, ensure_ascii=False).encode("utf-8")
    request = urllib.request.Request(
        url,
        data=body,
        method="POST",
        headers={
            "api-key": api_key,
            "Content-Type": "application/json",
        },
    )
    try:
        with urllib.request.urlopen(request, timeout=timeout) as response:
            return json.loads(response.read().decode("utf-8"))
    except urllib.error.HTTPError as exc:
        detail = exc.read().decode("utf-8", errors="replace")
        raise SystemExit(f"MiMo API HTTP {exc.code}: {detail}") from exc
    except urllib.error.URLError as exc:
        raise SystemExit(f"MiMo API request failed: {exc.reason}") from exc
    except json.JSONDecodeError as exc:
        raise SystemExit(f"MiMo API returned invalid JSON: {exc}") from exc


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Call Xiaomi MiMo web_search through chat completions."
    )
    parser.add_argument("query", help="User query to answer with MiMo web search")
    parser.add_argument("--model", default=DEFAULT_MODEL)
    parser.add_argument("--base-url", default=os.environ.get("MIMO_BASE_URL", DEFAULT_BASE_URL))
    parser.add_argument("--api-key", default=os.environ.get("MIMO_API_KEY"))
    parser.add_argument("--force-search", action="store_true")
    parser.add_argument("--max-keyword", type=int, default=2)
    parser.add_argument("--limit", type=int, default=3)
    parser.add_argument(
        "--location",
        help='Optional user_location JSON, e.g. {"type":"approximate","country":"China","region":"Hubei","city":"Wuhan"}',
    )
    parser.add_argument("--system", help="Optional system message")
    parser.add_argument("--max-completion-tokens", type=int, default=1024)
    parser.add_argument("--temperature", type=float, default=1.0)
    parser.add_argument("--top-p", type=float, default=0.95)
    parser.add_argument("--timeout", type=int, default=60)
    parser.add_argument("--raw", action="store_true", help="Return the raw API response")
    args = parser.parse_args(argv)

    if not args.api_key:
        raise SystemExit("MIMO_API_KEY is not set. Set it or pass --api-key.")
    if args.max_keyword < 1:
        raise SystemExit("--max-keyword must be >= 1")
    if args.limit < 1:
        raise SystemExit("--limit must be >= 1")

    url = args.base_url.rstrip("/") + "/chat/completions"
    payload = build_payload(args)
    data = post_json(url, args.api_key, payload, args.timeout)

    if args.raw:
        json.dump(data, sys.stdout, ensure_ascii=False, indent=2)
        sys.stdout.write("\n")
        return 0

    message = extract_message(data)
    result = {
        "answer": message.get("content", ""),
        "citations": normalize_citations(message),
        "usage": data.get("usage", {}),
        "model": data.get("model"),
        "id": data.get("id"),
    }
    json.dump(result, sys.stdout, ensure_ascii=False, indent=2)
    sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
