# personal-link-hub

A tiny generator that turns `links.json` into a self-contained `index.html` link
page: sections, accessible markup, inline CSS and no JavaScript.

## Features

- Sections with titles, links with labels and optional descriptions.
- Escapes all content; validates that URLs are `http(s)`.
- Inline CSS, no external requests, works offline.
- `--out` for the destination, `--json` to dump the parsed model.
- Tests check rendering, escaping, validation and section grouping.

## Installation

```bash
git clone https://github.com/victor-harden/personal-link-hub.git
cd personal-link-hub
```

## Usage

```bash
python3 build.py links.example.json --out index.html
```

`links.json` shape:

```json
{
  "title": "Victor",
  "sections": [
    {"name": "Projects", "links": [{"label": "VictorHub", "url": "https://github.com/victor-harden/victorhub"}]}
  ]
}
```

## Tests

```bash
python3 -m unittest discover -s tests -v
```

## License

MIT — see [LICENSE](LICENSE).
