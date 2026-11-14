// Reirradiation calculators: remaining OAR dose and spinal cord checks. Arithmetic only.
(function(){
  function num(box,k){var e=box.querySelector('[data-k="'+k+'"]');return e?parseFloat(e.value):NaN;}
  function eqd2(D,n,ab){return D*((D/n)+ab)/(2+ab);}
  function bed(D,n,ab){return D*(1+(D/n)/ab);}
  function f(x){return (Math.round(x*10)/10).toFixed(1);}
  function tick(ok){return ok?'<span class="flag new">within</span>':'<span class="flag caution">outside</span>';}
  function rem(box,out){
    var D1=num(box,'D1'),n1=num(box,'n1'),ab=num(box,'ab'),rec=num(box,'rec'),lim=num(box,'lim'),n2=num(box,'n2');
    if(!(D1>=0&&n1>0&&ab>0&&lim>=0&&n2>0)||isNaN(rec)){out.innerHTML='Enter all values.';return;}
    var e1=eqd2(D1,n1,ab), eff=e1*(1-rec/100), R=lim-eff;
    if(R<=0){out.innerHTML='Prior dose <b>'+f(e1)+' Gy EQD2</b>'+(rec?' ('+f(eff)+' Gy after '+rec+'% recovery)':'')+'. <b>No room left</b> under a '+f(lim)+' Gy limit.';return;}
    var D2=n2*(-ab+Math.sqrt(ab*ab+4*R*(2+ab)/n2))/2;
    out.innerHTML='Prior dose <b>'+f(e1)+' Gy EQD2</b>'+(rec?' ('+f(eff)+' Gy after '+rec+'% recovery)':'')+'. Remaining <b>'+f(R)+' Gy EQD2</b> = up to <b>'+f(D2)+' Gy in '+n2+' fraction'+(n2>1?'s':'')+'</b> ('+f(D2/n2)+' Gy per fraction) to this organ.';
  }
  function cord(box,out){
    var D1=num(box,'D1'),n1=num(box,'n1'),D2=num(box,'D2'),n2=num(box,'n2'),iv=num(box,'iv'),ab=num(box,'ab');
    if(!(D1>=0&&n1>0&&D2>=0&&n2>0&&iv>=0&&ab>0)){out.innerHTML='Enter all values.';return;}
    var b1=bed(D1,n1,ab),b2=bed(D2,n2,ab),bt=b1+b2;
    var e1=eqd2(D1,n1,2),e2=eqd2(D2,n2,2),et=e1+e2,ratio=et>0?e2/et:0;
    var nOK=bt<=135.5&&b1<=98&&b2<=98&&iv>=6, sOK=et<=70&&e2<=25&&ratio<=0.5&&iv>=5;
    var pts=(iv<6?4.5:0)+((e1>=51||e2>=51)?4.5:0)+(et>60?Math.ceil((et-60)/5):0);
    var grp=pts<=3?'low risk':(pts<=6?'intermediate risk':'high risk');
    var score='<br><b>Nieder risk score:</b> <b>'+pts+' point'+(pts===1?'':'s')+'</b> ('+grp+'; low 0–3, intermediate 4–6, high &gt;6)';
    out.innerHTML='<b>Nieder (conventional):</b> BED '+f(b1)+' + '+f(b2)+' = <b>'+f(bt)+' Gy<sub>'+ab+'</sub></b> (limit 135.5; each course ≤98; interval ≥6 months) '+tick(nOK)+(bt<=120&&nOK?' · within the 120 Gy<sub>2</sub> level with no reported myelopathy':'')+
      '<br><b>Sahgal (SBRT, thecal sac Dmax):</b> EQD2<sub>2</sub> '+f(e1)+' + '+f(e2)+' = <b>'+f(et)+' Gy</b> (≤70); SBRT course '+f(e2)+' Gy (≤25); share '+ratio.toFixed(2)+' (≤0.5); interval '+iv+' months (≥5) '+tick(sOK)+score;
  }
  function run(){
    document.querySelectorAll('[data-rr]').forEach(function(box){
      var k=box.getAttribute('data-rr'),out=document.querySelector('[data-rro="'+k+'"]'); if(!out)return;
      (k==='rem'?rem:cord)(box,out);
    });
  }
  document.addEventListener('input',run); document.addEventListener('change',run); run();
})();
