"""Generate Libdoc and reproducible visual captures of actual Robot/Rich output."""

import html
import io
import json
import os
import re
import shutil
import subprocess
import sys
import zipfile
from pathlib import Path
from unittest.mock import patch

from bilingual_libdoc import generate
from build_themes import generate as generate_themes
from rich.console import Console
from rich.terminal_theme import MONOKAI
from robot import run

ROOT = Path(__file__).resolve().parents[2]


def write_console_excerpt(text: str) -> None:
    """Use the same genuine Summary execution in the hero and full console export."""
    lines = [line.strip("│ ") for line in text.splitlines()]
    request_index = next(i for i, line in enumerate(lines) if "/books/42?" in line)
    request = lines[request_index]
    response = lines[request_index + 1]
    assert request.startswith("GET ") and response.startswith("HTTP 200 · ")
    assertion = next(line for line in lines if "Book title must contain a value" in line)
    _, result, message = re.split(r"\s{2,}", assertion, maxsplit=2)
    assert result == "FAIL"
    fragment = (
        '<div class="console-line" id="trace-request"><b>GET</b> '
        f"<code>{html.escape(request[4:])}</code></div>\n"
        '<div class="console-line" id="trace-response">HTTP <b>200</b>'
        f'<span class="console-duration">{html.escape(response[8:])}</span></div>\n'
        '<div class="console-assertion" id="trace-assertion">'
        '<div class="assertion-columns console-columns-labels" aria-hidden="true">'
        "<span>Assertion</span><span>Result</span><span>Message</span></div>"
        '<div class="assertion-columns"><span>Book title must contain a value</span>'
        f'<b>FAIL</b><span class="console-message">{html.escape(message)}</span></div></div>\n'
    )
    (ROOT / "docs/overrides/partials/console-excerpt.html").write_text(fragment, encoding="utf-8")


def main() -> None:
    for config_dir in (ROOT, ROOT / "docs/config"):
        fonts = config_dir / ".cache/plugin/social/fonts/DejaVu Sans"
        fonts.mkdir(parents=True, exist_ok=True)
        for source in (ROOT / "docs/assets/fonts").glob("*.ttf"):
            shutil.copyfile(source, fonts / source.name)
    assets = ROOT / "docs" / "assets"
    assets.mkdir(exist_ok=True)
    generate(
        "RequestLogger",
        ROOT,
        "keywords/index.html",
        "https://angel-valdezzz.github.io/robotframework-request-logger/",
    )
    for mode in ("summary", "failures", "full"):
        captured: list[Console] = []

        def console_factory(captured: list[Console] = captured, **kwargs: object) -> Console:
            # Recording is only for documentation; production retains auto-detection.
            console = Console(
                file=io.StringIO(),
                record=True,
                width=100,
                force_terminal=True,
                force_interactive=False,
                markup=False,
                highlight=False,
            )
            captured.append(console)
            return console

        with patch("request_logger.Console", side_effect=console_factory):
            code = run(
                str(ROOT / "tests" / "visual.robot"),
                console="none",
                outputdir=str(ROOT / "build" / "visual" / mode),
                variable=[f"MODE:{mode}"],
            )
        assert code == 1 and len(captured) == 1, "Expected one intentionally failing real HTTP test"
        console = captured[0]
        text = console.export_text(clear=False)
        assert "fake-secret-TOKEN" not in text and "fake-query-SECRET" not in text
        if mode == "summary":
            write_console_excerpt(text)
        console.save_svg(
            str(assets / f"console-{mode}.svg"),
            title=f"RequestLogger · {mode}",
            theme=MONOKAI,
            clear=False,
        )
        (assets / f"console-{mode}.txt").write_text(text, encoding="utf-8")
    with zipfile.ZipFile(assets / "book-example.zip", "w", zipfile.ZIP_DEFLATED) as archive:
        for name in ("visual.robot", "Fixture.py"):
            archive.write(ROOT / "tests" / name, name)
        archive.writestr(
            "README.md",
            "# Fictional book example\n\n"
            "Install: pip install robotframework-request-logger robotframework-requests\n\n"
            "Run: python -m robot --console none --variable MODE:summary visual.robot\n\n"
            "Modes: summary, failures, full. Exit code 1 is expected: the book title is empty.\n",
        )
    generate_themes(ROOT)
    # Assets are shared sources; each build publishes its own relative copies.
    for language in ("en", "es"):
        shutil.copytree(assets, ROOT / "docs" / language / "assets", dirs_exist_ok=True)
    for config in ("mkdocs.yml", "docs/config/es.yml"):
        subprocess.run(
            [sys.executable, "-m", "mkdocs", "build", "--strict", "--config-file", config],
            cwd=ROOT,
            check=True,
        )
    site = ROOT / "site"
    # Keep links shared during the pilot working after moving English to the root.
    pages = list(site.rglob("*.html"))
    for page in pages:
        relative = page.relative_to(site)
        if relative.name == "404.html":
            continue
        alias = site / "en" / relative
        alias.parent.mkdir(parents=True, exist_ok=True)
        target = os.path.relpath(page, alias.parent).replace(os.sep, "/")
        if target.endswith("index.html"):
            target = target.removesuffix("index.html")
        escaped = html.escape(target, quote=True)
        alias.write_text(
            '<!doctype html><html lang="en"><head><meta charset="utf-8">'
            f'<meta http-equiv="refresh" content="0;url={escaped}">'
            "<title>Documentation moved</title></head><body>"
            f'<a href="{escaped}">Continue to the English documentation</a>'
            f"<script>location.replace({json.dumps(target)} + location.search + location.hash);"
            "</script></body></html>",
            encoding="utf-8",
        )
    # Preserve previously shared console captures and download links as well.
    shutil.copytree(site / "assets", site / "en" / "assets", dirs_exist_ok=True)
    shutil.copytree(ROOT / "build" / "site-es", site / "es", dirs_exist_ok=True)


if __name__ == "__main__":
    main()
