// Floating Share button: link, copy, native share and an on-device QR code (assets/qrcode.js, MIT, Kazuhiko Arase).
(function(){
  if (document.querySelector('.sharebtn')) return;
  var base = (document.querySelector('script[src$="share.js"]').getAttribute('src') || '').replace(/share\.js$/, '');
  var btn = document.createElement('button');
  btn.type = 'button'; btn.className = 'sharebtn'; btn.setAttribute('aria-haspopup', 'dialog'); btn.title = 'Share this page';
  btn.innerHTML = '<svg viewBox="0 0 24 24" width="20" height="20" aria-hidden="true"><circle cx="17.5" cy="5.5" r="2.5" fill="currentColor"/><circle cx="6.5" cy="12" r="2.5" fill="currentColor"/><circle cx="17.5" cy="18.5" r="2.5" fill="currentColor"/><path d="M8.7 10.8l6.6-4M8.7 13.2l6.6 4" stroke="currentColor" stroke-width="1.8"/></svg><span>Share</span>';
  document.body.appendChild(btn);

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
