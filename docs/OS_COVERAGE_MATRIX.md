# OS Coverage Matrix

## Why the old 4-profile matrix is not enough

The Docker matrix covers backend classes, not the real installed OS landscape.
It is enough for architecture validation, but not enough to claim broad OS
support.

## Priority profiles

The package now defines these native targets in `src/urivision/native_profiles.py`:

- `windows-11-uia`
- `windows-10-uia-esu`
- `windows-server-rds`
- `macos-26-ax-apple-silicon`
- `macos-14-15-ax`
- `ubuntu-24-04-wayland`
- `ubuntu-22-04-x11`
- `fedora-gnome-wayland`
- `kde-plasma-wayland`
- `debian-rhel-enterprise`
- `chromeos-chrome-android-linux`
- `android-adb-uiautomator`
- `ios-xcuitest`
- `vnc-novnc-rfb`
- `rdp-citrix-horizon`
- `hid-kvm-rp2040`

## Interpretation

- Windows/macOS are native-only for real UI automation.
- Linux X11/noVNC can be tested partially in Docker.
- Wayland requires compositor/session-specific proof.
- Android/iOS require mobile automation stacks, not desktop stacks.
- BIOS/login/dead OS requires HID/KVM.
- ChromeOS is a mixed stack: Chrome DOM, Android container, Crostini Linux and
  possibly hardware fallback.

## Coverage levels

```text
L0 contract: URI resolves, payload schema valid, dry-run works.
L1 mock: URI action modifies controlled mock state.
L2 native smoke: real OS executes one query and one command with postcondition.
L3 app benchmark: representative apps pass.
L4 hostile UI: custom canvas/legacy app handled with fallback.
L5 production policy: telemetry, trace, safety and rollback strategy present.
```

Claim support only at the level that has evidence.
