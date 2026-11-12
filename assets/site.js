// All-pages menu: always open on wide screens, collapsed on phones
(function(){
  var m = document.querySelector('details.menu'); if(!m) return;
  var mq = window.matchMedia('(min-width:1100px)');
  function sync(){ if(mq.matches) m.open = true; }
  sync(); if(mq.addEventListener) mq.addEventListener('change', sync);
  var top = document.querySelector('.top');
  function setTop(){ if(top) document.documentElement.style.setProperty('--side-top', top.offsetHeight + 'px'); }
  setTop(); window.addEventListener('resize', setTop);
  var cur = m.querySelector('[aria-current="page"]');
  if(cur && mq.matches){ var side = m.closest('.side'); if(side) side.scrollTop = Math.max(0, cur.offsetTop - 120); }
})();

(function(){
  if(!document.getElementById('chips')) return;
  var KEY = 'qr-tab:' + (location.pathname.split('/').pop() || 'index');
  var panels = Array.prototype.slice.call(document.querySelectorAll('.panel'));
  var chips = document.getElementById('chips');
  var q = document.getElementById('q');
  var body = document.body;
  var tabs = panels.map(function(p){return p.getAttribute('data-tab');});

  // Build chips and per-panel jump lists
  panels.forEach(function(p){
    var b = document.createElement('button');
    b.className = 'chip'; b.type = 'button'; b.setAttribute('role','tab');
    b.id = 'chip-' + p.dataset.tab; b.textContent = p.dataset.label;
    b.setAttribute('aria-controls', p.id);
    b.addEventListener('click', function(){ clearSearch(); show(p.dataset.tab, true); window.scrollTo({top:0}); });
    chips.appendChild(b);
    var jump = p.querySelector('.jump');
    p.querySelectorAll('.card').forEach(function(c){
      var label = document.createElement('span');
      label.className = 'site'; label.textContent = p.dataset.label;
      c.querySelector('h3').appendChild(label);
      if(!jump) return;
      var j = document.createElement('button');
      j.type = 'button'; j.textContent = c.dataset.title;
      j.addEventListener('click', function(){ c.scrollIntoView({behavior: matchMedia('(prefers-reduced-motion: reduce)').matches ? 'auto':'smooth', block:'start'}); });
      jump.appendChild(j);
    });
  });

  function show(tab, push){
    if(tabs.indexOf(tab) < 0) tab = tabs[0];
    panels.forEach(function(p){ p.hidden = p.dataset.tab !== tab; });
    chips.querySelectorAll('.chip').forEach(function(c){
      var on = c.id === 'chip-' + tab;
      c.setAttribute('aria-selected', on ? 'true' : 'false');
      if(on && c.scrollIntoView) c.scrollIntoView({block:'nearest', inline:'center'});
    });
    if(push){ try{ history.replaceState(null,'','#'+tab); }catch(e){ location.hash = tab; } }
    try{ localStorage.setItem(KEY, tab); }catch(e){}
  }

  // Search with highlighting
  var originals = new Map();
  document.querySelectorAll('.card').forEach(function(c){ originals.set(c, c.innerHTML); });
  function unmark(){ originals.forEach(function(html, c){ if(c.dataset.marked){ c.innerHTML = html; delete c.dataset.marked; } }); }
  function markIn(node, terms){
    var walker = document.createTreeWalker(node, NodeFilter.SHOW_TEXT, null);
    var texts = []; while(walker.nextNode()) texts.push(walker.currentNode);
    var re = new RegExp('(' + terms.map(function(t){return t.replace(/[.*+?^${}()|[\]\\]/g,'\\$&');}).join('|') + ')','gi');
    texts.forEach(function(t){
      if(!re.test(t.nodeValue)) return; re.lastIndex = 0;
      var span = document.createElement('span');
      span.innerHTML = t.nodeValue.replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(re,'<mark>$1</mark>');
      t.parentNode.replaceChild(span, t);
    });
  }
  function run(){
    var v = q.value.trim().toLowerCase();
    unmark();
    var cards = document.querySelectorAll('.card');
    if(v.length < 2){
      body.classList.remove('searching','noresults');
      cards.forEach(function(c){ c.classList.remove('hide'); });
      var cur = (location.hash||'').slice(1); show(tabs.indexOf(cur)>=0?cur:(stored()||tabs[0]), false);
      return;
    }
    body.classList.add('searching');
    panels.forEach(function(p){ p.hidden = false; });
    chips.querySelectorAll('.chip').forEach(function(c){ c.setAttribute('aria-selected','false'); });
    var terms = v.split(/\s+/).filter(Boolean);
    var hits = 0;
    cards.forEach(function(c){
      var txt = c.textContent.toLowerCase();
      var ok = terms.every(function(t){ return txt.indexOf(t) >= 0; });
      c.classList.toggle('hide', !ok);
      if(ok){ hits++; markIn(c, terms); c.dataset.marked = '1'; }
    });
    body.classList.toggle('noresults', hits === 0);
  }
  function clearSearch(){ if(q.value){ q.value=''; run(); } }
  function stored(){ try{ return localStorage.getItem(KEY); }catch(e){ return null; } }
  q.addEventListener('input', run);
  document.getElementById('clear').addEventListener('click', function(){ q.value=''; run(); q.focus(); });
  document.getElementById('searchForm').addEventListener('submit', function(e){ e.preventDefault(); q.blur(); });
  window.addEventListener('hashchange', function(){ var h=(location.hash||'').slice(1); if(tabs.indexOf(h)>=0){ clearSearch(); show(h,false);} });

  var start = (location.hash||'').slice(1);
  show(tabs.indexOf(start)>=0 ? start : (stored() || tabs[0]), false);
})();
