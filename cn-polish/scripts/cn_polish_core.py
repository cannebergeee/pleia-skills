"""Chinese Polish core library - multi-provider text polish, translate, localize."""

import json
import os
import re
import sys
import time

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
CONFIG_PATH = os.path.join(SCRIPT_DIR, "config.json")

SUPPORTED_TYPES = ("openai", "gemini", "anthropic")
ANTHROPIC_VERSION = "2023-06-01"

DEFAULT_BASE_URL = {
    "openai": "https://api.openai.com/v1",
    "gemini": "https://generativelanguage.googleapis.com/v1beta",
    "anthropic": "https://api.anthropic.com/v1",
}

TYPE_ENV_VAR = {
    "openai": "OPENAI_API_KEY",
    "gemini": "GEMINI_API_KEY",
    "anthropic": "ANTHROPIC_API_KEY",
}

NUMERIC_INT_FIELDS = {"max_tokens"}
NUMERIC_FLOAT_FIELDS = {"temperature"}

# ─── System Prompts ─────────────────────────────────────────────────

SYSTEM_PROMPTS = {
    "polish": (
        "你是一位资深中文编辑。请润色以下中文文本，优化语法、流畅度和文采，"
        "使表达更自然优雅，同时严格保留原意。仅输出润色后的文本，不要任何解释。"
    ),
    "translate": (
        "你是一位专业英中翻译，擅长软件与技术领域。"
        "请将以下英文翻译为准确、自然的中文。"
        "软件术语使用行业标准译法（如 Settings→设置、Save→保存、Cancel→取消）。"
        "仅输出翻译结果，不要任何解释。"
    ),
    "localize": (
        "你是一位 UI 本地化专家。请将以下 UI 字符串从英文翻译为中文。"
        "保持 key=value 格式不变，仅翻译 value 部分。"
        "使用简洁标准的软件本地化惯例。"
        "仅输出翻译后的 key=value 对，不要任何解释。"
    ),
}


# ─── Errors ─────────────────────────────────────────────────────────

class PolishError(Exception):
    def __init__(self, message, category="unknown", retryable=False):
        super().__init__(message)
        self.category = category
        self.retryable = retryable


class ConfigError(Exception):
    pass


# ─── Config ─────────────────────────────────────────────────────────

def _empty_config():
    return {
        "active_provider": "openai",
        "providers": {
            "openai": {
                "type": "openai",
                "api_key": "",
                "base_url": DEFAULT_BASE_URL["openai"],
                "model": "gpt-4o-mini",
                "max_tokens": 4096,
                "temperature": 0.3,
            },
            "gemini": {
                "type": "gemini",
                "api_key": "",
                "base_url": DEFAULT_BASE_URL["gemini"],
                "model": "gemini-2.5-pro",
                "max_tokens": 4096,
                "temperature": 0.3,
            },
            "anthropic": {
                "type": "anthropic",
                "api_key": "",
                "base_url": DEFAULT_BASE_URL["anthropic"],
                "model": "claude-haiku-4-5",
                "max_tokens": 4096,
                "temperature": 0.3,
            },
        },
    }


def load_config():
    if not os.path.exists(CONFIG_PATH):
        return _empty_config()
    with open(CONFIG_PATH, "r", encoding="utf-8") as f:
        cfg = json.load(f)
    if "providers" not in cfg or not isinstance(cfg["providers"], dict):
        cfg["providers"] = _empty_config()["providers"]
    cfg.setdefault("active_provider", "openai")
    for name in ("openai", "gemini", "anthropic"):
        if name in cfg["providers"] and "type" not in cfg["providers"][name]:
            cfg["providers"][name]["type"] = name
    return cfg


def save_config(config):
    with open(CONFIG_PATH, "w", encoding="utf-8") as f:
        json.dump(config, f, indent=2, ensure_ascii=False)


def _coerce(field, value):
    if field in NUMERIC_INT_FIELDS:
        return int(value)
    if field in NUMERIC_FLOAT_FIELDS:
        return float(value)
    return value


