# Changelog

## [0.3.0] - 2026-07-05

### Fixed
- Fix ast-unused-imports issues (ticket-4d9db1fd)
- Fix ast-sorted-imports issues (ticket-cb1d25dd)
- Fix ruff-sorted-imports issues (ticket-e983bf45)
- Fix import-optimization issues (ticket-48798700)
- Fix no-relative-imports issues (ticket-f0039f54)
- Fix relative-imports issues (ticket-18354d79)
- Fix ast-unused-imports issues (ticket-ab36d561)
- Fix import-optimization issues (ticket-06f9bfc7)
- Fix no-relative-imports issues (ticket-11c52b45)
- Fix ast-unused-imports issues (ticket-accab73a)
- Fix ast-sorted-imports issues (ticket-9009fc44)
- Fix ast-print-statements issues (ticket-289ab4b5)
- Fix ruff-print-statements issues (ticket-961cf411)
- Fix ruff-sorted-imports issues (ticket-f6efc19c)
- Fix import-optimization issues (ticket-8ee835ed)
- Fix no-relative-imports issues (ticket-7d7b4580)
- Fix ast-unused-imports issues (ticket-2edffdad)
- Fix import-optimization issues (ticket-f7e5ed4a)
- Fix ast-unused-imports issues (ticket-ee3b04d4)
- Fix string-concat-fstring issues (ticket-279b9ae8)
- Fix import-optimization issues (ticket-e1009ff1)
- Fix no-relative-imports issues (ticket-c21e2dac)
- Fix relative-imports issues (ticket-c3095a1c)
- Fix ast-unused-imports issues (ticket-5dab41ed)
- Fix no-relative-imports issues (ticket-56c1e7f5)
- Fix ast-unused-imports issues (ticket-ec276bad)
- Fix ast-sorted-imports issues (ticket-b4d953a1)
- Fix relative-imports issues (ticket-d42c72c6)
- Fix ast-unused-imports issues (ticket-72dc4b62)
- Fix string-concat-fstring issues (ticket-757dd4d2)
- Fix pylint-string-concat issues (ticket-a797c6db)
- Fix magic-numbers issues (ticket-f5874ac0)
- Fix string-formatting issues (ticket-bd94cb58)
- Fix import-optimization issues (ticket-9b6830f8)
- Fix no-relative-imports issues (ticket-56893969)
- Fix relative-imports issues (ticket-b63e3160)
- Fix ast-unused-imports issues (ticket-8dda4925)
- Fix string-concat-fstring issues (ticket-aa6b6fbd)
- Fix import-optimization issues (ticket-63184783)
- Fix no-relative-imports issues (ticket-ddd43d66)
- Fix ast-unused-imports issues (ticket-dea1df07)
- Fix ast-sorted-imports issues (ticket-9deec90c)
- Fix pylint-string-concat issues (ticket-4b5f9f60)
- Fix string-formatting issues (ticket-67f7a4e0)
- Fix import-optimization issues (ticket-4a20d150)
- Fix ast-unused-imports issues (ticket-64980923)
- Fix ast-sorted-imports issues (ticket-03bf8e00)
- Fix import-optimization issues (ticket-eac52e7c)
- Fix ast-unused-imports issues (ticket-dc1fbf62)
- Fix import-optimization issues (ticket-31cfdae9)
- Fix no-relative-imports issues (ticket-e7ce27e6)
- Fix ast-unused-imports issues (ticket-a104b40c)
- Fix string-concat-fstring issues (ticket-3d28102a)
- Fix import-optimization issues (ticket-017c3cd7)
- Fix no-relative-imports issues (ticket-a7a82154)
- Fix relative-imports issues (ticket-99b1bfc2)
- Fix ast-unused-imports issues (ticket-ca5ab7a2)
- Fix ast-sorted-imports issues (ticket-8677f697)
- Fix ast-string-concat issues (ticket-73f4abc1)
- Fix ast-missing-return-type issues (ticket-2e9de217)
- Fix ruff-sorted-imports issues (ticket-e9eebdd8)
- Fix smart-return-type issues (ticket-cf99797e)
- Fix string-concat-fstring issues (ticket-a79e1151)
- Fix magic-numbers issues (ticket-de1c208e)
- Fix no-relative-imports issues (ticket-79c7fdb0)
- Fix relative-imports issues (ticket-719b9718)
- Fix ast-unused-imports issues (ticket-0783ab84)
- Fix ast-string-concat issues (ticket-412ca0c9)
- Fix string-concat-fstring issues (ticket-807b8a32)
- Fix import-optimization issues (ticket-427095e4)
- Fix no-relative-imports issues (ticket-0874e147)
- Fix ast-unused-imports issues (ticket-3b6ce654)
- Fix ast-unused-imports issues (ticket-1ed82426)
- Fix llm-generated-code issues (ticket-5f95b4a8)
- Fix import-optimization issues (ticket-efd39a96)
- Fix ast-unused-imports issues (ticket-573564e9)
- Fix string-concat-fstring issues (ticket-a3964124)
- Fix no-relative-imports issues (ticket-d2b32501)
- Fix ast-sorted-imports issues (ticket-b4b364d0)
- Fix ast-string-concat issues (ticket-9f0137ab)
- Fix ast-missing-return-type issues (ticket-9f69b997)
- Fix ruff-sorted-imports issues (ticket-9872b6b5)
- Fix string-concat-fstring issues (ticket-322cde9e)
- Fix import-optimization issues (ticket-feeb6fbc)
- Fix ast-missing-return-type issues (ticket-c783f64d)
- Fix ruff-sorted-imports issues (ticket-4357a227)
- Fix smart-return-type issues (ticket-157ccfb0)
- Fix ai-boilerplate issues (ticket-c1752654)
- Fix ast-unused-imports issues (ticket-4e2e9eb3)
- Fix ast-sorted-imports issues (ticket-8431e6f7)
- Fix ast-missing-return-type issues (ticket-a4f7785e)
- Fix ruff-sorted-imports issues (ticket-45feeabe)

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
