document.addEventListener('DOMContentLoaded', () => {
 const title = document.documentElement.lang === 'en'
  ? 'Opens in a new tab' : 'Abre en una pestaña nueva';
 document.querySelectorAll('a[href]').forEach(a => {
  const u = new URL(a.href, location.href);
  if (u.origin === location.origin && /\/keywords\//.test(u.pathname)) {
   a.target = '_blank'; a.rel = 'noopener'; a.title = title;
  }
 });
});
