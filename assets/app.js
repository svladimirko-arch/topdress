/* TOPDRESS — поведение сайта. Без библиотек. Настройки — в assets/config.js */
(function () {
  'use strict';
  var C = window.TOPDRESS || {};
  var CT = C.contacts || {};
  var $ = function (s, r) { return (r || document).querySelector(s); };
  var $$ = function (s, r) { return Array.prototype.slice.call((r || document).querySelectorAll(s)); };
  var reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  var root = document.documentElement;
  function esc(s) { return String(s).replace(/[&<>"']/g, function (c) { return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]; }); }
  function pad(n) { return (n < 10 ? '0' : '') + n; }

  /* ---------- 1. Контакты из config.js ---------- */
  (function applyConfig() {
    var short = (CT.address || '').split(',').slice(0, 2).join(',').trim();
    var map = {
      phone: CT.phone, hours: CT.hours,
      addressFull: CT.city && CT.address ? CT.city + ', ' + CT.address : '',
      addressShort: CT.city && short ? CT.city + ', ' + short : ''
    };
    $$('[data-cfg]').forEach(function (el) { var v = map[el.getAttribute('data-cfg')]; if (v) el.textContent = v; });
    var hrefs = {
      tel: CT.phoneHref && 'tel:' + CT.phoneHref,
      telegram: CT.telegram,
      telegramChat: CT.telegramChat,
      whatsapp: CT.whatsapp,
      max: CT.max,
      vk: CT.vk
    };
    $$('[data-cfg-href]').forEach(function (el) {
      var k = el.getAttribute('data-cfg-href'), v = hrefs[k];
      if (v) el.setAttribute('href', v);
      if (k === 'telegram' && CT.telegram && /@/.test(el.textContent)) el.textContent = '@' + CT.telegram.replace(/\/+$/, '').split('/').pop();
    });
    if (CT.routeUrl) $('#route').setAttribute('href', CT.routeUrl);
    if (CT.mapSrc) $('#map').setAttribute('src', CT.mapSrc);
    $('#year').textContent = new Date().getFullYear();
  })();

  /* ---------- 2. Старт: появление первого экрана ---------- */
  function start() { setTimeout(function () { root.classList.add('ready'); }, 60); }
  var heroImg = $('.hero__frame img');
  if (heroImg && !heroImg.complete) { heroImg.addEventListener('load', start); heroImg.addEventListener('error', start); setTimeout(start, 1800); } else start();

  /* ---------- 3. Шапка и меню ---------- */
  var hdr = $('#hdr'), burger = $('#burger'), menu = $('#menu');
  function setMenu(open) {
    document.body.classList.toggle('menu-open', open);
    burger.setAttribute('aria-expanded', open); burger.setAttribute('aria-label', open ? 'Закрыть меню' : 'Открыть меню');
    menu.setAttribute('aria-hidden', !open);
    document.body.style.overflow = open ? 'hidden' : '';
  }
  burger.addEventListener('click', function () { setMenu(!document.body.classList.contains('menu-open')); });
  $$('a', menu).forEach(function (a) { a.addEventListener('click', function () { setMenu(false); }); });
  document.addEventListener('keydown', function (e) { if (e.key === 'Escape' && document.body.classList.contains('menu-open')) setMenu(false); });
  window.addEventListener('resize', function () { if (innerWidth > 900) setMenu(false); });

  /* ---------- 4. Появление при прокрутке ---------- */
  // Свои проверки видимости: IntersectionObserver не срабатывает у элементов с clip-path
  var pending = [];
  function watch(el) { if (pending.indexOf(el) < 0) pending.push(el); }
  function reveal() {
    var vh = innerHeight;
    for (var i = pending.length - 1; i >= 0; i--) {
      var r = pending[i].getBoundingClientRect();
      if (r.top < vh * 0.92 && r.bottom > 0) { pending[i].classList.add('in'); pending.splice(i, 1); }
    }
  }
  $$('.ln').forEach(function (ln, i) {
    var p = ln.parentElement; if (p.closest('.hero__title')) return;
    ln.style.setProperty('--i', $$('.ln', p).indexOf(ln));
    if (!p.__w) { p.__w = 1; watch(p); }
  });
  $$('.hero__title .ln').forEach(function (ln, i) { ln.style.setProperty('--i', i); });
  $$('.rv,.mask,.why__item,.eyebrow').forEach(function (el, i) {
    if (el.closest('.hero')) return;
    if (el.classList.contains('rv')) { var sib = $$('.rv', el.parentElement); el.style.setProperty('--d', (Math.min(sib.indexOf(el), 4) * 0.08) + 's'); }
    watch(el);
  });

  /* ---------- 5. Абзац, проявляющийся по словам ---------- */
  var scrub = $('#scrub'), words = [];
  if (scrub && !reduce) {
    scrub.setAttribute('aria-label', scrub.textContent);
    scrub.innerHTML = scrub.textContent.split(' ').map(function (w) { return '<span class="w" aria-hidden="true">' + esc(w) + '</span>'; }).join(' ');
    words = $$('.w', scrub);
  }
  function scrubUpdate() {
    if (!words.length) return;
    var r = scrub.getBoundingClientRect(), vh = innerHeight;
    var p = (vh * 0.86 - r.top) / (vh * 0.5 + r.height * 0.6);
    p = Math.max(0, Math.min(1, p));
    var n = Math.round(p * words.length);
    words.forEach(function (w, i) { w.classList.toggle('on', i < n); });
  }

  /* ---------- 6. Параллакс и шапка (один rAF на прокрутку) ---------- */
  var pars = $$('[data-par]').map(function (img) { return { img: img, box: img.parentElement, k: parseFloat(img.getAttribute('data-par')) }; });
  var mbar = $('#mbar'), bookSec = $('#booking'), heroSec = $('#hero'), ticking = false;
  function frame() {
    ticking = false;
    var y = scrollY, vh = innerHeight;
    reveal();
    hdr.classList.toggle('is-solid', y > 60 && !document.body.classList.contains('menu-open'));
    if (!reduce) {
      pars.forEach(function (p) {
        var r = p.box.getBoundingClientRect();
        if (r.bottom < -100 || r.top > vh + 100) return;
        var max = r.height * (p.img.closest('.hero__frame') ? 0.02 : 0.045);
        var v = ((r.top + r.height / 2) - vh / 2) * p.k;
        v = Math.max(-max, Math.min(max, v));
        p.img.style.setProperty('--py', v.toFixed(1) + 'px');
      });
      scrubUpdate();
    }
    var hb = heroSec.getBoundingClientRect().bottom, bk = bookSec.getBoundingClientRect();
    mbar.classList.toggle('show', hb < vh * 0.3 && !(bk.top < vh * 0.85 && bk.bottom > 0));
  }
  function req() { if (!ticking) { ticking = true; requestAnimationFrame(frame); } }
  addEventListener('scroll', req, { passive: true }); addEventListener('resize', req); addEventListener('load', req); frame();

  /* ---------- 7. Галерея ---------- */
  var G = (C.gallery || []).map(function (g, i) { g.i = i; return g; });
  var grid = $('#galGrid'), moreWrap = $('.gal__more'), moreBtn = $('#galMore'), countEl = $('#galCount');
  var LIMIT = 12, shown = LIMIT, filter = 'all';
  var LABEL = { wedding: 'Свадебное', evening: 'Вечернее' };
  function list() { return G.filter(function (g) { return filter === 'all' || g.cat === filter; }); }
  function sizes(g) { return { s: Math.min(760, g.w), l: Math.min(1500, g.w) }; }
  function renderGallery() {
    var all = list(), vis = all.slice(0, shown);
    grid.innerHTML = vis.map(function (g, n) {
      var z = sizes(g), ss = 'images/' + g.k + '-s.webp', ll = 'images/' + g.k + '-l.webp';
      var set = z.s < z.l ? ' srcset="' + ss + ' ' + z.s + 'w, ' + ll + ' ' + z.l + 'w" sizes="(max-width:900px) 50vw, 33vw"' : '';
      return '<a class="g" href="' + ll + '" data-n="' + n + '" style="aspect-ratio:' + g.w + '/' + g.h + '" aria-label="Открыть фото ' + (n + 1) + '">' +
        '<img src="' + (z.s < z.l ? ss : ll) + '"' + set + ' width="' + g.w + '" height="' + g.h + '" alt="' + esc(g.alt || '') + '" loading="lazy" decoding="async">' +
        '<span class="g__t"><span>№ ' + pad(n + 1) + '</span><span>' + LABEL[g.cat] + '</span></span></a>';
    }).join('');
    $$('.g', grid).forEach(function (el, i) { el.style.transitionDelay = (i % 3) * 0.08 + 's'; watch(el); });
    countEl.textContent = vis.length + ' из ' + all.length; req();
    moreWrap.hidden = vis.length >= all.length;
  }
  function setFilter(f, scrollTo) {
    filter = f; shown = LIMIT;
    var galSec = $('#collection'); if (galSec) galSec.classList.toggle('gal--ev', f === 'evening');
    $$('.tabs button').forEach(function (b) { var on = b.getAttribute('data-f') === f; b.classList.toggle('is-on', on); b.setAttribute('aria-selected', on); });
    renderGallery();
  }
  $$('.tabs button').forEach(function (b) { b.addEventListener('click', function () { setFilter(b.getAttribute('data-f')); }); });
  moreBtn.addEventListener('click', function () { shown += 100; renderGallery(); });
  $$('[data-filter-link]').forEach(function (a) { a.addEventListener('click', function () { setFilter(a.getAttribute('data-filter-link')); }); });
  renderGallery();

  /* ---------- 8. Лайтбокс ---------- */
  var lb = $('#lb'), lbImg = $('#lbImg'), lbCap = $('#lbCap'), lbIdx = $('#lbIdx'), cur = 0, lastFocus = null, lbList = [];
  function lbShow(n) {
    lbList = list(); cur = (n + lbList.length) % lbList.length;
    var g = lbList[cur], src = 'images/' + g.k + '-l.webp';
    lbImg.classList.remove('show');
    var t = new Image();
    t.onload = function () { lbImg.src = src; lbImg.alt = g.alt || ''; requestAnimationFrame(function () { lbImg.classList.add('show'); }); };
    t.src = src;
    lbCap.textContent = LABEL[g.cat]; lbIdx.textContent = pad(cur + 1) + ' / ' + pad(lbList.length);
    [1, -1].forEach(function (d) { var o = lbList[(cur + d + lbList.length) % lbList.length]; new Image().src = 'images/' + o.k + '-l.webp'; });
  }
  function lbOpen(n, from) {
    lastFocus = from || document.activeElement; lb.classList.add('open'); lb.setAttribute('aria-hidden', 'false');
    document.body.classList.add('lb-open'); lbShow(n); $('#lbX').focus();
  }
  function lbClose() {
    lb.classList.remove('open'); lb.setAttribute('aria-hidden', 'true'); document.body.classList.remove('lb-open');
    if (lastFocus && lastFocus.focus) lastFocus.focus();
  }
  grid.addEventListener('click', function (e) { var a = e.target.closest('.g'); if (!a) return; e.preventDefault(); lbOpen(+a.getAttribute('data-n'), a); });
  $('#lbX').addEventListener('click', lbClose);
  $('#lbPrev').addEventListener('click', function () { lbShow(cur - 1); });
  $('#lbNext').addEventListener('click', function () { lbShow(cur + 1); });
  $('#lbCta').addEventListener('click', lbClose);
  lb.addEventListener('click', function (e) { if (e.target === lb || e.target.id === 'lbStage') lbClose(); });
  document.addEventListener('keydown', function (e) {
    if (!lb.classList.contains('open')) return;
    if (e.key === 'Escape') lbClose(); else if (e.key === 'ArrowLeft') lbShow(cur - 1); else if (e.key === 'ArrowRight') lbShow(cur + 1);
    else if (e.key === 'Tab') { var f = $$('button,a', lb); var i = f.indexOf(document.activeElement); e.preventDefault(); f[(i + (e.shiftKey ? -1 : 1) + f.length) % f.length].focus(); }
  });
  var tx = null;
  lb.addEventListener('touchstart', function (e) { tx = e.touches[0].clientX; }, { passive: true });
  lb.addEventListener('touchend', function (e) { if (tx === null) return; var dx = e.changedTouches[0].clientX - tx; if (Math.abs(dx) > 50) lbShow(cur + (dx < 0 ? 1 : -1)); tx = null; }, { passive: true });

  /* ---------- 9. Фотолента «Атмосфера» ---------- */
  var rail = $('#atmRail'), track = $('#atmTrack'), A = C.atmosphere || [];
  function atItem(a, dup) {
    var z = Math.min(1500, a.w), s = Math.min(760, a.w);
    return '<figure class="at"' + (dup ? ' aria-hidden="true"' : '') + '><img src="images/' + a.k + '-l.webp" width="' + a.w + '" height="' + a.h + '" alt="' + (dup ? '' : esc(a.cap || '')) + '" loading="lazy" decoding="async" draggable="false"><figcaption>' + esc(a.cap || '') + '</figcaption></figure>';
  }
  track.innerHTML = A.map(function (a) { return atItem(a, false); }).join('') + (reduce ? '' : A.map(function (a) { return atItem(a, true); }).join(''));
  var paused = false, half = 0, pos = 0, drag = null;
  function measure() { half = reduce ? 0 : track.scrollWidth / 2; }
  addEventListener('load', measure); addEventListener('resize', measure); $$('img', track).forEach(function (i) { i.addEventListener('load', measure); });
  if (!reduce) {
    var atmVisible = false;
    new IntersectionObserver(function (es) { atmVisible = es[0].isIntersecting; }).observe(rail);
    (function loop() {
      if (atmVisible && !paused && !drag && half) {
        pos = rail.scrollLeft + 0.45; if (pos >= half) pos -= half; rail.scrollLeft = pos;
      }
      requestAnimationFrame(loop);
    })();
    rail.addEventListener('mouseenter', function () { paused = true; });
    rail.addEventListener('mouseleave', function () { paused = false; });
    rail.addEventListener('focus', function () { paused = true; }); rail.addEventListener('blur', function () { paused = false; });
    rail.addEventListener('touchstart', function () { paused = true; }, { passive: true });
    rail.addEventListener('touchend', function () { setTimeout(function () { paused = false; }, 2500); }, { passive: true });
    rail.addEventListener('scroll', function () { if (half && rail.scrollLeft >= half) rail.scrollLeft -= half; }, { passive: true });
  }
  rail.addEventListener('mousedown', function (e) { drag = { x: e.clientX, l: rail.scrollLeft }; rail.style.cursor = 'grabbing'; });
  addEventListener('mouseup', function () { drag = null; rail.style.cursor = ''; });
  addEventListener('mousemove', function (e) { if (drag) rail.scrollLeft = drag.l - (e.clientX - drag.x); });

  /* ---------- 10. Отзывы ---------- */
  var R = C.reviews || [], slider = $('#revSlider'), prog = $('#revProg'), idx = $('#revIdx');
  slider.innerHTML = R.map(function (r) { return '<blockquote class="q"><p>' + esc(r.text) + '</p><footer><b>' + esc(r.name) + '</b><i></i><span>' + esc(r.src || '') + '</span></footer></blockquote>'; }).join('');
  function revPos() { var w = slider.clientWidth || 1, i = Math.round(slider.scrollLeft / w); idx.textContent = pad(i + 1) + ' / ' + pad(R.length); prog.style.width = ((i + 1) / R.length * 100) + '%'; }
  slider.addEventListener('scroll', revPos, { passive: true });
  $('#revPrev').addEventListener('click', function () { slider.scrollBy({ left: -slider.clientWidth, behavior: 'smooth' }); });
  $('#revNext').addEventListener('click', function () {
    var end = slider.scrollLeft + slider.clientWidth >= slider.scrollWidth - 4;
    if (end) slider.scrollTo({ left: 0, behavior: 'smooth' }); else slider.scrollBy({ left: slider.clientWidth, behavior: 'smooth' });
  });
  revPos();

  /* ---------- 11. Форма записи ---------- */
  var form = $('#form'), status = $('#status'), dateEl = $('#f-date');
  var today = new Date(); today.setMinutes(today.getMinutes() - today.getTimezoneOffset());
  var todayStr = today.toISOString().slice(0, 10); dateEl.min = todayStr;
  function digits(s) { return String(s).replace(/\D/g, ''); }
  function normPhone(v) { var d = digits(v); if (d.length === 11 && (d[0] === '7' || d[0] === '8')) d = d.slice(1); return d.length === 10 ? d : null; }
  function fmtPhone(d) { return '+7 ' + d.slice(0, 3) + ' ' + d.slice(3, 6) + '-' + d.slice(6, 8) + '-' + d.slice(8); }
  $('#f-phone').addEventListener('blur', function () { var d = normPhone(this.value); if (d) this.value = fmtPhone(d); });
  function setErr(name, msg) {
    var el = $('[data-err="' + name + '"]', form); if (!el) return; el.textContent = msg || '';
    var f = el.closest('.f'); if (f) f.classList.toggle('bad', !!msg);
  }
  function validate() {
    var ok = true, v = form.elements;
    var name = v.name.value.trim();
    if (name.length < 2) { setErr('name', 'Подскажите, как вас зовут'); ok = false; } else setErr('name', '');
    if (!normPhone(v.phone.value)) { setErr('phone', 'Введите номер полностью, например +7 900 000-00-00'); ok = false; } else setErr('phone', '');
    if (v.date.value && v.date.value < todayStr) { setErr('date', 'Выберите сегодняшнюю или более позднюю дату'); ok = false; } else setErr('date', '');
    if (!v.consent.checked) { setErr('consent', 'Нужно согласие на обработку данных'); ok = false; } else setErr('consent', '');
    return ok;
  }
  $$('input,textarea', form).forEach(function (el) { el.addEventListener('input', function () { var n = el.name; if (n && $('[data-err="' + n + '"]', form)) { var f = el.closest('.f'); if (f) { f.classList.remove('bad'); $('.err', f).textContent = ''; } } }); });
  function dateRu(s) { if (!s) return 'не указана'; var p = s.split('-'); return p[2] + '.' + p[1] + '.' + p[0]; }
  function utm() { var o = {}; new URLSearchParams(location.search).forEach(function (v, k) { if (/^(utm_|yclid|gclid|fbclid)/.test(k)) o[k] = v; }); return o; }
  function showStatus(kind, title, text, btns) {
    status.hidden = false; status.className = 'status status--' + kind;
    status.innerHTML = '<h3>' + esc(title) + '</h3><p>' + esc(text) + '</p><div class="status__btns">' + (btns || '') + '</div>';
    status.scrollIntoView({ block: 'nearest', behavior: reduce ? 'auto' : 'smooth' });
  }
  var tel = '<a class="btn btn--dark" href="tel:' + esc(CT.phoneHref || '') + '"><span>Позвонить</span></a>';
  form.addEventListener('submit', function (e) {
    e.preventDefault();
    if (form.elements.company.value) return; // ловушка для ботов
    if (!validate()) { var bad = $('.f.bad input,.f.bad textarea', form); if (bad) bad.focus(); return; }
    var v = form.elements, d = normPhone(v.phone.value);
    var data = { name: v.name.value.trim(), phone: fmtPhone(d), direction: v.direction.value, date: v.date.value, comment: v.comment.value.trim(), page: location.href.split('#')[0], utm: utm(), ts: new Date().toISOString() };
    var txt = 'Заявка на примерку\nИмя: ' + data.name + '\nТелефон: ' + data.phone + '\nНаправление: ' + data.direction + '\nДата: ' + dateRu(data.date) + (data.comment ? '\nКомментарий: ' + data.comment : '');
    var endpoint = (C.lead && C.lead.endpoint) || '';
    if (!endpoint) {
      var msg = [
        CT.whatsapp ? '<a class="btn btn--dark" href="' + esc(CT.whatsapp) + '" target="_blank" rel="noopener"><span>WhatsApp</span></a>' : '',
        CT.telegramChat ? '<a class="btn btn--dark" href="' + esc(CT.telegramChat) + '" target="_blank" rel="noopener"><span>Telegram</span></a>' : '',
        CT.max ? '<a class="btn btn--dark" href="' + esc(CT.max) + '" target="_blank" rel="noopener"><span>Max</span></a>' : '',
        CT.telegram ? '<a class="btn btn--line" href="' + esc(CT.telegram) + '" target="_blank" rel="noopener"><span>Телеграм-канал</span></a>' : ''
      ].filter(Boolean).join('');
      showStatus('err', 'Заявка пока не отправлена', 'Онлайн-приём заявок ещё не подключён, поэтому ваши данные никуда не переданы. Позвоните нам или напишите в мессенджер — мы подберём время.',
        tel + msg + '<button type="button" class="btn btn--line" id="copyReq"><span>Скопировать заявку</span></button>');
      var cb = $('#copyReq'); if (cb) cb.addEventListener('click', function () {
        var done = function () { cb.querySelector('span').textContent = 'Скопировано'; };
        if (navigator.clipboard) navigator.clipboard.writeText(txt).then(done, function () { window.prompt('Скопируйте текст заявки:', txt); }); else window.prompt('Скопируйте текст заявки:', txt);
      });
      return;
    }
    var btn = $('#submit'); btn.disabled = true; btn.querySelector('span').textContent = 'Отправляем…';
    var ctl = ('AbortController' in window) ? new AbortController() : null, to = setTimeout(function () { if (ctl) ctl.abort(); }, 12000);
    fetch(endpoint, { method: (C.lead && C.lead.method) || 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(data), signal: ctl ? ctl.signal : undefined })
      .then(function (r) { if (!r.ok) throw new Error(r.status); form.reset(); $$('.f.bad', form).forEach(function (f) { f.classList.remove('bad'); }); showStatus('ok', 'Спасибо, заявка отправлена', 'Мы свяжемся с вами по номеру ' + data.phone + ' и подтвердим время примерки.', ''); })
      .catch(function () { showStatus('err', 'Не удалось отправить заявку', 'Проверьте соединение и попробуйте ещё раз или позвоните нам — мы запишем вас по телефону.', tel); })
      .then(function () { clearTimeout(to); btn.disabled = false; btn.querySelector('span').textContent = 'Записаться'; });
  });

  /* ---------- 12. Диалоги ---------- */
  $$('[data-dlg]').forEach(function (b) { b.addEventListener('click', function () { var d = $('#dlg-' + b.getAttribute('data-dlg')); if (d && d.showModal) d.showModal(); }); });
  $$('.dlg').forEach(function (d) { d.addEventListener('click', function (e) { if (e.target === d) d.close(); }); });
})();
