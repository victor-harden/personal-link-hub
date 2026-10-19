#!/usr/bin/env python3
"""Generate a static link hub page from JSON."""
from __future__ import annotations

import argparse
import html
import json
import sys
from pathlib import Path
from urllib.parse import urlparse

CSS = """
:root { --bg:#0f172a; --card:#1e293b; --text:#e2e8f0; --accent:#38bdf8; }
* { box-sizing: border-box; }
body { margin:0; padding:3rem 1.5rem; background:var(--bg); color:var(--text);
       font-family:system-ui, sans-serif; }
main { max-width:640px; margin:0 auto; }
h1 { color:var(--accent); }
section { margin-top:2rem; }
h2 { font-size:0.85rem; text-transform:uppercase; color:#94a3b8; }
a { display:block; background:var(--card); color:var(--text); text-decoration:none;
    padding:1rem 1.25rem; border-radius:0.75rem; margin-bottom:0.75rem;
    border:1px solid #334155; min-height:44px; }
a:hover, a:focus { border-color:var(--accent); outline:none; }
a small { display:block; color:#94a3b8; margin-top:0.25rem; }
"""


def validate(data: dict) -> dict:
    title = (data.get("title") or "").strip()
    if not title:
        raise ValueError("title is required")
    sections = data.get("sections")
    if not isinstance(sections, list) or not sections:
        raise ValueError("at least one section is required")
    for section in sections:
        if not (section.get("name") or "").strip():
            raise ValueError("section name is required")
        links = section.get("links")
        if not isinstance(links, list) or not links:
            raise ValueError(f"section {section.get('name')!r} needs at least one link")
        for link in links:
            parsed = urlparse(link.get("url", ""))
            if parsed.scheme not in ("http", "https") or not parsed.netloc:
                raise ValueError(f"invalid link url: {link.get('url')!r}")
            if not (link.get("label") or "").strip():
                raise ValueError("link label is required")
    return data


def render(data: dict) -> str:
    body = []
    for section in data["sections"]:
        body.append(f"<section><h2>{html.escape(section['name'])}</h2>")
        for link in section["links"]:
            note = (f"<small>{html.escape(link['description'])}</small>"
                    if link.get("description") else "")
            body.append(
                f'<a href="{html.escape(link["url"], quote=True)}">'
                f'{html.escape(link["label"])}{note}</a>'
            )
        body.append("</section>")
    return (
        "<!doctype html>\n<html lang=\"en\">\n<head>\n<meta charset=\"utf-8\">\n"
        "<meta name=\"viewport\" content=\"width=device-width, initial-scale=1\">\n"
        f"<title>{html.escape(data['title'])}</title>\n<style>{CSS}</style>\n"
        "</head>\n<body>\n<main>\n"
        f"<h1>{html.escape(data['title'])}</h1>\n"
        + "\n".join(body)
        + "\n</main>\n</body>\n</html>\n"
    )


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description="Link hub generator")
    parser.add_argument("config", type=Path)
    parser.add_argument("--out", type=Path, default=Path("index.html"))
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args(argv)

    try:
        data = json.loads(args.config.read_text(encoding="utf-8"))
        validate(data)
    except (OSError, json.JSONDecodeError, ValueError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2
    if args.json:
        print(json.dumps(data, indent=2))
        return 0
    args.out.write_text(render(data), encoding="utf-8")
    print(f"wrote {args.out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
