"""Case-local HTTP records; no Robot execution objects or reporter dependency."""

from dataclasses import dataclass, field
from typing import Any


@dataclass
class Assertion:
    label: str
    status: str
    message: str = ""


@dataclass
class Exchange:
    id: str
    name: str
    method: str
    url: str
    request_headers: dict[str, str] = field(default_factory=dict)
    request_body: Any = None
    response_headers: dict[str, str] = field(default_factory=dict)
    response_body: Any = None
    status_code: int | None = None
    duration_ms: float | None = None
    error: str = ""
    assertions: list[Assertion] = field(default_factory=list)
    original_request: Any = field(default=None, repr=False)

    @property
    def failed(self) -> bool:
        return bool(self.error) or any(a.status == "FAIL" for a in self.assertions)
