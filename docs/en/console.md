# Modes and visual examples

These images are **Rich SVG exports from real Robot executions** using a local HTTP
API, fictitious data, and `--console none`. They are not screenshots of a CMD/PowerShell
window: they reproduce actual output at a fixed width of 100 columns.
The final font and colors may vary depending on your terminal.

=== "Summary"

    Method, protected URL, status, duration, and recorded results.

    ```bash
    poetry run robot --console none --variable MODE:summary tests/visual.robot
    ```

    ![Summary console](assets/console-summary.svg)

    [Complete text output](assets/console-summary.txt)

=== "Failures"

    Full details for exchanges with FAIL assertions or recorded errors.
    An expected 404 with a PASS assertion does not appear solely because of its HTTP code.

    ```bash
    poetry run robot --console none --variable MODE:failures tests/visual.robot
    ```

    ![Failures console](assets/console-failures.svg)

    [Complete text output](assets/console-failures.txt)

=== "Full"

    All exchanges: repeated params, headers, and complete bodies.

    ```bash
    poetry run robot --console none --variable MODE:full tests/visual.robot
    ```

    ![Full console](assets/console-full.svg)

    [Complete text output](assets/console-full.txt)

!!! note "The example fails intentionally"
    A passing health check is recorded first; then the service returns HTTP 200 and an
    empty RFC. The test records a PASS assertion for the status and a FAIL assertion
    for the RFC, then propagates the failure. Robot's exit code is 1.
    The reproducible source is tests/visual.robot in the repository.

## Keep Robot's console

```bash
poetry run robot --variable MODE:summary tests/visual.robot
```

This is the usual approach. The library works without quiet/none. `--console quiet`
reduces Robot output but keeps its errors and warnings. `--console none` suppresses
its console, without suppressing output.xml/log.html/report.html or changing exit codes.
Other libraries can still print directly. RequestLogger also displays the final native
FAIL/SKIP message, even when the test failed before recording HTTP traffic.

Compare JSON palettes separately in [Themes](themes.md).
