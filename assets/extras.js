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
    row.appendChild(btns);
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
      s.onload=function(){ var w=waiters; waiters=[]; w.forEach(function(c){load(c);}); }; document.head.appendChild(s);
    }
    function run(){
      var v=gq.value.trim().toLowerCase();
      if(v.length<2){ out.hidden=true; out.innerHTML=''; homebody.hidden=false; return; }
      load(function(){
        if(gq.value.trim().toLowerCase()!==v) return;
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
