"""Check real Chromium rendering, ambient motion and bilingual documentation flows."""

import json
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from threading import Thread

from playwright.sync_api import Page, expect, sync_playwright

ROOT = Path(__file__).resolve().parents[2]
MOUNT = "robotframework-request-logger"


def check_viewport(page: Page) -> None:
    """Persistent controls and both calls to action must fit without scrolling."""
    page.evaluate("scrollTo(0, 0)")
    assert page.evaluate("document.documentElement.scrollWidth <= innerWidth")
    assert page.locator(".er-action,.er-scroll-cue").evaluate_all(
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


def check_console(page: Page, lang: str) -> None:
    """The hero link exposes real Rich exports, and all three native tabs work."""
    page.locator(".er-action-secondary").click()
    section = page.locator(".er-real-console")
    for mode in ("Summary", "Failures", "Full"):
        section.locator("label").filter(has_text=mode).click()
        image = section.locator(f'img[src$="console-{mode.lower()}.svg"]')
        expect(image).to_be_visible()
        assert image.evaluate("el => el.complete && el.naturalWidth > 0")
    page.screenshot(path=str(ROOT / "build/landing-checks" / f"{lang}-real-console.png"))
    page.evaluate("scrollTo(0, 0)")


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
        a.backgroundImage===b.backgroundImage && a.backgroundPosition===b.backgroundPosition &&
        Math.abs(header.getAnimations()[0].currentTime-tabs.getAnimations()[0].currentTime)<1;
    }""")
    page.screenshot(path=str(ROOT / "build/landing-checks/docs-es-header.png"))
    # Material retains the header when returning through instant navigation.
    page.locator(".md-logo").first.click()
    expect(page.locator("[data-er-pause]")).to_be_visible()
    page.locator("[data-er-pause]").click()
    expect(page.locator("body")).to_have_attribute("data-er-motion-paused", "true")
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
            browser = playwright.chromium.launch(args=["--no-sandbox"])
            for lang in ("en", "es"):
                for width, height in ((1440, 1024), (1366, 625), (390, 844), (820, 1180)):
                    page = browser.new_page(viewport={"width": width, "height": height})
                    errors: list[str] = []
                    page.on("pageerror", lambda error, found=errors: found.append(str(error)))
                    page.goto(base + ("es/" if lang == "es" else ""))
                    expect(page.locator("[data-er-pause]")).to_be_visible()
                    page.locator(".er-pulse-art").first.wait_for(state="visible")
                    page.evaluate("Promise.all([...document.images].map(i=>i.decode()))")
                    page.evaluate("document.fonts.ready")
                    assert page.locator("h1").count() == 1
                    assert page.locator(".er-preview,canvas").count() == 0
                    logo = page.locator(".md-header .md-logo img").get_attribute("src")
                    assert logo and logo.endswith("assets/logo-dark.svg")
                    check_viewport(page)
                    page.screenshot(path=str(output / f"{lang}-{width}-{height}-initial.png"))
                    # The pulse advances over time and loops without a stopping tour.
                    before = page.locator(".er-pulse-art").evaluate_all(
                        "els=>els.map(el=>getComputedStyle(el).transform)"
                    )
                    page.wait_for_timeout(180)
                    assert before != page.locator(".er-pulse-art").evaluate_all(
                        "els=>els.map(el=>getComputedStyle(el).transform)"
                    )
                    page.locator("[data-er-pause]").click()
                    expect(page.locator("[data-er-pause]")).to_have_attribute(
                        "aria-pressed", "true"
                    )
                    page.wait_for_function(
                        "[...document.querySelectorAll('.er-pulse-art')].every("
                        "el=>getComputedStyle(el).animationPlayState==='paused')"
                    )
                    page.evaluate(
                        "new Promise(resolve=>requestAnimationFrame("
                        "()=>requestAnimationFrame(resolve)))"
                    )
                    paused = page.locator(".er-pulse-art").evaluate_all(
                        "els=>els.map(el=>getComputedStyle(el).transform)"
                    )
                    page.wait_for_timeout(180)
                    assert paused == page.locator(".er-pulse-art").evaluate_all(
                        "els=>els.map(el=>getComputedStyle(el).transform)"
                    )
                    styles = []
                    for scheme in ("default", "slate"):
                        page.evaluate(
                            "scheme => document.body.setAttribute('data-md-color-scheme',scheme)",
                            scheme,
                        )
                        styles.append(
                            page.locator("#er-headline").evaluate(
                                "el => getComputedStyle(el).color"
                            )
                        )
                        page.screenshot(path=str(output / f"{lang}-{width}-{height}-{scheme}.png"))
                    assert styles[0] == styles[1]
                    measurements.append(
                        {
                            "lang": lang,
                            "width": width,
                            "height": height,
                            "headline": page.locator("#er-headline").bounding_box(),
                        }
                    )
                    if width == 1440:
                        page.locator(".er-action-primary").hover()
                        page.screenshot(path=str(output / f"{lang}-hover.png"))
                        check_console(page, lang)
                    page.emulate_media(reduced_motion="reduce")
                    expect(page.locator("[data-er-pause]")).to_be_disabled()
                    assert page.locator(".er-pulse-art").evaluate_all(
                        "els=>els.every(el=>getComputedStyle(el).animationName==='none')"
                    )
                    page.emulate_media(reduced_motion="no-preference")
                    expect(page.locator("[data-er-pause]")).to_be_enabled()
                    assert not errors, errors
                    page.close()
            page = browser.new_page(viewport={"width": 1440, "height": 1024})
            check_documentation(page, base)
            page.close()
            context = browser.new_context(java_script_enabled=False)
            page = context.new_page()
            page.goto(base)
            expect(page.locator("[data-er-pause]")).to_be_hidden()
            expect(page.locator(".er-action-primary")).to_be_visible()
            page.locator(".er-action-secondary").click()
            assert page.url.endswith("#console-preview")
            browser.close()
    finally:
        server.shutdown()
    (output / "measurements.json").write_text(json.dumps(measurements, indent=2))
    print(
        "Landing passed: EN/ES, four viewports, themes, motion, "
        "real console, search and navigation."
    )


if __name__ == "__main__":
    main()
