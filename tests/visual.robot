*** Settings ***
Library           RequestsLibrary
Library           RequestLogger    mode=${MODE}
Library           Fixture.py

Suite Setup       Start fixture
Suite Teardown    Stop API


*** Variables ***
${MODE}    summary


*** Test Cases ***
Validate distributor
    ${health}=    GET    ${BASE_URL}/health    expected_status=anything    timeout=2
    ${health_id}=    Log Response    Health check    ${health}
    Should Be Equal As Integers    ${health.status_code}    200
    Log Assertion Result    ${health_id}    Health status    PASS
    VAR    &{headers}    Authorization=Bearer fake-secret-TOKEN
    ${response}=    GET    url=${BASE_URL}/distributor?tag=one&tag=two&api_key=fake-query-SECRET
    ...    headers=${headers}    expected_status=anything    timeout=2
    ${id}=    Log Response    Consult distributor    ${response}
    Should Be Equal As Integers    ${response.status_code}    200
    Log Assertion Result    ${id}    HTTP status    PASS
    VAR    ${body}    ${response.json()}
    ${status}    ${message}=    Run Keyword And Ignore Error
    ...    Should Not Be Empty    ${body}[rfc]
    Log Assertion Result    ${id}    RFC must contain a value    ${status}    ${message}
    IF    $status == 'FAIL'    Fail    ${message}


*** Keywords ***
Start fixture
    ${url}=    Start API
    VAR    ${BASE_URL}    ${url}    scope=SUITE
