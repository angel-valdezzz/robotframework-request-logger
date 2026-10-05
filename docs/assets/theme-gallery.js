/* One preview for all installed themes, independent of Material's tab limit. */
(() => {
  function initialize() {
    document.querySelectorAll('[data-theme-gallery]').forEach(gallery => {
      if (gallery.dataset.initialized) return;
      gallery.dataset.initialized = 'true';
      const get = selector => gallery.querySelector(selector);
      const picker = get('.theme-picker');
      const search = get('#theme-search');
      const select = get('#theme-select');
      const names = Array.from(select.options, option => option.value);
      const preview = get('[data-theme-preview]');
      const code = get('[data-theme-import]');
      const previous = get('[data-theme-prev]');
      const next = get('[data-theme-next]');
      let index = 0;

      function filter() {
        const matches = names.filter(name => name.includes(search.value.trim().toLowerCase()));
        select.replaceChildren(...matches.map(name => new Option(name, name)));
        select.value = names[index];
        select.hidden = !matches.length;
        get('[data-theme-empty]').hidden = !!matches.length;
      }
      function show(value) {
        if (value < 0 || value >= names.length) return;
        index = value;
        const name = names[index];
        get('[data-theme-current]').textContent = name;
        get('[data-theme-title]').textContent = name;
        preview.src = preview.dataset.base + name + '.svg';
        preview.alt = name;
        get('[data-theme-image-error]').hidden = true;
        const link = get('[data-theme-image-link]');
        link.href = preview.src;
        link.textContent = name + '.svg';
        code.textContent = '*** Settings ***\nLibrary    RequestLogger    mode=full    syntax_theme=' + name;
        get('[data-theme-position]').textContent = (index + 1) + ' / ' + names.length;
        get('[data-theme-copy-status]').textContent = '';
        previous.disabled = index === 0;
        next.disabled = index === names.length - 1;
        filter();
      }
      search.addEventListener('input', filter);
      search.addEventListener('keydown', event => {
        if (event.key === 'ArrowDown' && select.options.length) {
          event.preventDefault();
          select.focus();
        }
      });
      select.addEventListener('change', () => {
        const selected = names.indexOf(select.value);
        if (selected < 0) return;
        show(selected);
        picker.open = false;
        picker.querySelector('summary').focus();
      });
      picker.addEventListener('toggle', () => {
        if (picker.open) {
          search.focus();
        }
      });
      picker.addEventListener('keydown', event => {
        if (event.key === 'Escape') {
          picker.open = false;
          picker.querySelector('summary').focus();
        }
      });
      previous.addEventListener('click', () => show(index - 1));
      next.addEventListener('click', () => show(index + 1));
      preview.addEventListener('error', () => { get('[data-theme-image-error]').hidden = false; });
      get('[data-theme-copy]').addEventListener('click', async () => {
        const status = get('[data-theme-copy-status]');
        try {
          await navigator.clipboard.writeText(code.textContent);
          status.textContent = gallery.dataset.copied;
        } catch (_) {
          status.textContent = gallery.dataset.manual;
          const range = document.createRange();
          range.selectNodeContents(code);
          const selection = window.getSelection();
          selection.removeAllRanges();
          selection.addRange(range);
        }
      });
      picker.hidden = false;
      get('.theme-gallery-nav').hidden = false;
      get('[data-theme-copy]').hidden = false;
      show(0);
    });
  }
  initialize();
  if (typeof document$ !== 'undefined') document$.subscribe(initialize);
})();
