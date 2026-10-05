"""Generate every installed theme from the same protected response and renderer."""

import io
from pathlib import Path

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

All tabs below show the **same protected response**, exported from the production
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

Todas las pestañas muestran el **mismo response protegido**, exportado desde el
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
    for language, introduction in introductions.items():
        tabs = []
        for name in ordered:
            tabs.append(f'''=== "{name}"

    ### {name}

    ```robotframework
    *** Settings ***
    Library    RequestLogger    mode=full    syntax_theme={name}
    ```

    ![{name}](assets/themes/{name}.svg)

''')
        (root / "docs" / language / "themes.md").write_text(
            introduction + "".join(tabs), encoding="utf-8"
        )


if __name__ == "__main__":
    generate(Path(__file__).resolve().parents[1])
