#!/usr/bin/env bash
set -euo pipefail
export PYTHONPATH=src
python3 -m unittest discover -s tests -v
python3 tools/probe_native_host.py --out artifacts/native-host-probe.json
python3 -m urivision.cli native-matrix --format markdown > artifacts/native-matrix-from-cli.md
python3 -m urivision.cli route type_text --profile "${URIVISION_NATIVE_PROFILE:-ubuntu-24-04-wayland}" > artifacts/route-linux-type-text.json
native/linux/probe_linux_display.sh
