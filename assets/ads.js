/* Espacios publicitarios del Media Kit 2026 del Grupo SIT (página "Espacios web").
   Cada espacio se declara en el HTML con <div class="adslot" data-kit="N"></div> y este archivo lo dibuja con
   su nombre y medidas. Si el área comercial cambia el catálogo, solo hay que editar KIT.
   data-prop="1" marca un espacio que se propone en una página que el media kit no cubre (nota, columna, edición). */
(function(){
  /* n = nombre; w × h = medidas en px, tal como aparecen en el documento; p = dónde va; nota = observación del documento */
  const KIT={
    1:{n:'Top Large Leaderboard',w:970,h:90,p:'Home',nota:'Nuevo'},
    2:{n:'Leaderboard',w:728,h:90,p:'Home'},
    3:{n:'Medium Rectangle',w:300,h:250,p:'Home'},
    4:{n:'Half Page',w:300,h:600,p:'Home'},
    5:{n:'Top Large Leaderboard',w:970,h:90,p:'Secciones'},
    6:{n:'Leaderboard',w:728,h:90,p:'Secciones'},
    7:{n:'Medium Rectangle',w:300,h:250,p:'Secciones'},
    8:{n:'Billboard',w:970,h:200,p:'Secciones'},
    9:{n:'Floor Ad',w:970,h:250,p:'Secciones'},
    10:{n:'Layer',p:'Home y secciones',demo:'layer'},
    11:{n:'Intersticial móvil',p:'Home (móvil)',demo:'inter'}
  };
  const $$=(s,r)=>[...(r||document).querySelectorAll(s)];

  function pinta(el){
    if(el.dataset.ready)return;
    const k=+el.dataset.kit,s=KIT[k];
    if(!s||!s.w)return;
    const prop=el.hasAttribute('data-prop');
    el.dataset.ready='1';
    el.style.setProperty('--w',s.w);el.style.setProperty('--h',s.h);
    el.classList.toggle('wide',s.h<=100);
    el.setAttribute('role','note');
    el.setAttribute('aria-label',`Espacio publicitario ${k}: ${s.n}, ${s.w} por ${s.h} píxeles${prop?' (propuesta, no incluida en el media kit)':''}`);
    el.title=`${k} · ${s.n} · ${s.p}${prop?' · propuesta':''}`;
    el.innerHTML=`<span class="ad-num" aria-hidden="true">${k}</span><span class="ad-tag" aria-hidden="true">Publicidad${prop?' · propuesta':''}</span><strong>${s.n}</strong><span class="ad-size">${s.w} × ${s.h} px</span>${s.h>100?`<small>${s.p}${s.nota?' · '+s.nota:''}</small>`:''}`;
  }
  const pintaTodo=root=>$$('.adslot',root).forEach(pinta);
  pintaTodo(document);
  new MutationObserver(ms=>ms.forEach(m=>m.addedNodes.forEach(n=>{if(n.nodeType!==1)return;if(n.matches('.adslot'))pinta(n);pintaTodo(n)}))).observe(document.body,{childList:true,subtree:true});

  /* ---- Demostraciones de los formatos sin ubicación fija (10 Layer, 11 Intersticial móvil) ---- */
  function demo(tipo){
    const d=document.createElement('dialog');
    d.className=tipo==='layer'?'ad-demo ad-layer':'ad-demo ad-inter';
    const s=tipo==='layer'?KIT[10]:KIT[11];
    d.setAttribute('aria-label',`Demostración: ${s.n}`);
    d.innerHTML=`<button type="button" class="ad-close" aria-label="Cerrar">✕ Cerrar</button><div class="ad-demo-box"><span class="ad-tag" aria-hidden="true">Publicidad · demostración</span><strong>${s.n}</strong><span class="ad-size">${tipo==='layer'?'Capa que se superpone al contenido':'Pantalla completa en móvil'}</span><small>Tamaño no especificado en el media kit: por confirmar con el área comercial.</small></div>`;
    document.body.appendChild(d);
    d.querySelector('.ad-close').addEventListener('click',()=>d.close());
    d.addEventListener('close',()=>d.remove());
    d.addEventListener('click',e=>{if(e.target===d)d.close()});
    d.showModal();
  }

  /* ---- Guía de espacios ---- */
  function guia(){
    let g=document.getElementById('adGuide');
    if(g){g.showModal();return}
    g=document.createElement('dialog');g.id='adGuide';g.className='ad-guide';g.setAttribute('aria-labelledby','adGuideT');
    const filas=Object.entries(KIT).map(([k,s])=>{
      const n=s.w?$$(`.adslot[data-kit="${k}"]`).length:0;
      const medidas=s.w?`${s.w} × ${s.h} px`:'<em>no especificadas</em>';
      const accion=s.demo?`<button type="button" class="btn ad-go" data-demo="${s.demo}">Ver demostración</button>`:(n?`<button type="button" class="btn ad-go" data-ver="${k}">Mostrar (${n})</button>`:'<span class="ad-no">No está en esta página</span>');
      return `<tr><th scope="row"><span class="ad-num ad-num-static">${k}</span></th><td><strong>${s.n}</strong>${s.nota?` <small>(${s.nota})</small>`:''}</td><td>${medidas}</td><td>${s.p}</td><td>${accion}</td></tr>`;
    }).join('');
    g.innerHTML=`<div class="ad-guide-head"><h2 id="adGuideT">Espacios publicitarios</h2><button type="button" class="ad-close" aria-label="Cerrar">✕ Cerrar</button></div>
      <p class="ad-guide-intro">Los 11 espacios del <strong>Media Kit 2026 del Grupo SIT</strong> (página “Espacios web”), con las medidas del documento. Los marcados como <em>propuesta</em> están en páginas que el media kit no cubre (nota, columna, edición impresa).</p>
      <div class="ad-guide-scroll"><table><thead><tr><th scope="col">#</th><th scope="col">Espacio</th><th scope="col">Medidas</th><th scope="col">Dónde</th><th scope="col">En esta página</th></tr></thead><tbody>${filas}</tbody></table></div>
      <p class="ad-guide-foot">Espacios sujetos a disponibilidad. Las medidas son las del documento; el Billboard aparece como 970 × 200 px y el Floor Ad como 970 × 250 px.</p>`;
    document.body.appendChild(g);
    g.querySelector('.ad-close').addEventListener('click',()=>g.close());
    g.addEventListener('click',e=>{if(e.target===g)g.close()});
    g.addEventListener('close',()=>g.remove());
    g.addEventListener('click',e=>{
      const b=e.target.closest('button[data-ver],button[data-demo]');if(!b)return;
      g.close();
      if(b.dataset.demo){demo(b.dataset.demo);return}
      const els=$$(`.adslot[data-kit="${b.dataset.ver}"]`);
      els[0].scrollIntoView({block:'center',behavior:'smooth'});
      els.forEach(el=>{el.classList.remove('flash');void el.offsetWidth;el.classList.add('flash')});
      setTimeout(()=>els.forEach(el=>el.classList.remove('flash')),3200);
    });
    g.showModal();
  }

  /* ---- Barra de borrador (abajo a la izquierda) ---- */
  const t=document.createElement('div');t.className='draft-tools';
  t.innerHTML='<span>Borrador de rediseño · contenido de ejemplo</span><button type="button" id="adGuideBtn">Espacios publicitarios</button>';
  document.body.appendChild(t);
  t.querySelector('button').addEventListener('click',guia);
})();
