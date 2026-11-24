// My weekly roster: Week A/B clinical sessions merged with the KCC MDT planner.
// Anchor: Monday 23 Nov 2026 = roster Week A and MDT week 3. Weeks can be nudged on the page (saved on this device).
(function(){
  var ANCHOR = new Date(2026, 10, 23); // Mon 23 Nov 2026
  var DAYS = ['Monday','Tuesday','Wednesday','Thursday','Friday'];
  // Sessions: [AM, PM] per day. '' = nothing rostered.
  var ROSTER = {
    A: [['ZAP-X / MR-linac','ZAP-X / MR-linac'], ['MR-linac','SS clinic'], ['JdL overflow clinic','ZAP-X'], ['JdL clinic','JdL clinic'], ['','MR-linac']],
    B: [['ZAP-X / MR-linac','ZAP-X / MR-linac'], ['MR-linac','JdL clinic'], ['JdL overflow clinic','ZAP-X'], ['JdL clinic','SS clinic'], ['','MR-linac']]
  };
  // KCC Cancer Service MDT planner (updated Nov 2026). day 0 = Monday; start/end in minutes; weeks = MDT weeks 1-4.
  var MDTS = [
    {id:'ugi',  name:'Upper GI',        day:0, s:450, e:510, weeks:[2,4]},
    {id:'crc',  name:'Colorectal',      day:0, s:780, e:840, weeks:[1,3]},
    {id:'uro',  name:'Urology',         day:1, s:420, e:510, weeks:[2,4]},
    {id:'brst', name:'Breast',          day:1, s:540, e:600, weeks:[1,2,3,4]},
    {id:'hnp',  name:'H&N pathology',   day:1, s:600, e:645, weeks:[1,3]},
    {id:'hn',   name:'Head and neck',   day:1, s:660, e:780, weeks:[1,2,3,4]},
    {id:'haem', name:'Haematology',     day:1, s:930, e:990, weeks:[2,4]},
    {id:'liver',name:'Liver',           day:2, s:450, e:510, weeks:[2,4]},
    {id:'neuro',name:'Neuro-oncology',  day:2, s:480, e:540, weeks:[1,3]},
    {id:'lnod', name:'Lung nodule',     day:3, s:450, e:480, weeks:[3]},
    {id:'lung', name:'Lung',            day:3, s:480, e:540, weeks:[1,2,3,4]},
    {id:'thyr', name:'Thyroid',         day:3, s:540, e:600, weeks:[1]}
  ];
  var DEFAULT_MINE = ['crc','neuro'];
  var KEY = 'qr-roster';
  function load(){ try{ return JSON.parse(localStorage.getItem(KEY)||'{}'); }catch(e){ return {}; } }
  function save(o){ try{ localStorage.setItem(KEY, JSON.stringify(o)); }catch(e){} }
  var st = load(); if(!st.mine) st.mine = DEFAULT_MINE.slice(); st.abShift = st.abShift||0; st.mdtShift = st.mdtShift||0;
  var offset = 0; // weeks from the current week being viewed

  function monday(d){ var x = new Date(d.getFullYear(), d.getMonth(), d.getDate()); var w = (x.getDay()+6)%7; x.setDate(x.getDate()-w); return x; }
  function weeksBetween(a,b){ return Math.round((b - a) / 604800000); }
  function mod(n,m){ return ((n%m)+m)%m; }
  function t(m){ var h = Math.floor(m/60), mm = m%60, ap = h>=12?'pm':'am'; h = h%12||12; return h + (mm? ':' + (mm<10?'0':'') + mm : '') + ap; }
  function fmt(d){ return d.toLocaleDateString('en-AU',{day:'numeric', month:'short'}); }
  function esc(s){ return s.replace(/[&<>]/g, function(c){ return {'&':'&amp;','<':'&lt;','>':'&gt;'}[c]; }); }

  function weekInfo(off){
    var mon = monday(new Date()); mon.setDate(mon.getDate() + 7*off);
    var n = weeksBetween(ANCHOR, mon);
    return { mon: mon, ab: mod(n + st.abShift, 2) === 0 ? 'A' : 'B', mdt: mod(n + 2 + st.mdtShift, 4) + 1 };
  }

  function render(){
    var out = document.getElementById('rosterWeek'); if(!out) return;
    var w = weekInfo(offset), today = new Date(); today.setHours(0,0,0,0);
    var fri = new Date(w.mon); fri.setDate(fri.getDate()+4);
    document.getElementById('rosterLabel').innerHTML = '<b>Week ' + w.ab + '</b> · MDT week ' + w.mdt + '<br><span class="note">' + fmt(w.mon) + ' – ' + fmt(fri) + (offset===0?' (this week)':'') + '</span>';
    var html = '';
    DAYS.forEach(function(day, i){
      var date = new Date(w.mon); date.setDate(date.getDate()+i);
      var isToday = date.getTime() === today.getTime();
      var s = ROSTER[w.ab][i];
      var items = [];
      MDTS.forEach(function(m){ if(m.day===i && m.weeks.indexOf(w.mdt)>=0 && st.mine.indexOf(m.id)>=0) items.push({k: m.s, mdt: true, txt: m.name + ' MDT', time: t(m.s) + '–' + t(m.e)}); });
      items.push({k: 600, txt: s[0] || '—', time: 'AM', ses: true, free: !s[0]});
      items.push({k: 840, txt: s[1] || '—', time: 'PM', ses: true, free: !s[1]});
      // MDTs starting 9am or later fall inside a session; flag them if that session is rostered
      items.forEach(function(it){ if(it.mdt && it.k >= 540){ var am = it.k < 750, sess = am ? s[0] : s[1]; if(sess) it.clash = 'during ' + (am ? 'AM' : 'PM') + ' session'; } });
      items.sort(function(a,b){ return a.k - b.k; });
      html += '<div class="rday' + (isToday?' today':'') + '"><h4>' + day + ' <span class="note">' + fmt(date) + (isToday?' · today':'') + '</span></h4><ul>';
      items.forEach(function(it){
        html += '<li class="' + (it.mdt?'rmdt':'') + (it.free?' rfree':'') + '"><span class="rt">' + it.time + '</span><span>' + esc(it.txt) + (it.clash?' <span class="rclash">' + it.clash + '</span>':'') + '</span></li>';
      });
      html += '</ul></div>';
    });
    out.innerHTML = html;
  }

  function mineUI(){
    var box = document.getElementById('rosterMine'); if(!box) return;
    box.innerHTML = MDTS.map(function(m){
      return '<label class="rpick"><input type="checkbox" value="' + m.id + '"' + (st.mine.indexOf(m.id)>=0?' checked':'') + '> ' + esc(m.name) + ' <span class="note">(' + ['Mon','Tue','Wed','Thu'][m.day] + ' ' + t(m.s) + ')</span></label>';
    }).join('');
    box.addEventListener('change', function(e){
      var v = e.target.value, i = st.mine.indexOf(v);
      if(e.target.checked && i<0) st.mine.push(v); if(!e.target.checked && i>=0) st.mine.splice(i,1);
      save(st); render();
    });
  }

  function on(id, fn){ var b = document.getElementById(id); if(b) b.addEventListener('click', fn); }
  on('rPrev', function(){ offset--; render(); });
  on('rNow', function(){ offset = 0; render(); });
  on('rNext', function(){ offset++; render(); });
  on('rFlipAB', function(){ st.abShift = mod(st.abShift+1,2); save(st); render(); });
  on('rMdtUp', function(){ st.mdtShift = mod(st.mdtShift+1,4); save(st); render(); });
  on('rReset', function(){ st.abShift = 0; st.mdtShift = 0; st.mine = DEFAULT_MINE.slice(); save(st); document.getElementById('rosterMine').innerHTML=''; mineUI(); render(); });
  mineUI(); render();
})();
