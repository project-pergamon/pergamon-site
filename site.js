// mobile menu only — pages are real links, no routing needed
const nav=document.getElementById('nav'),tog=document.getElementById('menuToggle'),scrim=document.getElementById('scrim');
function setMenu(o){nav.classList.toggle('open',o);scrim.classList.toggle('show',o);tog.setAttribute('aria-expanded',o);}
if(tog){tog.addEventListener('click',()=>setMenu(!nav.classList.contains('open')));}
if(scrim){scrim.addEventListener('click',()=>setMenu(false));}
if(nav){nav.querySelectorAll('a').forEach(a=>a.addEventListener('click',()=>setMenu(false)))}

const notesPanel=document.getElementById('notesPanel');
if(notesPanel){
  const footnoteLinks=document.querySelectorAll('.faq a[id^="fnref"]');
  footnoteLinks.forEach(link=>{
    link.addEventListener('click',event=>{
      const href=link.getAttribute('href')||'';
      if(!href.startsWith('#fn')) return;
      event.preventDefault();
      notesPanel.open=true;
      const targetId=href.slice(1);
      const targetNote=document.getElementById(targetId);
      if(targetNote){
        targetNote.classList.add('is-active');
        targetNote.scrollIntoView({behavior:'smooth',block:'start'});
        window.setTimeout(()=>targetNote.classList.remove('is-active'),1800);
      }
    });
  });
}
