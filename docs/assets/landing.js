/* Native Material navigation surrounds the approved console journey. */
(() => {
  'use strict';
  const motion = matchMedia('(prefers-reduced-motion: reduce)');
  let paused = false, elapsed = 0, dispose = () => {};
  const smooth = n => { n = Math.max(0, Math.min(1, n)); return n*n*(3-2*n); };
  function mount() {
    dispose();
    const hero = document.querySelector('[data-er-hero]');
    const $ = selector => hero?.querySelector(selector);
    const pause = $('[data-er-pause]'), scene = $('#exchange'), traveler = $('#traveler');
    const es = hero ? hero.dataset.lang === 'es' : document.documentElement.lang === 'es';
    const captions = es ? ['Una petición. Su secreto protegido.', 'HTTP 200. Un título que llegó vacío.', 'La prueba registra FAIL para el título.', 'Al cerrar el test, el contexto llega a la consola.']
      : ['A request. Its secret protected.', 'HTTP 200. An empty title.', 'The test records FAIL for the title.', 'When the test closes, the context reaches the console.'];
    const cleanups = [], steps = hero ? [...hero.querySelectorAll('[data-stage]')] : [];
    const parts = hero ? [$('#trace-request'), $('#trace-response'), $('#trace-assertion')] : [];
    let raf = null, previous = null, inView = true, geometry = null;
    function listen(element, event, callback) {
      if (!element) return;
      element.addEventListener(event, callback);
      cleanups.push(() => element.removeEventListener(event, callback));
    }
    function center(selector) {
      const a = $(selector).getBoundingClientRect(), b = scene.getBoundingClientRect();
      return {x:a.left-b.left+a.width/2, y:a.top-b.top+a.height/2};
    }
    function resize() {
      if (!scene || !hero.isConnected) return;
      geometry = {get:center('#request-method'), response:center('#response-value'), title:center('#response-title'), assertion:center('#assert-result'), trace:center('#trace-assertion b')};
      render();
    }
    function transfer(from, to, value, color, progress) {
      traveler.hidden = false; traveler.textContent = value; traveler.style.color = color;
      const p = smooth(progress), a = geometry[from], b = geometry[to];
      const x = a.x+(b.x-a.x)*p, y = a.y+(b.y-a.y)*p-Math.sin(p*Math.PI)*(from==='assertion'?40:24);
      traveler.style.transform = `translate(${x-traveler.offsetWidth/2}px,${y-traveler.offsetHeight/2}px)`;
      traveler.style.opacity = String(Math.min(1,progress/.15,(1-progress)/.2));
    }
    function render() {
      if (!geometry) return;
      const t = motion.matches ? 7500 : elapsed%9700;
      const index = t>=6100 ? 3 : t>=4600 ? 2 : t>=2300 ? 1 : 0;
      $('.er-hero-inner').dataset.phase = ['request','response','assertion','trace'][index];
      steps.forEach((step,i) => {
        step.classList.toggle('active',i===0&&t<1500||i===1&&t>=2300&&t<3800||i===2&&t>=4600&&t<6100);
        step.classList.toggle('revealed',i===0||i===1&&t>=2300||i===2&&t>=4600);
      });
      const secret = $('#secret-value'), protectedValue = t>=650;
      secret.textContent = protectedValue ? '[REDACTED]' : 'fake-query-SECRET';
      secret.style.color = protectedValue ? '' : '#71849e';
      secret.style.filter = t>=350&&t<650 ? `blur(${Math.sin((t-350)/300*Math.PI)*2.5}px)` : 'none';
      secret.setAttribute('aria-label',protectedValue ? (es?'Clave protegida en la salida':'Key protected in the output') : (es?'Clave ficticia del caso de prueba':'Fictional key from the test case'));
      $('#trace-result').classList.toggle('complete',t>=6900&&t<8900);
      parts.forEach((part,i) => {
        let appearance = t<6100 ? 0 : smooth((t-6100-i*170)/450);
        if (t>=8900) appearance = 1-smooth((t-8900)/800);
        part.style.opacity = String(.32+.68*appearance);
        part.style.transform = `translateY(${(1-appearance)*4}px)`;
      });
      $('#stage-caption').textContent = captions[index];
      $('#stage-index').textContent = `0${index+1} / 04`;
      traveler.hidden = true;
      if (!motion.matches) {
        if (t>=1500&&t<2300) transfer('get','response','GET','#8bb7f7',(t-1500)/800);
        if (t>=3800&&t<4600) transfer('title','assertion','""','#b4e86d',(t-3800)/800);
        if (t>=6100&&t<6900) transfer('assertion','trace','FAIL','#f576a3',(t-6100)/800);
      }
    }
    function running() { return scene && !paused && !motion.matches && !document.hidden && inView; }
    function tick(now) {
      raf = null;
      if (!running()) { previous = null; return; }
      if (previous!==null) elapsed += now-previous;
      previous = now; render(); raf = requestAnimationFrame(tick);
    }
    function update() {
      previous = null;
      if (raf!==null) cancelAnimationFrame(raf);
      raf = null;
      document.body.dataset.erMotionPaused = String(paused||motion.matches);
      if (!pause) return;
      pause.hidden = false; pause.disabled = motion.matches;
      pause.setAttribute('aria-pressed',String(paused));
      pause.querySelector('span:last-child').textContent = motion.matches ? (es?'Movimiento reducido':'Reduced motion')
        : paused ? (es?'Continuar':'Resume') : (es?'Pausar':'Pause');
      render();
      if (running()) raf = requestAnimationFrame(tick);
    }
    function syncHeaderMotion() {
      if (hero) return;
      const animation = selector => document.querySelector(selector)?.getAnimations?.().find(item=>item.animationName==='er-header-flow');
      const header=animation('.md-header'), tabs=animation('.md-tabs');
      if (header&&tabs&&header.currentTime!==null) tabs.currentTime=header.currentTime;
    }
    listen(pause,'click',()=>{paused=!paused;update();});
    for (const [selector,id] of [['.er-scroll-cue','er-content'],['.er-action-secondary','console-preview']]) {
      listen($(selector),'click',event=>{
        const target=document.getElementById(id);
        if (!target) return;
        event.preventDefault();
        target.scrollIntoView({behavior:motion.matches?'auto':'smooth',block:'start'});
        target.focus({preventScroll:true});
      });
    }
    listen(document.querySelector('.er-search-trigger'),'keydown',event=>{
      if (event.key==='Enter'||event.key===' ') {event.preventDefault();event.currentTarget.click();}
    });
    listen(motion,'change',update);
    listen(document,'visibilitychange',update);
    listen(window,'resize',()=>{resize();syncHeaderMotion();});
    if (scene) {
      if ('ResizeObserver' in window) {const observer=new ResizeObserver(resize);observer.observe(scene);cleanups.push(()=>observer.disconnect());}
      if ('IntersectionObserver' in window) {const observer=new IntersectionObserver(entries=>{inView=entries[0].isIntersecting;update();});observer.observe(hero);cleanups.push(()=>observer.disconnect());}
      resize();
      document.fonts?.ready.then(()=>{if(hero.isConnected)resize();});
      hero.classList.add('er-motion-ready');
    }
    update();syncHeaderMotion();
    dispose=()=>{if(raf!==null)cancelAnimationFrame(raf);cleanups.forEach(cleanup=>cleanup());};
  }
  if (typeof document$!=='undefined') document$.subscribe(mount);
  else if (document.readyState==='loading') document.addEventListener('DOMContentLoaded',mount,{once:true});
  else mount();
})();
