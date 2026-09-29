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

/* Publish the header's measured height as --header-h-actual.

   The hero pads its copy by --header-h, a constant derived from the default
   font size. The header is fixed, so if it ever renders taller than that
   constant — the reader has enlarged text, or the brand wraps — the extra
   height lands on top of the hero kicker. Measuring it keeps the two in step.
   CSS falls back to the constant when this never runs. */
(function () {
  'use strict';

  var header = document.querySelector('.site-header');
  if (!header) return;

  var last = -1;
  function publish() {
    var h = Math.round(header.getBoundingClientRect().height);
    if (h === last) return;
    last = h;
    document.documentElement.style.setProperty('--header-h-actual', h + 'px');
  }

  publish();

  if ('ResizeObserver' in window) {
    new ResizeObserver(publish).observe(header);
  } else {
    window.addEventListener('resize', publish);
  }

  /* Web fonts land after first paint and change the brand's height. */
  if (document.fonts && document.fonts.ready) document.fonts.ready.then(publish);
})();
