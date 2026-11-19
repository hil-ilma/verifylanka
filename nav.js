(function () {
  var b = document.querySelector('.nav-toggle');
  var l = document.getElementById('nav-links');
  if (!b || !l) return;
  function set(open) {
    l.classList.toggle('open', open);
    b.classList.toggle('on', open);
    b.setAttribute('aria-expanded', open ? 'true' : 'false');
  }
  b.addEventListener('click', function () { set(!l.classList.contains('open')); });
  l.addEventListener('click', function (e) { if (e.target.closest('a')) set(false); });
  document.addEventListener('keydown', function (e) { if (e.key === 'Escape') set(false); });
  window.addEventListener('resize', function () { if (window.innerWidth > 1100) set(false); });
})();
