"""Generate translated Libdoc without changing the executable keyword interface."""

import copy
import hashlib
import html
import json
from pathlib import Path

from robot.libdocpkg import LibraryDocumentation


def generate(library: str, root: Path, relative: str, site_url: str) -> None:
    original = LibraryDocumentation(library)
    translated = copy.deepcopy(original)
    catalog = json.loads((root / "docs/translations/es/libdoc.json").read_text(encoding="utf-8"))
    entries = {"introduction": (original, translated)}
    entries.update(
        {f"init:{a.name}": (a, b) for a, b in zip(original.inits, translated.inits, strict=True)}
    )
    entries.update(
        {
            f"keyword:{a.name}": (a, b)
            for a, b in zip(original.keywords, translated.keywords, strict=True)
        }
    )
    if set(entries) != set(catalog):
        raise ValueError(f"Libdoc translation keys differ: {set(entries) ^ set(catalog)}")
    for key, (source, target) in entries.items():
        entry = catalog[key]
        digest = hashlib.sha256(source.doc.encode("utf-8")).hexdigest()
        if entry["source_sha256"] != digest or not entry["text"].strip():
            raise ValueError(f"Missing or outdated Libdoc translation: {key}")
        target.doc = entry["text"]
    base = site_url.rstrip("/") + "/"
    for language, model in [("en", original), ("es", translated)]:
        output = root / "docs" / language / relative
        output.parent.mkdir(parents=True, exist_ok=True)
        model.convert_docs_to_html()
        model.doc = (
            '<p aria-label="Documentation language">'
            f'<a href="{html.escape(base + relative)}">English</a> · '
            f'<a href="{html.escape(base + "es/" + relative)}">Español</a>'
            "</p>" + model.doc
        )
        model.save(str(output), format="HTML")
