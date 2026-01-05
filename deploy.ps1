#!/usr/bin/env pwsh
# Build and Deploy to Netlify via GitHub Push
param(
    [string]$Message = "Update vocabulary - $(Get-Date -Format 'yyyy-MM-dd HH:mm')"
)

Write-Host "`n" -NoNewline
Write-Host "================================" -ForegroundColor Cyan
Write-Host "  Vocabulary Trainer Deployment" -ForegroundColor White
Write-Host "================================" -ForegroundColor Cyan
Write-Host ""

# Step 1: Build the React app
Write-Host "[1/4] Building React app..." -ForegroundColor Yellow
Set-Location "vocabulary-trainer-web"
npm run build
if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ Build failed!" -ForegroundColor Red
    Set-Location ..
    exit 1
}
Write-Host "✅ Build completed successfully" -ForegroundColor Green
Set-Location ..

# Step 2: Check for changes
Write-Host "`n[2/4] Checking for changes..." -ForegroundColor Yellow
$status = git status --porcelain
if ([string]::IsNullOrWhiteSpace($status)) {
    Write-Host "⚠️  No changes detected" -ForegroundColor Yellow
    Write-Host "Creating empty commit to trigger rebuild..." -ForegroundColor Yellow
    git commit --allow-empty -m $Message
} else {
    Write-Host "✅ Changes detected" -ForegroundColor Green
    
    # Step 3: Stage and commit changes
    Write-Host "`n[3/4] Committing changes..." -ForegroundColor Yellow
    git add .
    git commit -m $Message
    if ($LASTEXITCODE -ne 0) {
        Write-Host "❌ Commit failed!" -ForegroundColor Red
        exit 1
    }
}
Write-Host "✅ Changes committed" -ForegroundColor Green

# Step 4: Push to GitHub (triggers Netlify deployment)
Write-Host "`n[4/4] Pushing to GitHub..." -ForegroundColor Yellow
git push
if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ Push failed!" -ForegroundColor Red
    exit 1
}

Write-Host ""
Write-Host "================================" -ForegroundColor Green
Write-Host "  ✅ Deployment Triggered!      " -ForegroundColor White
Write-Host "================================" -ForegroundColor Green
Write-Host ""
Write-Host "Netlify will automatically build and deploy your changes." -ForegroundColor Cyan
Write-Host "Check deployment status at: https://app.netlify.com" -ForegroundColor Cyan
Write-Host "Your app: https://effortless-bombolone-a7184d.netlify.app/" -ForegroundColor Cyan
Write-Host ""
Write-Host "Deployment usually takes 1-3 minutes." -ForegroundColor Yellow
Write-Host ""
