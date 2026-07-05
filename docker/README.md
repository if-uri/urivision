# Docker layer for URI Runtime backend testing

This layer has two purposes:

1. Run the dependency-free URI Runtime contract matrix in a reproducible container.
2. Prepare Linux display harnesses for later real adapter work: X11/noVNC and Wayland/headless.

## What is tested here

The default matrix covers four profiles:

- `linux-x11-novnc` — Linux X11/noVNC profile, prepared for Xvfb/x11vnc style connector tests.
- `linux-wayland-headless` — Linux Wayland/headless profile, prepared for portal/libei/AT-SPI style connector tests.
- `windows-uia-contract` — Windows UI Automation contract profile. This is **not** real UIA execution inside Linux Docker.
- `macos-ax-contract` — macOS AXUIElement contract profile. This is **not** real AX execution inside Linux Docker.

The Windows and macOS profiles validate URI contracts, payload schemas, capability discovery, orchestration and verify-before-act behavior. Real native execution requires native Windows/macOS runners.

## Run

From repository root:

```bash
# Contract matrix for all four profiles
python tools/run_backend_matrix.py

# Dockerized contract matrix
DOCKER_BUILDKIT=1 docker compose -f docker/docker-compose.yml run --rm uri-runtime-matrix

# Linux X11/noVNC harness
DOCKER_BUILDKIT=1 docker compose -f docker/docker-compose.yml --profile linux-x11 up --build --abort-on-container-exit

# Linux Wayland/headless harness
DOCKER_BUILDKIT=1 docker compose -f docker/docker-compose.yml --profile linux-wayland up --build --abort-on-container-exit

# Windows/macOS contract profiles in Linux container
DOCKER_BUILDKIT=1 docker compose -f docker/docker-compose.yml --profile contract up --build --abort-on-container-exit
```

Outputs are written to `artifacts/*.json` and `artifacts/backend-matrix.md`.

## Next native runners

For real four-OS testing add CI jobs outside Linux Docker:

- Windows Server/Windows 11 runner: install Python, install the package, run `tools/probe_runtime.py --profile windows-uia-contract`, then replace handlers with a real UIA adapter.
- macOS runner: install Python, grant Accessibility/Screen Recording/Input Monitoring permissions, run `tools/probe_runtime.py --profile macos-ax-contract`, then replace handlers with a real AX adapter.
- Linux X11 runner/container: mount real VNC/X11 connector.
- Linux Wayland runner/container: integrate AT-SPI + portal/libei path.
