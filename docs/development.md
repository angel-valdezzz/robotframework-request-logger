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
