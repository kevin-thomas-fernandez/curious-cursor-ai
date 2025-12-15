# Add npm global path to current session
$env:Path += ";C:\Users\kevin\AppData\Roaming\npm"

Write-Host "Firebase CLI is ready!" -ForegroundColor Green
Write-Host ""
Write-Host "Run these commands:" -ForegroundColor Yellow
Write-Host "1. firebase login" -ForegroundColor Cyan
Write-Host "2. firebase init hosting" -ForegroundColor Cyan
Write-Host "3. firebase deploy --only hosting" -ForegroundColor Cyan
Write-Host ""

# Check if already logged in
firebase projects:list 2>$null
if ($LASTEXITCODE -eq 0) {
    Write-Host "You're already logged in!" -ForegroundColor Green
    Write-Host "Run: firebase init hosting" -ForegroundColor Yellow
} else {
    Write-Host "You need to login first. Run: firebase login" -ForegroundColor Yellow
}

