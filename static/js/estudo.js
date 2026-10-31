const CIRCUNFERENCIA = 2 * Math.PI * 110;
const TITULO_PAGINA = document.title;

const MENSAGENS_FASE = {
  foco: "Hora de focar. Uma coisa de cada vez.",
  pausa: "Pausa. Levante, beba água e descanse os olhos."
};

let metodologias = [];
let metodologiaAtual = null;
let intervaloStatus = null;
let avancando = false;
let ultimaFase = null;
let audio = null;
let somLigado = true;

const telaLista = document.getElementById("tela-lista");
const telaSessao = document.getElementById("tela-sessao");
const blocoTempo = document.getElementById("bloco-tempo");
const blocoPassos = document.getElementById("bloco-passos");
const campoObjetivo = document.getElementById("objetivo");
const resumoSessao = document.getElementById("resumo-sessao");
const tituloSessao = document.getElementById("sessao-titulo");
const objetivoSessao = document.getElementById("sessao-objetivo");
const anel = document.getElementById("anel-tempo");
const anelProgresso = document.getElementById("anel-progresso");
const textoFase = document.getElementById("sessao-fase");
const textoTempo = document.getElementById("sessao-tempo");
const mensagemFase = document.getElementById("sessao-mensagem");
const estatisticas = document.getElementById("sessao-estatisticas");
const btnPausarRetomar = document.getElementById("btn-pausar-retomar");
const btnAvancarPasso = document.getElementById("btn-avancar-passo");
const btnSom = document.getElementById("btn-som");
const msgConcluida = document.getElementById("sessao-concluida");

anelProgresso.style.strokeDasharray = CIRCUNFERENCIA;
anelProgresso.style.strokeDashoffset = 0;

function detalhesMetodologia(m) {
  if (m.tipo === "tempo") {
    return m.ciclo.map(f => `${f.duracao_min} min de ${f.fase}`);
  }
  return [`${m.passos.length} passos`];
}

function carregarMetodologias() {
  return fetch("/metodologias")
    .then(r => r.json())
    .then(dados => {
      metodologias = dados;
      const lista = document.getElementById("lista-metodologias");
      lista.innerHTML = "";
      metodologias.forEach(m => {
        const item = document.createElement("button");
        item.className = `metodo ${m.tipo}`;

        const tag = document.createElement("span");
        tag.className = "tag";
        tag.textContent = m.tipo === "tempo" ? "Com tempo" : "Em passos";

        const titulo = document.createElement("h3");
        titulo.textContent = m.nome;

        const descricao = document.createElement("p");
        descricao.textContent = m.descricao;

        const meta = document.createElement("span");
        meta.className = "meta";
        detalhesMetodologia(m).forEach(texto => {
          const chip = document.createElement("span");
          chip.textContent = texto;
          meta.appendChild(chip);
        });

        item.append(tag, titulo, descricao, meta);
        item.onclick = () => iniciarSessao(m);
        lista.appendChild(item);
      });
    });
}

function prepararAvisos() {
  if (!audio) {
    const Contexto = window.AudioContext || window.webkitAudioContext;
    if (Contexto) audio = new Contexto();
  }
  if (audio) audio.resume();
  if ("Notification" in window && Notification.permission === "default") {
    Notification.requestPermission();
  }
}

function tocarAviso() {
  if (!audio || !somLigado) return;
  const oscilador = audio.createOscillator();
  const ganho = audio.createGain();
  oscilador.frequency.value = 660;
  ganho.gain.setValueAtTime(0.0001, audio.currentTime);
  ganho.gain.exponentialRampToValueAtTime(0.25, audio.currentTime + 0.02);
  ganho.gain.exponentialRampToValueAtTime(0.0001, audio.currentTime + 0.6);
  oscilador.connect(ganho);
  ganho.connect(audio.destination);
  oscilador.start();
  oscilador.stop(audio.currentTime + 0.65);
}

function avisarTrocaDeFase(fase) {
  tocarAviso();
  anel.classList.add("aviso");
  setTimeout(() => anel.classList.remove("aviso"), 3000);
  if ("Notification" in window && Notification.permission === "granted") {
    new Notification(`Hora de: ${fase}`, { body: MENSAGENS_FASE[fase] });
  }
}

function iniciarSessao(metodologia) {
  prepararAvisos();
  fetch("/sessoes/iniciar", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ metodologia_id: metodologia.id, objetivo: campoObjetivo.value })
  })
    .then(r => r.json())
    .then(sessao => abrirSessao(metodologia, sessao));
}

function abrirSessao(metodologia, sessao) {
  metodologiaAtual = metodologia;
  avancando = false;
  ultimaFase = null;
  resumoSessao.classList.add("oculto");
  telaLista.classList.add("oculto");
  telaSessao.classList.remove("oculto");
  tituloSessao.textContent = metodologia.nome;
  objetivoSessao.textContent = sessao.objetivo ? `Foco: ${sessao.objetivo}` : "";
  objetivoSessao.classList.toggle("oculto", !sessao.objetivo);

  clearInterval(intervaloStatus);
  if (sessao.tipo === "tempo") {
    blocoTempo.classList.remove("oculto");
    blocoPassos.classList.add("oculto");
    intervaloStatus = setInterval(atualizarStatus, 1000);
  } else {
    blocoPassos.classList.remove("oculto");
    blocoTempo.classList.add("oculto");
    montarPontos(metodologia.passos.length);
  }
  atualizarStatus();
}

