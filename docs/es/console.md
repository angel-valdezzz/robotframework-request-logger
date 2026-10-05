# Modos y ejemplos visuales

Estas imágenes son **exportaciones SVG de Rich desde ejecuciones reales de Robot**
con una API HTTP local, datos ficticios y `--console none`. No son capturas de una
ventana de CMD/PowerShell: reproducen la salida real con ancho fijo de 100 columnas.
La tipografía y los colores finales pueden variar según tu terminal.

=== "Summary"

    Método, URL protegida, status, duración y resultados registrados.

    ```bash
    poetry run robot --console none --variable MODE:summary tests/visual.robot
    ```

    ![Consola Summary](assets/console-summary.svg)

    [Salida de texto completa](assets/console-summary.txt)

=== "Failures"

    Detalle completo de intercambios con assertions FAIL o errores registrados.
    Un 404 esperado con assertion PASS no aparece por el código HTTP solamente.

    ```bash
    poetry run robot --console none --variable MODE:failures tests/visual.robot
    ```

    ![Consola Failures](assets/console-failures.svg)

    [Salida de texto completa](assets/console-failures.txt)

=== "Full"

    Todos los intercambios: params repetidos, headers y bodies completos.

    ```bash
    poetry run robot --console none --variable MODE:full tests/visual.robot
    ```

    ![Consola Full](assets/console-full.svg)

    [Salida de texto completa](assets/console-full.txt)

!!! note "El ejemplo falla intencionalmente"
    Primero se registra un health check aprobado; después el servicio devuelve HTTP 200 y un RFC vacío. El test registra una assertion PASS
    para el status y una FAIL para el RFC; luego propaga el fallo. El código de salida
    de Robot es 1. El código reproducible está en tests/visual.robot del repositorio.

## Conservar la consola de Robot

```bash
poetry run robot --variable MODE:summary tests/visual.robot
```

Esta es la forma habitual. No necesitamos quiet/none para funcionar. `--console quiet`
reduce la salida de Robot pero conserva sus errores/advertencias. `--console none`
suprime su consola, no output.xml/log.html/report.html ni sus códigos de salida.
Otras librerías todavía pueden imprimir directamente. RequestLogger también muestra
el mensaje nativo final de FAIL/SKIP, incluso si el caso falló antes de registrar HTTP.

Compara las paletas JSON en el apartado [Temas](themes.md).
