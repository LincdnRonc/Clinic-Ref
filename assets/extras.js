// Extras: pins, site-wide search, ?q= deep links, contour-now view, copy buttons, offline app
(function(){
  var inSub = /\/contouring\/[^\/]*$/.test(location.pathname);
  var ROOT = inSub ? '../' : '';
  var file = location.pathname.split('/').pop() || 'index.html';
  var rel = (inSub ? 'contouring/' : '') + file;
  function $(s,r){return (r||document).querySelector(s);}
  function $$(s,r){return Array.prototype.slice.call((r||document).querySelectorAll(s));}
  function esc(t){return t.replace(/&/g,'&amp;').replace(/</g,'&lt;');}

  // Offline app
  if('serviceWorker' in navigator && location.protocol.indexOf('http')===0){ navigator.serviceWorker.register(ROOT+'sw.js').catch(function(){}); }

  // Pins
  var PK='qr-pins';
  function pins(){ try{return JSON.parse(localStorage.getItem(PK)||'[]');}catch(e){return [];} }
  function savePins(p){ try{localStorage.setItem(PK,JSON.stringify(p));}catch(e){} }
  var row = $('.title-row'), chips = $('#chips');
  var btns = document.createElement('div'); btns.className='hdrbtns';
  if(row && chips){
    var meta = $('.meta',row); if(meta) btns.appendChild(meta);
    ($('.hdr-right',row)||row).appendChild(btns);
    var pb = document.createElement('button'); pb.type='button'; pb.className='hdrbtn';
    function curTab(){ var c=$('.chip[aria-selected="true"]'); return c?{id:c.id.replace('chip-',''),label:c.textContent}:null; }
    function key(){ var t=curTab(); return rel+(t?'#'+t.id:''); }
    function syncPin(){ var on=pins().some(function(p){return p.k===key();}); pb.textContent=on?'★ Pinned':'☆ Pin this tab'; pb.setAttribute('aria-pressed',on?'true':'false'); }
    pb.addEventListener('click',function(){
      var p=pins(), k=key(), i=p.findIndex(function(x){return x.k===k;});
      if(i>=0) p.splice(i,1); else { var t=curTab(); var h=$('h1'); var name=(h.firstChild.textContent||h.textContent).trim(); p.push({k:k,l:name+(t?' › '+t.label:'')}); }
      savePins(p); syncPin();
    });
    btns.appendChild(pb);
    chips.addEventListener('click',function(){ setTimeout(syncPin,0); }); window.addEventListener('hashchange',function(){setTimeout(syncPin,0);});
    setTimeout(syncPin,0);
  }
  var pinBox = $('#pinned');
  function drawPins(){
    if(!pinBox) return; var p=pins(); pinBox.hidden=!p.length; if(!p.length) return;
    pinBox.innerHTML='<h2>Pinned</h2><div class="pins">'+p.map(function(x,i){return '<span class="pin"><a href="'+x.k+'">'+esc(x.l)+'</a><button type="button" data-i="'+i+'" aria-label="Unpin">×</button></span>';}).join('')+'</div>';
  }
  if(pinBox){ drawPins(); pinBox.addEventListener('click',function(e){ var b=e.target.closest('button[data-i]'); if(!b) return; var p=pins(); p.splice(+b.dataset.i,1); savePins(p); drawPins(); }); }

  // ?q= deep link from site-wide search
  var q0 = new URLSearchParams(location.search).get('q'), qi = $('#q');
  if(q0 && qi){ qi.value=q0; qi.dispatchEvent(new Event('input')); }

  // Site-wide search (home page)
  var gq = $('#gq'), out = $('#gresults'), homebody = $('#homebody');
  if(gq && out){
    var loading=false, low=null, waiters=[];
    function load(cb){
      if(window.QR_INDEX){ if(!low) low=window.QR_INDEX.map(function(r){return (r[1]+' '+r[3]+' '+r[4]+' '+r[5]).toLowerCase();}); return cb(); }
      waiters.push(cb); if(loading) return; loading=true;
      var s=document.createElement('script'); s.src='assets/search-index.js';
      s.onload=function(){ unlock(function(){ var w=waiters; waiters=[]; w.forEach(function(c){load(c);}); }); }; document.head.appendChild(s);
    }
    // Live site: the index is encrypted (tools/encrypt_site.js); decrypt it with the key remembered at login.
    function unlock(cb){
      if(window.QR_INDEX || !window.QR_INDEX_ENC) return cb();
      function fail(){ window.QR_INDEX=[]; window.QR_LOCKED=true; cb(); }
      try{
        var hp=localStorage.getItem('staticrypt_passphrase'); if(!hp || !window.crypto || !crypto.subtle) return fail();
        var kb=new Uint8Array(hp.length/2); for(var i=0;i<kb.length;i++) kb[i]=parseInt(hp.substr(i*2,2),16);
        var raw=atob(window.QR_INDEX_ENC), b=new Uint8Array(raw.length); for(var j=0;j<raw.length;j++) b[j]=raw.charCodeAt(j);
        crypto.subtle.importKey('raw',kb,'AES-CBC',false,['decrypt'])
          .then(function(k){ return crypto.subtle.decrypt({name:'AES-CBC',iv:b.slice(0,16)},k,b.slice(16)); })
          .then(function(buf){ window.QR_INDEX=JSON.parse(new TextDecoder().decode(buf)); cb(); }, fail);
      }catch(e){ fail(); }
    }
    function run(){
      var v=gq.value.trim().toLowerCase();
      if(v.length<2){ out.hidden=true; out.innerHTML=''; homebody.hidden=false; return; }
      load(function(){
        if(gq.value.trim().toLowerCase()!==v) return;
        if(window.QR_LOCKED){ out.innerHTML='<p class="gcount">Search needs “Remember me on this device”. Tap Log out (top right), then log in again with it ticked.</p>'; out.hidden=false; homebody.hidden=true; return; }
        var terms=v.split(/\s+/), hits=[];
        for(var i=0;i<low.length;i++){
          var t=low[i]; if(!terms.every(function(x){return t.indexOf(x)>=0;})) continue;
          var r=window.QR_INDEX[i], head=(r[1]+' '+r[3]+' '+r[4]).toLowerCase(), sc=0;
          terms.forEach(function(x){ if(head.indexOf(x)>=0) sc+=5; if(r[4].toLowerCase().indexOf(x)>=0) sc+=5; });
          if(r[0].indexOf('contouring/')===0) sc+=1;
          hits.push([sc,i]);
        }
        hits.sort(function(a,b){return b[0]-a[0]||a[1]-b[1];});
        var re=new RegExp('('+terms.map(function(t){return t.replace(/[.*+?^${}()|[\]\\]/g,'\\$&');}).join('|')+')','gi');
        var h='<p class="gcount">'+hits.length+' card'+(hits.length===1?'':'s')+' match'+(hits.length>60?' (first 60 shown)':'')+'</p>';
        hits.slice(0,60).forEach(function(x){
          var r=window.QR_INDEX[x[1]], txt=r[5], p=txt.toLowerCase().indexOf(terms[0]), a=Math.max(0,p-60);
          var snip=(a>0?'…':'')+txt.slice(a,a+200)+(a+200<txt.length?'…':'');
          h+='<a class="gres" href="'+r[0]+'?q='+encodeURIComponent(v)+'#'+r[2]+'"><span class="where">'+esc(r[1])+' › '+esc(r[3])+'</span><b>'+esc(r[4]).replace(re,'<mark>$1</mark>')+'</b><span class="snip">'+esc(snip).replace(re,'<mark>$1</mark>')+'</span></a>';
        });
        out.innerHTML=h; out.hidden=false; homebody.hidden=true;
      });
    }
    gq.addEventListener('input',run); gq.addEventListener('focus',function(){load(function(){});});
    $('#gclear').addEventListener('click',function(){gq.value='';run();gq.focus();});
    if(location.hash==='#search') gq.focus();
  }

  // Copy buttons on tables
  $$('.tw').forEach(function(tw){
    var tb=$('table',tw); if(!tb||tb.classList.contains('toc')) return;
    var bar=document.createElement('div'); bar.className='twbar';
    bar.innerHTML='<button type="button" class="cpy">Copy table</button>'; tw.insertBefore(bar,tw.firstChild);
  });
  document.addEventListener('click',function(e){
    var b=e.target.closest('.cpy'); if(!b) return;
    var tb=b.closest('.tw').querySelector('table');
    var txt=$$('tr',tb).map(function(tr){return $$('th,td',tr).map(function(c){return c.innerText.replace(/\s+/g,' ').trim();}).join('\t');}).join('\n');
    function done(){ b.textContent='Copied'; setTimeout(function(){b.textContent='Copy table';},1500); }
    if(navigator.clipboard&&navigator.clipboard.writeText) navigator.clipboard.writeText(txt).then(done,fallback); else fallback();
    function fallback(){ var ta=document.createElement('textarea'); ta.value=txt; document.body.appendChild(ta); ta.select(); try{document.execCommand('copy');done();}catch(x){} ta.remove(); }
  });

  // Contour-now view on contouring guides
  if(document.body.classList.contains('proto') && chips){
    var cb=document.createElement('button'); cb.type='button'; cb.className='hdrbtn'; cb.textContent='Contour now';
    cb.title='Borders, margins, steps and diagrams only';
    btns.insertBefore(cb,btns.querySelector('.hdrbtn'));
    $$('.panel').forEach(function(p){
      if(/^(overview)$/.test(p.dataset.tab) || /pearls|references|guideline comparison|sources/i.test(p.dataset.label)) p.classList.add('cn-skip');
      $$('.card',p).forEach(function(c){ if(!c.querySelector('.tw table:not(.toc), figure, .fig, ol.steps, .callout.follow')) c.classList.add('cn-hide'); });
      if(!p.querySelector('.card:not(.cn-hide)')) p.classList.add('cn-skip');
    });
    function setCN(on){
      document.body.classList.toggle('cn',on); cb.setAttribute('aria-pressed',on?'true':'false'); cb.textContent=on?'Full guide':'Contour now';
      var u=new URL(location.href); if(on) u.searchParams.set('view','contour'); else u.searchParams.delete('view');
      try{history.replaceState(null,'',u);}catch(e){}
      $$('.panel.cn-skip').forEach(function(p){ var c=document.getElementById('chip-'+p.dataset.tab); if(c) c.style.display=on?'none':''; });
      window.dispatchEvent(new Event('resize'));
    }
    cb.addEventListener('click',function(){ setCN(!document.body.classList.contains('cn')); });
    chips.addEventListener('click',function(e){
      if(!document.body.classList.contains('cn')) return;
      var c=e.target.closest('.chip'); if(!c) return;
      e.stopImmediatePropagation(); e.preventDefault();
      var p=document.getElementById(c.getAttribute('aria-controls'));
      if(p && !p.classList.contains('cn-skip')){ var y=p.getBoundingClientRect().top+window.scrollY-($('.top').offsetHeight+8); window.scrollTo({top:y}); }
    },true);
    if(new URLSearchParams(location.search).get('view')==='contour') setCN(true);
  }
})();

