#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Huang Longxiang Scholar (황룡상 침구학술·고증) MCP Server
Standard JSON-RPC 2.0 Stdio Model Context Protocol Server

Zero-dependency implementation: runs directly with standard Python 3.8+
"""

import sys
import os
import json
import re
import glob

# Ensure UTF-8 stdout/stdin on Windows
if sys.platform == "win32":
    sys.stdin.reconfigure(encoding="utf-8")
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")

# Base directory paths
SERVER_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(SERVER_DIR)

# Corpus paths (look in PROJECT_ROOT or subdirs)
CORPUS_PATHS = {
    "4대명저_통합": os.path.join(PROJECT_ROOT, "황룡상_4대명저_통합_마스터_parsed.md"),
    "논문집_전체": os.path.join(PROJECT_ROOT, "황룡상_교수_논문집_전체_parsed.md"),
    "중국침구학술사대강": os.path.join(PROJECT_ROOT, "中国针灸学术史大纲_parsed.md"),
    "경맥이론의_발견과_재해석": os.path.join(PROJECT_ROOT, "경맥이론의 발견과 재해석_parsed.md"),
    "신고전_침구학대강": os.path.join(PROJECT_ROOT, "신고전 침구학대강_parsed.md"),
    "중국고전_침구학대강": os.path.join(PROJECT_ROOT, "중국고전 침구학대강_parsed.md"),
}

PAPERS_DIR = os.path.join(PROJECT_ROOT, "논문_parsed")
CHUNKS_DIR = os.path.join(PROJECT_ROOT, "chunks_refined")
SKILL_FILE = os.path.join(PROJECT_ROOT, "skill", "SKILL.md")

# In-memory cache for fast search
_TEXT_CACHE = {}


def load_file(path):
    if path in _TEXT_CACHE:
        return _TEXT_CACHE[path]
    if os.path.exists(path):
        try:
            with open(path, "r", encoding="utf-8", errors="replace") as f:
                content = f.read()
                _TEXT_CACHE[path] = content
                return content
        except Exception as e:
            sys.stderr.write(f"Error loading {path}: {e}\n")
    return ""


def get_all_corpus_files():
    files = []
    for name, path in CORPUS_PATHS.items():
        if os.path.exists(path):
            files.append((name, path))

    # Also include individual paper files if available
    if os.path.exists(PAPERS_DIR):
        for p in sorted(glob.glob(os.path.join(PAPERS_DIR, "*.md"))):
            p_name = "논문_" + os.path.basename(p)
            files.append((p_name, p))

    return files


def search_corpus(query, book_filter="", limit=10):
    """Search for query across all Huang Longxiang texts."""
    results = []
    if not query:
        return results

    pattern = re.compile(re.escape(query), re.IGNORECASE)
    files = get_all_corpus_files()

    for book_name, file_path in files:
        if book_filter and book_filter.lower() not in book_name.lower():
            continue

        text = load_file(file_path)
        if not text:
            continue

        for match in pattern.finditer(text):
            start = max(0, match.start() - 250)
            end = min(len(text), match.end() + 250)
            snippet = text[start:end].replace("\n", " ").strip()

            results.append({
                "source": book_name,
                "file": os.path.basename(file_path),
                "position": match.start(),
                "snippet": snippet
            })

            if len(results) >= limit:
                break
        if len(results) >= limit:
            break

    return results


def get_acupoint_source(acupoint_name):
    """Retrieve textual criticism and location rationale for a specific acupoint."""
    if not acupoint_name:
        return "혈위명을 입력해 주세요 (예: 合谷, 足三里, 内关)."

    results = search_corpus(acupoint_name, limit=15)
    if not results:
        return f"'{acupoint_name}'에 대한 황룡상 마스터 DB 검색 결과가 없습니다."

    output = [f"# 《황룡상 교수 저작 DB》 '{acupoint_name}' 고증 및 학술 자료 (총 {len(results)}건 발췌)\n"]
    for i, res in enumerate(results, 1):
        output.append(f"### [{i}] 출전: {res['source']} (위치: {res['position']})")
        output.append(f"> ... {res['snippet']} ...\n")

    return "\n".join(output)


def get_academic_paper(paper_id_or_title):
    """Retrieve full text or matched paper from the 42 research papers."""
    if not os.path.exists(PAPERS_DIR):
        return "논문_parsed 디렉토리를 찾을 수 없습니다."

    matched_file = None
    all_papers = sorted(os.listdir(PAPERS_DIR))

    # Match by index prefix (e.g. '01', '13', '42') or title
    for f in all_papers:
        if f.endswith(".md"):
            if str(paper_id_or_title).strip() in f:
                matched_file = os.path.join(PAPERS_DIR, f)
                break

    if not matched_file and str(paper_id_or_title).isdigit():
        idx_str = f"{int(paper_id_or_title):02d}_"
        for f in all_papers:
            if f.startswith(idx_str):
                matched_file = os.path.join(PAPERS_DIR, f)
                break

    if matched_file and os.path.exists(matched_file):
        content = load_file(matched_file)
        return f"# [황룡상 학술논문] {os.path.basename(matched_file)}\n\n{content}"

    # Return list of all available papers if not found
    paper_list = "\n".join([f"- {p}" for p in all_papers if p.endswith(".md")])
    return f"해당 논문을 찾을 수 없습니다. (입력: {paper_id_or_title})\n\n### 보유 논문 42편 목록:\n{paper_list}"


def get_scholar_framework():
    """Return the Huang Longxiang scholarly framework and prompt guide."""
    if os.path.exists(SKILL_FILE):
        return load_file(SKILL_FILE)
    return "황룡상 학술 프레임워크(SKILL.md)를 로드할 수 없습니다."


# --- MCP Tool Definitions ---
MCP_TOOLS = [
    {
        "name": "search_huanglongxiang_db",
        "description": "황룡상(黄龙祥) 교수의 4대 명저 및 42편 학술논문 전수 DB(총 369만 자)에서 키워드/한자/학술 개념을 고속 검색하여 문맥 발췌문을 반환합니다.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "검색할 용어 (예: 合谷, 11경맥, 手厥阴, 标本根结, 经脉病候, 压痛点)"
                },
                "book_filter": {
                    "type": "string",
                    "description": "특정 저작 필터링 (예: 중국침구학술사대강, 경맥이론, 신고전, 중국고전, 논문집)"
                },
                "limit": {
                    "type": "integer",
                    "description": "반환할 최대 결과 수 (기본값: 10)"
                }
            },
            "required": ["query"]
        }
    },
    {
        "name": "get_acupoint_source",
        "description": "특정 혈위(穴位)에 대한 황룡상 교수의 원전 고증, 문헌 층차(선진~명청), 정위 왜곡 비판, 올바른 표준 정위 및 배오 원리를 일괄 추출합니다.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "acupoint_name": {
                    "type": "string",
                    "description": "고증할 혈위명 (한자 또는 한글, 예: 合谷, 足三里, 内关, 委中, 百会)"
                }
            },
            "required": ["acupoint_name"]
        }
    },
    {
        "name": "get_academic_paper",
        "description": "황룡상 교수의 42편 전수 학술논문 중 지정된 번호(01~42) 또는 제목에 해당하는 논문 전문을 조회합니다.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "paper_id_or_title": {
                    "type": "string",
                    "description": "논문 번호(예: '13', '42') 또는 논문 제목 키워드(예: '경락학설의 유래', '五关')"
                }
            },
            "required": ["paper_id_or_title"]
        }
    },
    {
        "name": "get_scholar_framework",
        "description": "황룡상 침구학술사의 5대 핵심 공리 및 3단계 분석-평가-기술(Analysis-Evaluation-Description) 프로토콜 지침을 반환합니다.",
        "inputSchema": {
            "type": "object",
            "properties": {}
        }
    }
]


def handle_tool_call(tool_name, arguments):
    if tool_name == "search_huanglongxiang_db":
        query = arguments.get("query", "")
        book_filter = arguments.get("book_filter", "")
        limit = arguments.get("limit", 10)
        results = search_corpus(query, book_filter, limit)
        if not results:
            return f"'{query}'에 대한 검색 결과가 없습니다."
        out = [f"### 황룡상 마스터 DB 검색 결과: '{query}' (총 {len(results)}건)"]
        for r in results:
            out.append(f"- **[{r['source']}]** ... {r['snippet']} ...")
        return "\n\n".join(out)

    elif tool_name == "get_acupoint_source":
        acupoint_name = arguments.get("acupoint_name", "")
        return get_acupoint_source(acupoint_name)

    elif tool_name == "get_academic_paper":
        paper_id_or_title = arguments.get("paper_id_or_title", "")
        return get_academic_paper(paper_id_or_title)

    elif tool_name == "get_scholar_framework":
        return get_scholar_framework()

    else:
        raise ValueError(f"Unknown tool: {tool_name}")


def main():
    """Main JSON-RPC stdio loop."""
    while True:
        try:
            line = sys.stdin.readline()
            if not line:
                break
            line = line.strip()
            if not line:
                continue

            request = json.loads(line)
            req_id = request.get("id")
            method = request.get("method")
            params = request.get("params", {})

            if method == "initialize":
                response = {
                    "jsonrpc": "2.0",
                    "id": req_id,
                    "result": {
                        "protocolVersion": "2024-11-05",
                        "capabilities": {
                            "tools": {}
                        },
                        "serverInfo": {
                            "name": "huanglongxiang-scholar-mcp",
                            "version": "1.0.0"
                        }
                    }
                }
                sys.stdout.write(json.dumps(response, ensure_ascii=False) + "\n")
                sys.stdout.flush()

            elif method == "notifications/initialized":
                # Client notification after init, no response needed
                pass

            elif method == "tools/list":
                response = {
                    "jsonrpc": "2.0",
                    "id": req_id,
                    "result": {
                        "tools": MCP_TOOLS
                    }
                }
                sys.stdout.write(json.dumps(response, ensure_ascii=False) + "\n")
                sys.stdout.flush()

            elif method == "tools/call":
                tool_name = params.get("name")
                arguments = params.get("arguments", {})
                try:
                    result_text = handle_tool_call(tool_name, arguments)
                    response = {
                        "jsonrpc": "2.0",
                        "id": req_id,
                        "result": {
                            "content": [
                                {
                                    "type": "text",
                                    "text": str(result_text)
                                }
                            ]
                        }
                    }
                except Exception as e:
                    response = {
                        "jsonrpc": "2.0",
                        "id": req_id,
                        "error": {
                            "code": -32000,
                            "message": str(e)
                        }
                    }
                sys.stdout.write(json.dumps(response, ensure_ascii=False) + "\n")
                sys.stdout.flush()

            elif method == "ping":
                response = {"jsonrpc": "2.0", "id": req_id, "result": {}}
                sys.stdout.write(json.dumps(response, ensure_ascii=False) + "\n")
                sys.stdout.flush()

            else:
                if req_id is not None:
                    response = {
                        "jsonrpc": "2.0",
                        "id": req_id,
                        "error": {
                            "code": -32601,
                            "message": f"Method not found: {method}"
                        }
                    }
                    sys.stdout.write(json.dumps(response, ensure_ascii=False) + "\n")
                    sys.stdout.flush()

        except Exception as e:
            sys.stderr.write(f"MCP Server error: {e}\n")


if __name__ == "__main__":
    main()
