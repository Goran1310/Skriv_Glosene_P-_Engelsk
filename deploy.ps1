#!/usr/bin/env pwsh
# Build and Deploy to Netlify via GitHub Push
param(
    [string]$Message = "Update vocabulary - $(Get-Date -Format 'yyyy-MM-dd HH:mm')",
    [string]$ProductionBranch = "main"
)

$ErrorActionPreference = "Stop"
$RepoRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $RepoRoot
$SourceBranch = (git branch --show-current).Trim()

if ([string]::IsNullOrWhiteSpace($SourceBranch)) {
    Write-Host "Cannot determine the current git branch." -ForegroundColor Red
    exit 1
}

Write-Host "`n" -NoNewline
Write-Host "================================" -ForegroundColor Cyan
Write-Host "  Vocabulary Trainer Deployment" -ForegroundColor White
Write-Host "================================" -ForegroundColor Cyan
Write-Host ""

# Step 1: Build the React app
Write-Host "[1/5] Building React app..." -ForegroundColor Yellow
Set-Location "vocabulary-trainer-web"
npm run build
if ($LASTEXITCODE -ne 0) {
    Write-Host "Build failed!" -ForegroundColor Red
    Set-Location $RepoRoot
    exit 1
}
Write-Host "Build completed successfully" -ForegroundColor Green
Set-Location $RepoRoot

# Step 2: Check for changes
Write-Host "`n[2/5] Checking for changes..." -ForegroundColor Yellow
$status = git status --porcelain
if ([string]::IsNullOrWhiteSpace($status)) {
    Write-Host "No changes detected" -ForegroundColor Yellow
    Write-Host "Creating empty commit to trigger rebuild..." -ForegroundColor Yellow
    git commit --allow-empty -m $Message
} else {
    Write-Host "Changes detected" -ForegroundColor Green
    
    # Step 3: Stage and commit changes
    Write-Host "`n[3/5] Committing changes on $SourceBranch..." -ForegroundColor Yellow
    git add .
    git commit -m $Message
    if ($LASTEXITCODE -ne 0) {
        Write-Host "Commit failed!" -ForegroundColor Red
        exit 1
    }
}
Write-Host "Changes committed" -ForegroundColor Green

# Step 4: Push the source branch, then merge into production branch if needed
Write-Host "`n[4/5] Preparing production branch $ProductionBranch..." -ForegroundColor Yellow
git push -u origin $SourceBranch
if ($LASTEXITCODE -ne 0) {
    Write-Host "Push failed for $SourceBranch!" -ForegroundColor Red
    exit 1
}

if ($SourceBranch -ne $ProductionBranch) {
    git fetch origin $ProductionBranch
    git checkout $ProductionBranch
    if ($LASTEXITCODE -ne 0) {
        Write-Host "Could not check out $ProductionBranch." -ForegroundColor Red
        exit 1
    }

    git pull --ff-only origin $ProductionBranch
    if ($LASTEXITCODE -ne 0) {
        Write-Host "Could not fast-forward $ProductionBranch from origin." -ForegroundColor Red
        exit 1
    }

    git merge $SourceBranch --no-edit
    if ($LASTEXITCODE -ne 0) {
        Write-Host "Merge failed. Resolve conflicts, then rerun the deployment." -ForegroundColor Red
        exit 1
    }
}

# Step 5: Push production branch to GitHub (triggers Netlify deployment)
Write-Host "`n[5/5] Pushing $ProductionBranch to GitHub for Netlify deployment..." -ForegroundColor Yellow
git push origin $ProductionBranch
if ($LASTEXITCODE -ne 0) {
    Write-Host "Production push failed!" -ForegroundColor Red
    exit 1
}

if ($SourceBranch -ne $ProductionBranch) {
    git checkout $SourceBranch | Out-Null
}

Write-Host ""
Write-Host "================================" -ForegroundColor Green
Write-Host "  Deployment Triggered!        " -ForegroundColor White
Write-Host "================================" -ForegroundColor Green
Write-Host ""
Write-Host "Netlify will automatically build and deploy $ProductionBranch." -ForegroundColor Cyan
Write-Host "Check deployment status at: https://app.netlify.com" -ForegroundColor Cyan
Write-Host "Your app: https://effortless-bombolone-a7184d.netlify.app/" -ForegroundColor Cyan
Write-Host ""
Write-Host "Deployment usually takes 1-3 minutes." -ForegroundColor Yellow
Write-Host ""
