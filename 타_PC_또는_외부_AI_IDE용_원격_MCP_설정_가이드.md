# 🌐 타 PC 또는 외부 AI IDE용 [황룡상] 원격 MCP 설정 가이드

본 가이드는 대용량 데이터베이스 파일(수십 MB~수 GB)을 로컬에 직접 다운로드하거나 저장소를 복제(Clone)하지 않고도, **GitHub 공개 원격 저장소의 369만 자 전수 DB를 실시간 스트리밍으로 연결하여 조회하는 MCP(Model Context Protocol) 연동 방법**을 안내합니다.

- **공개 원격 저장소**: [https://github.com/jaehyokim-sketch/huanglongxiang-scholar](https://github.com/jaehyokim-sketch/huanglongxiang-scholar)
- **원격 스트리밍 서버 파일**: `mcp_server/remote_server.py` (표준 Python 라이브러리만 사용, 외부 패키지 설치 불필요 - Zero-Dependency)

---

## 1. 사전 준비 (Prerequisites)

1. **Python 3.8 이상 설치**:
   - 터미널에서 `python --version` 또는 `python3 --version`으로 확인.
2. **`remote_server.py` 단일 파일 다운로드**:
   - 원격 연동을 위해서는 `remote_server.py` 스크립트 파일 1개만 있으면 됩니다.
   - **PowerShell (Windows)**:
     ```powershell
     Invoke-WebRequest -Uri "https://raw.githubusercontent.com/jaehyokim-sketch/huanglongxiang-scholar/main/mcp_server/remote_server.py" -OutFile "remote_server.py"
     ```
   - **cURL (Mac / Linux / Windows)**:
     ```bash
     curl -O https://raw.githubusercontent.com/jaehyokim-sketch/huanglongxiang-scholar/main/mcp_server/remote_server.py
     ```

---

## 2. AI 환경별 원격 MCP 서버 설정

각 AI 도구의 MCP 설정 파일(`mcpServers` 객체)에 아래 설정을 복사하여 등록합니다.  
*(※ `<PATH_TO_FILE>`을 다운로드받은 `remote_server.py`의 실제 절대 경로로 변경하세요.)*

### ① Claude Desktop

설정 파일 경로:
- **Windows**: `%APPDATA%\Claude\claude_desktop_config.json`
- **macOS**: `~/Library/Application Support/Claude/claude_desktop_config.json`

```json
{
  "mcpServers": {
    "huanglongxiang-scholar-remote": {
      "command": "python",
      "args": [
        "C:/Users/사용자명/remote_server.py",
        "--repo", "jaehyokim-sketch/huanglongxiang-scholar",
        "--branch", "main"
      ],
      "env": {
        "PYTHONIOENCODING": "utf-8"
      }
    }
  }
}
```

---

### ② Antigravity IDE / VS Code

작업 공간의 `.vscode/mcp.json` 또는 전역 `mcp_config.json`:

```json
{
  "servers": {
    "huanglongxiang-scholar-remote": {
      "type": "stdio",
      "command": "python",
      "args": [
        "C:/Users/사용자명/remote_server.py",
        "--repo", "jaehyokim-sketch/huanglongxiang-scholar",
        "--branch", "main"
      ],
      "env": {
        "PYTHONIOENCODING": "utf-8"
      }
    }
  }
}
```

---

### ③ Cursor IDE

1. **Settings** (`Ctrl + Shift + J` 또는 `Cmd + Shift + J`) ➔ **Features** ➔ **MCP Servers** 이동
2. **Add New MCP Server** 클릭:
   - **Name**: `huanglongxiang-scholar-remote`
   - **Type**: `stdio`
   - **Command**: `python C:/Users/사용자명/remote_server.py --repo jaehyokim-sketch/huanglongxiang-scholar --branch main`

---

### ④ Cline / Roo Code / Windsurf

`cline_mcp_settings.json` 또는 확장 프로그램 MCP 설정:

```json
{
  "mcpServers": {
    "huanglongxiang-scholar-remote": {
      "command": "python",
      "args": [
        "/Users/사용자명/remote_server.py",
        "--repo", "jaehyokim-sketch/huanglongxiang-scholar",
        "--branch", "main"
      ],
      "env": {
        "PYTHONIOENCODING": "utf-8"
      },
      "disabled": false,
      "autoApprove": []
    }
  }
}
```

---

## 3. 원격 MCP 서버에서 제공하는 4대 도구 (Tools)

원격 MCP 서버가 연결되면 AI는 아래 4개 도구를 자율적으로 호출하여 369만 자 원문을 실시간으로 탐색합니다:

| 도구명 (Tool Name) | 설명 | 주요 매개변수 |
| :--- | :--- | :--- |
| **`search_huanglongxiang_db`** | 4대 명저 및 42편 논문 DB에서 키워드/한자/학술 개념 원격 고속 검색 | `query`, `book_filter`, `limit` |
| **`get_acupoint_source`** | 특정 경혈의 4단계 문헌 층차(선진~명청), 정위 왜곡 비판, 올바른 표준 정위 원문 일괄 추출 | `acupoint_name` (예: `合谷`, `足三里`) |
| **`get_academic_paper`** | 42편 전수 학술논문 중 번호(`01`~`42`) 또는 제목 키워드로 전문 조회 | `paper_id_or_title` (예: `06`, `五关`) |
| **`get_scholar_framework`** | 황룡상 5대 공리 및 3단계 분석-평가-기술(Analysis-Evaluation-Description) 프로토콜 반환 | 없음 |

---

## 4. [황룡상] AI 글로벌 스킬(Prompt) 연동

MCP 도구 외에 AI가 황룡상 교수의 엄밀한 고증학적 사고방식(5대 공리 및 3단계 프로토콜)으로 사고하도록 스킬 정의 파일을 글로벌 프롬프트로 등록할 수 있습니다.

### 스킬 정의 파일 다운로드 및 등록
- **스킬 파일 원격 URL**: `https://raw.githubusercontent.com/jaehyokim-sketch/huanglongxiang-scholar/main/skill/SKILL.md`
- **Windows 등록 경로**: `%USERPROFILE%\.gemini\config\skills\huanglongxiang-scholar\SKILL.md`
- **Mac / Linux 등록 경로**: `~/.gemini/config/skills/huanglongxiang-scholar/SKILL.md`

#### 원클릭 다운로드 스크립트 (PowerShell)
```powershell
$SkillDir = "$HOME\.gemini\config\skills\huanglongxiang-scholar"
if (-not (Test-Path $SkillDir)) { New-Item -ItemType Directory -Path $SkillDir -Force }
Invoke-WebRequest -Uri "https://raw.githubusercontent.com/jaehyokim-sketch/huanglongxiang-scholar/main/skill/SKILL.md" -OutFile "$SkillDir\SKILL.md"
Write-Host "황룡상 글로벌 스킬 등록 완료!" -ForegroundColor Green
```

---

## 5. 질문 및 활용 예시 프롬프트

설정이 완료되면 채팅창에서 다음과 같이 질문하여 원격 DB 기반의 실증적 고증 보고서를 작성받을 수 있습니다:

```text
[질문 예시 1]
"@황룡상 족삼리(ST36)의 취혈 자세와 춘수 계측 오류에 대해 황룡상 교수의 고증과 원전 근거를 바탕으로 3단계(분석-평가-기술) 보고서를 작성해줘."

[질문 예시 2]
"[황룡상] 수궐음심포경이 11경맥에서 12경맥으로 진화하게 된 문헌 층차와 발생학적 원인을 황룡상 교수의 논문 및 저작을 인용하여 설명해줘."

[질문 예시 3]
"관충혈(TE1) 점자출혈 요법의 신경해부학적 기전과 주치증 변천사를 황룡상 교수 저작 DB를 검색하여 HTML 보고서로 작성해줘."
```

---

## 6. 문제 해결 및 FAQ (Troubleshooting)

### Q1. 한글/한자가 깨져서 검색되지 않습니다.
- MCP 환경 변수에 `"PYTHONIOENCODING": "utf-8"`이 포함되어 있는지 확인하세요.
- `remote_server.py`는 내부적으로 Windows UTF-8 입출력 표준 재구성을 수행합니다.

### Q2. GitHub API 호출 횟수 제한(Rate Limit)이 발생하나요?
- `remote_server.py`는 메모리 캐싱(`_REMOTE_CACHE`)을 적용하여 한 번 읽어온 책/논문 데이터를 재다운로드하지 않고 재사용합니다.
- 대량 조회가 필요한 경우 GitHub Personal Access Token(PAT)을 인자로 추가할 수 있습니다:
  ```bash
  python remote_server.py --repo jaehyokim-sketch/huanglongxiang-scholar --branch main --token ghp_YOUR_TOKEN_HERE
  ```
