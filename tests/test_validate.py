import importlib.util
import json
from pathlib import Path
import shutil
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("vwb_validate", ROOT / "scripts/validate.py")
validator = importlib.util.module_from_spec(spec)
spec.loader.exec_module(validator)


class ValidationTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name) / "repo"
        shutil.copytree(ROOT, self.root, ignore=shutil.ignore_patterns(
            ".git", ".venv", "__pycache__", "dist", "node_modules"))

    def test_repository_passes(self):
        self.assertEqual(validator.validate(self.root), [])

    def test_invalid_manifest_rejected(self):
        path = self.root / ".codex-plugin/plugin.json"
        data = json.loads(path.read_text())
        data["skills"] = "../../elsewhere"
        path.write_text(json.dumps(data))
        self.assertTrue(any("manifest" in e for e in validator.validate(self.root)))

    def test_missing_frontmatter_rejected(self):
        path = self.root / "skills/vibe-web-builder/SKILL.md"
        path.write_text("# No metadata\n")
        self.assertTrue(any("metadata" in e for e in validator.validate(self.root)))

    def test_invalid_skill_name_rejected(self):
        path = self.root / "skills/vibe-web-builder/SKILL.md"
        path.write_text(path.read_text().replace("name: vibe-web-builder", "name: Invalid--Name", 1))
        self.assertTrue(any("name" in e for e in validator.validate(self.root)))

    def test_broken_markdown_link_rejected(self):
        with (self.root / "README.md").open("a") as file:
            file.write("\n[missing](docs/no-such-file.md)\n")
        self.assertTrue(any("资源路径无效" in e for e in validator.validate(self.root)))

    def test_template_generator_placeholder_rejected(self):
        with (self.root / "skills/vibe-web-builder/assets/templates/sitemap.md").open("a") as file:
            file.write("\nTODO: replace generated template\n")
        self.assertTrue(any("占位" in e for e in validator.validate(self.root)))

    def test_secret_detection_does_not_echo_secret(self):
        fake = "gh" + "p_" + "x" * 36
        (self.root / "accidental.txt").write_text(fake)
        errors = validator.validate(self.root)
        self.assertTrue(any("敏感" in e for e in errors))
        self.assertNotIn(fake, "\n".join(errors))

    def test_environment_file_distribution_refused(self):
        (self.root / ".env.local").write_text("EXAMPLE=value\n")
        self.assertTrue(any("私密配置" in e for e in validator.validate(self.root)))

    def test_version_changelog_must_match(self):
        path = self.root / ".codex-plugin/plugin.json"
        data = json.loads(path.read_text())
        data["version"] = "0.2.0"
        path.write_text(json.dumps(data))
        self.assertTrue(any("CHANGELOG" in e for e in validator.validate(self.root)))


if __name__ == "__main__":
    unittest.main()
