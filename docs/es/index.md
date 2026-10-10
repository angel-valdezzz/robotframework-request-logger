---
template: home.html
title: Request Logger
description: Peticiones, respuestas y validaciones en tu consola de Robot.
---

<div id="overview"></div>

## Elige cuánto quieres ver

<div class="grid cards" markdown>

- **Summary**

    Una vista compacta de cada intercambio.

- **Failures**

    Enfócate en operaciones asociadas con fallos registrados.

- **Full**

    Lee headers y cuerpos protegidos con resaltado JSON.

</div>

```bash
poetry add robotframework-request-logger
```

!!! tip "Empieza sencillo"
    `mode=summary` es el valor predeterminado. Conserva la consola habitual de Robot;
    no necesitas cambiar el comando de ejecución.

<section class="er-real-console" id="console-preview" tabindex="-1" markdown>

## La consola, tal como se genera

Estas imágenes son exportaciones SVG de Rich desde las pruebas ejecutables del proyecto. El caso ficticio de un libro devuelve HTTP 200 con el título vacío; la prueba registra el fallo de esa validación. Cada pestaña muestra la salida real.

=== "Summary"

    ![Request Logger · Summary](assets/console-summary.svg)

=== "Failures"

    ![Request Logger · Failures](assets/console-failures.svg)

=== "Full"

    ![Request Logger · Full](assets/console-full.svg)

[Ver cómo reproducir estas salidas](console.md) · [Descargar el caso de prueba](assets/book-example.zip){ download }

</section>

La impresión ocurre al cerrar el test. El buffering permite filtrar fallos y aplicar
secretos conocidos durante todo el caso antes de emitir cualquier bloque.

## Sigue el intercambio

```mermaid
flowchart TD
    A[RequestsLibrary] --> B[Log Response]
    B --> C[Log Assertion Result]
    C --> D[Console]
```

[Explora los temas de JSON](themes.md){ data-preview }
