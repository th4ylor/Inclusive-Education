var formCard = document.getElementById("formCard")
let baralho = []
let posicao = 0


formCard.addEventListener('submit', (e) => {
    e.preventDefault()

    baralho.push({
        materia: document.getElementById("materia").value.toUpperCase() || 'GERAL',
        pergunta: document.getElementById("pergunta").value,
        resposta: document.getElementById("resposta").value,
    });console.log(baralho)
    
    formCard.reset()
    posicao = baralho.length - 1
    renderList(posicao)
} )


function renderList(posicao){
    let cards = document.getElementById("flashcard")
    cards.innerHTML= ""
    let c = baralho[posicao]

    let card = document.createElement("div")
    card.className = "flipInner"

    card.innerHTML = `
        <div class="face Frente">
            <small>PERGUNTA . ${c.materia}</small>
                <h3 id="perguntaC">${c.pergunta}</h3>
            <span class="dica">Passe o mouse para virar -></span>
        </div>

        <div class="face Verso">
            <small>RESPOSTA . ${c.materia}</small>
                <h3 id="respostaC"> ${c.resposta}</h3>
            <span class="dica"><-Passe o mouse para voltar</span>
        </div>`
    cards.appendChild(card)
}

let acerto = document.getElementById("acerto")

acerto.addEventListener("click", () => {
    if (baralho.length === 0)return
    posicao = (posicao + 1) % baralho.length
    renderList(posicao)
} )


