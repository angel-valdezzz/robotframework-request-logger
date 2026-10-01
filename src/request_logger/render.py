"""Static Rich rendering suitable for native terminals and redirected CI logs."""

from typing import Any
from urllib.parse import parse_qsl, urlsplit

from rich.console import Group, RenderableType
from rich.json import JSON
from rich.panel import Panel
from rich.table import Table
from rich.text import Text

from .models import Exchange
from .protection import Protector


def body(value: Any, protector: Protector) -> RenderableType:
    value = protector.clean(value)
    if value is None or value == "":
        return Text("Body is empty", style="dim")
    if isinstance(value, (dict, list)):
        return JSON.from_data(value, indent=2, ensure_ascii=False)
    return Text(str(value))


def exchange(record: Exchange, full: bool, protector: Protector) -> RenderableType:
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
        if pairs:
            items += [
                Text("Params", style="bold"),
                JSON.from_data(
                    protector.clean([{"name": k, "value": v} for k, v in pairs]), ensure_ascii=False
                ),
            ]
        items += [
            Text("Request headers", style="bold"),
            JSON.from_data(protector.clean(record.request_headers), ensure_ascii=False),
            Text("Request body", style="bold"),
            body(record.request_body, protector),
        ]
        if record.status_code is not None:
            items += [
                Text("Response headers", style="bold"),
                JSON.from_data(protector.clean(record.response_headers), ensure_ascii=False),
                Text("Response body", style="bold"),
                body(record.response_body, protector),
            ]
    if record.assertions:
        table = Table("Assertion", "Result", "Message", box=None, expand=True)
        for a in record.assertions:
            table.add_row(
                Text(protector.text(a.label)),
                Text(a.status, style="green" if a.status == "PASS" else "red"),
                Text(protector.text(a.message)),
            )
        items.append(table)
    return Panel(Group(*items), title=Text(title), border_style="red" if record.failed else "cyan")
