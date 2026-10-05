"""Generate every installed theme from the same protected response and renderer."""

import html
import io
from pathlib import Path

from pygments import highlight
from pygments.formatters import HtmlFormatter
from pygments.lexers import RobotFrameworkLexer
from rich.console import Console
from rich.terminal_theme import MONOKAI

from request_logger.models import Assertion, Exchange
from request_logger.protection import Protector
from request_logger.render import exchange
from request_logger.theme import RequestLoggerTheme, available_themes


def generate(root: Path) -> None:
    assets = root / "docs" / "assets" / "themes"
    assets.mkdir(parents=True, exist_ok=True)
    record = Exchange(
        id="theme-preview",
        name="User profile",
        method="GET",
        url="https://example.test/users/42",
        status_code=200,
        duration_ms=12.5,
        response_headers={"Content-Type": "application/json"},
        response_body={
            "id": 42,
            "name": "Angel",
            "active": True,
            "roles": ["tester", "developer"],
            "score": 98.5,
            "notes": None,
            "access_token": "demo-secret",
        },
        assertions=[Assertion("HTTP status", "PASS")],
    )
    themes = available_themes()
    for name in themes:
        protector = Protector("Authorization", "access_token")
        console = Console(
            file=io.StringIO(),
            record=True,
            width=90,
            force_terminal=True,
            color_system="truecolor",
            highlight=False,
            markup=False,
        )
        console.print(exchange(record, True, protector, RequestLoggerTheme(name)))
        assert "demo-secret" not in console.export_text(clear=False)
        console.save_svg(
            str(assets / f"{name}.svg"), title=f"RequestLogger · {name}", theme=MONOKAI
        )
    introductions = {
        "en": """# Themes

Choose JSON syntax colors when importing the library. The default is `monokai`.
No configuration file is required. The theme supplies the JSON block background;
it does not change the terminal background, HTTP colors or assertion colors.
Text and empty responses do not receive JSON highlighting. Empty detail sections
are omitted. Borders and section separators use a soft neutral color.

All previews show the **same protected response**, exported from the production
Rich renderer at 90 columns. Terminal fonts and color capabilities may differ.
`ansi_dark` and `ansi_light` use your terminal palette; these exports use the
same dark terminal palette for comparison. Prefer `ansi_light` in a light terminal.

Available names depend on your installed Pygments version. An invalid name reports
the available choices. To list the names in your environment:

```bash
python -c "from request_logger.theme import available_themes; print(', '.join(available_themes()))"
```

## Theme previews

""",
        "es": """# Temas

Elige los colores del JSON desde el import. El tema predeterminado es `monokai`.
No necesitas un archivo de configuración. El tema aporta el fondo del bloque JSON;
no cambia el fondo de la terminal ni los colores HTTP o de assertions.
Las respuestas de texto y vacías no reciben resaltado JSON. Se omiten las secciones
vacías. Los bordes y separadores usan un color neutro suave.

Todas las vistas previas muestran el **mismo response protegido**, exportado desde el
renderizador Rich de producción a 90 columnas. La fuente y los colores pueden
variar según tu terminal. `ansi_dark` y `ansi_light` usan la paleta de tu terminal;
estas muestras usan la misma paleta oscura para comparar. Usa `ansi_light` en una
terminal clara.

Los nombres disponibles dependen de tu versión instalada de Pygments. Un nombre
inválido muestra las opciones disponibles. Para consultarlas en tu entorno:

```bash
python -c "from request_logger.theme import available_themes; print(', '.join(available_themes()))"
```

## Vista previa de temas

""",
    }
    # Put the default first, then every supported style without a hand-maintained list.
    ordered = ("monokai",) + tuple(name for name in themes if name != "monokai")
    snippets = {
        name: highlight(
            "*** Settings ***\nLibrary    RequestLogger    mode=full    syntax_theme=" + name,
            RobotFrameworkLexer(),
            HtmlFormatter(nowrap=True),
        ).rstrip("\n")
        for name in ordered
    }
    templates = "".join(
        f'<template data-theme-code="{name}">{snippet}</template>'
        for name, snippet in snippets.items()
    )
    labels = {
        "en": (
            "Choose a theme",
            "Search themes",
            "Available themes",
            "Previous",
            "Next",
            "No matching themes",
            "Preview unavailable",
            "Open preview",
        ),
        "es": (
            "Elige un tema",
            "Buscar temas",
            "Temas disponibles",
            "Anterior",
            "Siguiente",
            "No hay temas que coincidan",
            "Vista previa no disponible",
            "Abrir vista previa",
        ),
    }
    for language, introduction in introductions.items():
        choose, search, available, prev, nxt, empty, error, open_preview = labels[language]
        options = "".join(
            f'<option value="{html.escape(name)}">{html.escape(name)}</option>' for name in ordered
        )
        links = " · ".join(f'<a href="../assets/themes/{name}.svg">{name}</a>' for name in ordered)
        gallery = f"""<div class="theme-gallery" data-theme-gallery>
  <details class="theme-picker" hidden>
    <summary>{choose}: <strong data-theme-current>monokai</strong></summary>
    <div class="theme-picker-menu">
      <label for="theme-search">{search}</label>
      <input id="theme-search" type="search" autocomplete="off" placeholder="one-dark, dracula…">
      <label for="theme-select">{available}</label>
      <select id="theme-select" size="8">{options}</select>
      <p data-theme-empty hidden role="status">{empty}</p>
    </div>
  </details>
  <div class="theme-gallery-nav" hidden>
    <button type="button" data-theme-prev>{prev}</button>
    <span data-theme-position role="status" aria-live="polite"></span>
    <button type="button" data-theme-next>{nxt}</button>
  </div>
  <h3 data-theme-title>monokai</h3>
  <img data-theme-preview src="../assets/themes/monokai.svg" alt="monokai"
       data-base="../assets/themes/" width="1100">
  <p data-theme-image-error hidden role="alert">{error}.
    <a data-theme-image-link href="../assets/themes/monokai.svg">{open_preview}</a>
  </p>
  <div class="theme-gallery-code highlight">
    <pre><code data-theme-import>{snippets["monokai"]}</code></pre>
  </div>
  {templates}
  <noscript><p>{available}: {links}</p></noscript>
</div>
"""
        (root / "docs" / language / "themes.md").write_text(
            introduction + gallery, encoding="utf-8"
        )


if __name__ == "__main__":
    generate(Path(__file__).resolve().parents[1])
