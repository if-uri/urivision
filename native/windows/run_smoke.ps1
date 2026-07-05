$ErrorActionPreference = "Stop"
$env:PYTHONPATH = "src"
python -m unittest discover -s tests -v
python tools/probe_native_host.py --out artifacts/native-host-probe.json
python -m urivision.cli native-matrix --format json | Out-File -Encoding utf8 artifacts/native-matrix-from-cli.json
python -m urivision.cli route type_text --profile windows-11-uia | Out-File -Encoding utf8 artifacts/route-windows-type-text.json
powershell -ExecutionPolicy Bypass -File native/windows/probe_windows_uia.ps1
