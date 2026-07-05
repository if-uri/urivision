#!/usr/bin/env bash
set -euo pipefail
mkdir -p "$XDG_RUNTIME_DIR" artifacts
chmod 700 "$XDG_RUNTIME_DIR"
# Weston may fail in restricted CI; the probe still validates the URI contract and reports limitations.
weston --backend=headless-backend.so --socket="$WAYLAND_DISPLAY" >/tmp/weston.log 2>&1 &
WESTON_PID=$!
sleep 1
python tools/probe_runtime.py --profile linux-wayland-headless --out artifacts/linux-wayland-headless.json
kill "$WESTON_PID" >/dev/null 2>&1 || true
