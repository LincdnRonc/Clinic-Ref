// Trial tables tab: filter trials by text and "need to know" (Rad Onc Tables, Estes).
(function(){
  document.querySelectorAll('section[data-src="estes"]').forEach(function(p){
    var box = p.querySelector('.et-filter'), only = p.querySelector('.et-only');
    if(!box) return;
    function run(){
      var q = box.value.trim().toLowerCase(), k = only && only.checked;
      p.querySelectorAll('article.card').forEach(function(c){
        var tr = c.querySelectorAll('.trial.et'); if(!tr.length){ c.style.display = (q||k) ? 'none' : ''; return; }
        var shown = 0;
        tr.forEach(function(t){
          var ok = (!k || t.classList.contains('et-k')) && (!q || t.textContent.toLowerCase().indexOf(q) > -1);
          t.classList.toggle('et-hide', !ok); if(ok) shown++;
        });
        c.style.display = shown ? '' : 'none';
      });
    }
    box.addEventListener('input', run); if(only) only.addEventListener('change', run);
  });
})();
