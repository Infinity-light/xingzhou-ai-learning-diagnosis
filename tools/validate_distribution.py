#!/usr/bin/env python3
from __future__ import annotations

import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "skills" / "xingzhou-ai-learning-diagnosis"


def fail(message: str) -> None:
    print(f"ERROR: {message}")
    raise SystemExit(1)


def main() -> int:
    required = [
        SKILL / "SKILL.md",
        SKILL / "agents" / "openai.yaml",
        SKILL / "references" / "scoring.md",
        SKILL / "references" / "adaptive-interview.md",
        SKILL / "references" / "feishu-knowledge.md",
        SKILL / "references" / "benchmark.md",
        SKILL / "assets" / "report-template.html",
    ]
    missing = [str(path.relative_to(ROOT)) for path in required if not path.is_file()]
    if missing:
        fail("missing files: " + ", ".join(missing))

    texts = {path: path.read_text(encoding="utf-8") for path in required}
    corpus = "\n".join(texts.values())
    skill_text = texts[SKILL / "SKILL.md"]
    scoring = texts[SKILL / "references" / "scoring.md"]
    knowledge = texts[SKILL / "references" / "feishu-knowledge.md"]

    if not skill_text.startswith("---\nname: xingzhou-ai-learning-diagnosis\n"):
        fail("invalid Skill frontmatter or name")
    if "绝不超过三个" not in skill_text:
        fail("question ceiling is not explicit")
    for anchor in ("| 0 |", "| 1 |", "| 10 |", "| 30 |", "| 60 |", "| 100 |"):
        if anchor not in scoring:
            fail(f"missing scoring anchor {anchor}")
    if "U20FwdgVdiU0kFkdiV3crTL8n7f" not in knowledge:
        fail("canonical Feishu Wiki root is missing")
    if "不依赖编号" not in skill_text and "不解析文件名编号" not in knowledge:
        fail("dynamic discovery invariant is missing")

    forbidden_dependencies = [
        r"dependencies:\s*\n(?:.|\n)*mcp",
        r"https://ecnjgebfaiuk\.feishuapp\.com/app/",
        r"begin_diagnosis",
        r"render_html_report",
    ]
    for pattern in forbidden_dependencies:
        if re.search(pattern, corpus, re.IGNORECASE):
            fail(f"forbidden legacy dependency matched: {pattern}")

    secret_pattern = re.compile(r"(?i)(?:password|secret|token)\s*[:=]\s*[\"']?[A-Za-z0-9_-]{16,}")
    if secret_pattern.search(corpus):
        fail("possible embedded credential")

    print("OK: distribution structure, anchors, Feishu root, dynamic discovery, and no legacy service dependency")
    return 0


if __name__ == "__main__":
    sys.exit(main())

