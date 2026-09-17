#!/usr/bin/env bash
# setup_skill.sh
# Copy huanglongxiang-scholar skill to ~/.gemini/config/skills/

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
SKILL_SOURCE="$PROJECT_ROOT/skill"
GLOBAL_SKILL_DIR="$HOME/.gemini/config/skills/huanglongxiang-scholar"

echo "=========================================="
echo " 황룡상 스킬 자동 설치 스크립트 (Mac/Linux)"
echo "=========================================="

if [ ! -d "$SKILL_SOURCE" ]; then
    echo "[오류] 스킬 소스 디렉토리를 찾을 수 없습니다: $SKILL_SOURCE"
    exit 1
fi

mkdir -p "$GLOBAL_SKILL_DIR"
cp -r "$SKILL_SOURCE"/* "$GLOBAL_SKILL_DIR/"

echo "[성공] 황룡상 스킬이 글로벌 설정에 등록되었습니다!"
echo "설치 경로: $GLOBAL_SKILL_DIR"
