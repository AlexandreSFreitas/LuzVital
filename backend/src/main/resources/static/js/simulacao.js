/* LuzVital — demonstração interativa (100% local, dados fictícios).
 *
 * Organização:
 *  - DADOS_FICTICIOS: o cenário de exemplo (nada é real).
 *  - prioridadeDe(): mesma regra operacional do backend (docs/DATABASE_MODEL.md, seção 4).
 *  - fonteLocal: "fonte de dados" da demonstração. Para ligar na API real, basta criar
 *    outro objeto com os mesmos métodos usando fetch() em /api/... e trocar em FONTE.
 *  - Painel: estado + renderização + eventos.
 * Nada é gravado no navegador (sem localStorage/sessionStorage).
 */
(function () {
  'use strict';

  const DADOS_FICTICIOS = {
    regiao: 'Jardim Ângela',
    pacientes: [
      {
        id: 1, nome: 'Lúcia Andrade', idade: 71, regiao: 'Jardim Ângela',
        equipamentos: [{ nome: 'Concentrador de oxigênio', suporteVida: true, autonomiaMin: 180 }],
        contatos: [
          { nome: 'Mariana', vinculo: 'filha' },
          { nome: 'Paulo', vinculo: 'filho' },
          { nome: 'Equipe Vida em Casa', vinculo: 'home care' }
        ]
      },
      {
        id: 2, nome: 'Antônio Ribeiro', idade: 68, regiao: 'Jardim Ângela',
        equipamentos: [{ nome: 'Ventilador pulmonar', suporteVida: true, autonomiaMin: 90 }],
        contatos: [
          { nome: 'Cláudia', vinculo: 'esposa' },
          { nome: 'Equipe Vida em Casa', vinculo: 'home care' }
        ]
      },
      {
        id: 3, nome: 'Benedito Costa', idade: 80, regiao: 'Jardim Ângela',
        equipamentos: [{ nome: 'Bomba de alimentação enteral', suporteVida: false, autonomiaMin: 120 }],
        contatos: [
          { nome: 'Rosa', vinculo: 'cuidadora' },
          { nome: 'Jorge', vinculo: 'sobrinho' }
        ]
      },
      {
        id: 4, nome: 'Helena Prado', idade: 9, regiao: 'Jardim Ângela',
        equipamentos: [{ nome: 'Monitor de oximetria', suporteVida: false, autonomiaMin: 480 }],
        contatos: [{ nome: 'Sônia', vinculo: 'mãe' }]
      },
      {
        id: 5, nome: 'Joana Lima', idade: 77, regiao: 'Capão Redondo',
        equipamentos: [{ nome: 'Concentrador de oxigênio', suporteVida: true, autonomiaMin: 120 }],
        contatos: [{ nome: 'Célia', vinculo: 'filha' }]
      }
    ]
  };

  /* Regra operacional (não clínica), igual à do backend:
     1 = algum aparelho de suporte à vida não aguenta a duração estimada;
     2 = algum aparelho não aguenta a duração estimada;
     3 = demais casos. */
  function prioridadeDe(paciente, duracaoMin) {
    const naoAguenta = function (e) { return e.autonomiaMin < duracaoMin; };
    if (paciente.equipamentos.some(function (e) { return e.suporteVida && naoAguenta(e); })) return 1;
    if (paciente.equipamentos.some(naoAguenta)) return 2;
    return 3;
  }

  function menorAutonomia(paciente) {
    return Math.min.apply(null, paciente.equipamentos.map(function (e) { return e.autonomiaMin; }));
  }

  /* Fonte de dados local. Mesmo "formato" que uma futura chamada à API. */
  const fonteLocal = {
    totalPacientes: function () { return Promise.resolve(DADOS_FICTICIOS.pacientes.length); },
    registrarInterrupcao: function (regiao, duracaoMin) {
      const afetados = DADOS_FICTICIOS.pacientes
        .filter(function (p) { return p.regiao === regiao; })
        .map(function (p) { return Object.assign({}, p, { prioridade: prioridadeDe(p, duracaoMin) }); })
        .sort(function (a, b) { return a.prioridade - b.prioridade || menorAutonomia(a) - menorAutonomia(b); });
      const foraDaRegiao = DADOS_FICTICIOS.pacientes.filter(function (p) { return p.regiao !== regiao; });
      const alertas = [];
      afetados.forEach(function (p) {
        p.contatos.forEach(function (c, i) {
          alertas.push({ id: p.id + '-' + i, pacienteId: p.id, ordem: i + 1, contato: c, status: 'PENDENTE', confirmadoEm: null });
        });
      });
      return Promise.resolve({ afetados: afetados, foraDaRegiao: foraDaRegiao, alertas: alertas });
    },
    confirmarAlerta: function (alerta, minuto) {
      alerta.status = 'CONFIRMADO';
      alerta.confirmadoEm = minuto;
      return Promise.resolve(alerta);
    }
  };
  const FONTE = fonteLocal;

  /* ---------- Utilidades ---------- */
  const INICIO_MIN = 14 * 60;            // 14h00, horário simulado
  const ESCALA_MAX = 8 * 60;             // barra de autonomia em escala de 8 horas
  const reduzirMovimento = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  const esperar = function (ms) { return new Promise(function (r) { setTimeout(r, reduzirMovimento ? 0 : ms); }); };

  function hora(minutos) {
    const h = Math.floor(minutos / 60), m = minutos % 60;
    return h + 'h' + String(m).padStart(2, '0');
  }
  function duracaoTexto(min) {
    const h = Math.floor(min / 60), m = min % 60;
    if (!h) return m + ' min';
    return m ? h + 'h' + String(m).padStart(2, '0') : h + (h === 1 ? ' hora' : ' horas');
  }
  function el(tag, props, filhos) {
    const n = document.createElement(tag);
    Object.entries(props || {}).forEach(function (par) {
      const k = par[0], v = par[1];
      if (v === null || v === undefined || v === false) return;
      if (k === 'class') n.className = v;
      else if (k === 'text') n.textContent = v;
      else n.setAttribute(k, v === true ? '' : v);
    });
    (filhos || []).forEach(function (f) { if (f) n.append(f); });
    return n;
  }
  function icone(id) {
    const ns = 'http://www.w3.org/2000/svg';
    const svg = document.createElementNS(ns, 'svg');
    svg.setAttribute('class', 'icone'); svg.setAttribute('aria-hidden', 'true');
    const use = document.createElementNS(ns, 'use'); use.setAttribute('href', '#' + id);
    svg.append(use);
    return svg;
  }

  /* ---------- Painel ---------- */
  function iniciar(raiz) {
    const $ = function (s) { return raiz.querySelector(s); };
    const ui = {
      simular: $('[data-simular]'), encerrar: $('[data-encerrar]'), reiniciar: $('[data-reiniciar]'),
      radios: raiz.querySelectorAll('input[name="duracao"]'),
      estado: $('[data-estado]'), estadoTexto: $('[data-estado-texto]'), estadoIcone: $('[data-estado-icone]'),
      relogio: $('[data-relogio]'), vazio: $('[data-vazio]'), afetados: $('[data-afetados]'),
      lista: $('[data-lista]'), primeira: $('[data-primeira]'), historico: $('[data-historico]'), log: $('[data-log]'),
      passos: raiz.querySelectorAll('[data-passo]'),
      m: { cadastrados: $('[data-m="cadastrados"]'), afetados: $('[data-m="afetados"]'), alertas: $('[data-m="alertas"]'), confirmados: $('[data-m="confirmados"]') }
    };
    const anuncio = document.querySelector('[data-anuncio]');

    let estado;

    function anunciar(texto) {
      if (!anuncio) return;
      anuncio.textContent = '';
      setTimeout(function () { anuncio.textContent = texto; }, 60);
    }
    function relogio(min) { estado.minuto = min; ui.relogio.textContent = hora(min); }
    function metrica(nome, valor) {
      const dd = ui.m[nome];
      if (dd.textContent === String(valor)) return;
      dd.textContent = String(valor);
      const caixa = dd.parentElement;
      caixa.classList.remove('mudou'); void caixa.offsetWidth; caixa.classList.add('mudou');
    }
    function definirEstado(tom, texto, iconeId) {
      ui.estado.dataset.tom = tom;
      ui.estadoTexto.textContent = texto;
      ui.estadoIcone.setAttribute('href', '#' + iconeId);
    }
    function marcarPasso(nome) {
      let passou = true;
      ui.passos.forEach(function (li) {
        li.classList.remove('feito', 'atual');
        li.removeAttribute('aria-current');
        if (nome === 'fim') { li.classList.add('feito'); return; }
        if (li.dataset.passo === nome) { li.classList.add('atual'); li.setAttribute('aria-current', 'step'); passou = false; }
        else if (passou) li.classList.add('feito');
      });
    }
    function registrar(texto) {
      ui.historico.hidden = false;
      ui.log.append(el('li', {}, [el('time', { text: hora(estado.minuto) }), document.createTextNode(texto)]));
    }
    function travarDuracao(travar) { ui.radios.forEach(function (r) { r.disabled = travar; }); }
    function duracaoEscolhida() {
      const r = Array.from(ui.radios).find(function (x) { return x.checked; });
      return r ? Number(r.value) : 240;
    }

    function cartaoPaciente(p, fora) {
      const menor = p.equipamentos.reduce(function (a, b) { return a.autonomiaMin <= b.autonomiaMin ? a : b; });
      const curta = !fora && menor.autonomiaMin < estado.duracao;
      const rotulo = fora ? 'Fora da região: não afetada' : 'Prioridade ' + p.prioridade;
      const topo = el('div', { class: 'paciente__topo' }, [
        el('span', { class: 'paciente__nome', text: p.nome + ', ' + p.idade }),
        el('span', { class: 'prioridade prioridade--' + (fora ? 'fora' : p.prioridade), text: rotulo })
      ]);
      const equip = el('p', { class: 'paciente__equip', text: p.equipamentos.map(function (e) {
        return e.nome + (e.suporteVida ? ' · suporte à vida' : '');
      }).join(' · ') + (fora ? ' · ' + p.regiao : '') });

      const filhos = [topo, equip];
      if (!fora) {
        const nivel = el('span', { class: 'autonomia__nivel' + (curta ? ' autonomia__nivel--curta' : '') });
        nivel.style.width = Math.min(100, menor.autonomiaMin / ESCALA_MAX * 100) + '%';
        const marca = el('span', { class: 'autonomia__marca' });
        marca.style.left = Math.min(100, estado.duracao / ESCALA_MAX * 100) + '%';
        filhos.push(el('div', { class: 'autonomia' }, [
          el('div', { class: 'autonomia__barra', 'aria-hidden': 'true' }, [nivel, marca]),
          el('p', { class: 'autonomia__legenda' }, [
            el('span', {}, [document.createTextNode('Reserva: '), el('strong', { text: duracaoTexto(menor.autonomiaMin) })]),
            el('span', {}, [document.createTextNode('Falta estimada: '), el('strong', { text: duracaoTexto(estado.duracao) })]),
            el('span', { text: curta ? 'A reserva acaba antes' : 'A reserva aguenta' })
          ])
        ]));
        const contatos = el('ul', { class: 'contatos', 'aria-label': 'Rede de apoio de ' + p.nome + ', em ordem de acionamento' });
        estado.alertas.filter(function (a) { return a.pacienteId === p.id; }).forEach(function (a) {
          contatos.append(linhaContato(a, p));
        });
        filhos.push(contatos);
      }
      return el('li', { class: 'paciente' + (fora ? ' paciente--fora' : ''), 'data-paciente': p.id }, filhos);
    }

    function linhaContato(alerta, paciente) {
      const nome = el('span', { class: 'contato__nome' }, [
        document.createTextNode(alerta.ordem + '. ' + alerta.contato.nome + ' '),
        el('small', { text: '(' + alerta.contato.vinculo + ')' })
      ]);
      const li = el('li', { class: 'contato', 'data-alerta': alerta.id }, [nome]);
      if (alerta.status === 'CONFIRMADO') {
        li.append(el('span', { class: 'status status--confirmado', tabindex: '-1' }, [icone('i-check'), document.createTextNode('Confirmou às ' + hora(alerta.confirmadoEm))]));
      } else {
        li.append(el('span', { class: 'status status--pendente' }, [icone('i-relogio'), document.createTextNode(estado.fase === 'iniciando' ? 'Na fila de aviso' : 'Sem confirmação')]));
        if (estado.fase === 'ativa') {
          const b = el('button', { class: 'botao-confirmar', type: 'button', 'data-confirmar': alerta.id,
            'aria-label': 'Simular confirmação de ' + alerta.contato.nome + ' (' + alerta.contato.vinculo + ' de ' + paciente.nome + ')' },
            [document.createTextNode('Simular confirmação')]);
          li.append(b);
        }
      }
      return li;
    }

    function renderizarLista() {
      ui.lista.replaceChildren();
      estado.afetados.forEach(function (p) { ui.lista.append(cartaoPaciente(p, false)); });
      estado.foraDaRegiao.forEach(function (p) { ui.lista.append(cartaoPaciente(p, true)); });
    }

    function confirmados() { return estado.alertas.filter(function (a) { return a.status === 'CONFIRMADO'; }); }

    async function simular() {
      estado.fase = 'iniciando';
      estado.duracao = duracaoEscolhida();
      ui.simular.disabled = true;
      travarDuracao(true);
      ui.reiniciar.hidden = false;

      // 1. Ocorrência
      relogio(INICIO_MIN + 5);
      ui.vazio.hidden = true;
      definirEstado('alerta', 'Falta de energia simulada', 'i-raio-off');
      marcarPasso('identificacao');
      registrar('Interrupção simulada registrada no ' + DADOS_FICTICIOS.regiao + '. Duração estimada: ' + duracaoTexto(estado.duracao) + '.');
      anunciar('Interrupção simulada registrada no ' + DADOS_FICTICIOS.regiao + '. Identificando pacientes.');
      await esperar(900);

      // 2. Identificação
      const r = await FONTE.registrarInterrupcao(DADOS_FICTICIOS.regiao, estado.duracao);
      estado.afetados = r.afetados; estado.foraDaRegiao = r.foraDaRegiao; estado.alertas = r.alertas;
      relogio(INICIO_MIN + 6);
      ui.afetados.hidden = false;
      renderizarLista();
      metrica('afetados', r.afetados.length);
      marcarPasso('alertas');
      const p1 = r.afetados.filter(function (p) { return p.prioridade === 1; }).length;
      registrar(r.afetados.length + ' pacientes ativos identificados na região, ' + p1 + ' com prioridade 1. ' +
        r.foraDaRegiao.length + ' paciente de outra região não foi afetado.');
      anunciar(r.afetados.length + ' pacientes identificados. ' + p1 + ' com prioridade 1.');
      await esperar(900);

      // 3. Alertas
      estado.fase = 'ativa';
      renderizarLista();
      metrica('alertas', r.alertas.length);
      marcarPasso('acompanhamento');
      registrar(r.alertas.length + ' alertas emitidos para a rede de apoio, na ordem de acionamento. (Simulação: nenhuma mensagem real foi enviada.)');
      ui.encerrar.hidden = false;
      anunciar(r.alertas.length + ' alertas emitidos. Use os botões "Simular confirmação" para acompanhar as respostas.');
    }

    async function confirmar(idAlerta, botao) {
      const alerta = estado.alertas.find(function (a) { return a.id === idAlerta; });
      if (!alerta || alerta.status === 'CONFIRMADO' || estado.fase !== 'ativa') return;
      botao.disabled = true;
      relogio(estado.minuto + 2);
      await FONTE.confirmarAlerta(alerta, estado.minuto);
      const paciente = estado.afetados.find(function (p) { return p.id === alerta.pacienteId; });
      const linha = ui.lista.querySelector('[data-alerta="' + idAlerta + '"]');
      const nova = linhaContato(alerta, paciente);
      linha.replaceWith(nova);
      nova.querySelector('.status').focus();

      const total = confirmados().length;
      metrica('confirmados', total);
      registrar(alerta.contato.nome + ' (' + alerta.contato.vinculo + ' de ' + paciente.nome + ') confirmou que vai ajudar.');
      let msg = alerta.contato.nome + ' confirmou às ' + hora(alerta.confirmadoEm) + '.';
      if (total === 1) {
        const minutos = alerta.confirmadoEm - (INICIO_MIN + 5);
        ui.primeira.hidden = false;
        ui.primeira.textContent = 'Primeira confirmação ' + minutos + ' min após a falta de energia (simulado)';
        msg += ' Primeira confirmação, ' + minutos + ' minutos após a falta de energia.';
      }
      const pendentesDoPaciente = estado.alertas.filter(function (a) { return a.pacienteId === paciente.id && a.status !== 'CONFIRMADO'; }).length;
      if (pendentesDoPaciente === 0) msg += ' Toda a rede de ' + paciente.nome + ' respondeu.';
      anunciar(msg);
    }

    function encerrar() {
      if (estado.fase !== 'ativa') return;
      estado.fase = 'encerrada';
      relogio(INICIO_MIN + 5 + estado.duracao);
      definirEstado('info', 'Energia restabelecida', 'i-raio');
      marcarPasso('fim');
      renderizarLista();
      const total = confirmados().length;
      registrar('Energia restabelecida. Interrupção encerrada com ' + total + ' de ' + estado.alertas.length + ' alertas confirmados.');
      ui.encerrar.hidden = true;
      anunciar('Interrupção encerrada. ' + total + ' de ' + estado.alertas.length + ' alertas confirmados. Você pode reiniciar a simulação.');
      ui.reiniciar.focus();
    }

    function reiniciar() {
      estado = { fase: 'normal', duracao: duracaoEscolhida(), minuto: INICIO_MIN, afetados: [], foraDaRegiao: [], alertas: [] };
      relogio(INICIO_MIN);
      definirEstado('ok', 'Energia normal na região', 'i-raio');
      ui.passos.forEach(function (li) { li.classList.remove('feito', 'atual'); li.removeAttribute('aria-current'); });
      ui.lista.replaceChildren(); ui.log.replaceChildren();
      ui.afetados.hidden = true; ui.historico.hidden = true; ui.primeira.hidden = true; ui.vazio.hidden = false;
      ui.encerrar.hidden = true; ui.reiniciar.hidden = true;
      ui.simular.disabled = false;
      travarDuracao(false);
      ['afetados', 'alertas', 'confirmados'].forEach(function (k) { ui.m[k].textContent = '0'; });
    }

    ui.simular.addEventListener('click', function () { simular().catch(erro); });
    ui.encerrar.addEventListener('click', encerrar);
    ui.reiniciar.addEventListener('click', function () {
      reiniciar();
      anunciar('Simulação reiniciada. Energia normal na região.');
      ui.simular.focus();
    });
    ui.lista.addEventListener('click', function (e) {
      const b = e.target.closest('[data-confirmar]');
      if (b) confirmar(b.dataset.confirmar, b).catch(erro);
    });

    function erro(e) {
      console.error(e);
      anunciar('Não foi possível continuar a simulação. Use "Reiniciar simulação".');
      ui.reiniciar.hidden = false;
    }

    reiniciar();
    FONTE.totalPacientes().then(function (n) { ui.m.cadastrados.textContent = String(n); });
  }

  document.addEventListener('DOMContentLoaded', function () {
    const raiz = document.querySelector('[data-simulacao]');
    if (raiz) iniciar(raiz);
  });
})();
