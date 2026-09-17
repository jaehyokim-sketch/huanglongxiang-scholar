# 📖 [황룡상] 침구학술 마스터 DB 및 스킬 공개 연동 가이드

본 문서는 누구나 자유롭게 GitHub 공개(Public) 원격 저장소에 등록된 **황룡상(黄龙祥) 침구학술 마스터 DB 및 스킬**을 로컬 또는 온라인 MCP 방식으로 연동하여 사용하는 방법을 안내합니다.

- **공개 원격 저장소**: [https://github.com/jaehyokim-sketch/huanglongxiang-scholar](https://github.com/jaehyokim-sketch/huanglongxiang-scholar)
- **저장소 구분**: **Public (완전 공개)** - 별도의 로그인이나 인증 토큰(PAT) 없이 즉시 사용 가능

---

## 🚀 방법 1. 저장소 Clone 후 로컬 MCP 연동 (가장 추천)

369만 자 코퍼스를 로컬에 저장하여 오프라인에서도 지연 시간 없이 100% 초고속으로 검색 및 인용할 수 있는 방식입니다.

### 1단계: 저장소 복제 (Clone)
터미널(PowerShell 또는 Terminal)에서 명령을 실행합니다 (인증 불필요):
```bash
git clone https://github.com/jaehyokim-sketch/huanglongxiang-scholar.git
cd huanglongxiang-scholar
```

---

### 2단계: AI 글로벌 스킬 등록 (선택)
AI 환경(Antigravity 등)에서 `@황룡상` 또는 `[황룡상]` 키워드로 스킬을 자동 호출할 수 있도록 등록합니다:
- **Windows**:
  ```powershell
  powershell -ExecutionPolicy Bypass -File deploy\setup_skill.ps1
  ```
- **Mac / Linux**:
  ```bash
  bash deploy/setup_skill.sh
  ```

---

### 3단계: MCP 서버 등록 (`mcp_config.json`)
Claude Desktop, Antigravity IDE, Cursor, VS Code 등의 MCP 설정 파일에 아래 구문을 추가합니다:

```json
{
  "mcpServers": {
    "huanglongxiang-scholar": {
      "command": "python",
      "args": [
        "C:/경로/huanglongxiang-scholar/mcp_server/server.py"
      ],
      "env": {
        "PYTHONIOENCODING": "utf-8"
      }
    }
  }
}
```
*(※ `args` 경로에는 실제 clone 받은 `mcp_server/server.py`의 절대 경로를 입력합니다.)*

---

## 🌐 방법 2. Remote GitHub Streaming MCP (DB 다운로드 없이 온라인 사용)

다른 PC에 DB를 clone하지 않고, `remote_server.py` 단일 파일만 실행하여 GitHub에서 실시간으로 스트리밍 조회하는 방식입니다. **저장소가 공개(Public) 상태이므로 토큰 없이 즉시 연결됩니다.**

### 1단계: 원격 서버 스크립트 다운로드
```bash
# Windows (PowerShell)
Invoke-WebRequest -Uri "https://raw.githubusercontent.com/jaehyokim-sketch/huanglongxiang-scholar/main/mcp_server/remote_server.py" -OutFile "remote_server.py"

# Mac / Linux
curl -O https://raw.githubusercontent.com/jaehyokim-sketch/huanglongxiang-scholar/main/mcp_server/remote_server.py
```

### 2단계: MCP 설정 등록
```json
{
  "mcpServers": {
    "huanglongxiang-scholar-remote": {
      "command": "python",
      "args": [
        "C:/경로/remote_server.py"
      ],
      "env": {
        "PYTHONIOENCODING": "utf-8"
      }
    }
  }
}
```
*(※ 기본적으로 `jaehyokim-sketch/huanglongxiang-scholar` 공개 저장소를 자동 타겟팅하므로 별도의 추가 인자 없이 바로 작동합니다.)*

---

## 🛠️ 제공 MCP 도구 (Tools) 목록

| 도구명 | 설명 | 매개변수 |
| :--- | :--- | :--- |
| `search_huanglongxiang_db` | 369만 자 전체 코퍼스 고속 키워드/한자/정규식 검색 | `query`, `book_filter`, `limit` |
| `get_acupoint_source` | 특정 혈위(예: 合谷, 足三里)의 문헌 층차, 고증 비판, 정위 원문 추출 | `acupoint_name` |
| `get_academic_paper` | 황룡상 교수 42편 전수 논문 중 특정 번호(01~42) 또는 제목 전문 조회 | `paper_id_or_title` |
| `get_scholar_framework` | 황룡상 5대 공리 및 3단계 분석-평가-기술 프로토콜 지침 반환 | - |

---

## 💡 참고 사항
- Python 3.8 이상 환경이면 별도의 라이브러리(`pip install`) 설치가 전혀 필요 없는 **Zero-Dependency** 서버입니다.
- Windows 환경에서는 한글/한자 정상 처리를 위해 환경 변수 `"PYTHONIOENCODING": "utf-8"` 설정을 권장합니다.
