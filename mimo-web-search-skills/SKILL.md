---
name: mimo-web-search
description: Use Xiaomi MiMo Open Platform web_search through the OpenAI-compatible chat completions API for live public web answers with citations. Use when Codex needs current or China-web-sensitive information such as news, policy updates, prices, product availability, weather, events, recent company facts, or when the user explicitly asks to search, verify, browse, look up, or use MiMo web search.
---

# MiMo Web Search

Use Xiaomi MiMo's `web_search` tool when the answer depends on current public web information, especially China-facing sources. Prefer the bundled script for repeatable calls and citation extraction.

## Quick Start

1. Confirm `MIMO_API_KEY` is set in the environment. If it is missing, ask the user to configure it.
2. Run `scripts/mimo_web_search.py` from this skill directory.
3. Use the returned `answer`, `citations`, and `usage` fields in the final response.

Example:

```bash
python scripts/mimo_web_search.py "Wuhan weather tomorrow" --force-search --max-keyword 2 --limit 3
```

If the shell does not provide `python`, use the available Python runtime for the environment and pass the same script arguments.

## Decision Rules

Use this skill for:

- Recent facts, breaking news, market/product availability, current weather, live public events, updated rules, policy, model availability, pricing, or release status.
- Chinese web contexts where MiMo search is likely to retrieve more relevant local sources.
- User requests that explicitly mention MiMo, Xiaomi MiMo, web search, search, browse, verify, latest, today, tomorrow, yesterday, or current.

Do not use this skill for:

- Local repository inspection, local file analysis, code execution, or non-web tasks.
- Stable general knowledge that does not need verification.
- Private data, authenticated websites, or scraping behind logins.

## Defaults

Use conservative defaults unless the user asks otherwise:

- `model`: `mimo-v2.5-pro`
- `force_search`: `false` for ordinary questions, `true` when the user explicitly asks to search or verify current information
- `max_keyword`: `1` to `3`
- `limit`: `1` to `3`
- `thinking`: disabled
- `stream`: false

Set `user_location` only when the user's location is relevant and known. Do not invent a precise location.

## Output Standards

When using search results:

- Cite the returned sources from `citations`.
- Prefer sources with relevant titles, summaries, and publish times.
- Mention uncertainty when sources conflict or publish times are stale.
- Include usage details when cost or call volume matters, using `usage.web_search_usage` if present.

## Reference

Read `references/web-search-api.md` when changing request parameters, troubleshooting API behavior, or implementing a different caller.
