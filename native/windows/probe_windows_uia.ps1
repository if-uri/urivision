# Windows UIA native readiness probe.
# Run from repository root in an interactive desktop session.
$ErrorActionPreference = "Continue"
New-Item -ItemType Directory -Force -Path artifacts | Out-Null
$result = [ordered]@{
  schema = "schema://runtime/windows-uia-probe.v1"
  os = [Environment]::OSVersion.VersionString
  user = [Environment]::UserName
  session = (Get-Process -Id $PID).SessionId
  powershell = $PSVersionTable.PSVersion.ToString()
  checks = @{}
}
try {
  Add-Type -AssemblyName UIAutomationClient
  $root = [System.Windows.Automation.AutomationElement]::RootElement
  $result.checks.uia_root = @{ ok = $true; name = $root.Current.Name; className = $root.Current.ClassName }
} catch {
  $result.checks.uia_root = @{ ok = $false; error = $_.Exception.Message }
}
try {
  Add-Type -AssemblyName System.Windows.Forms
  $screens = [System.Windows.Forms.Screen]::AllScreens | ForEach-Object { @{ DeviceName=$_.DeviceName; Bounds=$_.Bounds.ToString(); Primary=$_.Primary } }
  $result.checks.screens = @{ ok = $true; screens = $screens }
} catch {
  $result.checks.screens = @{ ok = $false; error = $_.Exception.Message }
}
try {
  $result.checks.integrity = @{ ok = $true; whoami = (whoami /all | Out-String) }
} catch {
  $result.checks.integrity = @{ ok = $false; error = $_.Exception.Message }
}
$result | ConvertTo-Json -Depth 6 | Tee-Object -FilePath artifacts/windows-uia-probe.json
