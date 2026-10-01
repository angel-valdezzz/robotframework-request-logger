document.addEventListener('DOMContentLoaded',()=>{
 document.querySelectorAll('a[href]').forEach(a=>{
  const u=new URL(a.href,location.href);
  if(u.origin===location.origin&&/\/keywords\//.test(u.pathname)){
   a.target='_blank';a.rel='noopener';a.title='Abre en una pestaña nueva';
  }
 });
});
