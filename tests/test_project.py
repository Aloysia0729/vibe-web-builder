import contextlib
import io
from pathlib import Path
import shutil
import sys
import tempfile
import unittest

import yaml

ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "skills" / "vibe-web-builder"
sys.path.insert(0, str(SKILL / "scripts"))
import project


class ProjectTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        self.docs = project.initialize(self.root)

    def update(self, name, **changes):
        path = self.docs / name
        meta, body = project.read_document(path)
        meta.update(changes)
        path.write_text("---\n" + yaml.safe_dump(meta, allow_unicode=True, sort_keys=False)
                        + "---\n" + body, encoding="utf-8")

    def confirm(self, name):
        self.update(name, confirmation="confirmed", confirmed_revision=1,
                    confirmation_evidence="模拟测试用户在本轮确认 v1；非真实产品授权。")

    def both(self, mode="development", phase="implementation"):
        self.confirm("requirements.md")
        self.confirm("design.md")
        self.update("progress.md", mode=mode, phase=phase)

    def errors(self):
        return project.check_project(self.root)

    def test_initialization_writes_only_six_pending_documents(self):
        self.assertEqual(set(p.name for p in self.docs.iterdir()), set(project.FILES))
        self.assertEqual(self.errors(), [])
        self.assertFalse((self.root / "package.json").exists())
        for name in ("requirements.md", "design.md"):
            self.assertEqual(project.read_document(self.docs / name)[0]["confirmation"], "pending")

    def test_existing_documents_never_overwritten(self):
        before = (self.docs / "requirements.md").read_bytes()
        with self.assertRaisesRegex(ValueError, "已存在"):
            project.initialize(self.root)
        self.assertEqual((self.docs / "requirements.md").read_bytes(), before)

    def test_existing_empty_target_refused(self):
        shutil.rmtree(self.docs)
        self.docs.mkdir()
        with self.assertRaises(ValueError):
            project.initialize(self.root)

    def test_docs_symlink_refused(self):
        shutil.rmtree(self.root / "docs")
        outside = self.root / "outside"
        outside.mkdir()
        (self.root / "docs").symlink_to(outside, target_is_directory=True)
        with self.assertRaisesRegex(ValueError, "符号链接"):
            project.initialize(self.root)
        self.assertEqual(list(outside.iterdir()), [])

    def test_document_symlink_refused(self):
        path = self.docs / "requirements.md"
        path.rename(self.root / "original.md")
        path.symlink_to(self.root / "original.md")
        self.assertTrue(any("符号链接" in e for e in self.errors()))

    def test_missing_document_reported(self):
        (self.docs / "design.md").unlink()
        self.assertTrue(any("design.md" in e for e in self.errors()))

    def test_malformed_yaml_reported(self):
        (self.docs / "design.md").write_text("---\nrevision: [\n---\n# test\n")
        self.assertTrue(self.errors())

    def test_duplicate_yaml_keys_rejected(self):
        (self.docs / "design.md").write_text("---\nrevision: 1\nrevision: 2\n---\n# test\n")
        self.assertTrue(any("重复" in e for e in self.errors()))

    def test_non_mapping_yaml_rejected(self):
        (self.docs / "design.md").write_text("---\n- value\n---\n# test\n")
        self.assertTrue(self.errors())

    def test_unsupported_schema_rejected(self):
        self.update("design.md", schema_version=2)
        self.assertTrue(any("schema_version" in e for e in self.errors()))

    def test_boolean_revision_not_integer(self):
        self.update("requirements.md", revision=True)
        self.assertTrue(any("revision" in e for e in self.errors()))

    def test_confirmed_requires_evidence(self):
        self.update("requirements.md", confirmation="confirmed", confirmed_revision=1)
        self.assertTrue(any("确认" in e for e in self.errors()))

    def test_pending_cannot_keep_old_evidence(self):
        self.update("requirements.md", confirmed_revision=1, confirmation_evidence="old")
        self.assertTrue(any("过期" in e for e in self.errors()))

    def test_design_requires_requirements_confirmation(self):
        self.update("progress.md", phase="design")
        self.assertIn("需求门槛未通过", self.errors())

    def test_design_cannot_be_confirmed_before_requirements(self):
        self.confirm("design.md")
        self.assertIn("需求门槛未通过", self.errors())

    def test_requirements_alone_does_not_allow_development(self):
        self.confirm("requirements.md")
        self.update("progress.md", mode="development", phase="implementation")
        self.assertIn("草图门槛未通过", self.errors())

    def test_planning_cannot_implement_even_after_two_confirmations(self):
        self.both(mode="planning")
        self.assertIn("规划模式不得进入正式开发", self.errors())

    def test_development_requires_two_current_confirmations(self):
        self.both()
        self.assertEqual(self.errors(), [])

    def test_planning_delivery_valid_after_both_confirmations(self):
        self.both(mode="planning", phase="planning-delivered")
        self.assertEqual(self.errors(), [])

    def test_business_change_invalidates_old_confirmations(self):
        self.both()
        self.update("requirements.md", revision=2)
        self.assertTrue(any("版本" in e or "门槛" in e for e in self.errors()))

    def test_visual_change_invalidates_old_design_confirmation(self):
        self.both()
        self.update("design.md", revision=2)
        self.update("progress.md", design_revision=2)
        self.assertIn("草图门槛未通过", self.errors())

    def test_blocking_issues_prevent_confirmation(self):
        self.both()
        self.update("requirements.md", blocking_issues=["数据归属待决定"])
        self.assertIn("需求门槛未通过", self.errors())

    def test_invalid_metadata_types_are_errors_not_crashes(self):
        self.update("requirements.md", confirmation=["confirmed"], blocking_issues=3)
        self.update("progress.md", mode=[], phase={}, status=[], next_action=0)
        self.assertGreaterEqual(len(self.errors()), 5)

    def test_blank_body_rejected(self):
        path = self.docs / "sitemap.md"
        path.write_text("---\nschema_version: 1\n---\n")
        self.assertTrue(any("正文为空" in e for e in self.errors()))

    def test_missing_project_cli_nonzero(self):
        with contextlib.redirect_stderr(io.StringIO()):
            self.assertEqual(project.main(["check", "--project", str(self.root / "missing")]), 1)

    def test_cli_check_preserves_failure_status(self):
        self.update("progress.md", phase="implementation")
        with contextlib.redirect_stderr(io.StringIO()):
            self.assertEqual(project.main(["check", "--project", str(self.root)]), 1)

    def test_installed_copy_runs_without_repository(self):
        install = self.root / ".agents" / "skills" / "vibe-web-builder"
        shutil.copytree(SKILL, install, ignore=shutil.ignore_patterns("__pycache__"))
        target = self.root / "website"
        target.mkdir()
        import subprocess
        result = subprocess.run([sys.executable, str(install / "scripts/project.py"),
                                 "init", "--project", str(target)], capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, result.stderr)
        check = subprocess.run([sys.executable, str(install / "scripts/project.py"),
                                "check", "--project", str(target)], capture_output=True, text=True)
        self.assertEqual(check.returncode, 0, check.stderr)


if __name__ == "__main__":
    unittest.main()
