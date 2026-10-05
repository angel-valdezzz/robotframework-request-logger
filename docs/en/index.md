# HTTP visibility in your console

**RequestLogger** complements Robot execution with recorded requests, responses, and
assertion results. It does not call services, validate data, or depend on RequestReporter.

[Get started](usage.md){ .md-button .md-button--primary }
[View console output](console.md){ .md-button }
[Keywords](keywords/index.html){ .md-button }

```bash
poetry add robotframework-request-logger
```

!!! tip "Start simple"
    `mode=summary` is the default. Keep Robot's usual console;
    you do not need to change your execution command.

![Console summary generated from a real execution](assets/console-summary.svg)

Output is printed when the test ends. Buffering allows failure filtering and applies
known secrets across the entire test before any block is printed.
