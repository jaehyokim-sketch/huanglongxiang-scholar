# deploy/push_to_github.ps1
# GitHub 원격 저장소 생성 및 푸시 도우미 스크립트

param (
    [string]$RepoUrl = "",
    [string]$RepoName = "huanglongxiang-scholar",
    [switch]$Public
)

$GitExe = "C:\Users\meddo\.local\mingit\cmd\git.exe"
if (-not (Test-Path $GitExe)) {
    $GitExe = "git"
}

$GhExe = "C:\Users\meddo\.local\gh\bin\gh.exe"
if (-not (Test-Path $GhExe)) {
    $GhExe = "gh"
}

Write-Host "==========================================" -ForegroundColor Cyan
Write-Host " 황룡상 DB & 스킬 GitHub 푸시 도우미" -ForegroundColor Cyan
Write-Host "==========================================" -ForegroundColor Cyan

if ($RepoUrl -ne "") {
    Write-Host "[1] 지정된 원격 저장소 URL로 푸시합니다: $RepoUrl" -ForegroundColor Yellow
    & $GitExe remote remove origin 2>$null
    & $GitExe remote add origin $RepoUrl
    & $GitExe branch -M main
    & $GitExe push -u origin main
    if ($LASTEXITCODE -eq 0) {
        Write-Host "[성공] GitHub 푸시가 완료되었습니다!" -ForegroundColor Green
    } else {
        Write-Host "[오류] 푸시 실패. GitHub 계정 권한 또는 URL을 확인해 주세요." -ForegroundColor Red
    }
    exit
}

# Check gh auth status
Write-Host "[2] GitHub CLI(gh)를 통한 자동 원격 저장소 생성 시도 중..." -ForegroundColor Yellow
& $GhExe auth status 2>$null

if ($LASTEXITCODE -ne 0) {
    Write-Host ""
    Write-Host "[안내] GitHub 로그인이 필요합니다. 아래 명령어로 로그인해 주세요:" -ForegroundColor Yellow
    Write-Host "  gh auth login" -ForegroundColor White
    Write-Host ""
    Write-Host "또는 이미 GitHub에서 저장소를 생성하셨다면 아래 명령어로 푸시하세요:" -ForegroundColor Yellow
    Write-Host "  .\deploy\push_to_github.ps1 -RepoUrl 'https://github.com/<사용자ID>/$RepoName.git'" -ForegroundColor White
    exit
}

$VisibilityFlag = if ($Public) { "--public" } else { "--private" }
Write-Host "저장소 생성 중 ($RepoName, $VisibilityFlag)..." -ForegroundColor Yellow
& $GhExe repo create $RepoName $VisibilityFlag --source=. --remote=origin --push

if ($LASTEXITCODE -eq 0) {
    Write-Host "[성공] GitHub 원격 저장소가 성공적으로 생성되고 푸시되었습니다!" -ForegroundColor Green
}
