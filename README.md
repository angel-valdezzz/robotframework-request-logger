# Robot Framework Request Logger

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="docs/assets/logo-wordmark-dark.svg">
  <img src="docs/assets/logo-wordmark.svg" alt="Request Logger" width="380">
</picture>

**HTTP requests, responses and assertion results in your Robot Framework console, powered by Rich.**

**English** · [Español](README.es.md)

[User guide](https://angel-valdezzz.github.io/robotframework-request-logger/) · [Keyword reference](https://angel-valdezzz.github.io/robotframework-request-logger/keywords/) · [PyPI](https://pypi.org/project/robotframework-request-logger/) · [Visual examples](https://angel-valdezzz.github.io/robotframework-request-logger/console/)

## Features

- Three output modes: `summary`, `failures` and `full`.
- Existing RequestsLibrary requests and responses, linked to recorded assertion results.
- Protection for configured headers, fields and known secrets.
- Static output with terminal detection and plain text fallback for CI.

Output is buffered until each test ends. The library sends no HTTP requests and executes no assertions. It works independently of RequestReporter and preserves Robot's native console, output files and exit code.

## Installation

Python 3.12+ and Robot Framework 7.5+.

```bash
pip install robotframework-request-logger robotframework-requests
# Or, with Poetry:
poetry add robotframework-request-logger robotframework-requests
```

RequestsLibrary is installed separately from this package.

## Quick start

```robotframework
*** Settings ***
Library    RequestsLibrary
Library    RequestLogger    mode=summary

*** Test Cases ***
Health
    ${response}=    GET    http://localhost:8000/health    expected_status=anything
    ${id}=    Log Response    Health    ${response}
    ${status}    ${message}=    Run Keyword And Ignore Error
    ...    Should Be Equal As Integers    ${response.status_code}    200
    Log Assertion Result    ${id}    HTTP status    ${status}    ${message}
    IF    $status == 'FAIL'
        Fail    ${message}
    END
```

Use an available service URL. HTTP 4xx/5xx alone does not fail the test. `Log Assertion Result` records an existing PASS/FAIL result; preserve the actual assertion failure as shown above.

## Configuration and limitations

| Mode | Output |
| --- | --- |
| `summary` | Brief output for every exchange; default |
| `failures` | Full details for explicitly failed assertions or request errors |
| `full` | Full details for every exchange |

Configure `redact_headers` and `redact_body_fields` when importing the library. Protection affects this library's output only; Robot and RequestsLibrary logs remain independent. JSON/text bodies are complete; binary/multipart bodies are summarized. XML field redaction is not supported.

Buffering uses memory; abrupt termination may lose pending logs. Pabot workers can interleave output, with no cross-process ordering guarantee. Direct Python usage and pytest/unittest integrations are outside this version.

## Examples

Keep Robot's normal console for regular execution. To reproduce the visual examples with only this library's console output:

```bash
poetry run robot --console none tests/visual.robot
```

This example intentionally fails and returns exit code 1. [See the real console exports](https://angel-valdezzz.github.io/robotframework-request-logger/console/).

## Development and contribution

```bash
poetry install
poetry run python scripts/verify.py
poetry run ruff check .
poetry run ruff format --check .
poetry run robocop check tests
poetry run python scripts/build_docs.py
poetry build
```

Submit changes through a pull request with passing checks. Update both documentation languages. Libdoc translations live in `docs/translations/es/libdoc.json`; the build rejects missing or outdated entries. Preview the complete site with `python -m http.server 8000 --directory site`.

## License

MIT. See [LICENSE](LICENSE).

## JSON themes

Choose an installed Pygments theme from the import. Default: `monokai`. No theme file is needed. Compare every available style in [Themes](https://angel-valdezzz.github.io/robotframework-request-logger/themes/).

```robotframework
Library    RequestLogger    mode=full    syntax_theme=monokai
```
