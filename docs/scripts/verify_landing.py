"""Check the approved console journey and native bilingual Material navigation."""

import json
import os
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from threading import Thread

from playwright.sync_api import Page, expect, sync_playwright

ROOT = Path(__file__).resolve().parents[2]
MOUNT = "robotframework-request-logger"


def check_viewport(page: Page) -> None:
    """Actions and native controls remain visible; console text stays inside its surface."""
    page.evaluate("scrollTo(0, 0)")
    assert page.evaluate("document.documentElement.scrollWidth <= innerWidth")
    assert page.locator(".er-action").evaluate_all(
        "els => els.every(el => {const b=el.getBoundingClientRect();"
        "return b.top>=0 && b.bottom<=innerHeight && b.left>=0 && b.right<=innerWidth;})"
    )
    assert page.locator(".md-select button").evaluate(
        "el => el.getBoundingClientRect().right <= "
        "document.querySelector('.er-search-trigger').getBoundingClientRect().left"
    )
    assert page.locator(".md-header").evaluate(
        "el => getComputedStyle(el).backgroundColor === 'rgba(0, 0, 0, 0)'"
    )
    assert page.locator("#trace-result").evaluate("el => el.scrollWidth <= el.clientWidth")
    if page.viewport_size["width"] >= 1050:
        assert page.locator(".er-scroll-cue").evaluate(
            "el => el.getBoundingClientRect().bottom <= innerHeight"
        ), page.locator(".er-scroll-cue").bounding_box()


def check_console(page: Page, lang: str) -> None:
    """The native tabs display the actual neutral book execution in every mode."""
    page.locator(".er-action-secondary").click()
    section = page.locator(".er-real-console")
    expect(section).to_be_focused()
    for mode in ("Summary", "Failures", "Full"):
        section.locator("label").filter(has_text=mode).click()
        image = section.locator(f'img[src$="console-{mode.lower()}.svg"]')
        expect(image).to_be_visible()
        assert image.evaluate("el => el.complete && el.naturalWidth > 0")
    page.screenshot(path=str(ROOT / "build/landing-checks" / f"{lang}-real-console.png"))
    page.evaluate("scrollTo(0, 0)")


def check_motion(page: Page, base: str) -> None:
    """Motion loops, pauses, resumes and never pauses on hover."""
    page.goto(base)
    expect(page.locator(".er-motion-ready")).to_be_visible()
    page.locator(".er-action-primary").hover()
    page.wait_for_function("document.querySelector('.response').classList.contains('active')")
    expect(page.locator("body")).to_have_attribute("data-er-motion-paused", "false")
    page.wait_for_function("document.querySelector('#trace-result').classList.contains('complete')")
    expect(page.locator("#secret-value")).to_have_text("[REDACTED]")
    assert page.locator("#trace-assertion").inner_text().endswith("'' should not be empty.")
    page.locator("[data-er-pause]").click()
    expect(page.locator("[data-er-pause]")).to_have_attribute("aria-pressed", "true")
    before = page.locator("#exchange").inner_html()
    page.wait_for_timeout(180)
    assert before == page.locator("#exchange").inner_html()
    page.locator("[data-er-pause]").click()
    page.wait_for_function("document.querySelector('.er-hero-inner').dataset.phase==='request'")
    page.wait_for_function("document.querySelector('.response').classList.contains('active')")
    # A second mount must have one working pause listener and a running timeline.
    page.locator(".er-action-primary").click()
    page.wait_for_url("**/usage/")
    page.locator(".md-logo").first.click()
    expect(page.locator(".er-motion-ready")).to_be_visible()
    page.locator("[data-er-pause]").click()
    expect(page.locator("[data-er-pause]")).to_have_attribute("aria-pressed", "true")