def _resolve_type(pcfg, provider_name):
    t = pcfg.get("type")
    if t:
        return t
    if provider_name in SUPPORTED_TYPES:
        return provider_name
    return None


def set_config_value(key, value):
    config = load_config()
    display_value = "***" if "key" in key.lower() else value
    if key == "active_provider":
        if value not in config.get("providers", {}):
            raise ConfigError(
                f"no provider entry named '{value}'. Available: {list(config['providers'].keys())}"
            )
        config["active_provider"] = value
        save_config(config)
        return f"Config set: active_provider = {value}"

    if "." in key:
        provider, field = key.split(".", 1)
        if field == "type" and value not in SUPPORTED_TYPES:
            raise ConfigError(f"type must be one of {SUPPORTED_TYPES}")
        created = provider not in config["providers"]
        config["providers"].setdefault(provider, {})
        config["providers"][provider][field] = _coerce(field, value)
        save_config(config)
        suffix = "  (new provider entry - remember to set its `type`)" if created and field != "type" else ""
        return f"Config set: {provider}.{field} = {display_value}{suffix}"

    provider = config.get("active_provider", "openai")
    if provider not in config["providers"]:
        raise ConfigError(
            f"active provider '{provider}' has no config entry. "
            f"Run: config --set {provider}.type <openai|gemini|anthropic>"
        )
    if key == "type" and value not in SUPPORTED_TYPES:
        raise ConfigError(f"type must be one of {SUPPORTED_TYPES}")
    config["providers"][provider][key] = _coerce(key, value)
    save_config(config)
    return f"Config set: {provider}.{key} = {display_value}  (active provider)"


def get_config_value(key):
    config = load_config()
    if key == "active_provider":
        return config.get("active_provider")
    if "." in key:
        provider, field = key.split(".", 1)
        return config.get("providers", {}).get(provider, {}).get(field)
    provider = config.get("active_provider", "openai")
    return config.get("providers", {}).get(provider, {}).get(key)


def config_use(provider):
    config = load_config()
    if provider not in config.get("providers", {}):
        raise ConfigError(
            f"no provider entry named '{provider}'. Available: {list(config['providers'].keys())}"
        )
    config["active_provider"] = provider
    save_config(config)
    ptype = _resolve_type(config["providers"][provider], provider)
    return f"Active provider: {provider} (type={ptype})"


def config_check_key(provider=None):
    config = load_config()
    provider = provider or config.get("active_provider", "openai")
    pcfg = config.get("providers", {}).get(provider)
    if not pcfg:
        raise ConfigError(f"no provider entry named '{provider}'")
    ptype = _resolve_type(pcfg, provider) or "(missing type)"
    return {
        "active_provider": config.get("active_provider"),
        "provider_checked": provider,
        "type": ptype,
        "api_key_configured": bool(pcfg.get("api_key")),
    }


def config_list(masked=True):
    config = load_config()
    if not masked:
        return config
    safe = json.loads(json.dumps(config))
    for pcfg in safe.get("providers", {}).values():
        if pcfg.get("api_key"):
            pcfg["api_key"] = "***"
    return safe


# ─── Provider Resolution ───────────────────────────────────────────

def resolve_active(override_provider=None, override_model=None):
    config = load_config()
    provider = override_provider or config.get("active_provider", "openai")
    pcfg = config.get("providers", {}).get(provider)
    if not pcfg:
        raise ConfigError(
            f"provider '{provider}' not found. Available: {list(config.get('providers', {}).keys())}"
        )
    ptype = _resolve_type(pcfg, provider)
    if ptype not in SUPPORTED_TYPES:
        raise ConfigError(
            f"provider '{provider}' has invalid/missing type. "
            f"Set it: config --set {provider}.type <{'|'.join(SUPPORTED_TYPES)}>"
        )
    api_key = pcfg.get("api_key") or os.environ.get(TYPE_ENV_VAR.get(ptype, ""), "")
    if not api_key:
        raise ConfigError(
            f"api_key for provider '{provider}' is not configured.\n"
            f"  Fix: python cn_polish.py config --set {provider}.api_key YOUR_KEY"
        )
    base_url = (pcfg.get("base_url") or DEFAULT_BASE_URL[ptype]).rstrip("/")
    model = override_model or pcfg.get("model")
    if not model:
        raise ConfigError(
            f"model for provider '{provider}' not configured.\n"
            f"  Fix: python cn_polish.py config --set {provider}.model MODEL_NAME"
        )
    return {
        "provider": provider,
        "type": ptype,
        "api_key": api_key,
        "base_url": base_url,
        "model": model,
        "max_tokens": int(pcfg.get("max_tokens", 4096)),
        "temperature": float(pcfg.get("temperature", 0.3)),
    }


