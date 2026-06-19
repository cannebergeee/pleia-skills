---
name: cn-polish
description: >-
  Polish Chinese text, translate English to Chinese, and localize UI strings
  using third-party LLM providers (OpenAI-compatible, Gemini, Anthropic).
  Use when the user asks to polish/improve Chinese writing, translate
  English terms or sentences to Chinese, localize UI strings (key=value
  format), or needs Chinese terminology standardization. Trigger keywords:
  润色, 润色中文, 翻译, 汉化, 本地化, 术语对照, polish Chinese, translate to
  Chinese, localize, 中文优化, 文案润色.
---

# Chinese Polish

Send Chinese text (or English text to translate) to the configured LLM provider;
capture the polished / translated / localized result.

## Usage

> **IMPORTANT**: `scripts/cn_polish.py` is a relative path inside this skill's
> directory. When this skill is invoked, the system prints "Base directory for
> this skill: `<path>`" at the top. You MUST `cd` into that exact path before
> calling the script.

```bash
cd "<base_dir>"
python scripts/cn_polish.py polish -t "需要润色的中文文本"
python scripts/cn_polish.py translate -t "English text to translate"
python scripts/cn_polish.py localize -t "save=Save"
```

### Polish — 中文润色

```bash
# Inline text
cd "<base_dir>" && python scripts/cn_polish.py polish -t "这个功能挺好用的但是还有点小毛病需要改进一下"

# Via stdin
cd "<base_dir>" && echo "这个功能挺好用的但是还有点小毛病需要改进一下" | python scripts/cn_polish.py polish

# From file
cd "<base_dir>" && python scripts/cn_polish.py polish -t "$(cat draft.txt)"

# With retry
cd "<base_dir>" && python scripts/cn_polish.py polish -t "..." --retry 3
```

### Translate — 英中翻译

```bash
# Single term
cd "<base_dir>" && python scripts/cn_polish.py translate -t "Settings"

# Multi-line
cd "<base_dir>" && python scripts/cn_polish.py translate -t "Save\nCancel\nDelete"

# Via stdin
cd "<base_dir>" && echo "User Authentication Module" | python scripts/cn_polish.py translate
```

### Localize — UI 本地化

```bash
# Key=value format
cd "<base_dir>" && python scripts/cn_polish.py localize -t "save=Save\ndelete=Delete\ncancel=Cancel"

# Via stdin
cd "<base_dir>" && cat ui_strings.txt | python scripts/cn_polish.py localize
```

| Flag | Default | Description |
|---|---|---|
| `--text` / `-t` | stdin | Chinese/English text to process |
| `--retry` | `1` | Max attempts with exponential backoff |
| `--no-proxy` | off | Bypass system proxy (SSL fixes) |
| `--provider` | active | Override active provider for this call |
| `--model` | configured | Override configured model for this call |

The model's answer is printed under a `--- Polish Result ---` / `--- Translation ---` / `--- Localization ---` line.
Capture everything after that line.

## Configuration

Copy `scripts/config.example.json` to `scripts/config.json` and fill in your
API key, or use the CLI:

```bash
cd "<base_dir>"

# Set API key for a provider
python scripts/cn_polish.py config --set openai.api_key YOUR_KEY

# Switch active provider
python scripts/cn_polish.py config --use openai

# Check current status
python scripts/cn_polish.py config --check-key
python scripts/cn_polish.py config --list
```

Run `python scripts/cn_polish.py config --help` for the full configuration surface.

### Adding a custom OpenAI-compatible provider

```bash
python scripts/cn_polish.py config --set deepseek.type openai
python scripts/cn_polish.py config --set deepseek.base_url https://api.deepseek.com/v1
python scripts/cn_polish.py config --set deepseek.api_key sk-...
python scripts/cn_polish.py config --set deepseek.model deepseek-chat
python scripts/cn_polish.py config --use deepseek
```

## How to construct the prompt

**Never pass the user's raw words directly as `-t` without thinking.**
The user's message is a directive to you — infer their intent and choose the
right subcommand:

| User intent | Subcommand |
|---|---|
| 润色中文 / 优化文案 / 改一下这段 / polish this Chinese | `polish` |
| 翻译 / 这个英文怎么翻 / what's the Chinese for X / 术语对照 | `translate` |
| 汉化 / 本地化 / localize these strings / UI 翻译 | `localize` |

For `translate` with multiple terms, use newline-separated input. The model
returns each translation on its own line.

For `localize`, always use `key=value` format (one per line). The model
preserves keys and translates only the values.

## Security: never read config.json directly

`scripts/config.json` contains API keys in plaintext. **Never use the Read tool
or any file reading tool on config.json.** To check whether a key is configured,
use the CLI commands above; they mask key values. Never expose the raw file
contents.

## If you hit "api_key not configured"

The user hasn't set up a provider yet. Ask them to run:

```bash
cd "<base_dir>"
python scripts/cn_polish.py config --set <provider>.api_key YOUR_KEY
python scripts/cn_polish.py config --use <provider>
```

## Preflight check

Verify provider connectivity before use:

```bash
cd "<base_dir>" && python scripts/cn_polish.py preflight
```
