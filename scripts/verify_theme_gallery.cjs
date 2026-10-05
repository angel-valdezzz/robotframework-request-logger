/* Verify every theme and gallery action against the built bilingual pages. */
const fs = require('fs');
const path = require('path');
const assert = require('assert');
const { JSDOM } = require('jsdom');
(async () => {
  for (const language of ['en', 'es']) {
    const folder = path.join('site', language === 'es' ? 'es' : '');
    const dom = new JSDOM(fs.readFileSync(path.join(folder, 'themes/index.html'), 'utf8'), {
      url: 'https://example.test/robotframework-request-logger/' + (language === 'es' ? 'es/' : '') + 'themes/',
      runScripts: 'outside-only', pretendToBeVisual: true,
    });
    const win = dom.window;
    const doc = win.document;
    win.eval(fs.readFileSync('docs/assets/theme-gallery.js', 'utf8'));
    const gallery = doc.querySelector('[data-theme-gallery]');
    const select = gallery.querySelector('select');
    const names = Array.from(select.options, option => option.value);
    assert(names.length > 20);
    assert.equal(names[0], 'monokai');
    assert(names.includes('one-dark') && names.includes('gruvbox-light'));
    const preview = gallery.querySelector('[data-theme-preview]');
    const previous = gallery.querySelector('[data-theme-prev]');
    const next = gallery.querySelector('[data-theme-next]');
    assert(previous.disabled);
    for (const name of names) {
      select.value = name;
      select.dispatchEvent(new win.Event('change'));
      assert.equal(gallery.querySelector('[data-theme-title]').textContent, name);
      assert(gallery.querySelector('[data-theme-import]').textContent.endsWith('syntax_theme=' + name));
      assert(gallery.querySelector('[data-theme-import] span'));
      assert(preview.src.endsWith('/assets/themes/' + name + '.svg'));
      const local = path.join(folder, 'themes', preview.getAttribute('src'));
      assert(fs.existsSync(local), local);
      new JSDOM(fs.readFileSync(local, 'utf8'), { contentType: 'image/svg+xml' }).window.close();
    }
    assert(next.disabled);
    previous.click();
    assert.equal(gallery.querySelector('[data-theme-title]').textContent, names.at(-2));
    next.click();
    assert.equal(gallery.querySelector('[data-theme-title]').textContent, names.at(-1));
    const search = gallery.querySelector('input');
    search.value = 'ONE-DARK';
    search.dispatchEvent(new win.Event('input'));
    assert.deepEqual(Array.from(select.options, option => option.value), ['one-dark']);
    select.value = 'one-dark';
    select.dispatchEvent(new win.Event('change'));
    search.value = 'no-such-theme';
    search.dispatchEvent(new win.Event('input'));
    assert(select.hidden && !gallery.querySelector('[data-theme-empty]').hidden);
    search.value = '';
    search.dispatchEvent(new win.Event('input'));
    assert.equal(select.options.length, names.length);
    const picker = gallery.querySelector('details');
    picker.open = true;
    picker.dispatchEvent(new win.KeyboardEvent('keydown', {key: 'Escape'}));
    assert(!picker.open);
    assert(!gallery.querySelector('[data-theme-copy]'));
    assert(gallery.querySelector('[data-theme-import] span'));
    assert(gallery.querySelector('[data-theme-image-link]').closest('[hidden]'));
    preview.dispatchEvent(new win.Event('error'));
    assert(!gallery.querySelector('[data-theme-image-error]').hidden);
    dom.window.close();
    console.log(language + ': verified ' + names.length + ' previews, imports, search, navigation and syntax highlighting.');
  }
})().catch(error => { console.error(error); process.exit(1); });
