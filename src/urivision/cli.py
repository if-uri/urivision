# Author: Tom Sapletta · Part of the ifURI solution.
"""CLI VURI:  urivision run FILE [--dry-run] [--root NAME=DIR ...]"""
from __future__ import annotations

import argparse
import json
import sys

from . import run_file


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(prog="urivision")
    sub = ap.add_subparsers(dest="cmd", required=True)
    r = sub.add_parser("run", help="Uruchom proces .vuri")
    r.add_argument("file")
    r.add_argument("--dry-run", action="store_true", help="Skompiluj wywołanie bez uderzania w model")
    r.add_argument("--root", action="append", default=[], metavar="NAME=DIR",
                   help="Baza dla artifact://NAME/... (można wielokrotnie)")
    args = ap.parse_args(argv)
    roots = dict(kv.split("=", 1) for kv in args.root if "=" in kv)
    res = run_file(args.file, roots=roots or None, dry_run=args.dry_run)
    print(json.dumps(res, ensure_ascii=False, indent=2))
    return 0 if res.get("ok") else 1


if __name__ == "__main__":
    sys.exit(main())
