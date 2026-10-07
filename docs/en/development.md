---
tags:
  - Development
---

# Development and publishing

Poetry manages dependencies and builds WHL/sdist distributions. Ruff checks Python,
RoboCop checks Robot, and mypy checks implementation types. CI runs real tests using a
local API, protection/rendering tests, and WHL acceptance in a clean environment.

```bash
poetry install
poetry run python scripts/verify.py
poetry run python docs/scripts/build_docs.py
poetry build
poetry run twine check dist/*
```

build_docs generates Libdoc and SVG examples from tests/visual.robot, then builds both
Spanish and English documentation in strict mode. Pages publishes a single site
containing the manual, reference, and visual examples.

Changes enter main through a PR with passing CI. release.yml validates the tag and its
ancestry from main. PyPI uses Trusted Publishing with repository
robotframework-request-logger, workflow release.yml, and environment pypi; it does not
use permanent tokens. Configure the publisher before the first release.

## Maintain both documentation languages

The English source lives in `docs/en/` and is published at the site root by default.
Spanish lives in `docs/es/` and is published under `/es/`. Existing `/en/` page links
redirect to their English counterparts at the root. Both configurations inherit
shared styles and the language selector from `docs/config/base.yml`.

When changing a guide, update its counterpart in the other language and keep matching
filenames so the selector can retain the current page. Keep actual keyword names,
parameters, and commands unchanged. Console exports are shared. Libdoc descriptions are translated using
`docs/translations/es/libdoc.json`; builds reject missing or outdated entries.
Keep keyword names, argument names, types and defaults unchanged.

Run `poetry run python docs/scripts/build_docs.py` to build the complete bilingual site.
For a local preview after building, run `poetry run python -m http.server 8000 --directory site`
and open `http://localhost:8000/` or `http://localhost:8000/es/`. The selector uses
production URLs, so verify its links on GitHub Pages as well.
