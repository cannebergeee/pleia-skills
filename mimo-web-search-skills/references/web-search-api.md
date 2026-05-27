# MiMo web_search API Reference

Source: https://platform.xiaomimimo.com/docs/zh-CN/usage-guide/tool-calling/web-search

## Endpoint

Use the OpenAI-compatible chat completions API:

```text
POST https://api.xiaomimimo.com/v1/chat/completions
Header: api-key: $MIMO_API_KEY
Header: Content-Type: application/json
```

## Tool Shape

`web_search` is passed inside the chat completions `tools` array. It is not a standalone search endpoint.

```json
{
  "type": "web_search",
  "max_keyword": 3,
  "force_search": true,
  "limit": 1,
  "user_location": {
    "type": "approximate",
    "country": "China",
    "region": "Hubei",
    "city": "Wuhan"
  }
}
```

The documentation examples use `force_search`. The FAQ mentions `forced_search`; prefer `force_search` unless the platform changes.

## Supported Models

The documentation lists these models as supporting web search:

- `mimo-v2.5-pro`
- `mimo-v2.5`
- `mimo-v2-pro`
- `mimo-v2-omni`
- `mimo-v2-flash`

## Response Fields

The assistant message includes:

- `content`: generated answer
- `annotations`: URL citations with fields such as `url`, `title`, `summary`, `site_name`, `publish_time`, and `logo_url`
- `tool_calls`: usually null for this built-in search mode

Usage may include:

- `usage.web_search_usage.tool_usage`
- `usage.web_search_usage.page_usage`

## Cost Controls

Search cost is affected by `max_keyword`: one user request may trigger multiple keyword searches. Keep `max_keyword` low by default and increase it only when broader recall is needed.

Search content is inserted into the model context, so token usage also increases.

## Known Operational Notes

- The web service plugin must be enabled in the MiMo console before use.
- Opening or closing web search may have a cache delay.
- If `force_search` is false, the model may decide no search is needed.
- The documentation says Anthropic API protocol is not supported for this feature.
