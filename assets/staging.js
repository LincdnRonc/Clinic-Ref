// Auto-staging: pick T, N, M (or findings) and read the stage group.
// Groupings entered from the standard staging tables (AJCC 8 unless stated); verify against the manual.
(function(){
  function o(a){return a.map(function(x){return typeof x==='string'?[x,x]:x;});}
  var M01=o([['0','M0'],['1','M1']]);
  var D={
   nccn:{t:'Prostate NCCN risk group (initial risk stratification, 2025)',lab:'Risk group',src:'Definitions per NCCN Prostate Cancer 2025: high = one or more of cT3–cT4, grade group 4–5, PSA >20; very high = at least two of cT3–cT4, grade group 4–5, PSA >40. Check the current NCCN version.',note:'For clinically localised disease (N0 M0). Very-low criteria (fewer than 3 positive cores, each ≤50% cancer, PSA density <0.15) should be confirmed against the guideline.',
     f:[['T',o([['1c','cT1c'],['2a','cT1a–b or cT2a'],['2b','cT2b–cT2c'],['3','cT3–cT4']])],['GG',o([['1','Grade group 1 (3+3)'],['2','Grade group 2 (3+4)'],['3','Grade group 3 (4+3)'],['4','Grade group 4 (8)'],['5','Grade group 5 (9–10)']])],['PSA',o([['a','<10'],['b','10–20'],['c','>20 to 40'],['d','>40']])],['Cores positive',o([['lt','<50% of cores'],['ge','≥50% of cores']])],['Very-low criteria',o([['n','Not met or unknown'],['y','<3 cores positive, each ≤50%, PSA density <0.15']])]],
     s:function(v){var t3=v.T==='3', g45=(v.GG==='4'||v.GG==='5'), p20=(v.PSA==='c'||v.PSA==='d'), p40=v.PSA==='d';
       var vh=(t3?1:0)+(g45?1:0)+(p40?1:0), h=(t3?1:0)+(g45?1:0)+(p20?1:0);
       if(vh>=2)return 'Very high'; if(h>=1)return 'High';
       var irf=(v.T==='2b'?1:0)+((v.GG==='2'||v.GG==='3')?1:0)+(v.PSA==='b'?1:0);
       if(irf>=1){var why=[]; if(irf>=2)why.push(irf+' intermediate risk factors'); if(v.GG==='3')why.push('grade group 3'); if(v['Cores positive']==='ge')why.push('≥50% cores positive');
         return why.length?'Unfavourable intermediate ('+why.join(', ')+')':'Favourable intermediate (1 intermediate risk factor, grade group 1–2, <50% cores)';}
       return (v.T==='1c'&&v['Very-low criteria']==='y')?'Very low':'Low';}},
   breast:{t:'Breast (AJCC 8 anatomic stage)',note:'Anatomic groups only. The AJCC 8 prognostic stage also uses grade, ER, PR, HER2 and Oncotype: use a prognostic-stage tool for that.',
     f:[['T',o([['is','Tis (DCIS)'],['0','T0'],['1','T1 (≤2 cm)'],['2','T2 (>2–5 cm)'],['3','T3 (>5 cm)'],['4','T4 (chest wall, skin, inflammatory)']])],['N',o([['0','N0'],['1mi','N1mi'],['1','N1 (movable level I–II; pN1 1–3 nodes)'],['2','N2 (fixed/matted or clinical IMN alone; pN2 4–9)'],['3','N3 (infraclavicular, IMN + axilla, supraclavicular; pN3 ≥10)']])],['M',M01]],
     s:function(v){var T=v.T,N=v.N; if(v.M==='1')return 'IV'; if(N==='3')return 'IIIC'; if(T==='4')return 'IIIB'; if(T==='is')return N==='0'?'0':'Not a valid combination (Tis with nodes: look for invasion)';
       if(N==='2')return 'IIIA'; if(T==='3')return N==='0'?'IIB':'IIIA'; if(T==='2')return N==='0'?'IIA':'IIB'; if(N==='0')return T==='0'?'No primary or nodes (T0 N0)':'IA'; return N==='1mi'?'IB':'IIA';}},
   lung:{t:'Lung (TNM 9th edition, 2024)',note:'N2a = single N2 station; N2b = multiple N2 stations. M1c1 = multiple extrathoracic metastases in one organ system; M1c2 = in more than one.',
     f:[['T',o([['is','Tis'],['1a','T1mi / T1a (≤1 cm)'],['1b','T1b (>1–2 cm)'],['1c','T1c (>2–3 cm)'],['2a','T2a (>3–4 cm, or main bronchus, visceral pleura, atelectasis)'],['2b','T2b (>4–5 cm)'],['3','T3 (>5–7 cm, chest wall, same-lobe nodule)'],['4','T4 (>7 cm, mediastinum, diaphragm, other ipsilateral lobe)']])],['N',o([['0','N0'],['1','N1'],['2a','N2a'],['2b','N2b'],['3','N3']])],['M',o([['0','M0'],['1a','M1a (contralateral lobe, pleural or pericardial)'],['1b','M1b (single extrathoracic)'],['1c1','M1c1'],['1c2','M1c2']])]],
     s:function(v){var T=v.T,N=v.N; if(v.M==='1a'||v.M==='1b')return 'IVA'; if(v.M!=='0')return 'IVB'; if(T==='is')return N==='0'?'0':'Not a valid combination';
       var g=T[0]; var tab={'1':{'0':{'1a':'IA1','1b':'IA2','1c':'IA3'}[T],'1':'IIA','2a':'IIB','2b':'IIIA','3':'IIIB'},
         '2':{'0':T==='2a'?'IB':'IIA','1':'IIB','2a':'IIIA','2b':'IIIB','3':'IIIB'},'3':{'0':'IIB','1':'IIIA','2a':'IIIA','2b':'IIIB','3':'IIIC'},'4':{'0':'IIIA','1':'IIIA','2a':'IIIB','2b':'IIIB','3':'IIIC'}};
       return tab[g][N];}},
   prostate:{t:'Prostate (AJCC 8 prognostic stage group)',note:'Uses clinical T, PSA and grade group. NCCN risk groups are on this page\'s risk tab.',
     f:[['T',o([['1','cT1a–c or cT2a'],['2','cT2b–c'],['3','T3–T4']])],['PSA',o([['a','<10'],['b','10 to <20'],['c','≥20']])],['GG',o([['1','Grade group 1 (3+3)'],['2','Grade group 2 (3+4)'],['3','Grade group 3 (4+3)'],['4','Grade group 4 (8)'],['5','Grade group 5 (9–10)']])],['N',o([['0','N0'],['1','N1']])],['M',M01]],
     s:function(v){ if(v.M==='1')return 'IVB'; if(v.N==='1')return 'IVA'; if(v.GG==='5')return 'IIIC'; if(v.T==='3')return 'IIIB'; if(v.PSA==='c')return 'IIIA';
       if(v.GG==='3'||v.GG==='4')return 'IIC'; if(v.GG==='2')return 'IIB'; return (v.T==='1'&&v.PSA==='a')?'I':'IIA';}},
   crc:{t:'Colon and rectum (AJCC 8)',note:'',
     f:[['T',o([['is','Tis'],['1','T1 (submucosa)'],['2','T2 (muscularis propria)'],['3','T3 (pericolorectal tissue)'],['4a','T4a (visceral peritoneum)'],['4b','T4b (adjacent organs)']])],['N',o([['0','N0'],['1','N1 / N1c (1–3 nodes or deposits)'],['2a','N2a (4–6)'],['2b','N2b (≥7)']])],['M',o([['0','M0'],['1a','M1a (one site)'],['1b','M1b (two or more sites)'],['1c','M1c (peritoneal)']])]],
     s:function(v){var T=v.T,N=v.N; if(v.M!=='0')return {'1a':'IVA','1b':'IVB','1c':'IVC'}[v.M]; if(T==='is')return N==='0'?'0':'Not a valid combination';
       if(N==='0')return {'1':'I','2':'I','3':'IIA','4a':'IIB','4b':'IIC'}[T]; if(T==='4b')return 'IIIC';
       if(N==='1')return (T==='1'||T==='2')?'IIIA':'IIIB'; if(N==='2a')return T==='1'?'IIIA':T==='4a'?'IIIC':'IIIB'; return (T==='1'||T==='2')?'IIIB':'IIIC';}},
   anal:{t:'Anal canal (AJCC 8)',note:'AJCC version 9 (2023) regroups node-positive disease: check which edition your MDT uses.',
     f:[['T',o([['1','T1 (≤2 cm)'],['2','T2 (>2–5 cm)'],['3','T3 (>5 cm)'],['4','T4 (adjacent organs)']])],['N',o([['0','N0'],['1','N1 (N1a–c)']])],['M',M01]],
     s:function(v){ if(v.M==='1')return 'IV'; if(v.N==='0')return {'1':'I','2':'IIA','3':'IIB','4':'IIIB'}[v.T]; return (v.T==='1'||v.T==='2')?'IIIA':'IIIC';}},
   oes_scc:{t:'Oesophagus and GOJ, squamous (AJCC 8 clinical stage)',note:'Clinical (cTNM) groups. Pathological and post-neoadjuvant (yp) groups differ.',
     f:[['T',o([['1','cT1'],['2','cT2'],['3','cT3'],['4','cT4']])],['N',o([['0','N0'],['1','N1 (1–2)'],['2','N2 (3–6)'],['3','N3 (≥7)']])],['M',M01]],
     s:function(v){ if(v.M==='1')return 'IVB'; if(v.N==='3'||v.T==='4')return 'IVA'; if(v.N==='2')return 'III'; if(v.T==='1')return 'I'; if(v.T==='2')return 'II'; return v.N==='0'?'II':'III';}},
   oes_ac:{t:'Oesophagus and GOJ, adenocarcinoma (AJCC 8 clinical stage)',note:'Clinical (cTNM) groups. Pathological and post-neoadjuvant (yp) groups differ.',
     f:[['T',o([['1','cT1'],['2','cT2'],['3','cT3'],['4a','cT4a'],['4b','cT4b']])],['N',o([['0','N0'],['1','N1 (1–2)'],['2','N2 (3–6)'],['3','N3 (≥7)']])],['M',M01]],
     s:function(v){ if(v.M==='1')return 'IVB'; if(v.N==='3'||v.N==='2'||v.T==='4b')return 'IVA'; if(v.T==='1')return v.N==='0'?'I':'IIA'; if(v.T==='2')return v.N==='0'?'IIB':'III'; return 'III';}},
   gastric:{t:'Stomach (AJCC 8 clinical stage)',note:'Clinical groups; pathological groups are more detailed.',
     f:[['T',o([['1','cT1'],['2','cT2'],['3','cT3'],['4a','cT4a'],['4b','cT4b']])],['N',o([['0','N0'],['1','N+ (N1–3)']])],['M',M01]],
     s:function(v){ if(v.M==='1')return 'IVB'; if(v.T==='4b')return 'IVA'; var early=(v.T==='1'||v.T==='2'); return v.N==='0'?(early?'I':'IIB'):(early?'IIA':'III');}},
   pancreas:{t:'Pancreas (AJCC 8)',note:'Resectability (resectable, borderline, locally advanced) is separate from stage: see the pancreas page.',
     f:[['T',o([['1','T1 (≤2 cm)'],['2','T2 (>2–4 cm)'],['3','T3 (>4 cm)'],['4','T4 (coeliac axis, SMA or common hepatic artery)']])],['N',o([['0','N0'],['1','N1 (1–3)'],['2','N2 (≥4)']])],['M',M01]],
     s:function(v){ if(v.M==='1')return 'IV'; if(v.T==='4'||v.N==='2')return 'III'; if(v.N==='1')return 'IIB'; return {'1':'IA','2':'IB','3':'IIA'}[v.T];}},
   hcc:{t:'Hepatocellular carcinoma (AJCC 8)',note:'BCLC stage (which adds liver function and performance status) usually drives treatment.',
     f:[['T',o([['1a','T1a (solitary ≤2 cm)'],['1b','T1b (solitary >2 cm, no vascular invasion)'],['2','T2 (solitary >2 cm with vascular invasion, or multiple ≤5 cm)'],['3','T3 (multiple, at least one >5 cm)'],['4','T4 (major portal or hepatic vein branch, adjacent organs)']])],['N',o([['0','N0'],['1','N1']])],['M',M01]],
     s:function(v){ if(v.M==='1')return 'IVB'; if(v.N==='1')return 'IVA'; return {'1a':'IA','1b':'IB','2':'II','3':'IIIA','4':'IIIB'}[v.T];}},
   hn:{t:'Oral cavity, larynx, hypopharynx and p16-negative oropharynx (AJCC 8)',note:'T definitions differ by subsite. N3 includes N3b (clinical extranodal extension).',
     f:[['T',o([['1','T1'],['2','T2'],['3','T3'],['4a','T4a'],['4b','T4b']])],['N',o([['0','N0'],['1','N1'],['2','N2 (a–c)'],['3','N3 (a–b)']])],['M',M01]],
     s:function(v){ if(v.M==='1')return 'IVC'; if(v.T==='4b'||v.N==='3')return 'IVB'; if(v.T==='4a'||v.N==='2')return 'IVA'; if(v.N==='1'||v.T==='3')return 'III'; return v.T==='1'?'I':'II';}},
   opc:{t:'Oropharynx, p16-positive (AJCC 8 clinical stage)',note:'Clinical groups. Pathological staging after surgery uses node number (pN1 ≤4, pN2 >4) and different groups.',
     f:[['T',o([['1','T0–T1'],['2','T2'],['3','T3'],['4','T4']])],['N',o([['0','N0'],['1','N1 (ipsilateral, ≤6 cm)'],['2','N2 (contralateral or bilateral, ≤6 cm)'],['3','N3 (>6 cm)']])],['M',M01]],
     s:function(v){ if(v.M==='1')return 'IV'; if(v.T==='4'||v.N==='3')return 'III'; if(v.T==='3'||v.N==='2')return 'II'; return 'I';}},
   npc:{t:'Nasopharynx (AJCC 8)',note:'AJCC version 9 (2025) changes the groups (stage IVA becomes part of III; M1a/M1b): check which edition is in use.',
     f:[['T',o([['1','T0–T1'],['2','T2 (parapharyngeal, adjacent muscles)'],['3','T3 (skull base, cervical vertebra, sinuses)'],['4','T4 (intracranial, cranial nerves, orbit, parotid, hypopharynx)']])],['N',o([['0','N0'],['1','N1 (unilateral cervical or any retropharyngeal, ≤6 cm, above cricoid)'],['2','N2 (bilateral, ≤6 cm, above cricoid)'],['3','N3 (>6 cm or below cricoid)']])],['M',M01]],
     s:function(v){ if(v.M==='1')return 'IVB'; if(v.T==='4'||v.N==='3')return 'IVA'; if(v.T==='3'||v.N==='2')return 'III'; if(v.T==='2'||v.N==='1')return 'II'; return 'I';}},
   bladder:{t:'Bladder (AJCC 8)',note:'',
     f:[['T',o([['a','Ta'],['is','Tis'],['1','T1'],['2','T2 (a–b)'],['3','T3 or T4a'],['4b','T4b (pelvic or abdominal wall)']])],['N',o([['0','N0'],['1','N1 (single true-pelvic node)'],['2','N2–N3 (multiple pelvic, or common iliac)']])],['M',o([['0','M0'],['1a','M1a (nodes beyond common iliac)'],['1b','M1b (other distant)']])]],
     s:function(v){ if(v.M==='1b')return 'IVB'; if(v.M==='1a'||v.T==='4b')return 'IVA'; if(v.N==='2')return 'IIIB'; if(v.N==='1')return 'IIIA'; return {'a':'0a','is':'0is','1':'I','2':'II','3':'IIIA'}[v.T];}},
   kidney:{t:'Kidney (AJCC 8)',note:'',
     f:[['T',o([['1','T1 (≤7 cm, confined)'],['2','T2 (>7 cm, confined)'],['3','T3 (major veins or perinephric tissue)'],['4','T4 (beyond Gerota fascia, adrenal by direct extension)']])],['N',o([['0','N0'],['1','N1']])],['M',M01]],
     s:function(v){ if(v.M==='1'||v.T==='4')return 'IV'; if(v.T==='3'||v.N==='1')return 'III'; return v.T==='1'?'I':'II';}},
   cervix:{t:'Cervix (FIGO 2018)',note:'Imaging and pathology may be used to assign stage. The highest applicable finding sets the stage.',
     f:[['Tumour',o([['a1','Microscopic, depth ≤3 mm'],['a2','Microscopic, depth >3–5 mm'],['b1','Depth >5 mm, size ≤2 cm'],['b2','>2–4 cm'],['b3','>4 cm']])],['Extension',o([['0','Confined to cervix'],['v','Upper two-thirds of vagina'],['p','Parametrium'],['l','Lower third of vagina'],['w','Pelvic wall, hydronephrosis or non-functioning kidney'],['m','Bladder or rectal mucosa']])],['Nodes',o([['0','No nodal metastasis'],['p','Pelvic nodes'],['a','Para-aortic nodes']])],['Distant',o([['0','None'],['1','Distant organs']])]],
     s:function(v){ if(v.Distant==='1')return 'IVB'; if(v.Extension==='m')return 'IVA'; if(v.Nodes==='a')return 'IIIC2'; if(v.Nodes==='p')return 'IIIC1'; if(v.Extension==='w')return 'IIIB'; if(v.Extension==='l')return 'IIIA'; if(v.Extension==='p')return 'IIB';
       if(v.Extension==='v')return v.Tumour==='b3'?'IIA2':'IIA1'; return {'a1':'IA1','a2':'IA2','b1':'IB1','b2':'IB2','b3':'IB3'}[v.Tumour];}},
   endo:{t:'Endometrium (FIGO 2009)',note:'FIGO 2023 adds histology, LVSI and molecular class (e.g. IAm POLEmut, IICm p53abn) and is not calculated here.',
     f:[['Uterus',o([['a','<50% myometrial invasion'],['b','≥50% myometrial invasion'],['c','Cervical stromal invasion']])],['Spread',o([['0','None beyond uterus'],['s','Serosa or adnexa'],['v','Vagina or parametrium'],['m','Bladder or bowel mucosa']])],['Nodes',o([['0','No nodal metastasis'],['p','Pelvic nodes'],['a','Para-aortic nodes']])],['Distant',o([['0','None'],['1','Distant, intra-abdominal or inguinal nodes']])]],
     s:function(v){ if(v.Distant==='1')return 'IVB'; if(v.Spread==='m')return 'IVA'; if(v.Nodes==='a')return 'IIIC2'; if(v.Nodes==='p')return 'IIIC1'; if(v.Spread==='v')return 'IIIB'; if(v.Spread==='s')return 'IIIA'; return {'a':'IA','b':'IB','c':'II'}[v.Uterus];}},
   lugano:{t:'Lymphoma (Lugano modification of Ann Arbor)',note:'A/B symptoms are recorded for Hodgkin lymphoma only. Bulk: record the largest diameter.',
     f:[['Extent',o([['1','One nodal region, or a single extranodal site (IE)'],['2','Two or more nodal regions, same side of the diaphragm'],['2e','Stage II with limited contiguous extranodal extension'],['3','Nodes on both sides of the diaphragm, or above with spleen'],['4','Non-contiguous extranodal involvement']])],['Bulk',o([['0','No bulk'],['1','Bulky']])],['B',o([['A','No B symptoms'],['B','B symptoms']])]],
     s:function(v){var st={'1':'I','2':'II','2e':'IIE','3':'III','4':'IV'}[v.Extent]; var lim=(v.Extent==='1'||v.Extent==='2'||v.Extent==='2e');
       return st+v.B+((v.Extent==='2'||v.Extent==='2e')&&v.Bulk==='1'?' bulky':'')+' — '+(lim?(v.Bulk==='1'&&v.Extent!=='1'?'stage II bulky: limited or advanced by histology and prognostic factors':'limited stage'):'advanced stage');}}
  };
  document.querySelectorAll('[data-stage]').forEach(function(box){
    var k=box.getAttribute('data-stage'), d=D[k]; if(!d) return;
    var h='<div class="calc">'+d.f.map(function(fl){return '<label>'+fl[0]+'<select data-sf="'+k+'" data-k="'+fl[0]+'">'+fl[1].map(function(x){return '<option value="'+x[0]+'">'+x[1]+'</option>';}).join('')+'</select></label>';}).join('')+'</div><div class="calcout" data-so="'+k+'"></div>';
    box.innerHTML=h+'<p class="note">'+(d.note?d.note+' ':'')+(d.src?d.src:'<span class="flag caution">Verify</span> Groupings entered from the standard table; confirm against the staging manual before documenting.')+'</p>';
  });
  function run(){
    document.querySelectorAll('[data-stage]').forEach(function(box){
      var k=box.getAttribute('data-stage'), d=D[k]; if(!d) return; var v={};
      box.querySelectorAll('select[data-sf]').forEach(function(s){v[s.getAttribute('data-k')]=s.value;});
      var o=box.querySelector('[data-so]'); if(o) o.innerHTML=(d.lab||'Stage')+' <b>'+d.s(v)+'</b>';
    });
  }
  window.QR_STAGE_TITLES={}; Object.keys(D).forEach(function(k){window.QR_STAGE_TITLES[k]=D[k].t;});
  document.addEventListener('change',run); run();
})();