# ─── Network Helpers ───────────────────────────────────────────────

def _mask_key(text, api_key):
    return text.replace(api_key, "***") if api_key else text


def _get_requests(no_proxy=False):
    import requests as _requests
    kwargs = {}
    if no_proxy:
        kwargs["proxies"] = {"http": None, "https": None}
    return _requests, kwargs


def _classify_error(status_code, error_body):
    body_lower = error_body.lower()
    if status_code == 401 or "invalid api key" in body_lower or "unauthorized" in body_lower:
        return PolishError(f"Authentication failed (HTTP {status_code})", "auth", False)
    if status_code == 403:
        return PolishError(f"Permission denied (HTTP {status_code})", "auth", False)
    if status_code == 404 or "not found" in body_lower:
        return PolishError(f"Model or endpoint not found (HTTP {status_code})", "not_found", False)
    if status_code == 400:
        if "safety" in body_lower or "content_policy" in body_lower or "blocked" in body_lower:
            return PolishError(f"Content policy rejection (HTTP {status_code})", "content_policy", False)
        return PolishError(f"Bad request (HTTP {status_code}): {error_body[:200]}", "bad_request", False)
    if status_code == 429:
        return PolishError(f"Rate limited (HTTP {status_code})", "rate_limit", True)
    if status_code == 503:
        return PolishError(f"Model unavailable (HTTP {status_code})", "unavailable", True)
    if status_code >= 500:
        return PolishError(f"Server error (HTTP {status_code})", "server_error", True)
    return PolishError(f"HTTP {status_code}: {error_body[:200]}", "unknown", True)


def _auth_variants(ptype, api_key):
    common = {"Content-Type": "application/json"}
    if ptype == "anthropic":
        return [
            ({**common, "x-api-key": api_key, "anthropic-version": ANTHROPIC_VERSION}, "x-api-key"),
            ({**common, "Authorization": f"Bearer {api_key}", "anthropic-version": ANTHROPIC_VERSION}, "Authorization"),
        ]
    if ptype == "openai":
        return [({**common, "Authorization": f"Bearer {api_key}"}, "Authorization")]
    return [(common, "query-key")]


def _post_with_auth_fallback(_requests, url, payload, auth_variants, kwargs):
    last_resp = None
    last_label = None
    for idx, (headers, label) in enumerate(auth_variants):
        resp = _requests.post(url, headers=headers, json=payload, timeout=300, **kwargs)
        last_resp = resp
        last_label = label
        if resp.status_code in (401, 403) and idx + 1 < len(auth_variants):
            continue
        return resp, label
    return last_resp, last_label


# ─── Payload Builders (text-only) ──────────────────────────────────

def _build_openai(system_prompt, user_text, model, max_tokens, temperature):
    messages = []
    if system_prompt:
        messages.append({"role": "system", "content": system_prompt})
    messages.append({"role": "user", "content": user_text})
    return {
        "model": model,
        "messages": messages,
        "max_tokens": max_tokens,
        "temperature": temperature,
    }


def _build_gemini(system_prompt, user_text, max_tokens, temperature):
    text = f"{system_prompt}\n\n{user_text}" if system_prompt else user_text
    return {
        "contents": [{"parts": [{"text": text}]}],
        "generationConfig": {"maxOutputTokens": max_tokens, "temperature": temperature},
    }


