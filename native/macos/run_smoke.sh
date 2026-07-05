#!/usr/bin/env bash
set -euo pipefail
export PYTHONPATH=src
python3 -m unittest discover -s tests -v
python3 tools/probe_native_host.py --out artifacts/native-host-probe.json
python3 -m urivision.cli route type_text --profile macos-26-ax-apple-silicon > artifacts/route-macos-type-text.json
native/macos/probe_macos_ax.sh
