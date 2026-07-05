#!/usr/bin/env bash
set -euo pipefail
mkdir -p artifacts
if ! command -v adb >/dev/null 2>&1; then
  echo '{"ok": false, "error": "adb missing"}' | tee artifacts/android-adb-probe.json
  exit 0
fi
{
  echo '{'
  echo '  "schema": "schema://runtime/android-adb-probe.v1",'
  echo '  "devices": '
  adb devices -l | python3 -c 'import sys,json; print(json.dumps(sys.stdin.read()))'
  echo '  ,"wm_size": '
  adb shell wm size 2>&1 | python3 -c 'import sys,json; print(json.dumps(sys.stdin.read()))'
  echo '  ,"uiautomator_dump": '
  adb shell uiautomator dump /sdcard/window.xml >/dev/null 2>&1 && adb shell cat /sdcard/window.xml | head -c 4000 | python3 -c 'import sys,json; print(json.dumps(sys.stdin.read()))' || echo '"dump-failed"'
  echo '}'
} | tee artifacts/android-adb-probe.json
