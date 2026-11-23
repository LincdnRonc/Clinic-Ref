// Rarely used tabs (eviQ, Guidelines, Exam notes) sit behind a "More" chip.
// To revert, set MORE_TABS = False in build.py and rebuild.
(function(){
  var chips = document.getElementById('chips'); if(!chips) return;
  var RARE = ['eviq','guidelines','exam'];
  var extra = RARE.map(function(t){ return document.getElementById('chip-' + t); }).filter(Boolean);
  if(!extra.length) return;
  var more = document.createElement('button');
  more.type = 'button'; more.className = 'chip chip-more'; more.textContent = 'More ▾';
  more.setAttribute('aria-expanded', 'false');
  chips.appendChild(more);
  extra.forEach(function(c){ c.classList.add('chip-rare'); chips.appendChild(c); });
  function set(open){ chips.classList.toggle('more-open', open); more.setAttribute('aria-expanded', open ? 'true' : 'false'); more.textContent = open ? 'Less ▴' : 'More ▾'; }
  more.addEventListener('click', function(){ set(!chips.classList.contains('more-open')); });
  // keep them visible when one of them is the open tab
  function sync(){ if(extra.some(function(c){ return c.getAttribute('aria-selected') === 'true'; })) set(true); }
  sync(); window.addEventListener('hashchange', function(){ setTimeout(sync, 0); });
})();
