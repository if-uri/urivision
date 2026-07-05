# Changelog

## [0.3.0] - 2026-07-05

### Added
- URI Runtime Control Plane: CapabilityRegistry, parser/matcher URI, orchestrator planów JSON,
  `@uri_function` (migracja funkcji Pythona do kontraktów URI), katalog capability dla LLM.
- Native Test Lab: profile natywne OS (Windows/macOS/Linux X11+Wayland/Android/iOS/VNC/RDP/HID),
  method router, `urivision native-matrix|native-probe|route|route-matrix`, gate confidence.
- Warstwa Docker: 4 profile backendów (linux-x11-novnc, linux-wayland-headless,
  windows-uia-contract, macos-ax-contract) + `make docker-*`.
- CI: native-contract.yml + self-hosted-native-smoke.yml; artifacts/ z macierzami.
- Dokumentacja: ADAPTER_CONTRACT, NATIVE_TEST_LAB, OS_COVERAGE_MATRIX, METHOD_ROUTER_DESIGN,
  EVENT_TRACE_SCHEMA, BENCHMARK_PLAN, SECURITY_POLICY.

### Changed
- Warstwa runtime rozwinięta w `urivision_uri_runtime/` scalona do katalogu głównego
  (src/tests/tools/docs/docker/examples); podkatalog usunięty. README/pyproject/Makefile
  zaktualizowane do wersji 0.3.0.

## [0.1.10] - 2026-07-05

### Fixed
- Fix relative-imports issues (ticket-e4d036e1)
- Fix unused-imports issues (ticket-0c8a2320)
- Fix relative-imports issues (ticket-58e75d86)
- Fix string-concat issues (ticket-86b3cacb)
- Fix unused-imports issues (ticket-745d4e63)
- Fix relative-imports issues (ticket-701cf536)
- Fix unused-imports issues (ticket-7e5da924)
- Fix ai-boilerplate issues (ticket-d53fd5dc)
- Fix unused-imports issues (ticket-27a070a0)
- Fix unused-imports issues (ticket-74ee80de)
- Fix relative-imports issues (ticket-62bf42da)
- Fix unused-imports issues (ticket-94a21166)
- Fix relative-imports issues (ticket-26c51441)
- Fix string-concat issues (ticket-0dce1485)
- Fix unused-imports issues (ticket-d15ad1f2)
- Fix relative-imports issues (ticket-a3d14675)
- Fix string-concat issues (ticket-f782fed3)
- Fix unused-imports issues (ticket-0ad897b0)
- Fix smart-return-type issues (ticket-04dde2d7)
- Fix string-concat issues (ticket-47e1b998)
