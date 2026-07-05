#!/usr/bin/env bash
set -euo pipefail
mkdir -p artifacts
Xvfb :99 -screen 0 1280x800x24 >/tmp/xvfb.log 2>&1 &
XVFB_PID=$!
fluxbox >/tmp/fluxbox.log 2>&1 || true &
sleep 1
python tools/probe_runtime.py --profile linux-x11-novnc --out artifacts/linux-x11-novnc.json
kill "$XVFB_PID" >/dev/null 2>&1 || true
