#!/usr/bin/env bash
set -euo pipefail
mkdir -p artifacts
{
  echo "# Linux Display Probe"
  echo
  echo "- os-release: $(grep '^PRETTY_NAME=' /etc/os-release 2>/dev/null | cut -d= -f2- | tr -d '"' || true)"
  echo "- XDG_SESSION_TYPE: ${XDG_SESSION_TYPE:-}"
  echo "- XDG_CURRENT_DESKTOP: ${XDG_CURRENT_DESKTOP:-}"
  echo "- DISPLAY: ${DISPLAY:-}"
  echo "- WAYLAND_DISPLAY: ${WAYLAND_DISPLAY:-}"
  echo
  echo "## Commands"
  for c in gdbus busctl xprop xdotool wmctrl ydotool swaymsg loginctl; do
    if command -v "$c" >/dev/null 2>&1; then echo "- $c: $(command -v $c)"; else echo "- $c: missing"; fi
  done
  echo
  echo "## AT-SPI import"
  python3 - <<'PY' || true
try:
    import pyatspi
    print("pyatspi: ok")
except Exception as exc:
    print(f"pyatspi: fail: {type(exc).__name__}: {exc}")
PY
  echo
  echo "## Portal quick check"
  if command -v gdbus >/dev/null 2>&1; then
    gdbus introspect --session --dest org.freedesktop.portal.Desktop --object-path /org/freedesktop/portal/desktop 2>&1 | head -80 || true
  fi
} | tee artifacts/linux-display-probe.md