def _build_anthropic(system_prompt, user_text, model, max_tokens, temperature):
    payload = {
        "model": model,
        "max_tokens": max_tokens,
        "temperature": temperature,
        "messages": [{"role": "user", "content": user_text}],
    }
    if system_prompt:
        payload["system"] = system_prompt
    return payload


def _parse_openai(result):
    choices = result.get("choices", [])
    if not choices:
        return None
    msg = choices[0].get("message", {})
    content = msg.get("content")
    if isinstance(content, str):
        return content
    if isinstance(content, list):
        return "".join(c.get("text", "") for c in content if isinstance(c, dict))
    return None


def _parse_gemini(result):
    candidates = result.get("candidates", [])
    if not candidates:
        return None
    parts = candidates[0].get("content", {}).get("parts", [])
    return "".join(p.get("text", "") for p in parts if isinstance(p, dict))


def _parse_anthropic(result):
    blocks = result.get("content", [])
    if not blocks:
        return None
    return "".join(b.get("text", "") for b in blocks if b.get("type") == "text")


# ─── Core Chat ─────────────────────────────────────────────────────

def _chat(system_prompt, user_text, retry=1, no_proxy=False,
          override_provider=None, override_model=None):
    """Send text to the configured model and return the response."""
    settings = resolve_active(override_provider, override_model)
    provider = settings["provider"]
    ptype = settings["type"]
    api_key = settings["api_key"]
    base_url = settings["base_url"]
    model = settings["model"]
    max_tokens = settings["max_tokens"]
    temperature = settings["temperature"]

    # Build URL and payload
    if ptype == "openai":
        if base_url.endswith("/chat/completions"):
            url = base_url
        elif re.search(r"/v\d+$", base_url):
            url = f"{base_url}/chat/completions"
        else:
            url = f"{base_url}/v1/chat/completions"
        payload = _build_openai(system_prompt, user_text, model, max_tokens, temperature)
        parser = _parse_openai
    elif ptype == "gemini":
        if "generateContent" in base_url:
            url = base_url
        elif re.search(r"/v\d+(?:beta|alpha)?$", base_url):
            url = f"{base_url}/models/{model}:generateContent?key={api_key}"
        else:
            url = f"{base_url}/v1beta/models/{model}:generateContent?key={api_key}"
        payload = _build_gemini(system_prompt, user_text, max_tokens, temperature)
        parser = _parse_gemini
    elif ptype == "anthropic":
        if base_url.endswith("/messages"):
            url = base_url
        elif re.search(r"/v\d+$", base_url):
            url = f"{base_url}/messages"
        else:
            url = f"{base_url}/v1/messages"
        payload = _build_anthropic(system_prompt, user_text, model, max_tokens, temperature)
        parser = _parse_anthropic
    else:
        raise PolishError(f"unknown provider type {ptype}", "bad_request", False)

    auth_variants = _auth_variants(ptype, api_key)
    _requests, kwargs = _get_requests(no_proxy)
    last_error = None

    for attempt in range(1, retry + 1):
        if attempt > 1:
            wait = min(5 * (2 ** (attempt - 2)), 60)
            print(f"  Retry {attempt}/{retry} in {wait}s...", file=sys.stderr)
            time.sleep(wait)
        try:
            resp, used_label = _post_with_auth_fallback(_requests, url, payload, auth_variants, kwargs)
            if resp.status_code != 200:
                body = _mask_key(resp.text, api_key)
                err = _classify_error(resp.status_code, body)
                suffix = ""
                if err.category == "auth" and ptype == "anthropic" and len(auth_variants) > 1:
                    suffix = " (tried both x-api-key and Authorization)"
                print(f"  [{err.category}] {err}{suffix}", file=sys.stderr)
                last_error = err
                if not err.retryable:
                    break
                continue
            result = resp.json()
        except ImportError:
            raise PolishError("'requests' package not installed. Run: pip install requests", "setup", False)
        except Exception as e:
            ename = type(e).__name__
            if "SSL" in ename or "SSL" in str(e):
                print(f"  [network] SSL error - try --no-proxy flag: {str(e)[:100]}", file=sys.stderr)
            elif "Timeout" in ename:
                print(f"  [network] Request timed out after 300s", file=sys.stderr)
            elif "Proxy" in str(e):
                print(f"  [network] Proxy error - try --no-proxy flag: {str(e)[:100]}", file=sys.stderr)
            else:
                print(f"  [network] {ename}: {str(e)[:150]}", file=sys.stderr)
            last_error = e
            continue

        text = parser(result)
        if not text:
            last_error = PolishError(
                f"Empty/unparseable response. Raw: {_mask_key(json.dumps(result, indent=2, ensure_ascii=False)[:600], api_key)}",
                "empty_response",
                True,
            )
            continue
        return text.strip()

    if last_error is None:
        last_error = PolishError("Failed after retries", "unknown", True)
    raise last_error


