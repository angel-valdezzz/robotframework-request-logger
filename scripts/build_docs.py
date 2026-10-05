"""Generate Libdoc and reproducible visual captures of actual Robot/Rich output."""

import io
import shutil
import subprocess
import sys
from pathlib import Path
from unittest.mock import patch

from rich.console import Console
from rich.terminal_theme import MONOKAI
from robot import run

ROOT = Path(__file__).resolve().parents[1]


def main() -> None:
    assets = ROOT / "docs" / "assets"
    assets.mkdir(exist_ok=True)
    keywords = ROOT / "docs" / "keywords" / "index.html"
    keywords.parent.mkdir(exist_ok=True)
    subprocess.run(
        [sys.executable, "-m", "robot.libdoc", "RequestLogger", str(keywords)], check=True
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
        console.save_svg(
            str(assets / f"console-{mode}.svg"),
            title=f"RequestLogger · {mode}",
            theme=MONOKAI,
            clear=False,
        )
        (assets / f"console-{mode}.txt").write_text(text, encoding="utf-8")
    # Both languages use the same generated console captures and Libdoc reference.
    english = ROOT / "docs-en"
    for directory in ("assets", "keywords"):
        shutil.copytree(ROOT / "docs" / directory, english / directory, dirs_exist_ok=True)
    for config in ("mkdocs.yml", "mkdocs.en.yml"):
        subprocess.run(
            [sys.executable, "-m", "mkdocs", "build", "--strict", "--config-file", config],
            cwd=ROOT,
            check=True,
        )
    shutil.copytree(ROOT / "build" / "site-en", ROOT / "site" / "en")


if __name__ == "__main__":
    main()
