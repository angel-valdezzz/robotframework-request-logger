"""HTTP console logging for Robot Framework; does not execute requests or assertions.

```robotframework
*** Settings ***
Library    RequestsLibrary
Library    RequestLogger    mode=summary

*** Test Cases ***
Health
    ${response}=    GET    ${URL}    expected_status=anything
    ${id}=    Log Response    Health    ${response}
    Should Be Equal As Integers    ${response.status_code}    200
    Log Assertion Result    ${id}    HTTP status    PASS
```

Output is buffered until end_test so failures can be filtered and secrets learned
later in a case can be hidden. Robot's native console and return code are unchanged.
"""

import sys
from typing import Any

from requests import PreparedRequest, Response
from rich.console import Console, Group
from rich.text import Text
from robot.api import logger
from robot.api.deco import keyword, library

from .models import Assertion, Exchange
from .protection import Protector
from .render import exchange
from .theme import RequestLoggerTheme

__version__ = "0.2.0"
_HEADERS = "Authorization,Proxy-Authorization,Cookie,Set-Cookie,X-API-Key"
_FIELDS = "access_token,refresh_token,client_secret,password,token,api_key"


@library(scope="GLOBAL", version=__version__, doc_format="MARKDOWN", auto_keywords=False)
class RequestLogger:
    """Display HTTP exchanges and assertion results in the test's console output.

    Import alongside RequestsLibrary. This library records completed responses;
    it does not send requests, run assertions or create HTML reports. Output is
    buffered until the test finishes, allowing secrets learned later to be redacted.

    ```robotframework
    *** Settings ***
    Library    RequestsLibrary
    Library    RequestLogger

    *** Test Cases ***
    Health
        ${response}=    GET    ${URL}    expected_status=anything
        ${id}=    Log Response    Health    ${response}
        Should Be Equal As Integers    ${response.status_code}    200
        Log Assertion Result    ${id}    HTTP status    PASS
    ```

    Choose `mode=summary`, `failures` or `full` when importing; see [Importing]
    for JSON syntax themes and redaction options. Redaction affects this console
    only, not Robot's or RequestsLibrary's own logs.
    """

    ROBOT_LISTENER_API_VERSION = 3

    def __init__(
        self,
        mode: str = "summary",
        redact_headers: str = _HEADERS,
        redact_body_fields: str = _FIELDS,
        syntax_theme: str = "monokai",
    ) -> None:
        """Choose summary (default), failures or full.

        summary prints all exchanges briefly; failures prints full details only for
        explicitly failed assertions or request errors; full prints all details.
        HTTP 4xx/5xx alone does not imply test failure. Assertions accept PASS/FAIL only.
        No HTTP call or assertion is executed by this library. No console mode is
        changed. In CI output is static, with Rich terminal detection and plain text
        fallback. Full text/JSON bodies are kept; binary/multipart bodies are summarized.
        XML field redaction is not supported. Redaction affects this console only.

        syntax_theme selects an installed Pygments style (default: monokai), or
        ansi_dark/ansi_light. It changes JSON colors and the JSON block background
        only; HTTP/assertion colors stay unchanged. Empty detail sections are omitted.
        An unknown theme raises ValueError with the available names. No theme file is needed.

        ```robotframework
        Library    RequestLogger    mode=full    syntax_theme=monokai
        ```
        """
        if mode not in {"summary", "failures", "full"}:
            raise ValueError("mode must be summary, failures or full")
        self.theme = RequestLoggerTheme(syntax_theme=syntax_theme)
        self.mode = mode
        self.redact_headers = redact_headers
        self.redact_body_fields = redact_body_fields
        self.ROBOT_LIBRARY_LISTENER = self
        self.records: list[Exchange] = []
        self.protector = Protector(redact_headers, redact_body_fields)
        self.active = False

    def start_test(self, data: Any, result: Any) -> None:
        self.records = []
        self.protector = Protector(self.redact_headers, self.redact_body_fields)
        self.active = True

    def end_test(self, data: Any, result: Any) -> None:
        try:
            visible = [r for r in self.records if self.mode != "failures" or r.failed]
            items = [
                exchange(r, self.mode != "summary", self.protector, self.theme) for r in visible
            ]
            if result.status in {"FAIL", "SKIP"}:
                items.append(
                    Text(
                        self.protector.text(f"Robot {result.status}: {result.message}"),
                        style="red" if result.status == "FAIL" else "yellow",
                    )
                )
            if items:
                # Robot captures sys.stdout during keywords. Use its original stream,
                # while retaining Rich's detection for redirected/non-interactive output.
                console = Console(
                    file=sys.__stdout__ or sys.stdout,
                    force_interactive=False,
                    markup=False,
                    highlight=False,
                    safe_box=True,
                )
                console.print(Group(*items))
        except (OSError, UnicodeError) as error:
            logger.warn(f"RequestLogger output unavailable: {type(error).__name__}")
        finally:
            self.active = False
            self.records = []

    def _require_case(self) -> None:
        if not self.active:
            raise RuntimeError("Logger keywords must run inside an active Robot test")

    def _find(self, request_id: str) -> Exchange:
        self._require_case()
        for r in self.records:
            if r.id == request_id:
                return r
        raise ValueError(f"Unknown request ID in current test: {request_id}")

    @keyword("Log Request")
    def log_request(self, name: str, request: PreparedRequest) -> str:
        """Register an already prepared requests.PreparedRequest; return a case-local ID.

        Does not send HTTP. Usually Log Response alone is sufficient. Passing the same
        prepared request to Log Request and Log Response reuses the ID and one record.
        A request without a response is not automatically classified as a failed test.

        ```robotframework
        ${id}=    Log Request    Health    ${response.request}
        ```
        """
        self._require_case()
        if not isinstance(request, PreparedRequest):
            raise TypeError("request must be a requests.PreparedRequest")
        found = next((r for r in self.records if r.original_request is request), None)
        if found:
            return found.id
        headers = self.protector.header_values(request.headers)
        url = self.protector.url(request.url or "")
        request_body = self.protector.body(request.body, request.headers.get("Content-Type", ""))
        record = Exchange(
            id=f"request-{len(self.records) + 1}",
            name=name,
            method=request.method or "",
            url=url,
            request_headers=headers,
            request_body=request_body,
            original_request=request,
        )
        self.records.append(record)
        return record.id

    @keyword("Log Response")
    def log_response(self, name: str, response: Response) -> str:
        """Register an existing requests.Response and its prepared request; return its ID.

        Does not execute HTTP. Capture before validating status or parsing JSON.
        Headers, bodies, elapsed time and URL are shown according to mode at test end.
        A repeated call for the same prepared request updates its existing record.

        ```robotframework
        ${response}=    GET    ${URL}    expected_status=anything
        ${id}=    Log Response    Health    ${response}
        ```
        """
        self._require_case()
        if not isinstance(response, Response) or response.request is None:
            raise TypeError("response must be a requests.Response with a prepared request")
        request_id = self.log_request(name, response.request)
        r = self._find(request_id)
        r.response_headers = self.protector.header_values(response.headers)
        r.response_body = self.protector.body(
            response.content, response.headers.get("Content-Type", "")
        )
        r.status_code = response.status_code
        r.duration_ms = round(response.elapsed.total_seconds() * 1000, 2)
        return request_id

    @keyword("Log Request Error")
    def log_request_error(
        self, name: str, method: str, url: str, message: str, request_id: str | None = None
    ) -> str:
        """Register an HTTP attempt without a response; return its ID.

        No HTTP status or response body is fabricated. Optional request_id associates
        the error with an earlier Log Request. This keyword does not fail the test:
        propagate the original failure after logging it.

        ```robotframework
        TRY
            ${response}=    GET    ${URL}    timeout=10
        EXCEPT    AS    ${error}
            Log Request Error    Health    GET    ${URL}    ${error}
            Fail    ${error}
        END
        ```
        """
        self._require_case()
        protected_url = self.protector.url(url)
        if request_id:
            r = self._find(request_id)
            if r.status_code is not None:
                raise ValueError("A received HTTP response is not a request transport error")
        else:
            r = Exchange(
                id=f"request-{len(self.records) + 1}",
                name=name,
                method=method.upper(),
                url=protected_url,
            )
            self.records.append(r)
        r.error = self.protector.text(message) or "HTTP request failed without a response"
        return r.id

    @keyword("Log Assertion Result")
    def log_assertion_result(
        self, request_id: str, label: str, status: str, message: str = ""
    ) -> None:
        """Associate an already obtained PASS/FAIL result; does not execute assertions.

        status must be PASS or FAIL. Unknown IDs and SKIP are rejected. This records
        evidence only: a logged FAIL does not change Robot's native test result.
        Use Robot's actual assertion and preserve its failure when obtaining status.

        ```robotframework
        ${status}    ${message}=    Run Keyword And Ignore Error
        ...    Should Be Equal As Integers    ${response.status_code}    200
        Log Assertion Result    ${id}    HTTP status    ${status}    ${message}
        IF    $status == 'FAIL'
            Fail    ${message}
        END
        ```
        """
        r = self._find(request_id)
        if status not in {"PASS", "FAIL"}:
            raise ValueError("Assertion status must be PASS or FAIL")
        r.assertions.append(Assertion(label, status, message))
