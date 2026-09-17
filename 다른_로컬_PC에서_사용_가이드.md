# 📖 [황룡상] 스킬 및 마스터 DB 타 PC(로컬/온라인) 연동 가이드

본 문서는 다른 로컬 PC나 노트북 환경에서 GitHub 원격 저장소에 배포된 **황룡상(黄龙祥) 침구학술 마스터 DB 및 스킬**을 연동하여 사용하는 방법을 안내합니다.

- **GitHub 원격 저장소**: [https://github.com/jaehyokim-sketch/huanglongxiang-scholar](https://github.com/jaehyokim-sketch/huanglongxiang-scholar)
- **저장소 구분**: Private (비공개)

---

## 🚀 방법 1. 저장소 Clone 후 로컬 MCP 연동 (강력 권장)

오프라인 상태에서도 작동하며, 369만 자 코퍼스를 100% 로컬 환경에서 가장 빠른 속도로 검색/인용할 수 있는 표준 방식입니다.

### 1단계: 저장소 복제 (Clone)
새로운 PC의 터미널(PowerShell 또는 Terminal)을 열고 원하는 폴더에서 아래 명령을 실행합니다:

```bash
git clone https://github.com/jaehyokim-sketch/huanglongxiang-scholar.git
cd huanglongxiang-scholar
```
*(※ 비공개 저장소이므로 GitHub 로그인 또는 Personal Access Token(PAT) 입력 창이 나타납니다.)*

---

### 2단계: AI 글로벌 스킬 원클릭 등록
AI 환경(Antigravity 등)에서 `@황룡상` 또는 `[황룡상]` 키워드로 스킬을 자동 호출할 수 있도록 등록합니다:

- **Windows 환경**:
  ```powershell
  powershell -ExecutionPolicy Bypass -File deploy\setup_skill.ps1
  ```
- **Mac / Linux 환경**:
  ```bash
  bash deploy/setup_skill.sh
  ```
> 💡 위 스크립트를 실행하면 현재 사용자의 `~/.gemini/config/skills/huanglongxiang-scholar` 경로에 스킬 본문(`SKILL.md`)과 고증 레퍼런스가 자동으로 복사·등록됩니다.

---

### 3단계: MCP (Model Context Protocol) 서버 등록
사용하시는 AI 도구의 MCP 설정 파일에 서버 실행 구문을 등록합니다.

#### A. Antigravity IDE / Cursor / VS Code
- 프로젝트의 `.gemini/mcp_config.json` 또는 글로벌 MCP 설정 파일에 아래 내용을 추가합니다:
```json
{
  "mcpServers": {
    "huanglongxiang-scholar": {
      "command": "python",
      "args": [
        "C:/Users/<사용자명>/.../huanglongxiang-scholar/mcp_server/server.py"
      ],
      "env": {
        "PYTHONIOENCODING": "utf-8"
      }
    }
  }
}
```
*(※ `args` 경로의 슬래시는 `/`를 사용하며, 실제 clone 받은 `server.py`의 절대 경로를 입력합니다.)*

#### B. Claude Desktop
- 설정 파일 위치: `%APPDATA%\Claude\claude_desktop_config.json`
```json
{
  "mcpServers": {
    "huanglongxiang-scholar": {
      "command": "python",
      "args": [
        "C:/Users/<사용자명>/.../huanglongxiang-scholar/mcp_server/server.py"
      ],
      "env": {
        "PYTHONIOENCODING": "utf-8"
      }
    }
  }
}
```

---

## 🌐 방법 2. Remote GitHub Streaming MCP (DB 다운로드 없이 온라인 사용)

새 PC에 12MB 상당의 DB 파일을 직접 clone하지 않고, `mcp_server/remote_server.py` 파일만 다운받아 GitHub 원격 저장소에서 실시간으로 스트리밍 조회하는 방식입니다.

### 1단계: GitHub Personal Access Token (PAT) 발급 (Private 저장소 접근용)
1. GitHub 웹사이트 ➔ **Settings ➔ Developer Settings ➔ Personal access tokens ➔ Fine-grained tokens** (또는 Tokens classic) 이동
2. `repo` 읽기 권한을 부여하고 토큰 생성 (예: `ghp_xxxx...`)

### 2단계: MCP 설정 파일 등록
```json
{
  "mcpServers": {
    "huanglongxiang-scholar-remote": {
      "command": "python",
      "args": [
        "C:/경로/remote_server.py",
        "--repo", "jaehyokim-sketch/huanglongxiang-scholar",
        "--branch", "main",
        "--token", "ghp_여기에_토큰_입력"
      ],
      "env": {
        "PYTHONIOENCODING": "utf-8"
      }
    }
  }
}
```

---

## 🛠️ 제공되는 황룡상 학술 MCP 도구 (Tools)

연동이 완료되면 AI 대화창에서 아래 기능들을 자유롭게 활용할 수 있습니다:

| 도구명 | 기능 설명 | 활용 예시 |
| :--- | :--- | :--- |
| `search_huanglongxiang_db` | 369만 자 전체 코퍼스 고속 키워드/정규식 검색 및 문맥 발췌 | `query: "합곡"`, `query: "11경맥"` |
| `get_acupoint_source` | 특정 혈위의 선진~명청 문헌 층차, 고증 비판, 표준 정위 원문 일괄 추출 | `acupoint_name: "合谷"` |
| `get_academic_paper` | 황룡상 교수 42편 전수 논문 중 특정 번호(01~42) 또는 제목 전문 조회 | `paper_id_or_title: "42"` 또는 `"五关"` |
| `get_scholar_framework` | 황룡상 5대 공리 및 3단계 분석-평가-기술(Analysis-Evaluation-Description) 프로토콜 지침 반환 | - |

---

## ❓ 자주 묻는 질문 및 문제 해결 (Troubleshooting)

1. **Q. 한글/한자 출력 시 글자가 깨지거나 인코딩 에러가 발생합니다.**
   - MCP 설정의 `"env"` 블록에 `"PYTHONIOENCODING": "utf-8"`이 포함되어 있는지 확인하세요.
2. **Q. 파이썬 명령어가 인식되지 않습니다.**
   - 타 PC에 Python 3.8 이상이 설치되어 있고 환경 변수 PATH에 등록되어 있는지 확인하거나, `python` 대신 `python3` 또는 `C:/Python312/python.exe` 등 절대 경로를 지정하세요.
3. **Q. 의존성 패키지(pip install)가 필요한가요?**
   - **필요 없습니다.** 본 MCP 서버(`server.py`, `remote_server.py`)는 파이썬 표준 내장 라이브러리만을 사용하여 구현된 **Zero-Dependency** 서버이므로 추가 설치 없이 바로 실행됩니다.
