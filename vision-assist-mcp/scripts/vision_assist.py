#!/usr/bin/env python3
"""Vision Assist CLI - thin wrapper around scripts/vision_core.py."""

import argparse
import json
import sys

import vision_core as core


def cmd_ask(args):
   try:
       text = core.ask(
           prompt=args.prompt,
           image_paths=args.image,
           retry=args.retry,
           no_proxy=args.no_proxy,
           override_provider=args.provider,
           override_model=args.model,
       )
   except core.ConfigError as e:
       print(f"Config error: {e}", file=sys.stderr)
       sys.exit(1)
   except core.VisionError as e:
       print(f"[{e.category}] {e}", file=sys.stderr)
       sys.exit(1)
   except FileNotFoundError as e:
       print(f"Error: {e}", file=sys.stderr)
       sys.exit(1)
   print("--- Vision Response ---")
   print(text)


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
   print("  Vision Assist Preflight Check")
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

   parser = argparse.ArgumentParser(description="Vision Assist - multi-provider vision query")
   sub = parser.add_subparsers(dest="command")

   a = sub.add_parser("ask", help="Send prompt + image(s) to the vision model")
   a.add_argument("--prompt", "-p", required=True)
   a.add_argument("--image", "-i", nargs="+", required=True)
   a.add_argument("--provider")
   a.add_argument("--model")
   a.add_argument("--retry", type=int, default=1)
   a.add_argument("--no-proxy", action="store_true")

   pre = sub.add_parser("preflight", help="Check API availability")
   pre.add_argument("--quick", action="store_true")
   pre.add_argument("--no-proxy", action="store_true")
   pre.add_argument("--provider")

   cfg = sub.add_parser("config", help="Manage configuration")
   cfg.add_argument("--use", metavar="PROVIDER")
   cfg.add_argument("--set", nargs=2, metavar=("KEY", "VALUE"))
   cfg.add_argument("--get", metavar="KEY")
   cfg.add_argument("--check-key", nargs="?", const="__active__", metavar="PROVIDER")
   cfg.add_argument("--list", action="store_true")

   args = parser.parse_args()
   if not args.command:
       parser.print_help()
       sys.exit(0)

   if args.command == "config":
       cmd_config(args)
   elif args.command == "preflight":
       cmd_preflight(args)
   elif args.command == "ask":
       cmd_ask(args)


if __name__ == "__main__":
   main()
