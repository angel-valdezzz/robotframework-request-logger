"""Verify real Robot output plus pure rendering and protection contracts."""

import os
import subprocess
import sys
from pathlib import Path

from robot.api import ExecutionResult
from robot.libdocpkg import LibraryDocumentation

ROOT = Path(__file__).resolve().parents[1]


def main() -> None:
    subprocess.run(
        [sys.executable, "-m", "unittest", "discover", "-s", "tests", "-p", "test_*.py"],
        cwd=ROOT,
        check=True,
    )
    keywords = {k.name for k in LibraryDocumentation("RequestLogger").keywords}
    assert keywords == {"Log Request", "Log Response", "Log Request Error", "Log Assertion Result"}
    output = ROOT / "results"
    output.mkdir(exist_ok=True)
    for mode in ("summary", "failures", "full"):
        directory = output / mode
        command = [
            sys.executable,
            "-m",
            "robot",
            "--console",
            "none",
            "--outputdir",
            str(directory),
            "--variable",
            f"MODE:{mode}",
            str(ROOT / "tests" / "visual.robot"),
        ]
        process = subprocess.run(
            command,
            cwd=ROOT,
            capture_output=True,
            text=True,
            encoding="utf-8",
            env={**os.environ, "PYTHONUTF8": "1", "TTY_COMPATIBLE": "0"},
        )
        assert process.returncode == 1, process.stderr
        assert "Consult distributor" in process.stdout and "HTTP 200" in process.stdout
        assert ("Health check" in process.stdout) == (mode != "failures")
        assert (
            "fake-secret-TOKEN" not in process.stdout and "fake-query-SECRET" not in process.stdout
        )
        assert "\x1b" not in process.stdout
        assert ("Response body" in process.stdout) == (mode != "summary")
        result = ExecutionResult(str(directory / "output.xml"))
        assert result.suite.tests[0].status == "FAIL"
        (output / f"{mode}.txt").write_text(process.stdout, encoding="utf-8")
    directory = output / "errors"
    process = subprocess.run(
        [
            sys.executable,
            "-m",
            "robot",
            "--console",
            "none",
            "--outputdir",
            str(directory),
            str(ROOT / "tests" / "errors.robot"),
        ],
        cwd=ROOT,
        capture_output=True,
        text=True,
        encoding="utf-8",
        env={**os.environ, "PYTHONUTF8": "1", "TTY_COMPATIBLE": "0"},
    )
    assert process.returncode == 2, process.stderr
    assert "No response" in process.stdout and "Native failure still visible" in process.stdout
    assert "HTTP 404" in process.stdout and "Robot SKIP" in process.stdout
    assert "fake-query-SECRET" not in process.stdout
    result = ExecutionResult(str(directory / "output.xml"))
    assert [t.status for t in result.suite.tests] == ["FAIL", "FAIL", "PASS", "SKIP"]
    print("Verified console modes, Robot failures, timeout, skip, protection and isolation.")


if __name__ == "__main__":
    main()
