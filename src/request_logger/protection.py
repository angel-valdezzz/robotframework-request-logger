"""Protect secrets and terminal output without depending on an HTML reporter."""

import json
import re
from typing import Any
from urllib.parse import parse_qsl, unquote, urlencode, urlsplit, urlunsplit

MASK = "[REDACTED]"


def safe_text(value: str) -> str:
    """Remove terminal control sequences from untrusted HTTP and Robot text."""
    value = re.sub(r"\x1b\][^\x07\x1b]*(?:\x07|\x1b\\)", "", value)
    value = re.sub(r"\x1b\[[0-?]*[ -/]*[@-~]", "", value)
    return re.sub(r"[\x00-\x08\x0b-\x1f\x7f-\x9f]", "", value)


class Protector:
    def __init__(self, headers: str, fields: str) -> None:
        self.headers = {v.strip().lower() for v in headers.split(",") if v.strip()}
        self.fields = {v.strip().lower() for v in fields.split(",") if v.strip()}
        self.secrets: set[str] = set()

    def remember(self, value: Any) -> None:
        if isinstance(value, str) and value:
            self.secrets.add(value)
            if value.lower().startswith("bearer "):
                self.secrets.add(value[7:])
        elif isinstance(value, dict):
            for v in value.values():
                self.remember(v)
        elif isinstance(value, (list, tuple)):
            for v in value:
                self.remember(v)

    def text(self, value: str) -> str:
        for secret in sorted(self.secrets, key=len, reverse=True):
            value = value.replace(secret, MASK)
        return safe_text(value)

    def clean(self, value: Any) -> Any:
        if isinstance(value, dict):
            out = {}
            for k, v in value.items():
                if str(k).lower() in self.fields:
                    self.remember(v)
                    out[str(k)] = MASK
                else:
                    out[str(k)] = self.clean(v)
            return out
        if isinstance(value, (list, tuple)):
            return [self.clean(v) for v in value]
        if isinstance(value, str):
            return self.text(value)
        if value is None or isinstance(value, (int, float, bool)):
            return value
        return self.text(str(value))

    def header_values(self, headers: Any) -> dict[str, str]:
        out = {}
        for k, v in headers.items():
            if k.lower() in self.headers:
                self.remember(str(v))
                out[str(k)] = MASK
            else:
                out[str(k)] = self.text(str(v))
        return out

    def url(self, url: str) -> str:
        parts = urlsplit(url)
        pairs = []
        for k, v in parse_qsl(parts.query, keep_blank_values=True):
            if k.lower() in self.fields:
                self.remember(v)
                v = MASK
            pairs.append((k, v))
        netloc = parts.netloc
        if "@" in netloc:
            credentials, host = netloc.rsplit("@", 1)
            self.remember(credentials)
            if parts.password:
                self.remember(unquote(parts.password))
            netloc = MASK + "@" + host
        return self.text(
            urlunsplit((parts.scheme, netloc, parts.path, urlencode(pairs), parts.fragment))
        )

    def body(self, value: Any, content_type: str) -> Any:
        if value is None:
            return None
        if "multipart/" in content_type.lower():
            return "[Multipart body omitted]"
        if isinstance(value, bytes):
            if not any(
                v in content_type.lower() for v in ("json", "text/", "xml", "form", "javascript")
            ):
                return f"[Binary body: {len(value)} bytes]"
            value = value.decode("utf-8", errors="replace")
        if not isinstance(value, str):
            return self.clean(value)
        if "application/x-www-form-urlencoded" in content_type.lower():
            # Preserve repeated field names and empty values.
            pairs = parse_qsl(value, keep_blank_values=True)
            for k, v in pairs:
                if k.lower() in self.fields:
                    self.remember(v)
            return [
                {"name": k, "value": MASK if k.lower() in self.fields else self.text(v)}
                for k, v in pairs
            ]
        try:
            return self.clean(json.loads(value))
        except (ValueError, TypeError):
            return self.text(value)
