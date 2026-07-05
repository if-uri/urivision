# Author: Tom Sapletta · Part of the ifURI solution.
"""CLI VURI + URI Runtime.

Examples:
  urivision run FILE.vuri --dry-run
  urivision catalog --format markdown
  urivision call input://local/keyboard/command/type --json '{"text":"hello"}'
  urivision plan examples/desktop-control.plan.json
  urivision native-matrix --format markdown
  urivision route type_text --profile windows-11-uia
"""
from __future__ import annotations

import argparse
import json
import sys

from . import run_file
from .orchestrator import run_plan_file
from .runtime import default_runtime
from .native_profiles import list_native_targets, native_matrix_markdown, coverage_summary, detect_local_host
from .method_router import route_intent, route_matrix


def _json_arg(blob: str | None) -> dict:
    if not blob:
        return {}
    try:
        value = json.loads(blob)
    except json.JSONDecodeError as exc:
        raise SystemExit(f"bad JSON payload: {exc}") from exc
    if not isinstance(value, dict):
        raise SystemExit("JSON payload must be an object")
    return value


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(prog="urivision")
    sub = ap.add_subparsers(dest="cmd", required=True)

    r = sub.add_parser("run", help="Uruchom proces .vuri")
    r.add_argument("file")
    r.add_argument("--dry-run", action="store_true", help="Skompiluj wywołanie bez uderzania w model")
    r.add_argument("--root", action="append", default=[], metavar="NAME=DIR", help="Baza dla artifact://NAME/... (można wielokrotnie)")

    c = sub.add_parser("catalog", help="Pokaż katalog funkcji runtime dla LLM")
    c.add_argument("--format", choices=["json", "markdown", "prompt", "tools"], default="json")

    call = sub.add_parser("call", help="Wywołaj jedną funkcję przez URI")
    call.add_argument("uri")
    call.add_argument("--json", default="{}", help="Payload JSON")
    call.add_argument("--dry-run", action="store_true")

    p = sub.add_parser("plan", help="Uruchom JSON plan z krokami URI")
    p.add_argument("file")
    p.add_argument("--dry-run", action="store_true")

    e = sub.add_parser("explain", help="Wyjaśnij, która capability obsłuży URI")
    e.add_argument("uri")

    nm = sub.add_parser("native-matrix", help="Pokaż macierz natywnych runnerów OS")
    nm.add_argument("--format", choices=["json", "markdown"], default="json")

    np = sub.add_parser("native-probe", help="Wykryj lokalny host i prawdopodobne profile natywne")
    np.add_argument("--format", choices=["json", "markdown"], default="json")

    rt = sub.add_parser("route", help="Dobierz metodę wykonania dla intencji i profilu OS")
    rt.add_argument("intent", choices=["read_ui_tree", "find_element", "press_element", "type_text", "verify_text", "capture_screen"])
    rt.add_argument("--profile", required=True, help="Native target profile, np. windows-11-uia")
    rt.add_argument("--target", default="local")

    rm = sub.add_parser("route-matrix", help="Pokaż pełną macierz MethodRouter")
    rm.add_argument("--target", default="local")

    args = ap.parse_args(argv)

    if args.cmd == "run":
        roots = dict(kv.split("=", 1) for kv in args.root if "=" in kv)
        res = run_file(args.file, roots=roots or None, dry_run=args.dry_run)
        print(json.dumps(res, ensure_ascii=False, indent=2))
        return 0 if res.get("ok") else 1

    runtime = default_runtime(dry_run=getattr(args, "dry_run", False))

    if args.cmd == "catalog":
        data = runtime.catalog(args.format)
        if isinstance(data, str):
            print(data, end="")
        else:
            print(json.dumps(data, ensure_ascii=False, indent=2))
        return 0

    if args.cmd == "call":
        res = runtime.call(args.uri, _json_arg(args.json), dry_run=args.dry_run)
        print(json.dumps(res, ensure_ascii=False, indent=2))
        return 0 if res.get("ok") else 1

    if args.cmd == "plan":
        res = run_plan_file(args.file, runtime=runtime, dry_run=args.dry_run)
        print(json.dumps(res, ensure_ascii=False, indent=2))
        return 0 if res.get("ok") else 1


    if args.cmd == "native-matrix":
        if args.format == "markdown":
            print(native_matrix_markdown(), end="")
        else:
            print(json.dumps({"schema": "schema://runtime/native-matrix.v1", "summary": coverage_summary(), "targets": [t.to_dict() for t in list_native_targets()]}, ensure_ascii=False, indent=2))
        return 0

    if args.cmd == "native-probe":
        data = detect_local_host()
        if args.format == "markdown":
            print("# Native Host Probe\n")
            print(f"- system: {data['system']}")
            print(f"- release: {data['release']}")
            print(f"- machine: {data['machine']}")
            print(f"- candidate profiles: {', '.join(data['candidate_profiles']) or 'none'}")
        else:
            print(json.dumps(data, ensure_ascii=False, indent=2))
        return 0

    if args.cmd == "route":
        print(json.dumps(route_intent(args.intent, args.profile, target=args.target).to_dict(), ensure_ascii=False, indent=2))
        return 0

    if args.cmd == "route-matrix":
        print(json.dumps(route_matrix(target=args.target), ensure_ascii=False, indent=2))
        return 0

    if args.cmd == "explain":
        res = runtime.explain(args.uri)
        print(json.dumps(res, ensure_ascii=False, indent=2))
        return 0 if res.get("ok") else 1

    raise SystemExit(f"unknown command: {args.cmd}")


if __name__ == "__main__":
    sys.exit(main())
