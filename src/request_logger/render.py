"""Static Rich rendering suitable for native terminals and redirected CI logs."""

import json
from typing import Any
from urllib.parse import parse_qsl, urlsplit

from rich.console import Group, RenderableType
from rich.panel import Panel
from rich.rule import Rule
from rich.syntax import Syntax
from rich.table import Table
from rich.text import Text

from .models import Exchange
from .protection import Protector
from .theme import RequestLoggerTheme

DEFAULT_THEME = RequestLoggerTheme()


def body(
    value: Any, protector: Protector, theme: RequestLoggerTheme = DEFAULT_THEME
) -> RenderableType:
    value = protector.clean(value)
    if value is None or value == "":
        return Text("Body is empty", style="dim")
    if isinstance(value, (dict, list)):
        return Syntax(
            json.dumps(value, indent=2, ensure_ascii=False),
            "json",
            theme=theme.syntax_theme,
            word_wrap=True,
        )
    return Text(str(value))


def exchange(
    record: Exchange,
    full: bool,
    protector: Protector,
    theme: RequestLoggerTheme = DEFAULT_THEME,
) -> RenderableType:
    title = protector.text(record.name)
    status = "No response" if record.status_code is None else f"HTTP {record.status_code}"
    color = (
        "red"
        if record.error
        else ("green" if record.status_code and 200 <= record.status_code < 300 else "yellow")
    )
    facts = Text()
    facts.append(record.method + " ", style="bold cyan")
    facts.append(protector.text(record.url))
    facts.append("\n" + status, style=color)
    if record.duration_ms is not None:
        facts.append(f" · {record.duration_ms:.2f} ms")
    items: list[RenderableType] = [facts]
    if record.error:
        items.append(Text(protector.text(record.error), style="red"))
    if full:
        pairs = parse_qsl(urlsplit(record.url).query, keep_blank_values=True)
        sections: list[tuple[str, Any]] = []
        if pairs:
            sections.append(("Params", [{"name": k, "value": v} for k, v in pairs]))
        sections.extend(
            [("Request headers", record.request_headers), ("Request body", record.request_body)]
        )
        if record.status_code is not None:
            sections.extend(
                [
                    ("Response headers", record.response_headers),
                    ("Response body", record.response_body),
                ]
            )
        for label, value in sections:
            if value is None or value == "" or value == {} or value == []:
                continue
            items.extend(
                [Rule(Text(label, style="bold"), style=theme.border), body(value, protector, theme)]
            )
    if record.assertions:
        table = Table("Assertion", "Result", "Message", box=None, expand=True)
        for a in record.assertions:
            table.add_row(
                Text(protector.text(a.label)),
                Text(a.status, style="green" if a.status == "PASS" else "red"),
                Text(protector.text(a.message)),
            )
        items.extend([Rule("Assertions", style=theme.border), table])
    return Panel(Group(*items), title=Text(title), border_style=theme.border)
