---
template: home.html
title: Request Logger
description: Lleva peticiones HTTP, respuestas y validaciones registradas a la consola de Robot. Lee el resultado sin salir de tu ejecución.
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

![Resumen de consola generado desde una ejecución real](assets/console-summary.svg)

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
