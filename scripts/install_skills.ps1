[CmdletBinding()]
param(
    [switch]$DryRun,
    [switch]$Force
)

$ErrorActionPreference = "Stop"
$repoRoot = Split-Path -Parent $PSScriptRoot
$installer = Join-Path $repoRoot "paper-research-skill-v0.4.0\install.py"
if (-not (Test-Path -LiteralPath $installer)) {
    throw "Missing package installer: $installer"
}

$arguments = @($installer, "--target", "codex")
if ($DryRun) { $arguments += "--dry-run" }
if ($Force) { $arguments += "--force" }
& python @arguments
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
