$ErrorActionPreference = "Stop"

$repoRoot = Split-Path -Parent $PSScriptRoot
$sourceRoot = Join-Path $repoRoot "paper-research-skill-v0.3.0\skills"
$skillsRoot = Join-Path $env:USERPROFILE ".codex\skills"
$skills = @("paper-research-cn-core", "paper-review-cn-core")

New-Item -ItemType Directory -Force $skillsRoot | Out-Null

foreach ($skill in $skills) {
    $source = Join-Path $sourceRoot $skill
    $target = Join-Path $skillsRoot $skill
    if (-not (Test-Path -LiteralPath $source)) {
        throw "Missing skill source: $source"
    }
    Copy-Item -LiteralPath $source -Destination $target -Recurse -Force
    Write-Host "Installed $skill -> $target"
}

Write-Host "Done. Open a new Codex task and invoke `$paper-research-cn-core or `$paper-review-cn-core."
