// Clinical scores and calculators. Definitions entered from standard published criteria; verify before use.
(function(){
  function el(id){return document.getElementById(id);}
  function num(id){var e=el(id);return e?parseFloat(e.value):NaN;}
  function sel(id){var e=el(id);return e?e.value:'';}
  function f(x,d){return isFinite(x)?x.toFixed(d===undefined?1:d):'–';}
  function out(id,h){var e=el(id);if(e)e.innerHTML=h;}
  // ---- additive point scores, rendered from definitions ----
  var S={
   childpugh:{items:[
     ['Bilirubin',[['<34 µmol/L (<2 mg/dL)',1],['34–50 µmol/L (2–3 mg/dL)',2],['>50 µmol/L (>3 mg/dL)',3]]],
     ['Albumin',[['>35 g/L',1],['28–35 g/L',2],['<28 g/L',3]]],
     ['INR',[['<1.7',1],['1.7–2.3',2],['>2.3',3]]],
     ['Ascites',[['None',1],['Mild / diuretic-controlled',2],['Moderate–severe / refractory',3]]],
     ['Encephalopathy',[['None',1],['Grade 1–2',2],['Grade 3–4',3]]]],
     read:function(t){return 'Child-Pugh <b>'+(t<=6?'A':t<=9?'B':'C')+t+'</b> ('+t+' points; A 5–6, B 7–9, C 10–15)';}},
   capra:{items:[
     ['Age',[['<50',0],['≥50',1]]],
     ['PSA (ng/mL)',[['≤6',0],['6.1–10',1],['10.1–20',2],['20.1–30',3],['>30',4]]],
     ['Biopsy Gleason pattern',[['No pattern 4 or 5',0],['Secondary pattern 4 or 5',1],['Primary pattern 4 or 5',3]]],
     ['Clinical T stage',[['T1–T2',0],['T3a',1]]],
     ['Positive cores',[['<34%',0],['≥34%',1]]]],
     read:function(t){return 'CAPRA <b>'+t+'</b> of 10: '+(t<=2?'low':t<=5?'intermediate':'high')+' risk (0–2 low, 3–5 intermediate, 6–10 high)';}},
   sins:{items:[
     ['Location',[['Rigid (S2–S5)',0],['Semi-rigid (T3–T10)',1],['Mobile (C3–C6, L2–L4)',2],['Junctional (occiput–C2, C7–T2, T11–L1, L5–S1)',3]]],
     ['Pain',[['Pain-free lesion',0],['Occasional, not mechanical',1],['Mechanical (relief with recumbency / pain with movement or loading)',3]]],
     ['Bone lesion',[['Blastic',0],['Mixed',1],['Lytic',2]]],
     ['Alignment',[['Normal',0],['De novo deformity (kyphosis / scoliosis)',2],['Subluxation / translation',4]]],
     ['Vertebral body collapse',[['None of the below',0],['No collapse, >50% of body involved',1],['<50% collapse',2],['>50% collapse',3]]],
     ['Posterolateral involvement',[['None',0],['Unilateral',1],['Bilateral',3]]]],
     read:function(t){return 'SINS <b>'+t+'</b> of 18: '+(t<=6?'stable':t<=12?'indeterminate (possibly impending) instability — surgical opinion':'unstable — surgical opinion')+' (0–6, 7–12, 13–18)';}},
   mirels:{items:[
     ['Site',[['Upper limb',1],['Lower limb',2],['Peritrochanteric',3]]],
     ['Pain',[['Mild',1],['Moderate',2],['Functional',3]]],
     ['Lesion',[['Blastic',1],['Mixed',2],['Lytic',3]]],
     ['Size (fraction of cortex/diameter)',[['<1/3',1],['1/3–2/3',2],['>2/3',3]]]],
     read:function(t){return 'Mirels <b>'+t+'</b> of 12: '+(t>=9?'prophylactic fixation generally recommended':t==8?'borderline — consider fixation':'radiotherapy and observation')+' (≤7, 8, ≥9)';}},
   ipi:{items:[
     ['Age',[['≤60',0],['>60',1]]],['Stage',[['I–II',0],['III–IV',1]]],['LDH',[['Normal',0],['Raised',1]]],['ECOG',[['0–1',0],['≥2',1]]],['Extranodal sites',[['0–1',0],['>1',1]]]],
     read:function(t){return 'IPI <b>'+t+'</b>: '+['low','low','low-intermediate','high-intermediate','high','high'][t]+' risk. R-IPI: '+(t==0?'very good':t<=2?'good':'poor')+'.';}},
   ips:{items:[
     ['Albumin <40 g/L',[['No',0],['Yes',1]]],['Haemoglobin <105 g/L',[['No',0],['Yes',1]]],['Male',[['No',0],['Yes',1]]],['Age ≥45',[['No',0],['Yes',1]]],['Stage IV',[['No',0],['Yes',1]]],['White cells ≥15 × 10⁹/L',[['No',0],['Yes',1]]],['Lymphocytes <0.6 × 10⁹/L or <8%',[['No',0],['Yes',1]]]],
     read:function(t){return 'IPS (Hasenclever) <b>'+t+'</b> of 7 adverse factors (advanced Hodgkin lymphoma).';}},
   vnpi:{items:[
     ['Size',[['≤15 mm',1],['16–40 mm',2],['≥41 mm',3]]],
     ['Margin',[['≥10 mm',1],['1–9 mm',2],['<1 mm',3]]],
     ['Pathology',[['Not high grade, no necrosis',1],['Not high grade, with necrosis',2],['High grade',3]]],
     ['Age',[['>60',1],['40–60',2],['<40',3]]]],
     read:function(t){return 'USC/Van Nuys Prognostic Index <b>'+t+'</b> of 12 (4 lowest risk, 12 highest).';}}
  };
  Object.keys(S).forEach(function(k){
    var box=document.querySelector('[data-score="'+k+'"]'); if(!box) return;
    var h='<div class="calc">';
    S[k].items.forEach(function(it,i){ h+='<label>'+it[0]+'<select id="s_'+k+'_'+i+'">'+it[1].map(function(o){return '<option value="'+o[1]+'">'+o[0]+' ('+o[1]+')</option>';}).join('')+'</select></label>'; });
    box.innerHTML=h+'</div><div class="calcout" id="o_'+k+'"></div>';
  });
  function scores(){ Object.keys(S).forEach(function(k){ if(!el('o_'+k)) return; var t=0; S[k].items.forEach(function(it,i){t+=parseFloat(sel('s_'+k+'_'+i))||0;}); out('o_'+k,S[k].read(t)); }); }
  // ---- formula calculators ----
  function calc(){
    // PSA doubling time: least-squares slope of ln(PSA) against time
    var pts=[]; for(var i=1;i<=5;i++){ var d=el('pd'+i), p=num('pp'+i); if(d&&d.value&&p>0) pts.push([new Date(d.value).getTime()/864e5,Math.log(p)]); }
    if(pts.length>=2){ var n=pts.length,sx=0,sy=0,sxx=0,sxy=0; pts.forEach(function(q){sx+=q[0];sy+=q[1];sxx+=q[0]*q[0];sxy+=q[0]*q[1];});
      var den=n*sxx-sx*sx, m=den?(n*sxy-sx*sy)/den:NaN;
      if(!isFinite(m)) out('o_psadt','Dates must differ.'); else if(m<=0) out('o_psadt','PSA is stable or falling over this interval: no doubling time.');
      else { var dt=Math.LN2/m/30.44; out('o_psadt','PSA doubling time <b>'+f(dt)+' months</b> ('+f(dt/12,2)+' years); PSA velocity by this fit ≈ '+f(m*365.25*Math.exp(pts[pts.length-1][1]),2)+' ng/mL per year at the last value. '+n+' values used.'); }
    } else out('o_psadt','Enter at least two dated PSA values (three or more over ≥3 months is better).');
    // Roach
    var psa=num('r_psa'), gs=num('r_gs');
    if(psa>=0&&gs>=2){ var ln=Math.max(0,2/3*psa+(gs-6)*10), sv=Math.max(0,psa+(gs-6)*10), ece=Math.max(0,1.5*psa+(gs-3)*10);
      out('o_roach','Lymph node risk <b>'+f(Math.min(ln,100),0)+'%</b> · seminal vesicle risk <b>'+f(Math.min(sv,100),0)+'%</b> · extracapsular extension <b>'+f(Math.min(ece,100),0)+'%</b>'); } else out('o_roach','Enter PSA and Gleason score.');
    // D'Amico
    var dp=num('d_psa'), dg=num('d_gs'), dt2=sel('d_t');
    if(dp>=0&&dg>=2){ var hi=dp>20||dg>=8||dt2==='c', lo=dp<=10&&dg<=6&&dt2==='a'; out('o_damico','D\'Amico <b>'+(hi?'high':lo?'low':'intermediate')+'</b> risk'); } else out('o_damico','Enter PSA, Gleason score and T stage.');
    // CTS5
    var a=num('c_age'), sz=num('c_size'), gr=num('c_grade'), nd=num('c_nodes');
    if(a>0&&sz>0){ var s2=Math.min(sz,30), nc=nd==0?0:nd==1?1:nd<=3?2:nd<=9?3:4;
      var c=0.438*nc+0.988*(0.093*s2-0.001*s2*s2+0.375*gr+0.017*a);
      out('o_cts5','CTS5 <b>'+f(c,2)+'</b>: '+(c<3.13?'low':c<=3.86?'intermediate':'high')+' risk of late distant recurrence (years 5–10) (<3.13 low, 3.13–3.86 intermediate, >3.86 high)'); } else out('o_cts5','Enter age, tumour size, grade and number of positive nodes.');
    // ALBI and MELD
    var bil=num('l_bil'), alb=num('l_alb'), inr=num('l_inr'), cr=num('l_cr');
    if(bil>0&&alb>0){ var al=0.66*Math.log10(bil)-0.085*alb; out('o_albi','ALBI <b>'+f(al,2)+'</b>: grade <b>'+(al<=-2.60?1:al<=-1.39?2:3)+'</b> (≤ −2.60 grade 1; > −2.60 to −1.39 grade 2; > −1.39 grade 3)'); } else out('o_albi','Enter bilirubin (µmol/L) and albumin (g/L).');
    if(bil>0&&inr>0&&cr>0){ var b=Math.max(1,bil/17.1), c2=Math.min(4,Math.max(1,cr/88.4)), i2=Math.max(1,inr);
      out('o_meld','MELD <b>'+f(Math.max(6,Math.round(3.78*Math.log(b)+11.2*Math.log(i2)+9.57*Math.log(c2)+6.43)),0)+'</b> (original formula, without sodium; values below 1 set to 1, creatinine capped at 4 mg/dL)'); } else out('o_meld','Enter bilirubin, INR and creatinine (µmol/L).');
    // RPA
    var k=sel('rp_kps'), ok=sel('rp_age')==='y'&&sel('rp_prim')==='y'&&sel('rp_ecm')==='y';
    out('o_rpa','RPA class <b>'+(k==='lo'?'III':ok?'I':'II')+'</b> (I: KPS ≥70, age <65, controlled primary, brain only; III: KPS <70; II: all others)');
    // Sedlis
    var lv=sel('sd_lvsi')==='y', dep=sel('sd_depth'), ts=num('sd_size');
    if(ts>=0){ var met=(lv&&dep==='deep')||(lv&&dep==='mid'&&ts>=2)||(lv&&dep==='sup'&&ts>=5)||(!lv&&dep!=='sup'&&ts>=4);
      out('o_sedlis','Sedlis criteria <b>'+(met?'met':'not met')+'</b> (intermediate-risk, node-negative, margin-negative stage IB after radical hysterectomy)'); } else out('o_sedlis','Enter tumour size.');
    // Cervix EBRT + brachy EQD2
    var eD=num('g_eD'), en=num('g_en'), bd=num('g_bd'), bn=num('g_bn'), od=num('g_od');
    function e2(D,n,ab){return D*(D/n+ab)/(2+ab);}
    if(eD>0&&en>0&&bd>0&&bn>0){ var h='HR-CTV D90: EBRT '+f(e2(eD,en,10))+' + brachytherapy '+f(e2(bd*bn,bn,10))+' = <b>'+f(e2(eD,en,10)+e2(bd*bn,bn,10))+' Gy EQD2<sub>10</sub></b>';
      if(od>0) h+='<br>OAR D2cc: EBRT '+f(e2(eD,en,3))+' + brachytherapy '+f(e2(od*bn,bn,3))+' = <b>'+f(e2(eD,en,3)+e2(od*bn,bn,3))+' Gy EQD2<sub>3</sub></b> (assumes the OAR received the full EBRT dose)';
      out('o_gyn',h); } else out('o_gyn','Enter the EBRT schedule and the brachytherapy dose per fraction and fractions.');
    // General: BSA, Cockcroft-Gault, Calvert
    var ht=num('b_ht'), wt=num('b_wt'), ag=num('b_age'), scr=num('b_cr'), sex=sel('b_sex'), auc=num('b_auc'), h2='';
    if(ht>0&&wt>0) h2+='BSA (Mosteller) <b>'+f(Math.sqrt(ht*wt/3600),2)+' m²</b> · BMI '+f(wt/Math.pow(ht/100,2))+'<br>';
    if(ag>0&&wt>0&&scr>0){ var crcl=(140-ag)*wt*(sex==='f'?1.04:1.23)/scr; h2+='Creatinine clearance (Cockcroft-Gault, actual weight) <b>'+f(crcl,0)+' mL/min</b>';
      if(auc>0) h2+='<br>Carboplatin (Calvert) AUC '+auc+': <b>'+f(auc*(Math.min(crcl,125)+25),0)+' mg</b> (clearance capped at 125 mL/min)'; }
    out('o_gen',h2||'Enter height and weight; add age, sex and creatinine for clearance.');
    // ppo FEV1
    var fev=num('p_fev'), seg=num('p_seg'), tot=num('p_tot')||19;
    if(fev>0&&seg>=0) out('o_ppo','Predicted post-operative value <b>'+f(fev*(1-seg/tot),0)+'</b> (same units as entered; '+seg+' of '+tot+' functioning segments removed)'); else out('o_ppo','Enter the pre-operative value and segments to be resected.');
  }
  function all(){scores();calc();}
  document.addEventListener('input',all); document.addEventListener('change',all); all();
})();
