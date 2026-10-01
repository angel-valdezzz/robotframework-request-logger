*** Settings ***
Library           RequestsLibrary
Library           RequestLogger
Library           Fixture.py

Suite Setup       Start fixture
Suite Teardown    Stop API


*** Test Cases ***
Transport timeout
    TRY
        GET    url=${BASE_URL}/slow?api_key=fake-query-SECRET    timeout=0.01
    EXCEPT    AS    ${error}
        Log Request Error    Slow operation    GET
        ...    url=${BASE_URL}/slow?api_key=fake-query-SECRET    message=${error}
        Fail    ${error}
    END

Failure before logging
    Fail    Native failure still visible

Expected HTTP error
    ${response}=    GET    ${BASE_URL}/missing    expected_status=anything
    ${id}=    Log Request    Expected missing    ${response.request}
    ${same_id}=    Log Response    Expected missing    ${response}
    Should Be Equal    ${same_id}    ${id}
    Should Be Equal As Integers    ${response.status_code}    404
    Log Assertion Result    ${id}    Expected 404    PASS

Skipped test
    Skip    Not part of this example


*** Keywords ***
Start fixture
    ${url}=    Start API
    VAR    ${BASE_URL}    ${url}    scope=SUITE
