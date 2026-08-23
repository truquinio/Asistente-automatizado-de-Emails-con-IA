const CATEGORY_LABEL = {
    soporte:'Soporte', ventas:'Ventas', consulta:'Consulta', spam:'Spam', otro:'Otro'
  };

  const EMAILS = [
    {
      id:1, from:'cliente@empresa.com', subject:'Problema con mi pedido reciente',
      date:'15 may, 10:30', category:'soporte', confidence:94,
      body:'Hola, tengo un problema con el pedido #12345 que hice la semana pasada. El producto llegó dañado. ¿Cómo puedo solicitar un reemplazo?',
      response:'Estimado cliente,\n\nHemos recibido su reporte sobre "Problema con mi pedido reciente". Nuestro equipo de soporte se contactará con usted en las próximas 24 horas.\n\nAtentamente,\nEl equipo de soporte'
    },
    {
      id:2, from:'prospecto@otraempresa.com', subject:'Consulta sobre sus servicios',
      date:'15 may, 11:45', category:'consulta', confidence:88,
      body:'Buen día, estoy interesado en sus servicios empresariales. ¿Podrían enviarme información sobre sus planes y precios?',
      response:'Gracias por su interés en nuestros servicios.\n\nHemos recibido su consulta sobre "Consulta sobre sus servicios". Adjunto encontrará información detallada sobre nuestros productos.\n\nQuedamos atentos a sus comentarios.\n\nCordialmente,\nEl equipo comercial'
    },
    {
      id:3, from:'soporte@terceros.com', subject:'Colaboración entre empresas',
      date:'16 may, 09:15', category:'ventas', confidence:81,
      body:'Nos gustaría explorar oportunidades de colaboración. ¿Estarían disponibles para una reunión la próxima semana?',
      response:'Estimado/a,\n\nAgradecemos su interés en colaborar con nosotros. Nos encantaría programar una reunión para discutir oportunidades. ¿Estaría disponible el próximo miércoles a las 2pm?\n\nSaludos cordiales,\nEl equipo de alianzas'
    },
    {
      id:4, from:'facturacion@proveedorxyz.com', subject:'Factura #A-4471 vencida',
      date:'16 may, 14:02', category:'soporte', confidence:90,
      body:'Notamos que la factura #A-4471 sigue pendiente de pago. Por favor confirmen si hubo algún inconveniente con la transferencia.',
      response:'Estimado cliente,\n\nHemos recibido su reporte sobre "Factura #A-4471 vencida". Nuestro equipo de soporte se contactará con usted en las próximas 24 horas.\n\nAtentamente,\nEl equipo de soporte'
    },
    {
      id:5, from:'gana-dinero@promo-ofertas.biz', subject:'¡GANASTE un premio, reclamalo YA!',
      date:'16 may, 15:40', category:'spam', confidence:99,
      body:'Felicidades, has sido seleccionado para reclamar un premio exclusivo. Hacé clic en el enlace antes de que expire.',
      response:null
    },
    {
      id:6, from:'rrhh@empresa.com', subject:'Confirmación de entrevista',
      date:'17 may, 08:55', category:'otro', confidence:73,
      body:'Le escribimos para confirmar la entrevista programada para el jueves a las 10am en nuestras oficinas.',
      response:'Hemos recibido su mensaje con asunto: "Confirmación de entrevista".\n\nNos pondremos en contacto con usted pronto.\n\nAtentamente,\nEl equipo de atención al cliente'
    },
    {
      id:7, from:'partner@aliado-tech.com', subject:'Propuesta de integración API',
      date:'17 may, 11:20', category:'ventas', confidence:85,
      body:'Nos gustaría proponerles una integración entre nuestras plataformas. Adjunto documentación técnica preliminar.',
      response:'Estimado/a,\n\nAgradecemos su interés en colaborar con nosotros. Nos encantaría programar una reunión para discutir oportunidades. ¿Estaría disponible el próximo miércoles a las 2pm?\n\nSaludos cordiales,\nEl equipo de alianzas'
    }
  ];

  const state = { view:'inbox', filter:'todos', selectedId:null, status:{} };

  function counts(){
    const c = {soporte:0, ventas:0, consulta:0, spam:0, otro:0};
    EMAILS.forEach(e => c[e.category]++);
    return c;
  }

  function sentCount(){
    return Object.values(state.status).filter(s => s==='aprobado').length;
  }

  function renderManifest(){
    const c = counts();
    const el = document.getElementById('manifest');
    el.innerHTML = `
      <div class="stat"><span class="n">${EMAILS.length}</span><span class="l">Procesados</span></div>
      <div class="stat"><span class="n soporte">${c.soporte}</span><span class="l">Soporte</span></div>
      <div class="stat"><span class="n ventas">${c.ventas}</span><span class="l">Ventas</span></div>
      <div class="stat"><span class="n consulta">${c.consulta}</span><span class="l">Consulta</span></div>
      <div class="stat"><span class="n enviados">${sentCount()}</span><span class="l">Enviados</span></div>
    `;
  }

  function renderTabs(){
    const el = document.getElementById('tabs');
    if(!el) return;
    const tabs = [
      { id:'inbox', label:'Bandeja', count: EMAILS.length },
      { id:'sent', label:'Enviados', count: sentCount() }
    ];
    el.innerHTML = tabs.map(t =>
      `<button class="tab-btn ${state.view===t.id?'active':''}" data-view="${t.id}">${t.label} <span class="count">${t.count}</span></button>`
    ).join('');
    el.querySelectorAll('.tab-btn').forEach(btn=>{
      btn.addEventListener('click', ()=>{
        state.view = btn.dataset.view;
        renderTabs();
        renderInbox();
      });
    });
  }

  function renderFilters(){
    const cats = ['todos','soporte','ventas','consulta','spam','otro'];
    const el = document.getElementById('filters');
    el.innerHTML = cats.map(c =>
      `<button class="pill ${state.filter===c?'active':''}" data-cat="${c}">${c==='todos'?'Todos':CATEGORY_LABEL[c]}</button>`
    ).join('');
    el.querySelectorAll('.pill').forEach(btn=>{
      btn.addEventListener('click', ()=>{ state.filter = btn.dataset.cat; renderFilters(); renderInbox(); });
    });
  }

  function renderInbox(){
    const base = state.view==='sent'
      ? EMAILS.filter(e => state.status[e.id]==='aprobado')
      : EMAILS;
    const list = base.filter(e => state.filter==='todos' || e.category===state.filter);
    const el = document.getElementById('inbox');
    if(list.length===0){
      const msg = state.view==='sent'
        ? 'Todavía no enviaste ninguna respuesta. Aprobá un correo desde la Bandeja para verlo acá.'
        : 'No hay correos en esta categoría.';
      el.innerHTML = `<div class="empty">${msg}</div>`;
      return;
    }
    el.innerHTML = list.map(e => `
      <li class="row ${state.selectedId===e.id?'selected':''}" tabindex="0" data-id="${e.id}">
        <span class="dot ${e.category}"></span>
        <span class="meta">
          <span class="from">${e.from} · ${e.date}</span><br>
          <span class="subject">${e.subject}</span>
        </span>
        <span class="status ${state.status[e.id]==='aprobado'?'aprobado':''}">${state.status[e.id]==='aprobado' ? 'Aprobado' : (e.category==='spam' ? 'Descartado' : 'Pendiente')}</span>
      </li>
    `).join('');
    el.querySelectorAll('.row').forEach(row=>{
      const open = ()=>{ state.selectedId = Number(row.dataset.id); renderInbox(); renderDetail(); };
      row.addEventListener('click', open);
      row.addEventListener('keydown', ev=>{ if(ev.key==='Enter') open(); });
    });
  }

  function renderDetail(){
    const el = document.getElementById('detail');
    const e = EMAILS.find(x => x.id===state.selectedId);
    if(!e){
      el.innerHTML = `<div class="empty">Seleccioná un correo de la bandeja para ver la clasificación y la respuesta generada.</div>`;
      return;
    }
    const isSpam = e.category==='spam';
    const approved = state.status[e.id]==='aprobado';
    el.innerHTML = `
      <div class="detail-header">
        <div>
          <h2>${e.subject}</h2>
          <div class="from-line">De: ${e.from} · ${e.date}</div>
        </div>
        <div class="stamp ${e.category}">
          <span class="cat">${CATEGORY_LABEL[e.category]}</span>
          <span class="conf">${e.confidence}% conf.</span>
        </div>
      </div>

      <div class="body-block">
        <span class="label">Correo original</span>
        <p>${e.body}</p>
      </div>

      ${isSpam
        ? `<div class="response-block discarded"><span class="label">Respuesta automática</span>No se genera respuesta — los mensajes clasificados como spam se descartan automáticamente.</div>`
        : `<div class="response-block"><span class="label">Respuesta generada por IA</span><pre>${e.response}</pre></div>`
      }

      <div class="actions">
        ${isSpam
          ? `<button class="btn ghost" disabled>Sin acciones para spam</button>`
          : `<button class="btn primary" id="approveBtn" ${approved?'disabled':''}>${approved?'Aprobada ✓':'Aprobar y enviar'}</button>
             <button class="btn ghost" id="editBtn">Editar respuesta</button>`
        }
      </div>
    `;
    const approveBtn = document.getElementById('approveBtn');
    if(approveBtn){
      approveBtn.addEventListener('click', ()=>{
        state.status[e.id] = 'aprobado';
        renderManifest();
        renderTabs();
        renderInbox();
        renderDetail();
      });
    }
    const editBtn = document.getElementById('editBtn');
    if(editBtn){
      editBtn.addEventListener('click', ()=>{
        const pre = el.querySelector('.response-block pre');
        pre.contentEditable = 'true';
        pre.focus();
        editBtn.textContent = 'Editando…';
        editBtn.disabled = true;
      });
    }
  }

  renderManifest();
  renderTabs();
  renderFilters();
  renderInbox();
