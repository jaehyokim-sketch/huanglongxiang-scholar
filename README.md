# 황룡상(黄龙祥) 침구학술·고증 마스터 DB & MCP 서버

중국 침구학술사 및 문헌고증학의 최고 권위자인 **황룡상(黄龙祥) 교수**의 전수 학술 저작과 42편 논문(총 369만 자)을 집대성한 정밀 코퍼스 DB 및 어디서나 연결 가능한 **MCP(Model Context Protocol) 서버** 저장소입니다.

---

## 📚 수록 마스터 데이터베이스 (총 3,694,000자)

1. **4대 명저 통합 마스터 DB (`황룡상_4대명저_통합_마스터_parsed.md`)**
   - 《中国针灸学术史大纲》(중국침구학술사대강)
   - 《경맥이론의 발견과 재해석》
   - 《신고전 침구학대강》
   - 《중국고전 침구학대강》
2. **42편 전수 학술논문 DB (`황룡상_교수_논문집_전체_parsed.md` 및 `논문_parsed/`)**
   - 1993년 《경락학설의 유래》부터 2005년 《고대 경락학설의 현대 실험실 진입 5대 관문》, 《경락연구의 반성》까지 42편 완역/전수 수록
3. **정제 챕터 분할본 (`chunks_refined/`)**
   - 4대 명저의 총 28개 세부 챕터별 정제 마크다운
4. **황룡상 학술 분석 프레임워크 (`skill/SKILL.md` 및 `skill/references/`)**
   - 5대 핵심 공리(문헌 층차주의, 경맥-수혈 발생학, 해부학적 실증 정혈, 침구 처방학 원형 복원, 현대 경락연구 반성론)
   - 3단계 학술 프로토콜: **[1단계: 분석 ➔ 2단계: 평가 ➔ 3단계: 기술]**

---

## 📂 저장소 구조

```
huanglongxiang-scholar/
├── README.md                      # 저장소 종합 안내서 및 연동 가이드
├── .gitignore                     # 대용량 원본 PDF 제외 규칙
│
├── skill/                         # [황룡상] AI 스킬 정의
│   ├── SKILL.md                   # 황룡상 학술 프레임워크 스킬 본문
│   └── references/                # 경맥 진화 및 고증 가이드
│
├── mcp_server/                    # MCP (Model Context Protocol) 서버
│   ├── server.py                  # 표준 Stdio 로컬 고속 검색 서버 (Zero-Dependency)
│   └── remote_server.py           # GitHub Raw API 기반 원격 스트리밍 서버
│
├── deploy/                        # 타 PC / AI IDE 연동 템플릿
│   ├── mcp_config_local.json      # 로컬 클론 시 MCP 설정
│   ├── mcp_config_remote.json     # 원격 GitHub 스트리밍 MCP 설정
│   ├── setup_skill.ps1            # Windows 스킬 원클릭 설치 스크립트
│   └── setup_skill.sh             # Mac/Linux 스킬 원클릭 설치 스크립트
│
├── chunks_refined/                # 28개 챕터 분할 마크다운 DB
└── 논문_parsed/                   # 42편 전수 논문 마크다운 DB
```

---

## 🚀 다른 PC(원격 환경)에서 사용하는 방법

### 방법 1: 저장소 Clone 후 로컬 MCP 연동 (가장 빠르고 권장됨)

인터넷 연결 여부와 상관없이 100% 로컬 초고속 검색 및 인용이 가능합니다.

1. **저장소 복제**:
   ```bash
   git clone https://github.com/<사용자ID>/huanglongxiang-scholar.git
   cd huanglongxiang-scholar
   ```

2. **스킬 글로벌 등록 (선택)**:
   - **Windows**: `powershell -ExecutionPolicy Bypass -File deploy\setup_skill.ps1`
   - **Mac/Linux**: `bash deploy/setup_skill.sh`

3. **AI IDE / Claude Desktop에 MCP 서버 등록**:
   - `claude_desktop_config.json` 또는 Antigravity/Cursor `mcp_config.json`의 `mcpServers`에 아래 설정 추가:
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

---

### 방법 2: Remote GitHub Streaming MCP (DB 다운로드 없이 온라인 사용)

다른 PC에 수십 MB 용량의 DB를 clone하지 않고, GitHub 원격 저장소에서 실시간으로 스트리밍 조회합니다.

1. `mcp_server/remote_server.py` 단일 파일만 복사하여 실행하거나 아래와 같이 MCP에 등록:
   ```json
   {
     "mcpServers": {
       "huanglongxiang-scholar-remote": {
         "command": "python",
         "args": [
           "remote_server.py",
           "--repo", "사용자ID/huanglongxiang-scholar",
           "--branch", "main",
           "--token", "<비공개 저장소인 경우 GitHub PAT 토큰>"
         ],
         "env": {
           "PYTHONIOENCODING": "utf-8"
         }
       }
     }
   }
   ```

---

## 🛠️ 제공 MCP 도구 (Tools)

| 도구명 | 설명 | 주요 매개변수 |
| :--- | :--- | :--- |
| `search_huanglongxiang_db` | 369만 자 전체 코퍼스 고속 키워드/정규식 검색 및 출전 반환 | `query`, `book_filter`, `limit` |
| `get_acupoint_source` | 특정 혈위(예: 合谷, 足三里)의 문헌 층차, 고증 비판, 정위 원문 추출 | `acupoint_name` |
| `get_academic_paper` | 42편 전수 논문 중 특정 번호(01~42) 또는 제목 전문 조회 | `paper_id_or_title` |
| `get_scholar_framework` | 황룡상 5대 공리 및 3단계 학술 프로토콜 시스템 프롬프트 반환 | - |

---

## 📖 라이선스 및 학술 인용

본 저장소의 데이터베이스 및 스킬 프레임워크는 황룡상 교수의 침구학술사 연구 성과에 기반하며, 비영리 학술 연구 및 임상 진료 참조 목적으로 구축되었습니다.
