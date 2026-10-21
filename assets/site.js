/* Fecha */
const f=new Intl.DateTimeFormat('es-MX',{weekday:'long',day:'numeric',month:'long',year:'numeric'}).format(new Date());
document.getElementById('today').innerHTML=f.charAt(0).toUpperCase()+f.slice(1)+'<span class="city"> · Villahermosa, Tabasco</span>';

/* Tema, tamaño de texto, búsqueda, menú */
const root=document.documentElement;
try{const s=localStorage.getItem('presente-theme');if(s)root.dataset.theme=s}catch(e){}
document.getElementById('themeBtn').addEventListener('click',()=>{root.dataset.theme=root.dataset.theme==='dark'?'light':'dark';try{localStorage.setItem('presente-theme',root.dataset.theme)}catch(e){}});
/* Tamaño de texto: 5 niveles compartidos por todo el sitio y recordados entre visitas.
   El botón "Aa" del encabezado los recorre; la nota añade A− / A+ con los mismos niveles. */
const TEXT_LEVELS=[0.875,1,1.125,1.25,1.5],TEXT_DEFAULT=1;
let textLevel=TEXT_DEFAULT;
try{const s=parseInt(localStorage.getItem('presente-text-level'),10);if(s>=0&&s<TEXT_LEVELS.length)textLevel=s}catch(e){}
const tsMinus=document.getElementById('tsMinus'),tsPlus=document.getElementById('tsPlus'),tsLabel=document.getElementById('tsLabel');
function setTextLevel(n){
  textLevel=Math.min(TEXT_LEVELS.length-1,Math.max(0,n));
  root.style.setProperty('--reading-size',TEXT_LEVELS[textLevel]+'rem');
  try{localStorage.setItem('presente-text-level',textLevel)}catch(e){}
  if(tsLabel)tsLabel.textContent=Math.round(TEXT_LEVELS[textLevel]*100)+'%';
  if(tsMinus)tsMinus.disabled=textLevel===0;
  if(tsPlus)tsPlus.disabled=textLevel===TEXT_LEVELS.length-1;
}
setTextLevel(textLevel);
document.getElementById('fontBtn').addEventListener('click',()=>setTextLevel(textLevel+1>=TEXT_LEVELS.length?0:textLevel+1));
if(tsMinus)tsMinus.addEventListener('click',()=>setTextLevel(textLevel-1));
if(tsPlus)tsPlus.addEventListener('click',()=>setTextLevel(textLevel+1));
if(tsLabel)tsLabel.addEventListener('click',()=>setTextLevel(TEXT_DEFAULT));
const dlg=document.getElementById('searchDialog');document.getElementById('searchBtn').onclick=()=>dlg.showModal();document.getElementById('closeSearch').onclick=()=>dlg.close();dlg.addEventListener('click',e=>{if(e.target===dlg)dlg.close()});
const mb=document.getElementById('menuBtn'),nm=document.getElementById('navMenu');
mb.addEventListener('click',()=>{const o=nm.classList.toggle('open');mb.setAttribute('aria-expanded',o);mb.textContent=o?'✕':'☰'});
document.querySelectorAll('form').forEach(f=>f.addEventListener('submit',e=>{e.preventDefault();alert('Demostración: conectar con el buscador del CMS / lista de Mailchimp.')}));

/* Enlaces provisionales (href="#"): no saltar al inicio de la página */
document.addEventListener('click',e=>{const a=e.target.closest('a[href="#"]');if(a)e.preventDefault()});

/* Ticker: la segunda copia (para el bucle de la animación) no debe leerse ni recibir foco dos veces */
const tt=document.getElementById('tickerTrack');
if(tt){const kids=[...tt.children];kids.slice(kids.length/2).forEach(a=>{a.setAttribute('aria-hidden','true');a.tabIndex=-1})}

/* ---- Vista previa del draft (GitHub Pages) ----
   Las notas, columnas y páginas que aún no existen en el draft usan rutas del sitio actual (/seccion/slug/id).
   En la vista previa esos enlaces se abren en diariopresente.mx, en una pestaña nueva.
   Quitar este bloque cuando las páginas se generen desde el CMS. */
(function(){
  const LIVE='https://diariopresente.mx';
  /* Notas: /seccion/slug/id → nota.html?id=… (contenido en data/notas, ver tools/fetch_notas.py) */
  const NOTA=/^\/(?:tabasco|villahermosa|sucesos|mexico|politica|mundo|deportes|espectaculos|actualidad|cultura|sociales)\/(?:[^\/?#]+\/)+(\d{4,8})\/?$/;
  /* Columnas de opinión: /opinion/slug/id → columna.html?id=… (data/columnas, ver tools/fetch_columnas.py) */
  const COLUMNA=/^\/opinion\/[^\/?#]+\/(\d{4,8})\/?$/;
  const fixA=a=>{const h=a.getAttribute('href');if(!h||h.startsWith('//'))return;const m=h.match(NOTA);if(m){a.setAttribute('href','nota.html?id='+m[1]);return}const o=h.match(COLUMNA);if(o){a.setAttribute('href','columna.html?id='+o[1]);return}a.setAttribute('href',LIVE+h);a.target='_blank';a.rel='noopener';if(!a.title)a.title='Abre en el sitio actual (aún no rediseñado)'};
  const fixAll=root=>root.querySelectorAll('a[href^="/"]').forEach(fixA);
  fixAll(document);
  new MutationObserver(ms=>ms.forEach(m=>m.addedNodes.forEach(n=>{if(n.nodeType!==1)return;if(n.matches('a[href^="/"]'))fixA(n);fixAll(n)}))).observe(document.body,{childList:true,subtree:true});
  const b=document.createElement('div');b.className='draft-badge';b.textContent='Borrador de rediseño · contenido de ejemplo';document.body.appendChild(b);
})();