// Back to top: floating button, shown after scrolling down
(function(){
  var b=document.createElement('button'); b.type='button'; b.className='totop'; b.setAttribute('aria-label','Back to top'); b.title='Back to top';
  b.innerHTML='<span aria-hidden="true">↑</span><span class="totop-l">Top</span>';
  b.addEventListener('click',function(){ var r=window.matchMedia&&window.matchMedia('(prefers-reduced-motion: reduce)').matches; window.scrollTo({top:0,behavior:r?'auto':'smooth'}); var f=document.querySelector('h1'); if(f){ f.setAttribute('tabindex','-1'); f.focus({preventScroll:true}); } });
  document.body.appendChild(b);
  var tick=false;
  function upd(){ tick=false; b.classList.toggle('show', window.scrollY>400); }
  window.addEventListener('scroll',function(){ if(!tick){ tick=true; requestAnimationFrame(upd); } },{passive:true});
  upd();
})();

// Favourite clinic links (links.html): star a link to keep it in a Favourites card at the top of its tab.
// Stored in this browser only (localStorage), like pins.
(function(){
  var lists = document.querySelectorAll('ul.qlinks');
  if(!lists.length) return;
  var FK = 'qr-link-favs';
  function favs(){ try{return JSON.parse(localStorage.getItem(FK)||'[]');}catch(e){return [];} }
  function saveFavs(f){ try{localStorage.setItem(FK,JSON.stringify(f));}catch(e){} }
  function sync(){
    var f = favs();
    Array.prototype.forEach.call(document.querySelectorAll('.qlinks .fav'), function(b){
      var on = f.indexOf(b.dataset.href) >= 0;
      b.textContent = on ? '★' : '☆';
      b.classList.toggle('on', on);
      b.setAttribute('aria-pressed', on ? 'true' : 'false');
      b.setAttribute('aria-label', on ? 'Remove from favourites' : 'Add to favourites');
      b.title = on ? 'Remove from favourites' : 'Add to favourites';
    });
  }
  // Stars are built into each link by build.py; add an (initially empty) Favourites card to each tab with links
  var panels = Array.prototype.filter.call(document.querySelectorAll('section.panel'), function(p){ return p.querySelector('ul.qlinks'); });
  panels.forEach(function(p){
    var card = document.createElement('article'); card.className='card favcard'; card.hidden=true;
    card.innerHTML = '<h3>★ Favourites</h3><ul class="qlinks qfav"></ul>';
    var head = p.querySelector('.panel-head');
    p.insertBefore(card, head ? head.nextSibling : p.firstChild);
  });
  function draw(){
    var f = favs();
    panels.forEach(function(p){
      var card = p.querySelector('.favcard');
      card.innerHTML = '<h3>★ Favourites</h3><ul class="qlinks qfav"></ul>';
      var ul = card.querySelector('ul');
      var seen = {};
      // keep the order in which links were starred
      f.forEach(function(h){
        if(seen[h]) return;
        var src = p.querySelector('ul.qlinks:not(.qfav) .fav[data-href="'+(window.CSS&&CSS.escape?CSS.escape(h):h.replace(/"/g,'\\"'))+'"]');
        if(!src) return; seen[h]=1;
        var li = src.parentNode.cloneNode(true); ul.appendChild(li);
      });
      card.hidden = !ul.children.length;
    });
    sync();
  }
  document.addEventListener('click', function(e){
    var b = e.target.closest && e.target.closest('.qlinks .fav'); if(!b) return;
    e.preventDefault();
    var f = favs(), h = b.dataset.href, i = f.indexOf(h);
    if(i >= 0) f.splice(i,1); else f.push(h);
    saveFavs(f); draw();
  });
  window.addEventListener('storage', function(e){ if(e.key===FK) draw(); });
  // The page search restores cards from saved copies; redraw so stars and Favourites stay right
  var q = document.getElementById('q'); if(q) q.addEventListener('input', function(){ setTimeout(draw,0); });
  draw();
})();
