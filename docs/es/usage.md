# Uso y assertions

```robotframework
*** Settings ***
Library    RequestsLibrary
Library    RequestLogger    mode=summary

*** Test Cases ***
Consultar distribuidor
    ${response}=    GET    ${URL}    expected_status=anything    timeout=10
    ${id}=    Log Response    Consultar distribuidor    ${response}
    ${status}    ${message}=    Run Keyword And Ignore Error
    ...    Should Be Equal As Integers    ${response.status_code}    200
    Log Assertion Result    ${id}    HTTP esperado    ${status}    ${message}
    IF    $status == 'FAIL'
        Fail    ${message}
    END
```

El GET se ejecuta una sola vez. Log Response recibe la response ya existente y también
registra su request preparada. Su ID local vincula las assertions. Run Keyword And
Ignore Error obtiene el resultado sin duplicar la assertion; Fail conserva su fallo.
Puedes encapsular estas líneas en una keyword de negocio. Si no quieres registrar
assertions, usa las de Robot normalmente: el estado final del caso sigue siendo visible.

!!! warning "Registrar no es validar"
    Log Assertion Result acepta PASS/FAIL y no cambia el estado del test. No pases un
    resultado inventado ni ignores la propagación del fallo. HTTP 4xx/5xx no significa
    necesariamente FAIL: puede ser lo que tu prueba espera.

## Error sin response

```robotframework
*** Settings ***
Library    RequestsLibrary
Library    RequestLogger

*** Test Cases ***
Consultar servicio
    TRY
        ${response}=    GET    ${URL}    timeout=10    expected_status=anything
    EXCEPT    AS    ${error}
        Log Request Error    Consultar servicio    GET    ${URL}    ${error}
        Fail    ${error}
    END
    ${id}=    Log Response    Consultar servicio    ${response}
```

La salida indica No response. No fabrica headers, body ni código HTTP. El EXCEPT
captura errores de la llamada; no todos son timeouts. La librería no intercepta HTTP.

## Protección de datos

Authorization, cookies, API keys y campos habituales de credenciales se ocultan por
defecto. Puedes configurar `redact_headers` y `redact_body_fields` en el import.
Los valores conocidos también se ocultan en mensajes posteriores del caso. Los bodies
JSON/texto se conservan completos; binarios y multipart se resumen. XML se presenta
como texto, sin ocultación específica de sus campos. La protección solo afecta a esta
salida: no modifica los logs de Robot o RequestsLibrary. El contenido HTTP no se
interpreta como markup Rich y se eliminan secuencias de control del terminal.

!!! note "Límites"
    Solo admite requests.PreparedRequest y requests.Response. Otros clientes, Python
    directo y plugins pytest/unittest no forman parte de esta versión. Una terminación
    abrupta del proceso puede perder bloques pendientes. No escribe HTML ni archivos
    por test. Los bloques se agrupan, pero Pabot no tiene orden global garantizado.

## Temas del JSON

Usa `syntax_theme` para elegir los colores y el fondo del bloque JSON; los colores HTTP y de assertions se conservan. Consulta [Temas](themes.md) para comparar e importar cada tema.

```robotframework
Library    RequestLogger    mode=full    syntax_theme=monokai
```
