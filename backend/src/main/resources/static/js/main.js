/* LuzVital — navegação, cabeçalho, acordeão e animações de entrada. */
(function () {
  'use strict';

  const desktop = window.matchMedia('(min-width: 1100px)');

  /* ---------- Menu móvel ---------- */
  function iniciarMenu() {
    const botao = document.querySelector('[data-menu-botao]');
    const menu = document.querySelector('[data-menu]');
    if (!botao || !menu) return;
    const texto = botao.querySelector('.nav__botao-texto');
    const usoIcone = botao.querySelector('use');

    function definir(aberto, devolverFoco) {
      botao.setAttribute('aria-expanded', String(aberto));
      menu.classList.toggle('aberto', aberto);
      texto.textContent = aberto ? 'Fechar' : 'Menu';
      usoIcone.setAttribute('href', aberto ? '#i-fechar' : '#i-menu');
      if (!aberto && devolverFoco) botao.focus();
    }

    botao.addEventListener('click', function () {
      const aberto = botao.getAttribute('aria-expanded') === 'true';
      definir(!aberto, false);
      if (!aberto) menu.querySelector('a').focus();
    });

    menu.addEventListener('click', function (e) {
      if (e.target.closest('a') && !desktop.matches) definir(false, false);
    });

    document.addEventListener('keydown', function (e) {
      if (e.key === 'Escape' && botao.getAttribute('aria-expanded') === 'true') definir(false, true);
    });

    document.addEventListener('click', function (e) {
      if (botao.getAttribute('aria-expanded') === 'true' && !e.target.closest('.nav')) definir(false, false);
    });

    desktop.addEventListener('change', function () { definir(false, false); });
  }

  /* ---------- Cabeçalho ao rolar e seção atual ---------- */
  function iniciarCabecalho() {
    const cabecalho = document.querySelector('[data-cabecalho]');
    if (!cabecalho) return;
    const marcar = function () { cabecalho.classList.toggle('rolou', window.scrollY > 8); };
    marcar();
    window.addEventListener('scroll', marcar, { passive: true });

    if (!('IntersectionObserver' in window)) return;
    const links = Array.from(document.querySelectorAll('.nav__lista a[href^="#"]:not(.botao)'));
    const porId = new Map(links.map(function (a) { return [a.getAttribute('href').slice(1), a]; }));
    const observador = new IntersectionObserver(function (entradas) {
      entradas.forEach(function (entrada) {
        if (!entrada.isIntersecting) return;
        const link = porId.get(entrada.target.id);
        if (!link) return;
        links.forEach(function (a) { a.removeAttribute('aria-current'); });
        link.setAttribute('aria-current', 'true');
      });
    }, { rootMargin: '-45% 0px -50% 0px' });
    porId.forEach(function (_, id) {
      const secao = document.getElementById(id);
      if (secao) observador.observe(secao);
    });
  }

  /* ---------- Acordeão (padrão WAI-ARIA: botão + região) ---------- */
  function iniciarAcordeao() {
    document.querySelectorAll('[data-acordeao]').forEach(function (acordeao) {
      acordeao.addEventListener('click', function (e) {
        const botao = e.target.closest('button[aria-controls]');
        if (!botao) return;
        const painel = document.getElementById(botao.getAttribute('aria-controls'));
        if (!painel) return;
        const abrir = botao.getAttribute('aria-expanded') !== 'true';
        botao.setAttribute('aria-expanded', String(abrir));
        painel.hidden = !abrir;
      });
    });
  }

  /* ---------- Entrada suave dos blocos (respeita movimento reduzido) ---------- */
  function iniciarRevelar() {
    const itens = document.querySelectorAll('.revelar');
    const reduzir = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
    if (reduzir || !('IntersectionObserver' in window)) {
      itens.forEach(function (el) { el.classList.add('visivel'); });
      return;
    }
    const observador = new IntersectionObserver(function (entradas) {
      entradas.forEach(function (entrada) {
        if (entrada.isIntersecting) {
          entrada.target.classList.add('visivel');
          observador.unobserve(entrada.target);
        }
      });
    }, { rootMargin: '0px 0px -8% 0px' });
    itens.forEach(function (el) { observador.observe(el); });
  }

  /* ---------- "Pular para o conteúdo" foca o main ---------- */
  function iniciarPular() {
    const pular = document.querySelector('.pular');
    const main = document.getElementById('conteudo');
    if (!pular || !main) return;
    pular.addEventListener('click', function () { main.focus({ preventScroll: true }); });
  }

  function iniciarAno() {
    const ano = document.querySelector('[data-ano]');
    if (ano) ano.textContent = String(new Date().getFullYear());
  }

  document.addEventListener('DOMContentLoaded', function () {
    iniciarMenu();
    iniciarCabecalho();
    iniciarAcordeao();
    iniciarRevelar();
    iniciarPular();
    iniciarAno();
  });
})();
