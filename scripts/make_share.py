"""Generate link-preview images and per-sport share pages.

WhatsApp, iMessage, Slack and others build link previews from Open Graph
tags in the page HTML, and they ignore anything after "#". So each sport
gets a small static page at s/<slug>/ with its own tags, which forwards
people into the app at #s-<slug>.

Usage (with the site served locally, e.g. python3 -m http.server 8123):
    python3 scripts/make_share.py http://localhost:8123/
    python3 scripts/make_share.py --pages-only   # share pages only, keep images

Writes og/default.jpg, og/<slug>.jpg (1200x630) and s/<slug>/index.html.
Needs Google Chrome for the headless screenshots.
"""
import html
import json
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SITE = "https://nishithada.github.io/built-for/"
CHROME_CANDIDATES = [
    "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
    "/Applications/Google Chrome 2.app/Contents/MacOS/Google Chrome",
]
# Must match OGLABEL in index.html
LABEL = {
    "Football (soccer)": "football", "Road cycling (climbing)": "road cycling",
    "Long & triple jump": "the long jump", "Shot put & discus": "the throws",
    "Wrestling & judo": "wrestling", "Horse racing jockey": "horse racing",
    "Baseball pitcher": "pitching", "Coxswain": "coxing",
}


def slug(name):
    return re.sub(r"[^a-z0-9]+", "-", name.lower()).strip("-")


def sports():
    src = (ROOT / "index.html").read_text()
    # Top-level sports carry a category; positions don't
    for m in re.finditer(r"\{n:'([^']+)',cat:'([^']+)',why:'((?:[^'\\]|\\.)*)'", src):
        name, cat, why = m.groups()
        yield name, cat, json.loads('"' + why.replace('"', '\\"') + '"')


def chrome():
    for c in CHROME_CANDIDATES:
        if Path(c).exists():
            return c
    sys.exit("Google Chrome not found")


def shoot(base, key, out):
    png = out.with_suffix(".png")
    subprocess.run([chrome(), "--headless=new", "--hide-scrollbars", "--force-device-scale-factor=1",
                    "--window-size=1200,630", "--virtual-time-budget=6000",
                    f"--screenshot={png}", f"{base}?og={key}"], check=True, capture_output=True)
    subprocess.run(["sips", "-s", "format", "jpeg", "-s", "formatOptions", "82", str(png), "--out", str(out)],
                   check=True, capture_output=True)
    png.unlink()


PAGE = """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Are you built for {label}? · Built For</title>
<meta name="description" content="{desc}">
<meta property="og:type" content="website">
<meta property="og:site_name" content="Built For">
<meta property="og:title" content="Are you built for {label}?">
<meta property="og:description" content="{desc}">
<meta property="og:url" content="{site}s/{slug}/">
<meta property="og:image" content="{site}og/{slug}.jpg">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:image:alt" content="Are you built for {label}? Built For compares your body with elite athletes.">
<meta name="twitter:card" content="summary_large_image">
<meta name="robots" content="noindex, follow">
<link rel="canonical" href="{site}">
<link rel="icon" href="../../favicon.svg" type="image/svg+xml">
<script>location.replace("../../#s-{slug}")</script>
</head>
<body style="font-family:system-ui,sans-serif;padding:24px">
<p><a href="../../#s-{slug}">Open Built For: {name}</a></p>
</body>
</html>
"""


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    pages_only = "--pages-only" in sys.argv  # rewrite share pages without re-capturing images
    base = args[0] if args else "http://localhost:8123/"
    (ROOT / "og").mkdir(exist_ok=True)
    if not pages_only:
        shoot(base, "default", ROOT / "og" / "default.jpg")
        print("og/default.jpg")
    for name, cat, why in sports():
        s = slug(name)
        label = LABEL.get(name, name.lower())
        if not pages_only:
            shoot(base, s, ROOT / "og" / f"{s}.jpg")
        desc = f"{why} See how your build compares with elite athletes in about 2 minutes."
        page = ROOT / "s" / s / "index.html"
        page.parent.mkdir(parents=True, exist_ok=True)
        page.write_text(PAGE.format(label=html.escape(label), desc=html.escape(desc), site=SITE,
                                    slug=s, name=html.escape(name)))
        print(f"og/{s}.jpg  s/{s}/")


if __name__ == "__main__":
    main()
