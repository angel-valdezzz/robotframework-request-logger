---
tags:
  - Usage
---

# CI and compatibility

The library prints static blocks without animations or mandatory terminal-size queries.
Rich detects terminal capabilities and uses text without ANSI controls when output is
redirected. Width follows Rich's detection and fallback.

| Environment | Verification / configuration |
| --- | --- |
| Linux and Windows | CI runs contract tests and Robot suites with redirected stdout |
| Narrow terminal | Rendering tests at 45 columns |
| CMD / PowerShell / Windows Terminal | Rich detects capabilities; manual visual inspection is pending |
| Jenkins | Plain text by default; ANSI requires AnsiColor configuration |
| Azure Pipelines | Plain text by default; validation in a real pipeline is pending |
| Pabot | Blocks per test, without guaranteed global ordering; not validated in this version |

!!! tip "Optional colors in ANSI-compatible CI"
    You can use TTY_COMPATIBLE=1 and TTY_INTERACTIVE=0. Do not force colors if your
    viewer cannot interpret ANSI. Use TTY_COMPATIBLE=0 to ensure plain text.

The manual's images do not establish visual compatibility with every terminal.
Output failures caused by OSError/UnicodeError produce warnings without changing the
result of the test. The library does not alter the native console or exit codes.

## GitHub Actions runners

The Linux quality job uses `ubuntu-22.04` as an explicit alternative after repeated
runner allocation failures on `ubuntu-latest`. A job cancelled before its first step
with “The job was not acquired by Runner” indicates a hosted infrastructure failure,
not a test failure. Check deployment and quality workflows separately. This pinned
image does not guarantee runner availability.
