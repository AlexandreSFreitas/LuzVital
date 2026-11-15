/* LuzVital — guia da API: tabela de rotas e testador simples (fetch na mesma origem). */
(function () {
  'use strict';

  const regiao = { nome: 'Vila Sônia (teste)', cidade: 'São Paulo', uf: 'SP' };
  const paciente = {
    nome: 'Paciente Teste', dataNascimento: '1950-05-10',
    logradouro: 'Rua Exemplo', numero: '100', complemento: null, cep: '05870-010',
    idRegiao: 3, observacaoAtendimento: 'Dado fictício para teste', ativo: true
  };

  // Rotas que existem no backend (backend/src/main/java/br/com/luzvital/controller)
  const ROTAS = [
    { m: 'GET', p: '/api/regioes', d: 'Lista as regiões', r: '200' },
    { m: 'GET', p: '/api/regioes/1', d: 'Busca uma região pelo id', r: '200, 404' },
    { m: 'POST', p: '/api/regioes', d: 'Cria uma região', r: '201, 400, 409', b: regiao },
    { m: 'PUT', p: '/api/regioes/{id}', d: 'Atualiza uma região', r: '200, 400, 404', b: regiao },
    { m: 'DELETE', p: '/api/regioes/{id}', d: 'Remove uma região (bloqueado se tiver pacientes)', r: '204, 404, 409' },
    { m: 'GET', p: '/api/pacientes', d: 'Lista os pacientes', r: '200' },
    { m: 'GET', p: '/api/pacientes/1', d: 'Busca um paciente pelo id', r: '200, 404' },
    { m: 'POST', p: '/api/pacientes', d: 'Cadastra um paciente (região precisa existir)', r: '201, 400, 404', b: paciente },
    { m: 'PUT', p: '/api/pacientes/{id}', d: 'Atualiza um paciente; "ativo": false desativa', r: '200, 400, 404', b: Object.assign({}, paciente, { ativo: false }) },
    { m: 'DELETE', p: '/api/pacientes/{id}', d: 'Remove um paciente (bloqueado se tiver contatos ou alertas)', r: '204, 404, 409' },
    { m: 'GET', p: '/api/interrupcoes', d: 'Lista as interrupções de energia', r: '200' },
    { m: 'GET', p: '/api/interrupcoes/1', d: 'Busca uma interrupção pelo id', r: '200, 404' },
    { m: 'POST', p: '/api/interrupcoes', d: 'Registra uma interrupção e gera os alertas dos pacientes da região, por prioridade', r: '201, 400, 404', b: { idRegiao: 3, duracaoEstimadaMin: 120 } }
  ];

  function el(tag, props, filhos) {
    const n = document.createElement(tag);
    Object.entries(props || {}).forEach(function (kv) {
      if (kv[0] === 'class') n.className = kv[1];
      else if (kv[0] === 'text') n.textContent = kv[1];
      else n.setAttribute(kv[0], kv[1]);
    });
    (filhos || []).forEach(function (f) { n.append(f); });
    return n;
  }

  document.addEventListener('DOMContentLoaded', function () {
    const corpoTabela = document.querySelector('[data-rotas]');
    const form = document.querySelector('[data-testador]');
    const metodo = form.elements.metodo, caminho = form.elements.caminho, servidor = form.elements.servidor, corpo = form.elements.corpo;
    const campoCorpo = document.querySelector('[data-campo-corpo]');
    const exclusao = document.querySelector('[data-confirmar-exclusao]');
    const status = document.querySelector('[data-status]');
    const resposta = document.querySelector('[data-resposta]');
    const enviar = document.querySelector('[data-enviar]');
    const arquivoLocal = location.protocol === 'file:';

    document.querySelector('[data-base]').textContent = arquivoLocal ? '/api' : location.origin + '/api';
    if (arquivoLocal) document.querySelector('[data-aviso-origem]').hidden = false;

    ROTAS.forEach(function (r) {
      const botao = el('button', { class: 'botao-testar', type: 'button', 'aria-label': 'Testar ' + r.m + ' ' + r.p, text: 'Testar' });
      botao.addEventListener('click', function () {
        metodo.value = r.m; caminho.value = r.p;
        corpo.value = r.b ? JSON.stringify(r.b, null, 2) : '';
        atualizarCampos();
        document.getElementById('testador').scrollIntoView({ behavior: matchMedia('(prefers-reduced-motion: reduce)').matches ? 'auto' : 'smooth' });
        caminho.focus({ preventScroll: true });
      });
      corpoTabela.append(el('tr', {}, [
        el('td', {}, [el('span', { class: 'metodo metodo--' + r.m.toLowerCase(), text: r.m })]),
        el('td', {}, [el('code', { text: r.p.replace(/\/1$/, '/{id}') })]),
        el('td', { text: r.d }),
        el('td', { class: 'rotas__codigos', text: r.r }),
        el('td', {}, [botao])
      ]));
    });

    function atualizarCampos() {
      const m = metodo.value;
      campoCorpo.hidden = !(m === 'POST' || m === 'PUT');
      exclusao.hidden = m !== 'DELETE';
      if (m !== 'DELETE') form.elements.confirmaExclusao.checked = false;
    }
    metodo.addEventListener('change', atualizarCampos);
    atualizarCampos();

    function urlCompleta() {
      const base = servidor.value.trim().replace(/\/+$/, '');
      const p = caminho.value.trim();
      return (base || (arquivoLocal ? '' : location.origin)) + (p.startsWith('/') ? p : '/' + p);
    }

    function mostrar(texto, classe) {
      if (classe === 'erro' && !texto.startsWith('HTTP')) resposta.textContent = '';
      status.textContent = texto;
      status.className = 'resposta__status' + (classe ? ' resposta__status--' + classe : '');
    }

    form.addEventListener('submit', async function (e) {
      e.preventDefault();
      const m = metodo.value;
      if (!caminho.value.trim().startsWith('/api')) { mostrar('O caminho deve começar com /api.', 'erro'); caminho.focus(); return; }
      if (arquivoLocal && !servidor.value.trim()) { mostrar('Informe o servidor ou abra esta página pelo endereço do Render.', 'erro'); servidor.focus(); return; }
      if (caminho.value.includes('{')) { mostrar('Troque {id} pelo número do registro (por exemplo, o id devolvido pelo POST).', 'erro'); caminho.focus(); return; }
      if (m === 'DELETE' && !form.elements.confirmaExclusao.checked) { mostrar('Marque a confirmação para enviar um DELETE.', 'erro'); form.elements.confirmaExclusao.focus(); return; }
      let body;
      if (m === 'POST' || m === 'PUT') {
        try { body = JSON.stringify(JSON.parse(corpo.value || '{}')); }
        catch (erro) { mostrar('O corpo não é um JSON válido: ' + erro.message, 'erro'); corpo.focus(); return; }
      }
      enviar.disabled = true;
      mostrar('Enviando ' + m + ' ' + caminho.value.trim() + '…');
      resposta.textContent = '';
      const inicio = performance.now();
      try {
        const r = await fetch(urlCompleta(), { method: m, headers: body ? { 'Content-Type': 'application/json', 'Accept': 'application/json' } : { 'Accept': 'application/json' }, body: body });
        const ms = Math.round(performance.now() - inicio);
        const texto = await r.text();
        let exibicao = texto;
        try { exibicao = JSON.stringify(JSON.parse(texto), null, 2); } catch (_) { /* não é JSON */ }
        resposta.textContent = exibicao || '(sem corpo)';
        mostrar('HTTP ' + r.status + (r.statusText ? ' ' + r.statusText : '') + ' · ' + ms + ' ms' + (r.headers.get('Location') ? ' · Location: ' + r.headers.get('Location') : ''), r.ok ? 'ok' : 'erro');
      } catch (erro) {
        mostrar('Não foi possível conectar. No plano gratuito do Render, o servidor pode levar cerca de 1 minuto para "acordar"; tente de novo.', 'erro');
        resposta.textContent = String(erro);
      } finally {
        enviar.disabled = false;
        if (m === 'DELETE') form.elements.confirmaExclusao.checked = false;
      }
    });

    document.querySelector('[data-copiar]').addEventListener('click', async function () {
      const m = metodo.value;
      let cmd = 'curl -i -X ' + m + ' "' + urlCompleta() + '"';
      if (m === 'POST' || m === 'PUT') cmd += " -H 'Content-Type: application/json' -d '" + (corpo.value || '{}').replace(/\s*\n\s*/g, ' ').replace(/'/g, "'\\''") + "'";
      try { await navigator.clipboard.writeText(cmd); mostrar('Comando curl copiado.', 'ok'); }
      catch (_) { resposta.textContent = cmd; mostrar('Não foi possível copiar automaticamente; o comando está abaixo.'); }
    });
  });
})();
