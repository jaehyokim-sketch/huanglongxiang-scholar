# setup_skill.ps1
# 황룡상 스킬을 현재 PC의 Antigravity / Gemini 글로벌 스킬 디렉토리에 자동 복사합니다.

$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$ProjectRoot = Split-Path -Parent $ScriptDir
$SkillSource = Join-Path $ProjectRoot "skill"

$GlobalSkillDir = Join-Path $env:USERPROFILE ".gemini\config\skills\huanglongxiang-scholar"

Write-Host "==========================================" -ForegroundColor Cyan
Write-Host " 황룡상 스킬 자동 설치 스크립트 (Windows)" -ForegroundColor Cyan
Write-Host "==========================================" -ForegroundColor Cyan

if (-not (Test-Path $SkillSource)) {
    Write-Error "스킬 소스 디렉토리를 찾을 수 없습니다: $SkillSource"
    exit 1
}

New-Item -ItemType Directory -Force -Path $GlobalSkillDir | Out-Null
Copy-Item -Path "$SkillSource\*" -Destination $GlobalSkillDir -Recurse -Force

Write-Host "[성공] 황룡상 스킬이 글로벌 설정에 성공적으로 등록되었습니다!" -ForegroundColor Green
Write-Host "설치 경로: $GlobalSkillDir" -ForegroundColor Yellow
Write-Host ""
Write-Host "이제 Antigravity IDE 또는 AI 환경에서 [황룡상] 또는 @황룡상 키워드로 즉시 호출할 수 있습니다." -ForegroundColor White
