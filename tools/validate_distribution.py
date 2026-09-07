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
    interview = texts[SKILL / "references" / "adaptive-interview.md"]
    knowledge = texts[SKILL / "references" / "feishu-knowledge.md"]

    if not skill_text.startswith("---\nname: xingzhou-ai-learning-diagnosis\n"):
        fail("invalid Skill frontmatter or name")
    if "绝不超过三个" not in skill_text:
        fail("question ceiling is not explicit")
    if "每轮只让用户完成一个回答动作" not in skill_text:
        fail("single-answer-action interview contract is missing")
    if "问题必须指向已经发生的事情或现存产物" not in skill_text:
        fail("actual-event interview contract is missing")
    if "回一个序号就行" not in skill_text or "只说事情名称就行" not in skill_text:
        fail("low-burden answer formats are missing")
    if "现有证据最高确认到多少分" not in skill_text or "没有 E3 时置信度最高为“中”" not in skill_text:
        fail("evidence confidence contract is missing")
    for score_node in (
        "| 0 分 |",
        "| 1 分 |",
        "| 3 分 |",
        "| 5 分 |",
        "| 7 分 |",
        "| 10 分 |",
        "| 15 分 |",
        "| 20 分 |",
        "| 30 分 |",
        "| 40 分 |",
        "| 50 分 |",
        "| 60 分 |",
        "| 75 分 |",
        "| 90 分 |",
        "| 100 分 |",
    ):
        if score_node not in scoring:
            fail(f"missing scoring node {score_node}")
    if "锚点" in corpus:
        fail("legacy anchor terminology remains in user-facing skill files")
    if "禁止让用户假设未来再次发生时会怎样" not in interview:
        fail("counterfactual-question ban is missing")
    if "P8C0fW8CYl7FPPdgvlUc2UDOnRg" not in knowledge:
        fail("canonical Feishu Drive folder is missing")
    if "不依赖编号" not in skill_text and "不解析文件名编号" not in knowledge:
        fail("dynamic discovery invariant is missing")
    if "显示标题不带 `.md`" not in knowledge:
        fail("Feishu document-title invariant is missing")

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

    print("OK: distribution structure, score nodes, low-burden interview, Feishu Drive root, dynamic discovery, and no legacy service dependency")
    return 0


if __name__ == "__main__":
    sys.exit(main())
