# Robot Framework Request Logger

HTTP request/response logging in the console with Rich. Independent of RequestReporter:
this library sends no HTTP requests and executes no assertions. Robot's console and
exit code remain unchanged. Output is buffered until each test finishes.

[Manual de usuario](https://angel-valdezzz.github.io/robotframework-request-logger/)
· [Keywords](https://angel-valdezzz.github.io/robotframework-request-logger/keywords/)
· [Ejemplos visuales](https://angel-valdezzz.github.io/robotframework-request-logger/console/)

```bash
poetry add robotframework-request-logger
```

```robotframework
*** Settings ***
Library    RequestsLibrary
Library    RequestLogger    mode=summary

*** Test Cases ***
Health
    ${response}=    GET    http://localhost:8000/health    expected_status=anything
    ${id}=    Log Response    Health    ${response}
    Should Be Equal As Integers    ${response.status_code}    200
    Log Assertion Result    ${id}    HTTP status    PASS
```

`mode=summary` shows every exchange briefly; `failures` shows full details of explicitly
failed assertions or request errors; `full` shows every exchange in detail. An HTTP
4xx/5xx response alone does not make a test fail. Assertions accept PASS/FAIL only.

Default operation complements Robot's normal console. For examples showing only this
library, use `poetry run robot --console none tests/visual.robot`. `quiet` still permits
Robot errors and warnings. Native `output.xml`, `log.html` and exit codes are preserved.

## Development

```bash
poetry install
poetry run python scripts/verify.py
poetry run ruff check .
poetry run ruff format .
poetry run robocop check tests
poetry run robocop format tests
poetry run python scripts/build_docs.py
poetry build
```

Known limits: buffering is in memory and output occurs at end_test. Abrupt termination
may lose pending logs. Pabot workers can interleave output; no cross-process ordering
is promised. JSON/text bodies are complete; binary/multipart bodies are summarized.
XML field redaction is not supported. Protection affects this library's output only,
not RequestsLibrary/Robot's own logs. Typer and pytest/unittest integration are outside
this version. Unit tests of implementation use Python's standard test tools.
