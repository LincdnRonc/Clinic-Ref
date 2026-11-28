// Request forms: fill in, then make an A4 PDF with jsPDF (assets/jspdf.umd.min.js).
// Patient details are never stored. "My details" (and the signature, if ticked) are kept in localStorage on this device only.
(function(){
  var ME_KEY='rq_me', SIG_KEY='rq_sig';
  function ls(k,v){ try{ if(v===undefined) return localStorage.getItem(k); if(v===null) localStorage.removeItem(k); else localStorage.setItem(k,v); }catch(e){ return null; } }
  var forms=[].slice.call(document.querySelectorAll('.rqform'));
  var meForm=document.querySelector('.rqme');
  if(!forms.length||!meForm) return;

  // Today's date in each form
  function today(){ var d=new Date(); return d.getFullYear()+'-'+('0'+(d.getMonth()+1)).slice(-2)+'-'+('0'+d.getDate()).slice(-2); }
  forms.forEach(function(f){ if(!f.rq_date.value) f.rq_date.value=today(); });

  // Patient fields are shared between the forms
  forms.forEach(function(f){
    f.addEventListener('input',function(e){
      var n=e.target.name; if(!n||n.indexOf('pt_')!==0) return;
      forms.forEach(function(g){ if(g!==f && g.elements[n]) g.elements[n].value=e.target.value; });
    });
  });

  // My details
  var me={}; try{ me=JSON.parse(ls(ME_KEY)||'{}'); }catch(e){ me={}; }
  [].forEach.call(meForm.elements,function(el){ if(el.name&&me[el.name]) el.value=me[el.name]; });
  meForm.addEventListener('input',function(){
    var o={}; [].forEach.call(meForm.elements,function(el){ if(el.name&&el.value) o[el.name]=el.value; });
    ls(ME_KEY,JSON.stringify(o));
  });

  // Signature pad
  var cv=document.getElementById('rqSig'), cx=cv.getContext('2d'), drawn=false, keep=document.getElementById('rqSigKeep');
  cx.lineWidth=3; cx.lineCap='round'; cx.lineJoin='round'; cx.strokeStyle='#0b1f3a';
  var saved=ls(SIG_KEY);
  if(saved){ keep.checked=true; var im=new Image(); im.onload=function(){ cx.drawImage(im,0,0); drawn=true; }; im.src=saved; }
  function pos(e){ var r=cv.getBoundingClientRect(); return [(e.clientX-r.left)*cv.width/r.width,(e.clientY-r.top)*cv.height/r.height]; }
  var down=false;
  cv.addEventListener('pointerdown',function(e){ down=true; cv.setPointerCapture(e.pointerId); var p=pos(e); cx.beginPath(); cx.moveTo(p[0],p[1]); e.preventDefault(); });
  cv.addEventListener('pointermove',function(e){ if(!down) return; var p=pos(e); cx.lineTo(p[0],p[1]); cx.stroke(); drawn=true; e.preventDefault(); });
  function up(){ if(!down) return; down=false; if(keep.checked) ls(SIG_KEY,cv.toDataURL('image/png')); }
  cv.addEventListener('pointerup',up); cv.addEventListener('pointercancel',up);
  document.getElementById('rqSigClear').addEventListener('click',function(){ cx.clearRect(0,0,cv.width,cv.height); drawn=false; ls(SIG_KEY,null); });
  keep.addEventListener('change',function(){ if(keep.checked&&drawn) ls(SIG_KEY,cv.toDataURL('image/png')); if(!keep.checked) ls(SIG_KEY,null); });

  // Clear
  [].forEach.call(document.querySelectorAll('.rqclear'),function(b){
    b.addEventListener('click',function(){
      forms.forEach(function(f){ f.reset(); f.rq_date.value=today(); });
      [].forEach.call(document.querySelectorAll('.rqmsg'),function(m){ m.textContent=''; });
    });
  });

  // ---------- PDF ----------
  function clean(s){ return String(s==null?'':s).replace(/β/g,'beta ').replace(/beta -/g,'beta-').replace(/[‘’]/g,"'").replace(/[“”]/g,'"').replace(/[^\x09\x0A\x0D\x20-\x7E -ÿ–—•]/g,''); }
  function dmy(v){ if(!v) return ''; var p=v.split('-'); return p.length===3?p[2]+'/'+p[1]+'/'+p[0]:v; }
  function val(f,n){ var el=f.elements[n]; if(!el) return ''; return el.type==='date'?dmy(el.value):(el.value||'').trim(); }

  function build(kind){
    var f=forms.filter(function(x){ return x.dataset.form===kind; })[0];
    var J=window.jspdf&&window.jspdf.jsPDF; if(!J) throw new Error('PDF library did not load');
    var doc=new J({unit:'mm',format:'a4'}), W=210, M=14, y=0, cw=W-2*M;
    var ink=[11,31,58], mute=[90,100,115];
    function c(a){ doc.setTextColor(a[0],a[1],a[2]); }
    function need(h){ if(y+h>284){ doc.addPage(); y=16; } }
    function head(t){ need(12); y+=3; doc.setFillColor(232,238,246); doc.rect(M,y,cw,6.5,'F'); doc.setFont('helvetica','bold'); doc.setFontSize(10); c(ink); doc.text(clean(t).toUpperCase(),M+2,y+4.6); y+=9.5; }
    function pairs(list,cols){
      cols=cols||2; var colW=cw/cols; list=list.filter(function(p){ return p[1]; });
      for(var i=0;i<list.length;i+=cols){
        var h=0;
        for(var j=0;j<cols&&i+j<list.length;j++){
          var p=list[i+j], x=M+j*colW;
          doc.setFont('helvetica','normal'); doc.setFontSize(7.5); c(mute); doc.text(clean(p[0]),x,y);
          doc.setFont('helvetica','bold'); doc.setFontSize(10); c(ink);
          var ln=doc.splitTextToSize(clean(p[1]),colW-4); doc.text(ln,x,y+4.3); h=Math.max(h,4.3+ln.length*4.4);
        }
        y+=h+2; need(10);
      }
    }
    function para(label,text){
      if(!text) return; need(12);
      doc.setFont('helvetica','normal'); doc.setFontSize(7.5); c(mute); doc.text(clean(label),M,y);
      doc.setFontSize(10); c(ink); var ln=doc.splitTextToSize(clean(text),cw);
      for(var i=0;i<ln.length;i++){ need(5); doc.text(ln[i],M,y+4.3); y+=4.6; }
      y+=4;
    }
    // Title band
    var title=kind==='path'?'Pathology request':'Radiology / nuclear medicine request';
    doc.setFillColor(16,36,63); doc.rect(0,0,W,20,'F');
    doc.setTextColor(255,255,255); doc.setFont('helvetica','bold'); doc.setFontSize(16); doc.text(title,M,12.5);
    var urg=val(f,kind==='path'?'t_urgency':'i_urgency');
    if(urg&&urg!=='Routine'){ doc.setFontSize(10); doc.setFillColor(176,32,40); var tw=doc.getTextWidth(urg.toUpperCase())+8; doc.roundedRect(W-M-tw,6.5,tw,8,1.5,1.5,'F'); doc.text(urg.toUpperCase(),W-M-tw+4,12); }
    y=28;

    // Referrer
    var m={}; [].forEach.call(meForm.elements,function(el){ if(el.name) m[el.name]=(el.value||'').trim(); });
    head('Requesting doctor');
    pairs([['Name',[m.me_name,m.me_quals].filter(Boolean).join(', ')],['Provider number',m.me_prov],['Department or practice',m.me_prac],['Address',m.me_addr],['Phone',m.me_phone],['Fax',m.me_fax],['Email',m.me_email]]);

    // Patient
    head('Patient');
    var name=[val(f,'pt_surname').toUpperCase(),val(f,'pt_given')].filter(Boolean).join(', ');
    pairs([['Name',name],['Date of birth',val(f,'pt_dob')],['Sex',val(f,'pt_sex')],['Phone',val(f,'pt_phone')],['Address',val(f,'pt_address')],['Medicare number',[val(f,'pt_medicare'),val(f,'pt_irn')?'IRN '+val(f,'pt_irn'):''].filter(Boolean).join('  ')],['DVA number',val(f,'pt_dva')],['MRN / URN',val(f,'pt_mrn')],['Billing',val(f,'pt_billing')],['Copy results to',val(f,'pt_copyto')]]);

    if(kind==='path'){
      head('Tests requested');
      var hs=f.querySelectorAll('h4'), boxes=f.querySelectorAll('.rqbox');
      for(var k=0;k<boxes.length;k++){
        drawGroup(hs[k]?hs[k].textContent:'',[].slice.call(boxes[k].querySelectorAll('input')));
      }
      pairs([['Other tests',val(f,'t_other')],['Urgency',val(f,'t_urgency')],['Fasting',val(f,'t_fasting')],['Collect on or after',val(f,'t_collect')],['Repeat (standing order)',val(f,'t_repeat')]]);
      head('Clinical notes');
      para('',val(f,'t_notes')||' ');
    } else {
      head('Examination');
      drawGroup('Modality',[].slice.call(f.querySelectorAll('input[name="i_mod"]')));
      pairs([['Examination and region',val(f,'i_exam')],['Contrast',val(f,'i_contrast')],['Urgency',val(f,'i_urgency')],['Needed by',val(f,'i_by')],['Preferred provider or site',val(f,'i_site')]]);
      head('Clinical details');
      para('Clinical notes and question to answer',val(f,'i_notes')||' ');
      para('Previous relevant imaging',val(f,'i_prev'));
      var s=[['eGFR (mL/min/1.73 m2)',[val(f,'i_egfr'),val(f,'i_egfrdate')?'('+val(f,'i_egfrdate')+')':''].filter(Boolean).join(' ')],['Diabetes on metformin',val(f,'i_dm')],['Previous contrast reaction',val(f,'i_allergy')],['Pregnant or may be',val(f,'i_preg')],['Breastfeeding',val(f,'i_breast')],['Pacemaker, implant or metal',val(f,'i_implant')],['Claustrophobia',val(f,'i_claus')],['Weight (kg)',val(f,'i_wt')],['Height (cm)',val(f,'i_ht')]];
      if(s.some(function(p){ return p[1]; })||val(f,'i_safety')){ head('Safety screening'); pairs(s,3); para('Safety details',val(f,'i_safety')); }
    }

    function drawGroup(t,inputs){
      if(t){ need(8); doc.setFont('helvetica','bold'); doc.setFontSize(8.5); c(mute); doc.text(clean(t),M,y); y+=4.5; }
      var cols=3, colW=cw/cols;
      for(var i=0;i<inputs.length;i+=cols){
        need(6);
        for(var j=0;j<cols&&i+j<inputs.length;j++){
          var el=inputs[i+j], x=M+j*colW;
          doc.setDrawColor(60,70,85); doc.setLineWidth(0.3); doc.rect(x,y-3,3.4,3.4);
          if(el.checked){ doc.setLineWidth(0.6); doc.line(x+0.6,y-2.4,x+2.8,y-0.2); doc.line(x+2.8,y-2.4,x+0.6,y-0.2); }
          doc.setFont('helvetica',el.checked?'bold':'normal'); doc.setFontSize(9.5); c(el.checked?ink:mute); doc.text(clean(el.value),x+5,y);
        }
        y+=5.4;
      }
      y+=2;
    }

    // Signature block
    need(32); y+=2;
    doc.setDrawColor(150,158,170); doc.setLineWidth(0.3); doc.line(M,y,W-M,y); y+=6;
    doc.setFont('helvetica','normal'); doc.setFontSize(7.5); c(mute); doc.text('Signature',M,y); doc.text('Date of request',M+cw*0.62,y);
    if(drawn){ try{ doc.addImage(cv.toDataURL('image/png'),'PNG',M,y+1,60,18); }catch(e){} }
    doc.setDrawColor(60,70,85); doc.line(M,y+20,M+80,y+20);
    doc.setFont('helvetica','bold'); doc.setFontSize(10); c(ink); doc.text(clean(val(f,'rq_date')),M+cw*0.62,y+6);
    if(m.me_name){ doc.setFont('helvetica','normal'); doc.setFontSize(9); doc.text(clean(m.me_name),M,y+24.5); }

    // Footer on each page
    var n=doc.getNumberOfPages();
    for(var p=1;p<=n;p++){ doc.setPage(p); doc.setFont('helvetica','normal'); doc.setFontSize(7); c(mute); doc.text(clean(title+(name?' - '+name:'')+'   Page '+p+' of '+n),M,292); }

    var fn=(kind==='path'?'Pathology':'Imaging')+'_request_'+(val(f,'pt_surname')||'patient').replace(/[^A-Za-z0-9-]+/g,'')+'_'+(f.rq_date.value||today())+'.pdf';
    return {doc:doc,name:fn,form:f};
  }

  function msg(f,t){ var m=f.querySelector('.rqmsg'); if(m) m.textContent=t; }
  function check(f,kind){
    var miss=[];
    if(!val(f,'pt_surname')) miss.push('patient surname');
    if(!val(f,'pt_dob')) miss.push('date of birth');
    if(kind==='img'&&!val(f,'i_exam')) miss.push('examination');
    if(kind==='path'&&!f.querySelector('input[name="t_tests"]:checked')&&!val(f,'t_other')) miss.push('at least one test');
    var mn=meForm.elements.me_name.value.trim(), mp=meForm.elements.me_prov.value.trim();
    if(!mn||!mp) miss.push('your name and provider number (My details tab)');
    return miss;
  }

  [].forEach.call(document.querySelectorAll('.rqgo'),function(b){
    b.addEventListener('click',function(){
      var kind=b.dataset.form, f=b.closest('form'), miss=check(f,kind);
      if(miss.length) msg(f,'Missing: '+miss.join(', ')+'. The PDF was still made.'); else msg(f,'');
      try{ var r=build(kind); r.doc.save(r.name); if(!miss.length) msg(f,'Saved '+r.name); }
      catch(e){ msg(f,'Could not make the PDF: '+e.message); }
    });
  });
  [].forEach.call(document.querySelectorAll('.rqshare'),function(b){
    if(!(navigator.canShare&&window.File)) return;
    try{ if(!navigator.canShare({files:[new File(['x'],'x.pdf',{type:'application/pdf'})]})) return; }catch(e){ return; }
    b.hidden=false;
    b.addEventListener('click',function(){
      var f=b.closest('form');
      try{ var r=build(b.dataset.form); var file=new File([r.doc.output('blob')],r.name,{type:'application/pdf'});
        navigator.share({files:[file],title:r.name}).catch(function(){}); }
      catch(e){ msg(f,'Could not make the PDF: '+e.message); }
    });
  });
})();
