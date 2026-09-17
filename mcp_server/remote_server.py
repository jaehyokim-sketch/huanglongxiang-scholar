#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Huang Longxiang Scholar - Remote GitHub Streaming MCP Server
Connects to Huang Longxiang's DB hosted on GitHub without requiring local clones.

Usage:
  python remote_server.py --repo <owner>/<repo> [--branch main] [--token <github_pat>]
"""

import sys
import os
import json
import re
import urllib.request
import argparse

# Ensure UTF-8 stdout/stdin
if sys.platform == "win32":
    sys.stdin.reconfigure(encoding="utf-8")
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")

# Parse command line arguments
parser = argparse.ArgumentParser(description="Remote Huang Longxiang MCP Server via GitHub")
parser.add_argument("--repo", type=str, default=os.getenv("GITHUB_REPO", ""), help="GitHub Repository (e.g. owner/huanglongxiang-scholar)")
parser.add_argument("--branch", type=str, default=os.getenv("GITHUB_BRANCH", "main"), help="Git Branch (default: main)")
parser.add_argument("--token", type=str, default=os.getenv("GITHUB_TOKEN", ""), help="GitHub Personal Access Token (for private repos)")

args, unknown = parser.parse_known_args()

GITHUB_REPO = args.repo
GITHUB_BRANCH = args.branch
GITHUB_TOKEN = args.token

# In-memory document cache
_REMOTE_CACHE = {}

CORPUS_FILES = {
    "4대명저_통합": "황룡상_4대명저_통합_마스터_parsed.md",
    "논문집_전체": "황룡상_교수_논문집_전체_parsed.md",
    "중국침구학술사대강": "中国针灸学术史大纲_parsed.md",
    "경맥이론의_발견과_재해석": "경맥이론의 발견과 재해석_parsed.md",
    "신고전_침구학대강": "신고전 침구학대강_parsed.md",
    "중국고전_침구학대강": "중국고전 침구학대강_parsed.md",
    "스킬정의": "skill/SKILL.md",
}


def fetch_github_file(file_path):
    """Fetch raw file content from GitHub repository with caching."""
    if file_path in _REMOTE_CACHE:
        return _REMOTE_CACHE[file_path]

    if not GITHUB_REPO:
        return ""

    # Quote URL for Korean / Chinese path names
    from urllib.parse import quote
    encoded_path = quote(file_path)
    url = f"https://raw.githubusercontent.com/{GITHUB_REPO}/{GITHUB_BRANCH}/{encoded_path}"

    try:
        headers = {"User-Agent": "HuangLongxiang-Remote-MCP/1.0"}
        if GITHUB_TOKEN:
            headers["Authorization"] = f"token {GITHUB_TOKEN}"

        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=15) as resp:
            content = resp.read().decode("utf-8", errors="replace")
            _REMOTE_CACHE[file_path] = content
            return content
    except Exception as e:
        sys.stderr.write(f"Failed to fetch {url}: {e}\n")
        return ""


def search_remote_corpus(query, book_filter="", limit=10):
    results = []
    if not query:
        return results

    pattern = re.compile(re.escape(query), re.IGNORECASE)

    # Search in main books
    for book_name, rel_path in CORPUS_FILES.items():
        if book_filter and book_filter.lower() not in book_name.lower():
            continue

        text = fetch_github_file(rel_path)
        if not text:
            continue

        for match in pattern.finditer(text):
            start = max(0, match.start() - 250)
            end = min(len(text), match.end() + 250)
            snippet = text[start:end].replace("\n", " ").strip()

            results.append({
                "source": book_name,
                "file": rel_path,
                "position": match.start(),
                "snippet": snippet
            })

            if len(results) >= limit:
                break
        if len(results) >= limit:
            break

    return results


# --- MCP Tool Definitions ---
MCP_TOOLS = [
    {
        "name": "search_huanglongxiang_db",
        "description": "황룡상(黄龙祥) 교수의 4대 명저 및 42편 학술논문 전수 DB(총 369만 자)에서 키워드/한자/학술 개념을 원격 검색하여 문맥 발췌문을 반환합니다.",
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
        results = search_remote_corpus(query, book_filter, limit)
        if not results:
            return f"'{query}'에 대한 원격 GitHub DB 검색 결과가 없습니다."
        out = [f"### [원격 GitHub DB] 황룡상 마스터 검색 결과: '{query}' (총 {len(results)}건)"]
        for r in results:
            out.append(f"- **[{r['source']}]** ... {r['snippet']} ...")
        return "\n\n".join(out)

    elif tool_name == "get_acupoint_source":
        acupoint_name = arguments.get("acupoint_name", "")
        results = search_remote_corpus(acupoint_name, limit=15)
        if not results:
            return f"'{acupoint_name}'에 대한 원격 DB 검색 결과가 없습니다."
        out = [f"# 《원격 황룡상 저작 DB》 '{acupoint_name}' 고증 및 학술 자료 (총 {len(results)}건 발췌)\n"]
        for i, res in enumerate(results, 1):
            out.append(f"### [{i}] 출전: {res['source']} (위치: {res['position']})")
            out.append(f"> ... {res['snippet']} ...\n")
        return "\n".join(out)

    elif tool_name == "get_scholar_framework":
        content = fetch_github_file("skill/SKILL.md")
        return content if content else "황룡상 학술 프레임워크(SKILL.md)를 원격에서 로드할 수 없습니다."

    else:
        raise ValueError(f"Unknown tool: {tool_name}")


def main():
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
                        "capabilities": {"tools": {}},
                        "serverInfo": {
                            "name": "huanglongxiang-remote-mcp",
                            "version": "1.0.0"
                        }
                    }
                }
                sys.stdout.write(json.dumps(response, ensure_ascii=False) + "\n")
                sys.stdout.flush()

            elif method == "notifications/initialized":
                pass

            elif method == "tools/list":
                response = {
                    "jsonrpc": "2.0",
                    "id": req_id,
                    "result": {"tools": MCP_TOOLS}
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
                            "content": [{"type": "text", "text": str(result_text)}]
                        }
                    }
                except Exception as e:
                    response = {
                        "jsonrpc": "2.0",
                        "id": req_id,
                        "error": {"code": -32000, "message": str(e)}
                    }
                sys.stdout.write(json.dumps(response, ensure_ascii=False) + "\n")
                sys.stdout.flush()

            elif method == "ping":
                response = {"jsonrpc": "2.0", "id": req_id, "result": {}}
                sys.stdout.write(json.dumps(response, ensure_ascii=False) + "\n")
                sys.stdout.flush()

        except Exception as e:
            sys.stderr.write(f"Remote MCP Server error: {e}\n")


if __name__ == "__main__":
    main()
