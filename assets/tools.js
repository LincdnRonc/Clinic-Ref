// Calculators (linear-quadratic model). Education and cross-checking only.
(function(){
  function v(id){ var e=document.getElementById(id); return e?parseFloat(e.value):NaN; }
  function f(x,d){ return isFinite(x)?x.toFixed(d===undefined?1:d):'–'; }
  function bed(D,n,ab){ var d=D/n; return D*(1+d/ab); }
  function eqd2(D,n,ab){ var d=D/n; return D*(d+ab)/(2+ab); }
  function set(id,h){ var e=document.getElementById(id); if(e) e.innerHTML=h; }
  function one(){
    var D=v('c1D'),n=v('c1n'),ab=v('c1ab');
    if(!(D>0&&n>0&&ab>0)) return set('c1out','Enter total dose, fractions and α/β.');
    var h='<b>EQD2 '+f(eqd2(D,n,ab))+' Gy</b> · BED '+f(bed(D,n,ab))+' Gy<sub>'+ab+'</sub> · '+f(D/n,2)+' Gy per fraction';
    var nn=v('c1n2');
    if(nn>0){ // isoeffective total dose in nn fractions: solve D2 + D^2/(nn*ab) = BED
      var B=bed(D,n,ab), D2=(-1+Math.sqrt(1+4*B/(nn*ab)))*nn*ab/2;
      h+='<br>Same BED in '+nn+' fractions: <b>'+f(D2)+' Gy</b> ('+f(D2/nn,2)+' Gy per fraction)';
    }
    set('c1out',h);
  }
  function cum(){
    var ab=v('c2ab'), tot=0, rows=[], ok=false;
    for(var i=1;i<=4;i++){
      var D=v('c2D'+i),n=v('c2n'+i),rec=v('c2r'+i); if(!(D>0&&n>0)) continue; ok=true;
      var e=eqd2(D,n,ab), keep=e*(1-(rec>0?rec:0)/100); tot+=keep;
      rows.push('Course '+i+': EQD2 '+f(e)+' Gy'+(rec>0?' → '+f(keep)+' Gy after '+rec+'% recovery':''));
    }
    if(!(ok&&ab>0)) return set('c2out','Enter at least one course and α/β.');
    var lim=v('c2lim'), h=rows.join('<br>')+'<br><b>Cumulative EQD2 '+f(tot)+' Gy<sub>'+ab+'</sub></b>';
    if(lim>0){ var rem=lim-tot; h+='<br>Limit '+f(lim)+' Gy: '+(rem>=0?'<b>'+f(rem)+' Gy EQD2 remaining</b>':'<b class="warn">exceeded by '+f(-rem)+' Gy</b>');
      var nn=v('c2n5'); if(rem>0&&nn>0){ var B=rem*(1+2/ab), D2=(-1+Math.sqrt(1+4*B/(nn*ab)))*nn*ab/2; h+='<br>Remaining as a point dose in '+nn+' fractions: <b>'+f(D2)+' Gy</b> ('+f(D2/nn,2)+' Gy per fraction)'; } }
    set('c2out',h);
  }
  function gap(){
    var D=v('c3D'),n=v('c3n'),ab=v('c3ab'),T=v('c3T'),T2=v('c3T2'),K=v('c3K'),Tk=v('c3Tk');
    if(!(D>0&&n>0&&ab>0&&T>0&&T2>0)) return set('c3out','Enter the prescription, planned and actual overall time.');
    var B=bed(D,n,ab), lossPlan=K*Math.max(0,T-Tk), lossAct=K*Math.max(0,T2-Tk), extra=lossAct-lossPlan;
    var h='Planned tumour BED '+f(B)+' Gy<sub>'+ab+'</sub>; time-corrected '+f(B-lossPlan)+' Gy as planned, <b>'+f(B-lossAct)+' Gy</b> with the gap.';
    h+='<br>BED lost to the extra '+f(T2-T,0)+' days: <b>'+f(extra)+' Gy<sub>'+ab+'</sub></b> (about '+f(extra/(1+2/ab))+' Gy EQD2).';
    set('c3out',h);
  }
  document.addEventListener('input',function(e){ var id=e.target.id||''; if(id.indexOf('c1')===0) one(); else if(id.indexOf('c2')===0) cum(); else if(id.indexOf('c3')===0) gap(); });
  one(); cum(); gap();
})();
