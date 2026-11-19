(function () {
  var d = document, root = d.documentElement, lenis = null;
  root.classList.add("js");

  /* Header sólido ao rolar */
  var hdr = d.querySelector(".hdr");
  function onScroll() { hdr.classList.toggle("solid", window.scrollY > 40 || root.classList.contains("nav-open")); }
  onScroll();
  window.addEventListener("scroll", onScroll, { passive: true });

  /* Menu mobile */
  var burger = d.querySelector(".burger");
  burger.addEventListener("click", function () {
    var open = root.classList.toggle("nav-open");
    burger.setAttribute("aria-expanded", open);
    onScroll();
  });
  d.querySelectorAll(".nav a").forEach(function (a) {
    a.addEventListener("click", function () { root.classList.remove("nav-open"); burger.setAttribute("aria-expanded", false); onScroll(); });
  });

  /* Animação de entrada */
  var rv = d.querySelectorAll(".rv");
  if ("IntersectionObserver" in window) {
    var io = new IntersectionObserver(function (es) {
      es.forEach(function (e) { if (e.isIntersecting) { e.target.classList.add("in"); io.unobserve(e.target); } });
    }, { rootMargin: "0px 0px -8% 0px" });
    rv.forEach(function (el) { io.observe(el); });
  } else rv.forEach(function (el) { el.classList.add("in"); });

  /* Abas (lazer) */
  d.querySelectorAll("[role=tablist]").forEach(function (list) {
    var tabs = list.querySelectorAll("[role=tab]");
    tabs.forEach(function (t) {
      t.addEventListener("click", function () {
        tabs.forEach(function (o) {
          var on = o === t;
          o.setAttribute("aria-selected", on);
          d.getElementById(o.getAttribute("aria-controls")).hidden = !on;
        });
      });
    });
  });

  /* Lightbox */
  var data = JSON.parse(d.getElementById("albums").textContent);
  var lb = d.querySelector(".lb"), img = lb.querySelector("img"), cap = lb.querySelector(".lb-cap"),
      ttl = lb.querySelector(".lb-top b"), cnt = lb.querySelector(".lb-count");
  var album = null, i = 0, lastFocus = null;

  function show(n) {
    var items = album.items;
    i = (n + items.length) % items.length;
    var it = items[i];
    img.src = it.src; img.alt = it.alt; img.width = it.w; img.height = it.h;
    cap.textContent = it.alt;
    cnt.textContent = (i + 1) + " / " + items.length;
    [1, -1].forEach(function (k) { var p = new Image(); p.src = items[(i + k + items.length) % items.length].src; });
  }
  function open(key, n) {
    album = data[key]; if (!album) return;
    lastFocus = d.activeElement;
    ttl.textContent = album.title;
    lb.classList.add("open"); lb.setAttribute("aria-hidden", "false");
    root.style.overflow = "hidden";
    if (lenis) lenis.stop();
    show(n || 0);
    lb.querySelector(".lb-close").focus();
  }
  function close() {
    lb.classList.remove("open"); lb.setAttribute("aria-hidden", "true");
    root.style.overflow = ""; img.removeAttribute("src");
    if (lenis) lenis.start();
    if (lastFocus) lastFocus.focus();
  }
  d.addEventListener("click", function (e) {
    var b = e.target.closest("[data-album]");
    if (b) { e.preventDefault(); open(b.getAttribute("data-album"), +b.getAttribute("data-i") || 0); }
  });
  lb.querySelector(".lb-close").addEventListener("click", close);
  lb.querySelector(".lb-prev").addEventListener("click", function () { show(i - 1); });
  lb.querySelector(".lb-next").addEventListener("click", function () { show(i + 1); });
  lb.addEventListener("click", function (e) { if (e.target.classList.contains("lb-stage")) close(); });
  d.addEventListener("keydown", function (e) {
    if (!lb.classList.contains("open")) return;
    if (e.key === "Escape") close();
    else if (e.key === "ArrowRight") show(i + 1);
    else if (e.key === "ArrowLeft") show(i - 1);
  });
  var x0 = null;
  lb.addEventListener("touchstart", function (e) { x0 = e.touches[0].clientX; }, { passive: true });
  lb.addEventListener("touchend", function (e) {
    if (x0 === null) return;
    var dx = e.changedTouches[0].clientX - x0;
    if (Math.abs(dx) > 45) show(i + (dx < 0 ? 1 : -1));
    x0 = null;
  });

  /* Rolagem suave do mouse (Lenis) — só em dispositivos com mouse/trackpad */
  var fine = window.matchMedia && matchMedia("(pointer: fine)").matches;
  var calm = window.matchMedia && matchMedia("(prefers-reduced-motion: reduce)").matches;
  if (fine && !calm) {
    var me = d.querySelector('script[src*="main.js"]');
    var s = d.createElement("script");
    s.src = me ? me.src.replace(/main\.js(\?.*)?$/, "lenis.min.js") : "js/lenis.min.js";
    s.async = true;
    s.onload = function () {
      if (!window.Lenis) return;
      lenis = new Lenis({ duration: 1.2, easing: function (t) { return Math.min(1, 1.001 - Math.pow(2, -10 * t)); }, smoothWheel: true, wheelMultiplier: 1 });
      lenis.on("scroll", onScroll);
      (function raf(t) { lenis.raf(t); requestAnimationFrame(raf); })(performance.now());
    };
    d.head.appendChild(s);
  }
  /* Posts do Instagram: carrega o script oficial só quando a seção se aproxima */
  var ig = d.querySelector("[data-ig-embed]");
  if (ig) {
    var loadIg = function () {
      if (window.instgrm) { window.instgrm.Embeds.process(); return; }
      var sc = d.createElement("script");
      sc.src = "https://www.instagram.com/embed.js"; sc.async = true;
      sc.onload = function () { if (window.instgrm) window.instgrm.Embeds.process(); };
      d.body.appendChild(sc);
    };
    if ("IntersectionObserver" in window) {
      var igo = new IntersectionObserver(function (es) {
        if (es[0].isIntersecting) { igo.disconnect(); loadIg(); }
      }, { rootMargin: "800px 0px" });
      igo.observe(ig);
    } else loadIg();
    d.querySelectorAll("[data-ig-dir]").forEach(function (b) {
      b.addEventListener("click", function () {
        var card = ig.firstElementChild, step = card ? card.getBoundingClientRect().width + 16 : 340;
        ig.scrollBy({ left: +b.getAttribute("data-ig-dir") * step, behavior: calm ? "auto" : "smooth" });
      });
    });
  }

  /* Links internos (#seção) com rolagem suave e compensando o header fixo */
  d.addEventListener("click", function (e) {
    var a = e.target.closest('a[href^="#"]');
    if (!a) return;
    var id = a.getAttribute("href").slice(1), el = id && d.getElementById(id);
    if (!el) return;
    e.preventDefault();
    if (lenis) lenis.scrollTo(el, { offset: id === "top" ? 0 : -72 });
    else el.scrollIntoView({ behavior: calm ? "auto" : "smooth" });
  });
})();
