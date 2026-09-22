(() => {
  'use strict';
  const menu = document.querySelector('.site-menu');
  const toggle = document.querySelector('.menu-toggle');
  const closeMenu = () => { menu.hidden = true; toggle.setAttribute('aria-expanded', 'false'); };
  toggle.addEventListener('click', () => {
    const open = toggle.getAttribute('aria-expanded') !== 'true';
    menu.hidden = !open; toggle.setAttribute('aria-expanded', String(open));
  });
  document.addEventListener('keydown', e => { if (e.key === 'Escape' && !menu.hidden) { closeMenu(); toggle.focus(); } });
  document.addEventListener('click', e => { if (!menu.contains(e.target) && !toggle.contains(e.target)) closeMenu(); });
  const reduced = matchMedia('(prefers-reduced-motion: reduce)');
  for (const card of document.querySelectorAll('.tilt')) {
    let frame;
    const reset = () => { cancelAnimationFrame(frame); card.style.removeProperty('--rx'); card.style.removeProperty('--ry'); card.classList.remove('touching'); };
    const follow = e => {
      if (reduced.matches) return;
      cancelAnimationFrame(frame);
      frame = requestAnimationFrame(() => {
        const rect = card.getBoundingClientRect();
        const x = Math.max(0, Math.min(1, (e.clientX - rect.left) / rect.width));
        const y = Math.max(0, Math.min(1, (e.clientY - rect.top) / rect.height));
        card.style.setProperty('--mx', `${x * 100}%`); card.style.setProperty('--my', `${y * 100}%`);
        card.style.setProperty('--rx', `${(0.5 - y) * 5}deg`); card.style.setProperty('--ry', `${(x - 0.5) * 5}deg`);
        if (e.pointerType === 'touch') card.classList.add('touching');
      });
    };
    card.addEventListener('pointermove', follow, { passive: true });
    card.addEventListener('pointerdown', follow, { passive: true });
    for (const name of ['pointerleave', 'pointerup', 'pointercancel', 'blur']) card.addEventListener(name, reset);
    reduced.addEventListener('change', reset);
  }
  let scrollFrame;
  const progress = () => {
    cancelAnimationFrame(scrollFrame);
    scrollFrame = requestAnimationFrame(() => {
      const height = document.documentElement.scrollHeight - innerHeight;
      document.documentElement.style.setProperty('--progress', `${height > 0 ? 100 * scrollY / height : 0}%`);
    });
  };
  addEventListener('scroll', progress, { passive: true }); addEventListener('resize', progress); progress();
  const search = document.querySelector('#document-search');
  if (search) {
    const cards = [...document.querySelectorAll('[data-search]')];
    search.addEventListener('input', () => {
      const words = search.value.toLowerCase().trim().split(/\s+/).filter(Boolean);
      let count = 0;
      for (const card of cards) { card.hidden = !words.every(word => card.dataset.search.includes(word)); if (!card.hidden) count++; }
      document.querySelector('#document-count').textContent = `${count} ${count === 1 ? 'document' : 'documents'}`;
      document.querySelector('.no-results').hidden = count !== 0;
    });
  }
})();