function restaurarSessao() {
  fetch("/sessoes/status")
    .then(r => r.json())
    .then(sessao => {
      if (sessao.erro) return;
      const metodologia = metodologias.find(m => m.id === sessao.metodologia_id);
      if (metodologia) abrirSessao(metodologia, sessao);
    });
}

function montarPontos(total) {
  const pontos = document.getElementById("sessao-pontos");
  pontos.innerHTML = "";
  for (let i = 0; i < total; i++) {
    const ponto = document.createElement("span");
    ponto.className = "ponto";
    pontos.appendChild(ponto);
  }
}

function formatarTempo(segundos) {
  const min = String(Math.floor(segundos / 60)).padStart(2, "0");
  const seg = String(segundos % 60).padStart(2, "0");
  return `${min}:${seg}`;
}

function mostrarTempo(sessao) {
  const restante = sessao.tempo_restante_segundos;
  const proporcao = restante / sessao.duracao_fase_segundos;

  anelProgresso.style.strokeDashoffset = CIRCUNFERENCIA * (1 - proporcao);
  anel.classList.toggle("pausado", sessao.pausado);
  textoFase.textContent = sessao.pausado ? `${sessao.fase}, pausado` : sessao.fase;
  textoTempo.textContent = formatarTempo(restante);
  btnPausarRetomar.textContent = sessao.pausado ? "Retomar" : "Pausar";
  mensagemFase.textContent = sessao.pausado ? "Sessão pausada. Retome quando estiver pronto." : MENSAGENS_FASE[sessao.fase];
  estatisticas.textContent = `Ciclos de foco concluídos: ${sessao.ciclos_concluidos}. Tempo focado: ${sessao.minutos_focados} min.`;
  document.title = `${sessao.pausado ? "Pausado" : sessao.fase} ${formatarTempo(restante)}`;

  if (ultimaFase !== null && sessao.fase !== ultimaFase) avisarTrocaDeFase(sessao.fase);
  ultimaFase = sessao.fase;

  if (restante === 0 && !sessao.pausado && !avancando) avancarSessao();
}

function mostrarPassos(sessao) {
  const pontos = document.querySelectorAll("#sessao-pontos .ponto");
  pontos.forEach((ponto, i) => {
    ponto.className = "ponto";
    if (i < sessao.indice_passo || sessao.concluida) ponto.classList.add("feito");
    else if (i === sessao.indice_passo) ponto.classList.add("atual");
  });
  document.getElementById("sessao-progresso").textContent = `Passo ${sessao.indice_passo + 1} de ${sessao.total_passos}`;
  document.getElementById("sessao-passo").textContent = sessao.passo_atual;

  if (sessao.concluida) {
    msgConcluida.classList.remove("oculto");
    btnAvancarPasso.classList.add("oculto");
  }
}

function atualizarStatus() {
  return fetch("/sessoes/status")
    .then(r => r.json())
    .then(sessao => {
      if (sessao.erro) return;
      if (sessao.tipo === "tempo") mostrarTempo(sessao);
      else mostrarPassos(sessao);
    });
}

function avancarSessao() {
  avancando = true;
  fetch("/sessoes/avancar", { method: "POST" })
    .then(atualizarStatus)
    .then(() => { avancando = false; });
}

function alternarPausa() {
  const rota = btnPausarRetomar.textContent === "Pausar" ? "/sessoes/pausar" : "/sessoes/retomar";
  fetch(rota, { method: "POST" }).then(atualizarStatus);
}

function alternarSom() {
  somLigado = !somLigado;
  btnSom.textContent = somLigado ? "Som: ligado" : "Som: desligado";
}

function mostrarResumo(resumo) {
  let texto = "Sessão encerrada.";
  if (resumo.minutos_focados !== undefined) {
    const ciclos = resumo.ciclos_concluidos;
    texto = `Sessão encerrada. Você focou ${resumo.minutos_focados} min e completou ${ciclos} ${ciclos === 1 ? "ciclo" : "ciclos"}.`;
  } else if (resumo.passos_concluidos !== undefined) {
    const passos = resumo.passos_concluidos;
    texto = `Sessão encerrada. Você concluiu ${passos} ${passos === 1 ? "passo" : "passos"}.`;
  }
  resumoSessao.textContent = texto;
  resumoSessao.classList.remove("oculto");
}

function encerrarSessao() {
  fetch("/sessoes/encerrar", { method: "POST" })
    .then(r => r.json())
    .then(resumo => {
      clearInterval(intervaloStatus);
      document.title = TITULO_PAGINA;
      telaSessao.classList.add("oculto");
      telaLista.classList.remove("oculto");
      msgConcluida.classList.add("oculto");
      btnAvancarPasso.classList.remove("oculto");
      anel.classList.remove("pausado");
      anelProgresso.style.strokeDashoffset = 0;
      mostrarResumo(resumo);
    });
}

btnPausarRetomar.onclick = alternarPausa;
btnSom.onclick = alternarSom;
document.getElementById("btn-avancar").onclick = avancarSessao;
btnAvancarPasso.onclick = avancarSessao;
document.getElementById("btn-encerrar").onclick = encerrarSessao;

carregarMetodologias().then(restaurarSessao);
