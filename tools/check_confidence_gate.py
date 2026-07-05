#!/usr/bin/env python3
"""Check whether the project is allowed to claim broad OS support."""
from __future__ import annotations

import argparse
import json
from pathlib import Path


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("matrix", nargs="?", default="artifacts/native-lab-matrix.json")
    ap.add_argument("--strict", action="store_true", help="Fail if native evidence is still missing")
    args = ap.parse_args()
    data = json.loads(Path(args.matrix).read_text(encoding="utf-8"))
    contract_ok = data["core_contract"]["passed"] and all(t["contract"]["passed"] for t in data["targets"])
    missing_native = [t["profile"]["id"] for t in data["targets"] if t["native_execution"]["status"] == "requires-native-runner"]
    result = {
        "ok": contract_ok and (not args.strict or not missing_native),
        "contract_ok": contract_ok,
        "missing_native_evidence": missing_native,
        "can_claim_broad_os_support": contract_ok and not missing_native,
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if result["ok"] else 2


if __name__ == "__main__":
    raise SystemExit(main())
