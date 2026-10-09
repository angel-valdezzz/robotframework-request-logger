# Request Logger — Pulse visual QA

Source visual truth: `/workspace/scratch/2ffb0fc245da/generated_images/exec-ef1b2023-0811-4ea3-aace-69ebd0bd3b97.png`.
Selected direction: displayed option 3, refined with the authorized transparent SVG identity.
Reference pixels: 1487×1058; comparison target: 1440×1024 CSS pixels, density 1.
Expected state: Spanish home, scroll zero, background paused for comparison.

## Findings

Iteration 1 (CI run 37898049414, head bc7f8e30d403ad733703a4ed8f374aa333191f04):
- [P2] Desktop headline/actions undersized relative to the selected target.
  Evidence: combined full and headline/action captures in qa/logger-ci12.
  Fix: headline 6.45vw (96px cap), subtitle 1.6vw (24px cap), 60px actions,
  250/288px desktop button widths. Responsive overrides remain fitted to viewport.
- [P2] Documentation and Libdoc retained white logo tiles after the home was transparent.
  Evidence: docs-es-header.png and the explicit old logo tile styles.
  Fix: transparent global Material logo presentation; transparent Libdoc brand mark,
  lighter blue supplied SVG variant on dark headers. Adjust home icon to 52px container
  to compensate for the refined vector's more balanced intrinsic margins.

Final implementation captures: `/workspace/scratch/2ffb0fc245da/qa/logger-ci13/`.
Full comparison: `comparison-full.png`.
Focused comparisons: `comparison-headline-actions.png`, `comparison-header.png`.
Browser captures: `es-1440-1024-default.png`, `es-1366-625-default.png`,
`es-390-844-default.png`, `es-820-1180-default.png`, `docs-es-header.png`,
`es-real-console.png`. Source normalized from 1487×1058 to 1440×1024; Chromium
1440×1024 pixels at deviceScaleFactor 1. Source shows Pause; capture is intentionally
paused for a repeatable comparison and shows Resume.

All functional checks passed in iteration 1: EN/ES, four viewports, no overflow,
above-fold actions/cue, motion advance, real pause/resume, reduced-motion changes,
Summary/Failures/Full tabs, search, instant navigation, EN→ES usage page preservation,
dark-theme preservation, synchronized header/tab gradient (<1ms phase difference),
scroll cue focusing content and working links with JavaScript disabled. No page
JavaScript errors. Linux/Windows package and strict bilingual build checks passed
in run 37898049444. The earlier test-only failures were line-length lint and an
ambiguous header/sidebar logo selector; these were corrected without weakening
production behavior.

Iteration 2 (head 0e0e78c911c67e3e312ed586f99d690abf6bbc8b): both P2 findings
resolved and visually confirmed in full, headline/actions, header and background
comparisons, plus mobile, tablet, short desktop and documentation captures.
The same functional checks passed again in run 37898551385; package, strict
bilingual build, navigation, Libdoc and Windows checks passed in run 37898551371.
No remaining P0/P1/P2 findings. P3 differences are the generated field's slightly
brighter lime and native Material glyphs replacing illustrative glyphs; the
composition and product palette match the approved direction. The precise refined
SVG geometry is an intentional, explicitly authorized identity update.

## Required fidelity surfaces

- Fonts/typography: locally hosted, OFL-licensed Inter regular/bold; editable white/lime headline.
- Spacing/layout: full viewport hero, transparent header, calls to action above the fold, scroll cue.
- Colors/tokens: original blue/deep-blue/lime identity; homepage appearance independent of docs theme.
- Image quality: generated raster pulse field; supplied SVG logo refined per explicit user instruction.
  Logo rows use consistent thickness/radius and progressively shorter lengths; alpha confirmed.
- Copy/content: exact selected Spanish hero copy, translated English; genuine Rich exports below hero.

## Implementation checklist

- [x] Refine selected target and supplied vector identity.
- [x] Implement raster background, accessible motion, native search and transparent header.
- [x] Expose actual Summary/Failures/Full console exports below the hero.
- [x] Pass CI browser checks, inspect captures and combined comparison.
- [ ] Verify published page and save final public evidence.

final result: passed