# ─── Public API ────────────────────────────────────────────────────

def polish(text, retry=1, no_proxy=False, override_provider=None, override_model=None):
    """Polish Chinese text for grammar, fluency, and style."""
    return _chat(
        system_prompt=SYSTEM_PROMPTS["polish"],
        user_text=text,
        retry=retry,
        no_proxy=no_proxy,
        override_provider=override_provider,
        override_model=override_model,
    )


def translate(text, retry=1, no_proxy=False, override_provider=None, override_model=None):
    """Translate English text to Chinese."""
    return _chat(
        system_prompt=SYSTEM_PROMPTS["translate"],
        user_text=text,
        retry=retry,
        no_proxy=no_proxy,
        override_provider=override_provider,
        override_model=override_model,
    )


def localize(text, retry=1, no_proxy=False, override_provider=None, override_model=None):
    """Localize UI strings from English to Chinese (key=value format)."""
    return _chat(
        system_prompt=SYSTEM_PROMPTS["localize"],
        user_text=text,
        retry=retry,
        no_proxy=no_proxy,
        override_provider=override_provider,
        override_model=override_model,
    )


# ─── Preflight ─────────────────────────────────────────────────────

def preflight(quick=False, no_proxy=False, override_provider=None):
    settings = resolve_active(override_provider)
    provider = settings["provider"]
    ptype = settings["type"]
    api_key = settings["api_key"]
    base_url = settings["base_url"]
    model = settings["model"]

    result = {
        "ok": True,
        "provider": provider,
        "type": ptype,
        "base_url": base_url,
        "model": model,
        "auth_ok": True,
        "network_reachable": True,
        "message": "Preflight complete",
    }

    try:
        _requests, kwargs = _get_requests(no_proxy)
        if ptype == "openai":
            probe = f"{base_url}/models"
            headers = {"Authorization": f"Bearer {api_key}"}
            r = _requests.get(probe, headers=headers, timeout=10, **kwargs)
        elif ptype == "gemini":
            probe = f"{base_url}/models/{model}?key={api_key}"
            r = _requests.get(probe, timeout=10, **kwargs)
        else:
            probe = f"{base_url}/models"
            for label, hdrs in (
                ("x-api-key", {"x-api-key": api_key, "anthropic-version": ANTHROPIC_VERSION}),
                ("Authorization", {"Authorization": f"Bearer {api_key}", "anthropic-version": ANTHROPIC_VERSION}),
            ):
                r = _requests.get(probe, headers=hdrs, timeout=10, **kwargs)
                if r.status_code not in (401, 403):
                    break

        if r.status_code in (200, 401, 403):
            result["network_reachable"] = True
            if r.status_code in (401, 403):
                result["auth_ok"] = False
                result["message"] = "Network reachable, but server rejected the key for the probe endpoint"
        else:
            result["network_reachable"] = False
            result["message"] = f"Probe returned HTTP {r.status_code}: {_mask_key(r.text[:120], api_key)}"
    except Exception as e:
        result["ok"] = False
        result["network_reachable"] = False
        result["message"] = f"Network error: {type(e).__name__}: {str(e)[:100]}"

    return result
