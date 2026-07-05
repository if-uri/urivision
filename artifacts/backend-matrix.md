# URI Runtime backend matrix

| Profile | OS family | Stack | Kind | Result | Steps | Limitations |
|---|---:|---|---|---:|---:|---|
| `linux-x11-novnc` | linux | x11/novnc | docker-contract-plus-x11-tools | OK | 13/13 | Coordinate mapping may differ between Xvfb, VNC and client browser scaling<br>AT-SPI data quality depends on application toolkit |
| `linux-wayland-headless` | linux | wayland/headless | docker-contract-plus-wayland-tools | OK | 13/13 | Wayland commonly blocks global pointer/keyboard injection<br>Coordinates may be surface-relative instead of global |
| `windows-uia-contract` | windows | desktop/uia | contract-only-in-linux-docker | OK | 13/13 | This Docker profile validates schema and orchestration only<br>Real UIA requires Windows permissions/session boundary handling |
| `macos-ax-contract` | macos | desktop/ax | contract-only-in-linux-docker | OK | 13/13 | This Docker profile validates schema and orchestration only<br>Real AX requires Accessibility, Screen Recording and Input Monitoring permissions |

## Important

Linux Docker cannot execute real Windows UIA or macOS AX APIs. Those two rows validate URI contracts, payload schemas and orchestration behavior only. Native adapters must be tested on real Windows/macOS hosts.
