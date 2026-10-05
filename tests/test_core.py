"""Meaningful contract tests; no real network or dependency on the HTML reporter."""

import io
import unittest
from datetime import timedelta
from types import SimpleNamespace
from unittest.mock import patch

import requests
from rich.console import Console

from request_logger import RequestLogger
from request_logger.protection import Protector, safe_text
from request_logger.theme import available_themes


def response(status: int = 200) -> requests.Response:
    r = requests.Response()
    r.status_code = status
    r.request = requests.Request(
        "POST",
        "https://example.test/?tag=a&tag=b&api_key=secret-QUERY",
        headers={"Authorization": "Bearer secret-TOKEN"},
        json={"password": "secret-PASSWORD", "text": "[bold]literal[/bold]"},
    ).prepare()
    r.headers["Content-Type"] = "application/json"
    r._content = b'{"access_token":"secret-TOKEN","message":"OK"}'
    r.elapsed = timedelta(milliseconds=12)
    return r


class CoreTests(unittest.TestCase):
    def render(self, lib: RequestLogger, result: str = "PASS", width: int = 45) -> str:
        out = io.StringIO()
        with patch(
            "request_logger.Console",
            return_value=Console(
                file=out, width=width, force_terminal=False, force_interactive=False
            ),
        ):
            lib.end_test(None, SimpleNamespace(status=result, message="native result"))
        return out.getvalue()

    def test_complete_safe_output(self) -> None:
        lib = RequestLogger("full")
        lib.start_test(None, None)
        r = response()
        rid = lib.log_request("Prepared", r.request)
        self.assertEqual(lib.log_response("Response", r), rid)
        self.assertEqual(len(lib.records), 1)
        lib.log_assertion_result(rid, "Expected status", "PASS")
        text = self.render(lib)
        for secret in ("secret-QUERY", "secret-TOKEN", "secret-PASSWORD"):
            self.assertNotIn(secret, text)
        self.assertIn("[bold]literal[/bold]", text)
        self.assertIn("Params", text)
        self.assertNotIn("\x1b", text)
        self.assertFalse(lib.active)

    def test_all_themes_preserve_protected_plain_output(self) -> None:
        expected = None
        for theme in available_themes():
            with self.subTest(theme=theme):
                lib = RequestLogger("full", syntax_theme=theme)
                lib.start_test(None, None)
                lib.log_response("Themed", response())
                text = self.render(lib, width=100)
                for secret in ("secret-QUERY", "secret-TOKEN", "secret-PASSWORD"):
                    self.assertNotIn(secret, text)
                self.assertNotIn("\x1b", text)
                if expected is None:
                    expected = text
                self.assertEqual(text, expected)

    def test_unknown_theme_fails_at_import(self) -> None:
        with self.assertRaisesRegex(ValueError, "Unknown syntax_theme.*Available themes"):
            RequestLogger(syntax_theme="not-a-theme")
        self.assertEqual(RequestLogger().theme.syntax_theme, "monokai")

    def test_empty_sections_omitted_and_text_body_preserved(self) -> None:
        lib = RequestLogger("full", syntax_theme="github-dark")
        lib.start_test(None, None)
        r = response()
        r.request = requests.Request("GET", "https://example.test/").prepare()
        r.headers.clear()
        r.headers["Content-Type"] = "text/plain"
        r._content = b"literal [bold]text[/bold]"
        lib.log_response("Text", r)
        text = self.render(lib, width=100)
        self.assertNotIn("Request body", text)
        self.assertNotIn("Request headers", text)
        self.assertIn("Response body", text)
        self.assertIn("literal [bold]text[/bold]", text)
        lib.start_test(None, None)
        r._content = b""
        lib.log_response("Empty", r)
        self.assertNotIn("Response body", self.render(lib))

    def test_failures_use_assertions_not_http_code(self) -> None:
        lib = RequestLogger("failures")
        lib.start_test(None, None)
        rid = lib.log_response("Expected404", response(404))
        lib.log_assertion_result(rid, "Expected error", "PASS")
        self.assertEqual(self.render(lib), "")
        lib.start_test(None, None)
        rid = lib.log_response("Invalid200", response())
        lib.log_assertion_result(rid, "Invalid content", "FAIL", "Missing RFC")
        self.assertIn("Missing RFC", self.render(lib, "FAIL"))

    def test_timeout_no_fabricated_response(self) -> None:
        lib = RequestLogger("full")
        lib.start_test(None, None)
        lib.log_request_error(
            "Timeout", "GET", "https://example.test/?api_key=secret-QUERY", "Timeout secret-QUERY"
        )
        text = self.render(lib, "FAIL")
        self.assertIn("No response", text)
        self.assertNotIn("Response body", text)
        self.assertNotIn("secret-QUERY", text)

    def test_case_isolation_and_validation(self) -> None:
        with self.assertRaises(ValueError):
            RequestLogger("unknown")
        lib = RequestLogger()
        with self.assertRaises(RuntimeError):
            lib.log_response("Outside", response())
        lib.start_test(None, None)
        rid = lib.log_response("One", response())
        with self.assertRaises(ValueError):
            lib.log_assertion_result(rid, "Skip forbidden", "SKIP")
        lib.end_test(None, SimpleNamespace(status="PASS", message=""))
        lib.start_test(None, None)
        with self.assertRaises(ValueError):
            lib.log_assertion_result(rid, "Old ID", "PASS")

    def test_terminal_injection_and_form_duplicates(self) -> None:
        self.assertEqual(safe_text("ok\x1b[31mRED\x1b[0m\x1b]0;title\x07"), "okRED")
        p = Protector("Authorization", "password")
        form = p.body("tag=a&tag=b&password=secret&empty=", "application/x-www-form-urlencoded")
        self.assertEqual(len(form), 4)
        self.assertNotIn("secret", str(form))

    def test_unlinked_failure_and_skip_visible(self) -> None:
        lib = RequestLogger("failures")
        lib.start_test(None, None)
        self.assertIn("Robot FAIL", self.render(lib, "FAIL"))
        lib.start_test(None, None)
        self.assertIn("Robot SKIP", self.render(lib, "SKIP"))


if __name__ == "__main__":
    unittest.main()
