#!/usr/bin/env python3
"""Initialize six project documents; check metadata without granting consent."""

import argparse
from datetime import datetime, timezone
from pathlib import Path
import re
import shutil
import sys
import tempfile

try:
    import yaml
except ImportError:
    raise SystemExit("缺少 PyYAML；请安装 PyYAML>=6,<7，或按 Skill 模板手动维护文档。")

FILES = ("requirements.md", "sitemap.md", "interactions.md", "design.md",
         "implementation-plan.md", "progress.md")
PHASES = {"interview", "requirements-review", "design", "design-review",
          "planning-delivered", "implementation", "validation", "delivered"}
DEV_PHASES = {"implementation", "validation", "delivered"}


class UniqueLoader(yaml.SafeLoader):
    """Reject duplicate metadata keys rather than silently taking the last."""


def unique_mapping(loader, node):
    result = {}
    for key_node, value_node in node.value:
        key = loader.construct_object(key_node)
        if not isinstance(key, str) or key in result:
            raise ValueError("YAML key 非字符串或重复")
        result[key] = loader.construct_object(value_node)
    return result


UniqueLoader.add_constructor(yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG, unique_mapping)


def read_document(path):
    text = path.read_text(encoding="utf-8")
    match = re.match(r"\A---\r?\n(.*?)\r?\n---(?:\r?\n|$)", text, re.S)
    if not match:
        raise ValueError(f"{path.name}: 缺少有效 YAML frontmatter")
    data = yaml.load(match[1], Loader=UniqueLoader)
    if not isinstance(data, dict):
        raise ValueError(f"{path.name}: frontmatter 必须是 mapping")
    return data, text[match.end():]


def document_directory(project):
    root = Path(project).resolve(strict=True)
    if not root.is_dir():
        raise ValueError("project 必须是现有目录")
    docs = root / "docs"
    target = docs / "web-builder"
    if docs.is_symlink() or target.is_symlink():
        raise ValueError("拒绝经 docs 或 web-builder 符号链接写入/读取")
    return target


def initialize(project, mode="planning"):
    if mode not in {"planning", "development"}:
        raise ValueError("无效 mode")
    target = document_directory(project)
    if target.exists():
        raise ValueError(f"已存在 {target}；请先读取状态，不覆盖或合并")
    target.parent.mkdir(exist_ok=True)
    templates = Path(__file__).resolve().parents[1] / "assets" / "templates"
    staging = Path(tempfile.mkdtemp(prefix=".web-builder-", dir=target.parent))
    try:
        for name in FILES:
            source = templates / name
            data, body = read_document(source)
            if name == "progress.md":
                data["mode"] = mode
                data["initialized_at"] = datetime.now(timezone.utc).isoformat()
            output = "---\n" + yaml.safe_dump(data, allow_unicode=True, sort_keys=False) + "---\n" + body
            (staging / name).write_text(output, encoding="utf-8")
        if target.exists() or target.is_symlink():
            raise ValueError("初始化期间目标已出现，拒绝覆盖")
        staging.rename(target)
    finally:
        if staging.exists():
            shutil.rmtree(staging)
    return target


def positive(value):
    return type(value) is int and value > 0


def confirmed(data):
    return (data.get("confirmation") == "confirmed"
            and positive(data.get("revision"))
            and type(data.get("confirmed_revision")) is int
            and data["confirmed_revision"] == data["revision"]
            and isinstance(data.get("confirmation_evidence"), str)
            and bool(data["confirmation_evidence"].strip())
            and data.get("blocking_issues") == [])


def check_project(project):
    target = document_directory(project)
    records, errors = {}, []
    for name in FILES:
        try:
            path = target / name
            if path.is_symlink():
                raise ValueError(f"{name}: 不允许符号链接")
            data, body = read_document(path)
            if type(data.get("schema_version")) is not int or data["schema_version"] != 1:
                errors.append(f"{name}: 不支持的 schema_version")
            if not body.strip():
                errors.append(f"{name}: 正文为空")
            records[name] = data
        except (OSError, ValueError, yaml.YAMLError) as exc:
            errors.append(f"{name}: {exc}")
    if len(records) != len(FILES):
        return errors
    req, design, progress = (records[name] for name in ("requirements.md", "design.md", "progress.md"))
    for name, data in (("requirements", req), ("design", design)):
        if not positive(data.get("revision")):
            errors.append(f"{name}: revision 必须为正整数")
        if not isinstance(data.get("confirmation"), str) or data["confirmation"] not in {"pending", "confirmed"}:
            errors.append(f"{name}: 无效 confirmation")
        if not isinstance(data.get("blocking_issues"), list) or not all(
                isinstance(item, str) and item.strip() for item in data.get("blocking_issues", [])):
            errors.append(f"{name}: blocking_issues 必须为字符串列表")
        if data.get("confirmation") == "confirmed" and not confirmed(data):
            errors.append(f"{name}: 确认版本、依据缺失或仍有阻塞")
        if data.get("confirmation") == "pending" and (
                data.get("confirmed_revision") is not None or data.get("confirmation_evidence") is not None):
            errors.append(f"{name}: pending 不得保留过期确认")
    for owner, key, revision in ((design, "requirements_revision", req.get("revision")),
                                 (progress, "requirements_revision", req.get("revision")),
                                 (progress, "design_revision", design.get("revision"))):
        if not positive(owner.get(key)) or owner[key] != revision:
            errors.append(f"{key}: 文档版本不一致")
    phase = progress.get("phase") if isinstance(progress.get("phase"), str) else None
    if phase not in PHASES:
        errors.append("progress: 无效 phase")
    if not isinstance(progress.get("mode"), str) or progress["mode"] not in {"planning", "development"}:
        errors.append("progress: 无效 mode")
    if not isinstance(progress.get("status"), str) or progress["status"] not in {"active", "paused", "blocked"}:
        errors.append("progress: 无效 status")
    if not isinstance(progress.get("next_action"), str) or not progress["next_action"].strip():
        errors.append("progress: next_action 不能为空")
    after_req = {"design", "design-review", "planning-delivered"} | DEV_PHASES
    if (phase in after_req or design.get("confirmation") == "confirmed") and not confirmed(req):
        errors.append("需求门槛未通过")
    if phase in {"planning-delivered"} | DEV_PHASES and not confirmed(design):
        errors.append("草图门槛未通过")
    if phase in DEV_PHASES and progress.get("mode") != "development":
        errors.append("规划模式不得进入正式开发")
    if phase == "planning-delivered" and progress.get("mode") != "planning":
        errors.append("planning-delivered 仅适用于规划模式")
    return errors


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)
    init = sub.add_parser("init", help="安全初始化六份文档，不创建网站应用")
    init.add_argument("--project", required=True)
    init.add_argument("--mode", choices=("planning", "development"), default="planning")
    check = sub.add_parser("check", help="检查状态一致性，不代替真实确认与行为验收")
    check.add_argument("--project", required=True)
    args = parser.parse_args(argv)
    try:
        if args.command == "init":
            print(f"已初始化：{initialize(args.project, args.mode)}")
        else:
            errors = check_project(args.project)
            if errors:
                print("\n".join(errors), file=sys.stderr)
                return 1
            print("文档状态一致；不代表语义完整、用户已授权或应用测试通过。")
    except (OSError, ValueError, yaml.YAMLError) as exc:
        print(f"错误：{exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
