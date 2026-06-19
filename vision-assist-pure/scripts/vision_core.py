"""Vision Assist core library - provider-agnostic vision queries, no CLI side effects."""

import base64
import json
import os
import re
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

MIME_MAP = {
    ".png": "image/png",
    ".jpg": "image/jpeg",
    ".jpeg": "image/jpeg",
    ".webp": "image/webp",
    ".gif": "image/gif",
}

DATA_URI_RE = re.compile(
    r"^data:(?P<mime>[\w/+-]+)?(?:;charset=[\w-]+)?;base64,(?P<data>.+)$",
    re.IGNORECASE,
)


class VisionError(Exception):
    def __init__(self, message, category="unknown", retryable=False):
        super().__init__(message)
        self.category = category
        self.retryable = retryable


class ConfigError(Exception):
    pass


def _empty_config():
    return {
        "active_provider": "openai",
        "providers": {
            "openai": {
                "type": "openai",
                "api_key": "",
                "base_url": DEFAULT_BASE_URL["openai"],
                "model": "gpt-4o-mini",
                "max_tokens": 2048,
                "temperature": 0.4,
            },
            "gemini": {
                "type": "gemini",
                "api_key": "",
                "base_url": DEFAULT_BASE_URL["gemini"],
                "model": "gemini-2.5-pro",
                "max_tokens": 2048,
                "temperature": 0.4,
            },
            "anthropic": {
                "type": "anthropic",
                "api_key": "",
                "base_url": DEFAULT_BASE_URL["anthropic"],
                "model": "claude-opus-4-7",
                "max_tokens": 2048,
                "temperature": 0.4,
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
            f"  Fix: python vision_assist.py config --set {provider}.api_key YOUR_KEY"
        )
    base_url = (pcfg.get("base_url") or DEFAULT_BASE_URL[ptype]).rstrip("/")
    model = override_model or pcfg.get("model")
    if not model:
        raise ConfigError(
            f"model for provider '{provider}' not configured.\n"
            f"  Fix: python vision_assist.py config --set {provider}.model MODEL_NAME"
        )
    return {
        "provider": provider,
        "type": ptype,
        "api_key": api_key,
        "base_url": base_url,
        "model": model,
        "max_tokens": int(pcfg.get("max_tokens", 2048)),
        "temperature": float(pcfg.get("temperature", 0.4)),
    }


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
        return VisionError(f"Authentication failed (HTTP {status_code})", "auth", False)
    if status_code == 403:
        return VisionError(f"Permission denied (HTTP {status_code})", "auth", False)
    if status_code == 404 or "not found" in body_lower:
        return VisionError(f"Model or endpoint not found (HTTP {status_code})", "not_found", False)
    if status_code == 400:
        if "safety" in body_lower or "content_policy" in body_lower or "blocked" in body_lower:
            return VisionError(f"Content policy rejection (HTTP {status_code})", "content_policy", False)
        return VisionError(f"Bad request (HTTP {status_code}): {error_body[:200]}", "bad_request", False)
    if status_code == 429:
        return VisionError(f"Rate limited (HTTP {status_code})", "rate_limit", True)
    if status_code == 503:
        return VisionError(f"Model unavailable (HTTP {status_code})", "unavailable", True)
    if status_code >= 500:
        return VisionError(f"Server error (HTTP {status_code})", "server_error", True)
    return VisionError(f"HTTP {status_code}: {error_body[:200]}", "unknown", True)


def _is_url(s):
    return bool(re.match(r"^https?://", s, re.IGNORECASE))


def load_image(path_or_url):
    data_uri = DATA_URI_RE.match(path_or_url)
    if data_uri:
        mime = data_uri.group("mime") or "image/png"
        data = data_uri.group("data").strip()
        try:
            base64.b64decode(data)
        except Exception:
            raise ValueError("Invalid base64 data URI")
        return {"kind": "b64", "mime": mime, "data": data, "source": "data-uri"}
    if _is_url(path_or_url):
        ext = os.path.splitext(path_or_url.split("?")[0])[1].lower()
        mime = MIME_MAP.get(ext, "image/png")
        return {"kind": "url", "mime": mime, "data": path_or_url, "source": path_or_url}
    if not os.path.exists(path_or_url):
        raise FileNotFoundError(f"Image not found: {path_or_url}")
    ext = os.path.splitext(path_or_url)[1].lower()
    mime = MIME_MAP.get(ext, "image/png")
    with open(path_or_url, "rb") as f:
        b64 = base64.b64encode(f.read()).decode("utf-8")
    return {"kind": "b64", "mime": mime, "data": b64, "source": path_or_url}


def _build_openai(prompt, images, model, max_tokens, temperature):
    content = [{"type": "text", "text": prompt}]
    for img in images:
        url = img["data"] if img["kind"] == "url" else f"data:{img['mime']};base64,{img['data']}"
        content.append({"type": "image_url", "image_url": {"url": url}})
    return {
        "model": model,
        "messages": [{"role": "user", "content": content}],
        "max_tokens": max_tokens,
        "temperature": temperature,
    }


def _build_gemini(prompt, images, max_tokens, temperature):
    parts = [{"text": prompt}]
    for img in images:
        if img["kind"] == "url":
            parts.append({"fileData": {"mimeType": img["mime"], "fileUri": img["data"]}})
        else:
            parts.append({"inlineData": {"mimeType": img["mime"], "data": img["data"]}})
    return {
        "contents": [{"parts": parts}],
        "generationConfig": {"maxOutputTokens": max_tokens, "temperature": temperature},
    }


def _build_anthropic(prompt, images, model, max_tokens, temperature):
    content = []
    for img in images:
        if img["kind"] == "url":
            content.append({"type": "image", "source": {"type": "url", "url": img["data"]}})
        else:
            content.append({
                "type": "image",
                "source": {"type": "base64", "media_type": img["mime"], "data": img["data"]},
            })
    content.append({"type": "text", "text": prompt})
    return {
        "model": model,
        "max_tokens": max_tokens,
        "temperature": temperature,
        "messages": [{"role": "user", "content": content}],
    }


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


def ask(prompt, image_paths, retry=1, no_proxy=False, override_provider=None, override_model=None):
    settings = resolve_active(override_provider, override_model)
    provider = settings["provider"]
    ptype = settings["type"]
    api_key = settings["api_key"]
    base_url = settings["base_url"]
    model = settings["model"]
    max_tokens = settings["max_tokens"]
    temperature = settings["temperature"]

    images = []
    for p in image_paths:
        try:
            images.append(load_image(p))
        except FileNotFoundError as e:
            raise VisionError(str(e), "not_found", False)

    if not images:
        raise VisionError("at least one image is required", "bad_request", False)

    if ptype == "openai":
        if base_url.endswith("/chat/completions"):
            url = base_url
        elif re.search(r"/v\d+$", base_url):
            url = f"{base_url}/chat/completions"
        else:
            url = f"{base_url}/v1/chat/completions"
        payload = _build_openai(prompt, images, model, max_tokens, temperature)
        parser = _parse_openai
    elif ptype == "gemini":
        if "generateContent" in base_url:
            url = base_url
        elif re.search(r"/v\d+(?:beta|alpha)?$", base_url):
            url = f"{base_url}/models/{model}:generateContent?key={api_key}"
        else:
            url = f"{base_url}/v1beta/models/{model}:generateContent?key={api_key}"
        payload = _build_gemini(prompt, images, max_tokens, temperature)
        parser = _parse_gemini
    elif ptype == "anthropic":
        if base_url.endswith("/messages"):
            url = base_url
        elif re.search(r"/v\d+$", base_url):
            url = f"{base_url}/messages"
        else:
            url = f"{base_url}/v1/messages"
        payload = _build_anthropic(prompt, images, model, max_tokens, temperature)
        parser = _parse_anthropic
    else:
        raise VisionError(f"unknown provider type {ptype}", "bad_request", False)

    auth_variants = _auth_variants(ptype, api_key)
    _requests, kwargs = _get_requests(no_proxy)
    last_error = None

    for attempt in range(1, retry + 1):
        if attempt > 1:
            wait = min(5 * (2 ** (attempt - 2)), 60)
            time.sleep(wait)
        try:
            resp, used_label = _post_with_auth_fallback(_requests, url, payload, auth_variants, kwargs)
            if resp.status_code != 200:
                body = _mask_key(resp.text, api_key)
                err = _classify_error(resp.status_code, body)
                last_error = err
                if not err.retryable:
                    break
                continue
            result = resp.json()
        except ImportError:
            raise VisionError("'requests' package not installed. Run: pip install requests", "setup", False)
        except Exception as e:
            last_error = e
            continue

        text = parser(result)
        if not text:
            last_error = VisionError(
                f"Empty/unparseable response. Raw: {_mask_key(json.dumps(result, indent=2, ensure_ascii=False)[:600], api_key)}",
                "empty_response",
                True,
            )
            continue
        return text.strip()

    if last_error is None:
        last_error = VisionError("Failed after retries", "unknown", True)
    raise last_error


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
