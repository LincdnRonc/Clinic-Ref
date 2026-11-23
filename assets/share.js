// Floating Share button: link, copy, native share and an on-device QR code (assets/qrcode.js, MIT, Kazuhiko Arase).
(function(){
  if (document.querySelector('.sharewrap')) return;
  var base = (document.querySelector('script[src$="share.js"]').getAttribute('src') || '').replace(/share\.js$/, '');
  // Hidden for the rest of this browser session if dismissed with its ×
  try { if (sessionStorage.getItem('qr-share-hidden')) return; } catch(e) {}
  var wrap = document.createElement('div'); wrap.className = 'sharewrap';
  var btn = document.createElement('button');
  btn.type = 'button'; btn.className = 'sharebtn'; btn.setAttribute('aria-haspopup', 'dialog'); btn.title = 'Share this page (link and QR code)';
  btn.innerHTML = '<svg viewBox="0 0 24 24" width="24" height="24" aria-hidden="true" fill="currentColor"><path d="M3 3h7v7H3zm2 2v3h3V5zM14 3h7v7h-7zm2 2v3h3V5zM3 14h7v7H3zm2 2v3h3v-3z"/><path d="M14 14h2v2h-2zM18 14h3v2h-3zM16 16h2v2h-2zM14 18h2v3h-2zM18 18h3v3h-3z"/></svg><span>Share</span>';
  var hide = document.createElement('button');
  hide.type = 'button'; hide.className = 'sharehide'; hide.setAttribute('aria-label', 'Hide the Share button'); hide.title = 'Hide (comes back next visit)'; hide.textContent = '×';
  wrap.appendChild(btn); wrap.appendChild(hide);
  document.body.appendChild(wrap);

  var pop = document.createElement('div');
  pop.className = 'sharepop'; pop.setAttribute('role', 'dialog'); pop.setAttribute('aria-label', 'Share this page'); pop.hidden = true;
  pop.innerHTML = '<div class="sp-head"><b>Share this page</b><button type="button" class="sp-x" aria-label="Close">×</button></div>'
    + '<div class="sp-qr" aria-label="QR code for this page"></div>'
    + '<input class="sp-url" type="text" readonly aria-label="Page link">'
    + '<div class="sp-btns"><button type="button" class="sp-copy">Copy link</button><button type="button" class="sp-native" hidden>Share…</button></div>'
    + '<label class="sp-opt"><input type="checkbox" class="sp-tab" checked> Open on this tab</label>'
    + '<p class="sp-note">The site still asks for the password.</p>';
  document.body.appendChild(pop);
  var url = pop.querySelector('.sp-url'), qr = pop.querySelector('.sp-qr'), keepTab = pop.querySelector('.sp-tab');
  var nat = pop.querySelector('.sp-native');
  if (navigator.share) nat.hidden = false;

  function link(){ var u = location.href.split('#')[0].split('?')[0]; return keepTab.checked && location.hash ? u + location.hash : u; }
  function loadQR(cb){
    if (window.qrcode) return cb();
    var s = document.createElement('script'); s.src = base + 'qrcode.js'; s.onload = cb; s.onerror = function(){ qr.textContent = 'QR code unavailable offline.'; };
    document.head.appendChild(s);
  }
  function render(){
    var u = link(); url.value = u;
    loadQR(function(){
      try { var q = qrcode(0, 'M'); q.addData(u); q.make(); qr.innerHTML = q.createSvgTag({cellSize: 4, margin: 2, scalable: true}); }
      catch(e){ qr.textContent = 'Link too long for a QR code.'; }
    });
  }
  function open(){ render(); pop.hidden = false; btn.setAttribute('aria-expanded', 'true'); pop.querySelector('.sp-copy').focus(); }
  function close(){ pop.hidden = true; btn.setAttribute('aria-expanded', 'false'); }
  btn.addEventListener('click', function(){ pop.hidden ? open() : close(); });
  pop.querySelector('.sp-x').addEventListener('click', close);
  hide.addEventListener('click', function(){ close(); wrap.remove(); pop.remove(); try { sessionStorage.setItem('qr-share-hidden', '1'); } catch(e) {} });
  keepTab.addEventListener('change', render);
  window.addEventListener('hashchange', function(){ if (!pop.hidden) render(); });
  document.addEventListener('keydown', function(e){ if (e.key === 'Escape' && !pop.hidden) { close(); btn.focus(); } });
  document.addEventListener('click', function(e){ if (!pop.hidden && !pop.contains(e.target) && !btn.contains(e.target)) close(); });
  pop.querySelector('.sp-copy').addEventListener('click', function(){
    var b = this, done = function(){ b.textContent = 'Copied'; setTimeout(function(){ b.textContent = 'Copy link'; }, 1500); };
    if (navigator.clipboard && navigator.clipboard.writeText) navigator.clipboard.writeText(url.value).then(done, function(){ url.select(); document.execCommand('copy'); done(); });
    else { url.select(); document.execCommand('copy'); done(); }
  });
  nat.addEventListener('click', function(){ navigator.share({title: document.title, url: url.value}).catch(function(){}); });
})();
