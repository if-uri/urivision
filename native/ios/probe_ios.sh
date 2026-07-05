#!/usr/bin/env bash
set -euo pipefail
mkdir -p artifacts
{
  echo '# iOS/XCUITest Probe'
  echo
  if command -v xcodebuild >/dev/null 2>&1; then
    echo '## xcodebuild version'
    xcodebuild -version || true
  else
    echo 'xcodebuild: missing'
  fi
  echo
  if command -v xcrun >/dev/null 2>&1; then
    echo '## Available simulators'
    xcrun simctl list devices available | head -120 || true
  else
    echo 'xcrun: missing'
  fi
  echo
  echo 'Need native Mac runner with simulator/device, signing, WebDriverAgent/Appium or XCUITest harness.'
} | tee artifacts/ios-xcuitest-probe.md