def check_documentation(page: Page, base: str) -> None:
    page.goto(base)
    page.locator(".er-search-trigger").focus()
    page.keyboard.press("Enter")
    query = page.locator('[data-md-component="search-query"]')
    query.fill("Log Response")
    expect(page.locator(".md-search-result__link").first).to_be_visible(timeout=30000)
    page.keyboard.press("Escape")
    page.locator(".er-action-primary").click()
    page.wait_for_url("**/usage/")
    expect(page.locator("[data-er-hero]")).to_have_count(0)
    page.locator('label[for="__palette_1"]').click()
    expect(page.locator("body")).to_have_attribute("data-md-color-scheme", "slate")
    page.locator(".md-select button").click()
    page.locator('[data-doc-language="es"]').click()
    page.wait_for_url("**/es/usage/")
    expect(page.locator("body")).to_have_attribute("data-md-color-scheme", "slate")
    assert page.evaluate("""() => {
      const header=document.querySelector('.md-header'),tabs=document.querySelector('.md-tabs');
      const a=getComputedStyle(header),b=getComputedStyle(tabs);
      return a.animationName==='er-header-flow' && b.animationName===a.animationName &&
        a.backgroundImage===b.backgroundImage &&
        Math.abs(header.getAnimations()[0].currentTime-tabs.getAnimations()[0].currentTime)<2;
    }""")
    page.screenshot(path=str(ROOT / "build/landing-checks/docs-es-header.png"))
    page.locator(".md-logo").first.click()
    expect(page.locator(".er-motion-ready")).to_be_visible()
    expect(page.locator("#trace-label")).to_have_text("SALIDA DE CONSOLA")
    page.locator(".er-scroll-cue").click()
    expect(page.locator("#er-content")).to_be_focused()
    page.wait_for_function("scrollY > 100")


def main() -> None:
    server_root = ROOT / "build/docs-server"
    server_root.mkdir(parents=True, exist_ok=True)
    mount = server_root / MOUNT
    if not mount.exists():
        mount.symlink_to(ROOT / "site", target_is_directory=True)
    handler = partial(SimpleHTTPRequestHandler, directory=str(server_root))
    server = ThreadingHTTPServer(("127.0.0.1", 0), handler)
    Thread(target=server.serve_forever, daemon=True).start()
    base = f"http://127.0.0.1:{server.server_port}/{MOUNT}/"
    output = ROOT / "build/landing-checks"
    output.mkdir(parents=True, exist_ok=True)
    measurements = []
    try:
        with sync_playwright() as playwright:
            executable = os.environ.get("LOGGER_CHROMIUM_PATH")
            browser = playwright.chromium.launch(
                executable_path=executable, args=["--no-sandbox", "--disable-dev-shm-usage"]
            )
            for lang in ("en", "es"):
                for width, height in (
                    (1440, 1024),
                    (1366, 625),
                    (390, 844),
                    (820, 1180),
                    (320, 740),
                ):
                    page = browser.new_page(
                        viewport={"width": width, "height": height}, reduced_motion="reduce"
                    )
                    errors: list[str] = []
                    page.on("pageerror", lambda error, found=errors: found.append(str(error)))
                    page.goto(base + ("es/" if lang == "es" else ""))
                    expect(page.locator(".er-motion-ready")).to_be_visible()
                    page.evaluate("document.fonts.ready")
                    assert page.locator("h1").count() == 1
                    assert page.locator(".er-preview,canvas,.er-pulse-art").count() == 0
                    expect(page.locator("#trace-result")).to_have_class("trace-result complete")
                    expect(page.locator("[data-er-pause]")).to_be_disabled()
                    assert page.locator("#traveler").is_hidden()
                    assert page.locator(".md-header .md-logo").first.is_visible()
                    page.screenshot(path=str(output / f"{lang}-{width}-{height}-initial.png"))
                    check_viewport(page)
                    for scheme in ("default", "slate"):
                        page.evaluate(
                            "scheme=>document.body.setAttribute('data-md-color-scheme',scheme)",
                            scheme,
                        )
                        assert (
                            page.locator("#er-headline").evaluate("el=>getComputedStyle(el).color")
                            == "rgb(237, 242, 250)"
                        )
                    page.screenshot(path=str(output / f"{lang}-{width}-{height}.png"))
                    measurements.append({"lang": lang, "width": width, "height": height})
                    if width == 1440:
                        check_console(page, lang)
                    assert not errors, errors
                    page.close()
            page = browser.new_page(viewport={"width": 1440, "height": 1024})
            check_motion(page, base)
            check_documentation(page, base)
            page.close()
            context = browser.new_context(java_script_enabled=False)
            page = context.new_page()
            page.goto(base)
            expect(page.locator("[data-er-pause]")).to_be_hidden()
            expect(page.locator("#trace-result")).to_have_class("trace-result complete")
            page.locator(".er-action-secondary").click()
            assert page.url.endswith("#console-preview")
            browser.close()
    finally:
        server.shutdown()
    (output / "measurements.json").write_text(json.dumps(measurements, indent=2))
    print(
        "Landing passed: EN/ES, five viewports, real console, loop, pause, reduced motion, "
        "themes, search, instant navigation and shared header/nav phase."
    )


if __name__ == "__main__":
    main()
