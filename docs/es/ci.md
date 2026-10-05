# CI y compatibilidad

La librería imprime bloques estáticos, sin animaciones ni consultas obligatorias a
las dimensiones del terminal. Rich detecta capacidades y utiliza texto sin controles
ANSI cuando la salida está redirigida. El ancho sigue la detección de Rich y su respaldo.

| Entorno | Verificación / configuración |
| --- | --- |
| Linux y Windows | CI ejecuta contratos y suites Robot con stdout redirigido |
| Terminal estrecho | Pruebas de render a 45 columnas |
| CMD / PowerShell / Windows Terminal | Rich detecta capacidades; inspección visual manual pendiente |
| Jenkins | Texto limpio predeterminado; ANSI requiere AnsiColor configurado |
| Azure Pipelines | Texto limpio predeterminado; validación en un pipeline real pendiente |
| Pabot | Bloques por test, sin orden global garantizado; no validado en esta versión |

!!! tip "Colores opcionales en CI compatible con ANSI"
    Puedes usar TTY_COMPATIBLE=1 y TTY_INTERACTIVE=0. No fuerces colores si tu visor
    no interpreta ANSI. Para asegurar texto simple usa TTY_COMPATIBLE=0.

Las imágenes del manual no demuestran compatibilidad visual con todos los terminales.
Los fallos de salida por OSError/UnicodeError se advierten sin cambiar el resultado
del test. La librería no modifica la consola nativa ni los códigos de salida.

## GitHub Actions runners

El job de calidad Linux usa `ubuntu-22.04` como alternativa explícita después de
fallos repetidos al asignar runners con `ubuntu-latest`. Si se cancela antes del
primer paso con “The job was not acquired by Runner”, el fallo es de infraestructura
y no de las pruebas. Revisa por separado la publicación y el workflow de calidad.
Fijar esta imagen no garantiza la disponibilidad de runners.
