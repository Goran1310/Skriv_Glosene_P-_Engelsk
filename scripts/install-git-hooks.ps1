#!/usr/bin/env pwsh

$ErrorActionPreference = "Stop"
$RepoRoot = Split-Path -Parent $PSScriptRoot

git -C $RepoRoot config core.hooksPath scripts/git-hooks
Write-Host "Git pre-push deployment guard installed for this repository."