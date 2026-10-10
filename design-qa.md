# Request Logger — From exchange to diagnosis

Approved visual reference: the interactive diagnostic demo, including the compact
console destination and neutral fictional book case. The original transparent
SVG logo and blue/navy/lime identity are retained.

The cover follows the actual API exchange: protected GET, HTTP 200 with an empty
title, an assertion recorded as FAIL, and output emitted when the test closes.
Request Logger does not make requests or evaluate assertions itself. The final
console fragment is extracted from the same genuine Summary execution as the
console export below the cover. The test case is downloadable.

## Validation

`docs/scripts/verify_landing.py` checks English and Spanish at 1440×1024,
1366×625, 820×1180, 390×844, and 320×740. Screenshots are generated in
`build/landing-checks/` and uploaded by the Animated documentation workflow.

The Chromium checks cover viewport overflow, visible primary actions, separated
language/search controls, transparent cover header, console text containment,
all three real console tabs, continuous looping, pause/resume, no hover pause,
reduced motion, no-JavaScript output, native search, instant navigation,
page/theme preservation on language changes, and synchronized documentation
header/tab gradient phases.

The laptop layout uses tighter spacing so the console and scroll cue fit in a
625px-high viewport. The mobile layout stacks the stages and permits natural
vertical scrolling; primary actions remain visible on the first screen.
The Material logo remains visible at tablet and mobile widths.

The regular quality workflow additionally verifies the library, expected Robot
failure propagation, secret protection, bilingual strict builds, Libdoc,
translation links, theme gallery, formatting, package and wheel integrity.
