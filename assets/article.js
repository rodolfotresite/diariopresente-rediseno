/* Tiempo de lectura (200 palabras/min) */
const words=document.getElementById('body').innerText.trim().split(/\s+/).length;
document.getElementById('readTime').textContent=Math.max(1,Math.round(words/200))+' min de lectura';

/* Compartir: usa la URL canónica de la nota publicada */
const U=encodeURIComponent(document.querySelector('link[rel=canonical]').href), T=encodeURIComponent(document.querySelector('h1').textContent.trim());
document.getElementById('shFb').href='https://www.facebook.com/sharer/sharer.php?u='+U;
document.getElementById('shX').href='https://twitter.com/intent/tweet?url='+U+'&text='+T;
document.getElementById('shWa').href='https://wa.me/?text='+T+'%20'+U;
const cp=document.getElementById('shCopy');
cp.addEventListener('click',async()=>{try{await navigator.clipboard.writeText(decodeURIComponent(U));cp.textContent='¡Enlace copiado!'}catch(e){cp.textContent='Copia el enlace de la barra'}setTimeout(()=>cp.textContent='Copiar enlace',2200)});

/* Comentarios: carga diferida (aquí solo demostración) */
document.getElementById('loadComments').addEventListener('click',e=>{e.target.closest('.panel').innerHTML='<p>Demostración: aquí se cargaría el plugin de comentarios de Facebook.</p>'});

/* Progreso de lectura */
const bar=document.getElementById('progressBar'),art=document.getElementById('nota');
const upd=()=>{const r=art.getBoundingClientRect(),h=r.height-innerHeight;bar.style.width=Math.min(100,Math.max(0,(-r.top/(h>0?h:1))*100))+'%'};
addEventListener('scroll',upd,{passive:true});addEventListener('resize',upd);upd();
