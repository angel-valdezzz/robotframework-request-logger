# Desarrollo y publicación

Poetry gestiona dependencias y genera WHL/sdist. Ruff verifica Python, RoboCop Robot
y mypy los tipos de la implementación. CI ejecuta pruebas reales con una API local,
pruebas de protección/render y aceptación del WHL en un entorno limpio.

```bash
poetry install
poetry run python scripts/verify.py
poetry run python scripts/build_docs.py
poetry build
poetry run twine check dist/*
```

build_docs genera Libdoc y los ejemplos SVG desde tests/visual.robot y después MkDocs
estricto. Pages publica un sitio con manual, referencia y ejemplos visuales.

Las entregas entran por PR a main con CI correcto. release.yml valida tag y ascendencia
respecto a main. PyPI utiliza Trusted Publishing con repository
robotframework-request-logger, workflow release.yml y environment pypi; no utiliza tokens
permanentes. Configurar el publisher es un paso previo a la primera publicación.

## Mantener los dos idiomas de documentación

El inglés vive en `docs/en/` y se publica por defecto en la raíz del sitio.
El contenido en español vive en `docs/es/` y se publica bajo `/es/`. Los enlaces anteriores
de `/en/` redirigen a sus páginas equivalentes en la raíz. Las dos configuraciones heredan
los estilos y el selector de idiomas de `mkdocs.base.yml`.

Al modificar una guía, actualiza su equivalente en el otro idioma y conserva los mismos
nombres de archivo para que el selector mantenga la página actual. Los nombres reales
de keywords, parámetros y comandos se conservan. Las exportaciones de consola se comparten entre ambos idiomas. Libdoc genera
una referencia con descripciones en inglés y otra en español.

Ejecuta `poetry run python scripts/build_docs.py` para construir el sitio bilingüe completo.
Para una vista previa local después de construir, ejecuta
`poetry run python -m http.server 8000 --directory site` y abre
`http://localhost:8000/` o `http://localhost:8000/es/`. El selector utiliza las URLs de
producción, así que verifica sus enlaces también en GitHub Pages.

Las traducciones de Libdoc viven en `docs/translations/es/libdoc.json`. Cada entrada
conserva el SHA-256 del texto original; la compilación rechaza traducciones faltantes
o desactualizadas. Los nombres de keywords, argumentos, tipos y valores por defecto
se mantienen iguales. El selector nativo de Libdoc cambia los controles y las descripciones de keywords.
