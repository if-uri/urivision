#!/usr/bin/env bash
set -euo pipefail
mkdir -p artifacts
{
  echo '{'
  echo '  "schema": "schema://runtime/macos-ax-probe.v1",'
  echo '  "sw_vers": '
  sw_vers | python3 -c 'import sys,json; print(json.dumps(sys.stdin.read()))'
  echo '  ,"checks": {'
  echo '    "system_events_ui_enabled": '
  if command -v osascript >/dev/null 2>&1; then
    osascript -e 'tell application "System Events" to get UI elements enabled' 2>&1 | python3 -c 'import sys,json; s=sys.stdin.read().strip(); print(json.dumps({"ok": s.lower()=="true", "raw": s}))'
  else
    echo '{"ok": false, "error": "osascript missing"}'
  fi
  echo '  }'
  echo '}'
} | tee artifacts/macos-ax-probe.json

echo "Manual TCC checklist: System Settings → Privacy & Security → Accessibility, Screen Recording, Input Monitoring. Add terminal/runner app."
