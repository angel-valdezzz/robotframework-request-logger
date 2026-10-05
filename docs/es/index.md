<div class="hero" markdown>

# HTTP visible en tu consola

**RequestLogger** complementa la ejecución de Robot con requests, responses y assertions
registradas. No ejecuta servicios, no valida datos y no depende de RequestReporter.

[Primer uso](usage.md){ .md-button .md-button--primary }
[Ver consola](console.md){ .md-button }
[Keywords](keywords/index.html){ .md-button }

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
