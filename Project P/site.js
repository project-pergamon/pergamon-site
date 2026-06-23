// mobile menu only — pages are real links, no routing needed
const nav=document.getElementById('nav'),tog=document.getElementById('menuToggle'),scrim=document.getElementById('scrim');
function setMenu(o){nav.classList.toggle('open',o);scrim.classList.toggle('show',o);tog.setAttribute('aria-expanded',o);}
tog.addEventListener('click',()=>setMenu(!nav.classList.contains('open')));
scrim.addEventListener('click',()=>setMenu(false));
nav.querySelectorAll('a').forEach(a=>a.addEventListener('click',()=>setMenu(false)));
