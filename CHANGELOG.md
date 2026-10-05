# Changelog

## 0.2.0 — Unreleased

### Added

- `syntax_theme` import argument for installed Pygments themes and Rich's ANSI themes.
- English and Spanish Themes galleries with matching response previews and imports.
- Reproducible theme previews generated from the production renderer.

### Fixed

- Themes documentation now uses a searchable selector with Previous/Next controls, preview and copyable import instead of a tab row limited to 20 visible panels.

### Changed

- JSON uses themed syntax highlighting with the theme's block background (default: monokai).
- Softer neutral borders and labeled separators for populated detail sections and assertions.
- Empty headers and bodies are omitted from full details.

HTTP/assertion colors, console modes, secret protection and Robot results are preserved.
