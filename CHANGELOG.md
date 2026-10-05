# Changelog

## 0.2.0 — Unreleased

### Added

- `syntax_theme` import argument for installed Pygments themes and Rich's ANSI themes.
- English and Spanish Themes galleries with matching response previews and imports.
- Reproducible theme previews generated from the production renderer.

### Fixed

- Integrate the Themes gallery into the manual layout, use native code-copy controls and preserve Robot Framework syntax highlighting for every import. Show direct image links only on preview errors.

- Pin the Linux quality job to Ubuntu 22.04 after repeated hosted runner allocation failures on ubuntu-latest.

- Themes documentation now uses a searchable selector with Previous/Next controls, preview and copyable import instead of a tab row limited to 20 visible panels.

### Changed

- JSON uses themed syntax highlighting with the theme's block background (default: monokai).
- Softer neutral borders and labeled separators for populated detail sections and assertions.
- Empty headers and bodies are omitted from full details.

HTTP/assertion colors, console modes, secret protection and Robot results are preserved.
