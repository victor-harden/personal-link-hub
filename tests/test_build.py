import json
import sys
import tempfile
import unittest
from pathlib import Path

BASE = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE))
import build

SAMPLE = {
    "title": "Victor",
    "sections": [
        {"name": "Projects", "links": [
            {"label": "VictorHub", "url": "https://github.com/victor-harden/victorhub",
             "description": "Platform"}]},
    ],
}


class BuildTests(unittest.TestCase):
    def test_render_contains_link(self):
        html_text = build.render(SAMPLE)
        self.assertIn("VictorHub", html_text)
        self.assertIn("https://github.com/victor-harden/victorhub", html_text)

    def test_render_escapes_html(self):
        data = json.loads(json.dumps(SAMPLE))
        data["sections"][0]["links"][0]["label"] = "<script>alert(1)</script>"
        html_text = build.render(data)
        self.assertNotIn("<script>alert(1)</script>", html_text)
        self.assertIn("&lt;script&gt;", html_text)

    def test_validate_missing_title(self):
        with self.assertRaises(ValueError):
            build.validate({"sections": SAMPLE["sections"]})

    def test_validate_bad_url(self):
        bad = {"title": "x", "sections": [{"name": "s", "links": [
            {"label": "l", "url": "javascript:alert(1)"}]}]}
        with self.assertRaises(ValueError):
            build.validate(bad)

    def test_validate_empty_sections(self):
        with self.assertRaises(ValueError):
            build.validate({"title": "x", "sections": []})

    def test_cli_writes_file(self):
        with tempfile.TemporaryDirectory() as tmp:
            config = Path(tmp) / "links.json"
            config.write_text(json.dumps(SAMPLE))
            out = Path(tmp) / "index.html"
            code = build.main([str(config), "--out", str(out)])
            self.assertEqual(code, 0)
            self.assertIn("VictorHub", out.read_text())

    def test_cli_invalid_config(self):
        import contextlib
        import io
        with tempfile.TemporaryDirectory() as tmp:
            config = Path(tmp) / "links.json"
            config.write_text("{bad json")
            with contextlib.redirect_stderr(io.StringIO()):
                self.assertEqual(build.main([str(config)]), 2)


if __name__ == "__main__":
    unittest.main()
