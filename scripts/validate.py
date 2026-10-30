#!/usr/bin/env python3
"""Offline repository checks. Does not evaluate model conversation behavior."""

import argparse
import json
from pathlib import Path
import re
import sys
import tempfile
from urllib.parse import unquote, urlsplit

import jsonschema
import yaml

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "skills" / "vibe-web-builder" / "scripts"))
from project import check_project, read_document  # noqa: E402

NAME = "vibe-web-builder"
EXCLUDED = {".git", ".venv", "__pycache__", ".pytest_cache", "node_modules", "dist"}
SECRET_PATTERNS = [
    re.compile(r"gh[pousr]_[A-Za-z0-9]{30,}"),
    re.compile(r"github_pat_[A-Za-z0-9_]{40,}"),
    re.compile(r"AKIA[A-Z0-9]{16}"),
    re.compile(r"sk-(?:proj-)?[A-Za-z0-9_-]{32,}"),
    re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----"),
]


def files(root):
    return sorted(p for p in root.rglob("*") if p.is_file()
                  and not any(part in EXCLUDED for part in p.relative_to(root).parts))


def validate(root=ROOT):
    root = Path(root).resolve()
    errors = []
    skill = root / "skills" / NAME
    required = ["README.md", "CONTRIBUTING.md", "CHANGELOG.md", "LICENSE",
                ".github/workflows/validate.yml", ".codex-plugin/plugin.json",
                "schemas/plugin.schema.json", "docs/behavior-scenarios.md",
                "docs/acceptance.md", "docs/releasing.md", "requirements-dev.txt"]
    required += [f"skills/{NAME}/{p}" for p in [
        "SKILL.md", "LICENSE.txt", "agents/openai.yaml", "scripts/project.py",
        "references/interview-workflow.md", "references/site-specification.md",
        "references/design-and-wireframes.md", "references/implementation-workflow.md",
        "references/testing-and-delivery.md", "references/project-resumption.md"]]
    for path in required:
        if not (root / path).is_file():
            errors.append(f"缺少文件: {path}")
    if (root / "LICENSE").is_file() and (skill / "LICENSE.txt").is_file():
        if (root / "LICENSE").read_bytes() != (skill / "LICENSE.txt").read_bytes():
            errors.append("独立安装的 Skill 许可证与仓库不一致")
    try:
        meta, body = read_document(skill / "SKILL.md")
        name, description = meta.get("name"), meta.get("description")
        if (not isinstance(name, str) or not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", name)
                or len(name) > 64 or name != skill.name):
            errors.append("Skill name 无效或与目录不符")
        if (not isinstance(description, str) or not 1 <= len(description.strip()) <= 1024
                or "<" in description or ">" in description):
            errors.append("Skill description 无效")
        if set(meta) != {"name", "description"}:
            errors.append("本项目 frontmatter 只允许 name/description")
        if not body.strip() or len(body.splitlines()) > 500:
            errors.append("Skill 正文为空或超过 500 行")
        ui = yaml.safe_load((skill / "agents/openai.yaml").read_text(encoding="utf-8"))["interface"]
        if not isinstance(ui.get("display_name"), str) or not ui["display_name"].strip():
            errors.append("缺少 UI display_name")
        short = ui.get("short_description")
        if not isinstance(short, str) or not 25 <= len(short) <= 64:
            errors.append("UI short_description 长度应为 25–64")
        if "$vibe-web-builder" not in ui.get("default_prompt", ""):
            errors.append("UI default_prompt 必须显式调用 Skill")
    except (OSError, ValueError, TypeError, KeyError, yaml.YAMLError) as exc:
        errors.append(f"Skill metadata: {exc}")
    try:
        manifest = json.loads((root / ".codex-plugin/plugin.json").read_text())
        schema = json.loads((root / "schemas/plugin.schema.json").read_text())
        jsonschema.Draft202012Validator.check_schema(schema)
        for error in jsonschema.Draft202012Validator(schema).iter_errors(manifest):
            errors.append(f"plugin manifest: {error.message}")
        if not (root / manifest["skills"] / NAME / "SKILL.md").is_file():
            errors.append("manifest skills 路径无法发现 Skill")
        if f'## [{manifest["version"]}]' not in (root / "CHANGELOG.md").read_text():
            errors.append("CHANGELOG 缺少 manifest 当前版本")
    except (OSError, ValueError, KeyError, TypeError, jsonschema.SchemaError) as exc:
        errors.append(f"plugin manifest: {exc}")
    for path in files(root):
        relative = path.relative_to(root)
        if not path.resolve().is_relative_to(root):
            errors.append(f"资源越出仓库: {relative}")
            continue
        if path.name.startswith(".env") and path.name != ".env.example":
            errors.append(f"不应分发环境私密配置: {relative}")
        try:
            content = path.read_text(encoding="utf-8")
        except (UnicodeError, OSError):
            continue
        for pattern in SECRET_PATTERNS:
            if pattern.search(content):
                errors.append(f"疑似敏感信息: {relative}（不输出匹配内容）")
        if path.suffix != ".md":
            continue
        if "assets/templates" in relative.as_posix() and re.search(r"\b(?:TODO|FIXME|TBD)\b|\{\{.+?\}\}", content):
            errors.append(f"未完成模板占位: {relative}")
        prose = re.sub(r"^```.*?^```\s*$", "", content, flags=re.S | re.M)
        for link in re.findall(r"\[[^\]\n]*\]\(([^)\s]+)\)", prose):
            target = urlsplit(link.strip("<>"))
            if target.scheme in {"https", "http", "mailto"} or not target.path:
                continue
            if target.scheme:
                errors.append(f"不支持的链接 scheme: {relative}")
                continue
            destination = (path.parent / unquote(target.path)).resolve()
            if not destination.is_relative_to(root) or not destination.exists():
                errors.append(f"资源路径无效: {relative} -> {target.path}")
    try:
        # Check the selected root's distributed templates, not a separate mock.
        with tempfile.TemporaryDirectory() as directory:
            import shutil
            target = Path(directory) / "docs" / "web-builder"
            target.parent.mkdir()
            shutil.copytree(skill / "assets" / "templates", target)
            errors.extend(f"模板: {error}" for error in check_project(directory))
    except (OSError, ValueError, yaml.YAMLError) as exc:
        errors.append(f"模板: {exc}")
    return errors


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=ROOT)
    args = parser.parse_args()
    errors = validate(args.root)
    if errors:
        print("\n".join(errors), file=sys.stderr)
        return 1
    print("PASS: Skill/UI metadata、manifest profile、模板状态、Markdown 本地资源与基础敏感信息检查")
    return 0


if __name__ == "__main__":
    sys.exit(main())
