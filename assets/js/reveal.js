/* Scroll reveal for [data-reveal] elements.
   Adds .is-in once per element, then stops observing it — the reveal is a
   one-shot entrance, not a scroll-linked effect. Progressive enhancement: the
   stylesheet's .no-js rule keeps content visible if this never runs. */
(function () {
  'use strict';

  document.documentElement.classList.remove('no-js');

  function revealAll(nodes) {
    for (var i = 0; i < nodes.length; i++) nodes[i].classList.add('is-in');
  }

  function init() {
    var nodes = document.querySelectorAll('[data-reveal]');
    if (!nodes.length) return;

    if (!('IntersectionObserver' in window)) {
      revealAll(nodes);
      return;
    }

    var observer = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (!entry.isIntersecting) return;
        entry.target.classList.add('is-in');
        observer.unobserve(entry.target);
      });
    }, { threshold: 0.1, rootMargin: '0px 0px -6% 0px' });

    for (var i = 0; i < nodes.length; i++) observer.observe(nodes[i]);
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();
