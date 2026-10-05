"""Shared presentation defaults and installed syntax theme validation."""

from dataclasses import dataclass

from pygments.styles import get_all_styles


def available_themes() -> tuple[str, ...]:
    return tuple(sorted(set(get_all_styles()) | {"ansi_dark", "ansi_light"}))


@dataclass(frozen=True)
class RequestLoggerTheme:
    syntax_theme: str = "monokai"
    border: str = "#6C7086"

    def __post_init__(self) -> None:
        if self.syntax_theme not in available_themes():
            raise ValueError(
                f"Unknown syntax_theme {self.syntax_theme!r}. Available themes: "
                + ", ".join(available_themes())
            )
