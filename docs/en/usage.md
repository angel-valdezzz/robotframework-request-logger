---
tags:
  - Usage
---

# Usage and assertions

```robotframework hl_lines="8 11-13"
*** Settings ***
Library    RequestsLibrary
Library    RequestLogger    mode=summary

*** Test Cases ***
Get distributor
    ${response}=    GET    ${URL}    expected_status=anything    timeout=10
    ${id}=    Log Response    Get distributor    ${response}
    ${status}    ${message}=    Run Keyword And Ignore Error
    ...    Should Be Equal As Integers    ${response.status_code}    200
    Log Assertion Result    ${id}    Expected HTTP status    ${status}    ${message}
    IF    $status == 'FAIL'
        Fail    ${message}
    END
```

GET runs only once. Log Response receives the existing response and also records its
prepared request. Its local ID links the assertions. Run Keyword And Ignore Error
obtains the result without duplicating the assertion; Fail preserves the failure.
You can encapsulate these lines in a business keyword. If you do not want to record
assertions, use Robot's assertions normally: the final test status remains visible.

!!! warning "Recording is not validation"
    Log Assertion Result accepts PASS/FAIL and does not change the test status. Do not
    provide an invented result or omit failure propagation. HTTP 4xx/5xx does not
    necessarily mean FAIL: it may be what your test expects.

## Error without a response

```robotframework hl_lines="9-11 13"
*** Settings ***
Library    RequestsLibrary
Library    RequestLogger

*** Test Cases ***
Call service
    TRY
        ${response}=    GET    ${URL}    timeout=10    expected_status=anything
    EXCEPT    AS    ${error}
        Log Request Error    Call service    GET    ${URL}    ${error}
        Fail    ${error}
    END
    ${id}=    Log Response    Call service    ${response}
```

Output displays No response. It does not fabricate headers, a body, or an HTTP code.
EXCEPT catches call errors; not all of them are timeouts. The library does not intercept HTTP.

## Data protection

Authorization, cookies, API keys, and common credential fields are hidden by default.
You can configure `redact_headers` and `redact_body_fields` when importing the library.
Known values are also hidden in later messages within the test. JSON/text bodies are
preserved in full; binary and multipart bodies are summarized. XML is displayed as
text, without field-specific redaction. Protection only affects this output: it does
not modify Robot or RequestsLibrary logs. HTTP content is not interpreted as Rich
markup, and terminal control sequences are removed.

!!! note "Limitations"
    Only requests.PreparedRequest and requests.Response are supported. Other clients,
    direct Python usage, and pytest/unittest plugins are outside this version's scope.
    Abrupt process termination may lose pending blocks. The library does not write
    HTML or per-test files. Blocks are grouped, but Pabot has no guaranteed global order.

## JSON themes

Use `syntax_theme` to select JSON colors and the block background; HTTP and assertion colors stay unchanged. See [Themes](themes.md) for imports and visual comparisons.

```robotframework hl_lines="2"
*** Settings ***
Library    RequestLogger    mode=full    syntax_theme=monokai
```
