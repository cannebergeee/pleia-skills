#!/usr/bin/env python3
"""Chinese Polish CLI - thin wrapper around scripts/cn_polish_core.py."""

import argparse
import json
import sys

import cn_polish_core as core


def _read_text(args):
    """Get text from -t/--text arg or stdin (priority: arg > stdin pipe)."""
    if args.text:
        return args.text
    if not sys.stdin.isatty():
        return sys.stdin.read().strip()
    return None


def cmd_polish(args):
    text = _read_text(args)
    if not text:
        print("Error: no text provided. Use -t/--text or pipe via stdin.", file=sys.stderr)
        sys.exit(1)
    try:
        result = core.polish(
            text=text,
            retry=args.retry,
            no_proxy=args.no_proxy,
            override_provider=args.provider,
            override_model=args.model,
        )
    except core.ConfigError as e:
        print(f"Config error: {e}", file=sys.stderr)
        sys.exit(1)
    except core.PolishError as e:
        print(f"[{e.category}] {e}", file=sys.stderr)
        sys.exit(1)
    print("--- Polish Result ---")
    print(result)


def cmd_translate(args):
    text = _read_text(args)
    if not text:
        print("Error: no text provided. Use -t/--text or pipe via stdin.", file=sys.stderr)
        sys.exit(1)
    try:
        result = core.translate(
            text=text,
            retry=args.retry,
            no_proxy=args.no_proxy,
            override_provider=args.provider,
            override_model=args.model,
        )
    except core.ConfigError as e:
        print(f"Config error: {e}", file=sys.stderr)
        sys.exit(1)
    except core.PolishError as e:
        print(f"[{e.category}] {e}", file=sys.stderr)
        sys.exit(1)
    print("--- Translation ---")
    print(result)


def cmd_localize(args):
    text = _read_text(args)
    if not text:
        print("Error: no text provided. Use -t/--text or pipe via stdin.", file=sys.stderr)
        sys.exit(1)
    try:
        result = core.localize(
            text=text,
            retry=args.retry,
            no_proxy=args.no_proxy,
            override_provider=args.provider,
            override_model=args.model,
        )
    except core.ConfigError as e:
        print(f"Config error: {e}", file=sys.stderr)
        sys.exit(1)
    except core.PolishError as e:
        print(f"[{e.category}] {e}", file=sys.stderr)
        sys.exit(1)
    print("--- Localization ---")
    print(result)


def cmd_preflight(args):
    try:
        result = core.preflight(
            quick=args.quick,
            no_proxy=args.no_proxy,
            override_provider=args.provider,
        )
    except core.ConfigError as e:
        print(f"Config error: {e}", file=sys.stderr)
        sys.exit(1)

    print("=" * 50)
    print("  Chinese Polish Preflight Check")
    print("=" * 50)
    print(f"[INFO] Provider: {result['provider']} (type={result['type']})")
    print(f"[INFO] Base URL: {result['base_url']}")
    print(f"[INFO] Model:    {result['model']}")
    print(f"[{'OK' if result['auth_ok'] else 'WARN'}]   API key: {'configured' if result['auth_ok'] else 'probe rejected'}")
    print(f"[{'OK' if result['network_reachable'] else 'FAIL'}]   Network: {'reachable' if result['network_reachable'] else 'unreachable'}")
    print(f"[INFO] {result['message']}")
    sys.exit(0 if result["ok"] else 1)


def cmd_config(args):
    try:
        if args.use:
            print(core.config_use(args.use))
        if args.check_key:
            provider = None if args.check_key == "__active__" else args.check_key
            info = core.config_check_key(provider)
            print(f"active_provider: {info['active_provider']}")
            print(f"provider checked: {info['provider_checked']} (type={info['type']})")
            print(f"api_key: {'configured' if info['api_key_configured'] else 'empty'}")
        if args.list:
            print(json.dumps(core.config_list(masked=True), indent=2, ensure_ascii=False))
        if args.set:
            print(core.set_config_value(args.set[0], args.set[1]))
        if args.get:
            val = core.get_config_value(args.get)
            if "key" in args.get.lower():
                print(f"{args.get}: {'configured' if val else 'empty'}")
            else:
                print(f"{args.get}: {val}")
    except core.ConfigError as e:
        print(f"Config error: {e}", file=sys.stderr)
        sys.exit(1)


def main():
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")

    parser = argparse.ArgumentParser(
        description="Chinese Polish - multi-provider text polish, translate, localize"
    )
    sub = parser.add_subparsers(dest="command")

    # polish
    p = sub.add_parser("polish", help="Polish Chinese text (grammar, fluency, style)")
    p.add_argument("--text", "-t", help="Chinese text to polish (or pipe via stdin)")
    p.add_argument("--provider", help="Override active provider for this call")
    p.add_argument("--model", help="Override configured model for this call")
    p.add_argument("--retry", type=int, default=1, help="Max retry attempts (default 1)")
    p.add_argument("--no-proxy", action="store_true", help="Bypass system proxy")

    # translate
    t = sub.add_parser("translate", help="Translate English text to Chinese")
    t.add_argument("--text", "-t", help="English text to translate (or pipe via stdin)")
    t.add_argument("--provider", help="Override active provider for this call")
    t.add_argument("--model", help="Override configured model for this call")
    t.add_argument("--retry", type=int, default=1, help="Max retry attempts (default 1)")
    t.add_argument("--no-proxy", action="store_true", help="Bypass system proxy")

    # localize
    l = sub.add_parser("localize", help="Localize UI strings to Chinese (key=value format)")
    l.add_argument("--text", "-t", help="UI strings to localize (or pipe via stdin)")
    l.add_argument("--provider", help="Override active provider for this call")
    l.add_argument("--model", help="Override configured model for this call")
    l.add_argument("--retry", type=int, default=1, help="Max retry attempts (default 1)")
    l.add_argument("--no-proxy", action="store_true", help="Bypass system proxy")

    # preflight
    pre = sub.add_parser("preflight", help="Check API availability")
    pre.add_argument("--quick", action="store_true", help="Skip deep checks")
    pre.add_argument("--no-proxy", action="store_true", help="Bypass system proxy")
    pre.add_argument("--provider", help="Check a specific provider entry instead of active")

    # config
    cfg = sub.add_parser("config", help="Manage configuration")
    cfg.add_argument("--use", metavar="PROVIDER", help="Switch the active provider")
    cfg.add_argument("--set", nargs=2, metavar=("KEY", "VALUE"),
                     help="Set a value. KEY may be 'field', '<provider>.<field>', or 'active_provider'")
    cfg.add_argument("--get", metavar="KEY", help="Get a value (same KEY rules as --set)")
    cfg.add_argument("--check-key", nargs="?", const="__active__", metavar="PROVIDER",
                     help="Check if API key is configured (defaults to active provider)")
    cfg.add_argument("--list", action="store_true", help="Show all config (keys masked)")

    args = parser.parse_args()
    if not args.command:
        parser.print_help()
        sys.exit(0)

    if args.command == "polish":
        cmd_polish(args)
    elif args.command == "translate":
        cmd_translate(args)
    elif args.command == "localize":
        cmd_localize(args)
    elif args.command == "preflight":
        cmd_preflight(args)
    elif args.command == "config":
        cmd_config(args)


if __name__ == "__main__":
    main()
