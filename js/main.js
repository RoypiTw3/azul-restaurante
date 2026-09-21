/* Azul Restaurante — interacción */
(function () {
  const html = document.documentElement;
  const body = document.body;
  const WA = 'https://wa.me/573235105573';
  const MAIL = 'azul.azulrestaurante@gmail.com';

  /* Preloader: solo la primera vez en la sesión */
  const pre = document.querySelector('.preloader');
  if (pre) {
    if (sessionStorage.getItem('azul-pre')) {
      html.classList.add('no-preloader');
    } else {
      body.classList.add('is-locked');
      const dismiss = () => {
        setTimeout(() => {
          pre.classList.add('is-done');
          body.classList.remove('is-locked');
          sessionStorage.setItem('azul-pre', '1');
          pre.addEventListener('transitionend', () => pre.remove(), { once: true });
        }, 400);
      };
      if (document.readyState === 'complete') {
        dismiss();
      } else {
        window.addEventListener('load', dismiss);
      }
    }
  }

  /* Menú de navegación */
  const burger = document.querySelector('.header__burger');
  const scrim = document.querySelector('.nav__scrim');
  const toggleMenu = (force) => {
    const open = force !== undefined ? force : !html.classList.contains('is-menu-open');
    html.classList.toggle('is-menu-open', open);
    body.classList.toggle('is-locked', open);
    if (burger) burger.setAttribute('aria-expanded', String(open));
  };
  if (burger) burger.addEventListener('click', () => toggleMenu());
  if (scrim) scrim.addEventListener('click', () => toggleMenu(false));
  document.addEventListener('keydown', (e) => { if (e.key === 'Escape') toggleMenu(false); });

  /* Página actual en el menú */
  const here = location.pathname.split('/').pop() || 'index.html';
  document.querySelectorAll('.nav__links a').forEach((a) => {
    const target = a.getAttribute('href').split('/').pop() || 'index.html';
    if (target === here) a.setAttribute('aria-current', 'page');
  });

  /* Revelado al hacer scroll */
  const io = new IntersectionObserver((entries) => {
    entries.forEach((en) => {
      if (en.isIntersecting) { en.target.classList.add('is-in'); io.unobserve(en.target); }
    });
  }, { rootMargin: '0px 0px -10% 0px', threshold: 0.1 });
  document.querySelectorAll('.reveal').forEach((el) => io.observe(el));

  /* Carrusel de tarjetas */
  document.querySelectorAll('.cards').forEach((wrap) => {
    const track = wrap.querySelector('.cards__track');
    const prev = wrap.querySelector('[data-prev]');
    const next = wrap.querySelector('[data-next]');
    const bar = wrap.querySelector('.cards__bar i');
    if (!track) return;
    const step = () => track.querySelector('.card').getBoundingClientRect().width + 20;
    const update = () => {
      if (!bar) return;
      const max = track.scrollWidth - track.clientWidth;
      const n = track.children.length;
      const visible = Math.max(1, Math.round(track.clientWidth / step()));
      bar.style.width = (visible / n * 100) + '%';
      const p = max > 0 ? track.scrollLeft / max : 0;
      bar.style.transform = `translateX(${p * (100 / (visible / n) - 100)}%)`;
    };
    prev && prev.addEventListener('click', () => track.scrollBy({ left: -step(), behavior: 'smooth' }));
    next && next.addEventListener('click', () => track.scrollBy({ left: step(), behavior: 'smooth' }));
    track.addEventListener('scroll', update, { passive: true });
    window.addEventListener('resize', update);
    update();
  });

  /* Índice de categorías del menú: resalta la sección visible y la centra en la barra */
  const menuNav = document.querySelector('.menu-nav');
  if (menuNav) {
    const links = [...menuNav.querySelectorAll('a')];
    const track = menuNav.querySelector('.menu-nav__track');
    const cats = links.map((a) => document.querySelector(a.getAttribute('href'))).filter(Boolean);
    let current = null;
    const setActive = (id) => {
      if (id === current) return;
      current = id;
      links.forEach((a) => {
        const on = a.getAttribute('href') === '#' + id;
        a.classList.toggle('is-active', on);
        if (on && track) {
          const left = a.offsetLeft - (track.clientWidth - a.offsetWidth) / 2;
          track.scrollTo({ left, behavior: 'smooth' });
        }
      });
    };
    const spy = () => {
      const line = menuNav.getBoundingClientRect().bottom + 24;
      let best = cats[0];
      for (const c of cats) { if (c.getBoundingClientRect().top <= line) best = c; }
      if (best) setActive(best.id);
    };
    window.addEventListener('scroll', spy, { passive: true });
    window.addEventListener('resize', spy);
    window.addEventListener('load', () => setTimeout(spy, 50));
    window.addEventListener('hashchange', () => setTimeout(spy, 50));
    spy();
  }

  /* Formulario de contacto → abre WhatsApp con el mensaje listo.
     Las sugerencias van por correo, como en el Linktree del restaurante. */
  const form = document.querySelector('#contact-form');
  if (form) {
    const motivo = form.querySelector('#f-motivo');
    const btn = form.querySelector('button[type="submit"]');
    const hint = form.querySelector('.form-hint');
    const isMail = () => motivo && motivo.value === 'Sugerencia';
    const refresh = () => {
      if (!btn) return;
      btn.textContent = isMail() ? 'Enviar por correo' : 'Enviar por WhatsApp';
      if (hint) hint.textContent = isMail()
        ? 'Al enviar se abre tu correo con el mensaje listo para azul.azulrestaurante@gmail.com.'
        : 'Al enviar se abre WhatsApp con tu mensaje listo para que lo envíes desde tu número.';
    };
    if (motivo) motivo.addEventListener('change', refresh);
    refresh();
    form.addEventListener('submit', (e) => {
      e.preventDefault();
      const d = new FormData(form);
      const msg =
        `Hola, Azul. Soy ${d.get('nombre')}.\n` +
        `Teléfono: ${d.get('telefono')}\n` +
        `Motivo: ${d.get('motivo')}\n\n` +
        `${d.get('mensaje')}`;
      if (isMail()) {
        location.href = 'mailto:' + MAIL + '?subject=' + encodeURIComponent('Sugerencia para Azul') + '&body=' + encodeURIComponent(msg);
      } else {
        window.open(WA + '?text=' + encodeURIComponent(msg), '_blank', 'noopener');
      }
    });
  }
})();
