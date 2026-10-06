# Robot Framework Request Logger

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="docs/assets/logo-wordmark-dark.svg">
  <img src="docs/assets/logo-wordmark.svg" alt="Request Logger" width="380">
</picture>

**Requests HTTP, responses y resultados de assertions en la consola de Robot Framework, con Rich.**

[English](README.md) · **Español**

[Manual de usuario](https://angel-valdezzz.github.io/robotframework-request-logger/es/) · [Referencia de keywords](https://angel-valdezzz.github.io/robotframework-request-logger/es/keywords/) · [PyPI](https://pypi.org/project/robotframework-request-logger/) · [Ejemplos visuales](https://angel-valdezzz.github.io/robotframework-request-logger/es/console/)


[![PyPI](https://img.shields.io/pypi/v/robotframework-request-logger?logo=pypi)](https://pypi.org/project/robotframework-request-logger/)
![Python](https://img.shields.io/pypi/pyversions/robotframework-request-logger?logo=python)
![Robot Framework](https://img.shields.io/badge/Robot_Framework-compatible-00A6A6?logo=robotframework)
[![License](https://img.shields.io/github/license/angel-valdezzz/robotframework-request-logger)](LICENSE)
[![CI](https://github.com/angel-valdezzz/robotframework-request-logger/actions/workflows/ci.yml/badge.svg)](https://github.com/angel-valdezzz/robotframework-request-logger/actions/workflows/ci.yml)

## Funcionalidades

- Tres modos de salida: `summary`, `failures` y `full`.
- Requests y responses existentes de RequestsLibrary, vinculados con los resultados de assertions registrados.
- Protección de headers, campos configurados y secretos conocidos.
- Salida estática con detección del terminal y alternativa de texto plano para CI.

La salida se guarda en memoria hasta terminar cada caso. La biblioteca no envía requests HTTP ni ejecuta assertions. Funciona independientemente de RequestReporter y conserva la consola, archivos de salida y código de retorno nativos de Robot.

## Instalación

Python 3.12+ y Robot Framework 7.5+.

```bash
pip install robotframework-request-logger robotframework-requests
# O con Poetry:
poetry add robotframework-request-logger robotframework-requests
```

RequestsLibrary se instala por separado de este paquete.

## Uso rápido

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

Utiliza la URL de un servicio disponible. Un HTTP 4xx/5xx por sí solo no falla el caso. `Log Assertion Result` registra un resultado PASS/FAIL existente; conserva el fallo real de la assertion como muestra el ejemplo.

## Configuración y limitaciones

| Modo | Salida |
| --- | --- |
| `summary` | Salida breve de cada intercambio; predeterminado |
| `failures` | Detalles completos de assertions fallidas explícitamente o errores de request |
| `full` | Detalles completos de cada intercambio |

Configura `redact_headers` y `redact_body_fields` al importar la biblioteca. La protección solo afecta esta salida; los logs de Robot y RequestsLibrary son independientes. Los cuerpos JSON/texto se conservan completos; los binarios/multipart se resumen. No se admite ocultar campos XML.

El almacenamiento temporal usa memoria; una terminación abrupta puede perder logs pendientes. Los procesos de Pabot pueden intercalar su salida, sin orden global garantizado. El uso directo desde Python y las integraciones con pytest/unittest quedan fuera de esta versión.

## Ejemplos

Conserva la consola normal de Robot para ejecuciones habituales. Para reproducir los ejemplos visuales mostrando únicamente la salida de esta biblioteca:

```bash
poetry run robot --console none tests/visual.robot
```

Este ejemplo falla deliberadamente y devuelve el código 1. [Consulta las exportaciones reales de consola](https://angel-valdezzz.github.io/robotframework-request-logger/es/console/).

## Desarrollo y contribución

```bash
poetry install
poetry run python scripts/verify.py
poetry run ruff check .
poetry run ruff format --check .
poetry run robocop check tests
poetry run python docs/scripts/build_docs.py
poetry build
```

Envía los cambios mediante un pull request con las verificaciones aprobadas. Actualiza ambos idiomas. Las traducciones de Libdoc están en `docs/translations/es/libdoc.json`; la compilación rechaza entradas faltantes o desactualizadas. Para una vista previa del sitio completo ejecuta `python -m http.server 8000 --directory site`.

## Licencia

MIT. Consulta [LICENSE](LICENSE).

## Temas del JSON

Elige un tema instalado de Pygments desde el import. Predeterminado: `monokai`. No necesitas un archivo. Compara los temas en [Temas](https://angel-valdezzz.github.io/robotframework-request-logger/es/themes/).

```robotframework
Library    RequestLogger    mode=full    syntax_theme=monokai
```
