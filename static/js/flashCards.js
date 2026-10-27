const formCard = document.getElementById("formCard")
const areaCard = document.getElementById("flashcard")
const botaoAcerto = document.getElementById("acertei")
const mensagem = document.getElementById("mensagem")


function mostrarmensagem(texto, tipo){
    mensagem.textContent = texto
    mensagem.className = tipo
}


function criarFace(classe, idText, rotulo, materia, text, dica){
    const face = document.createElement("small")
    face.className = "face" + classe

    const small = document.createElement("small")
    small.textContent = rotulo + " . " + materia

    const h3 = document.createElement("h3")
    h3.id = idText
    h3.textContent = text

    const span = document.createElement("span")
    span.className = "dica"
    span.textContent = dica

    face.append(small, h3, span)
    return face
}


function renderCard(card){
    areaCard.replaceChildren()

    if (!card){
        const aviso = document.createElement("p")
        aviso.textContent = "Nenhum card ainda. Crie o primeiro no formulario ao lado"
        areaCard.appendChild(aviso)
        botaoAcerto.hidden = true
        return
    }

    const flip = document.createElement("div")
    flip.className = "flipInner"
    flip.append(
        criarFace("Frente", "perguntaC", "PERGUNTA", card.materia, card.pergunta, "Passe o mouse para virar ->"),
        criarFace("Verso", "respostaC", "RESPOSTA", card.materia, card.resposta, "<- Passe o mouse para voltar ")
    )
    areaCard.appendChild(flip)
    botaoAcerto.hidden = false
}


async function loadCardAtual(){
    const resposta = await fetch("/api/flashcards/atual")
    const dados = await resposta.json()
    renderCard(dados.card)
}


formCard.addEventListener("submit", async (e) => {
    e.preventDefault()

    let newCard = {
        materia: document.getElementById("materia").value,
        pergunta: document.getElementById("pergunta").value,
        resposta: document.getElementById("resposta").value
    }

    try{
        const resposta = await fetch("/api/flashcards", {
            method: "POST",
            headers: {"Content-Type": "application/json" },
            body: JSON.stringify(newCard)
        })
        let dados = await resposta.json()
        
        if (!resposta.ok){
            mostrarmensagem(dados.erro, "erro")
            return
        }
        mostrarmensagem("", "")
        formCard.reset()
        renderCard(dados.card)
    }catch (erro) {
        mostrarmensagem("Erro ao conectar com  Python", "erro")
    }
})

botaoAcerto.addEventListener("click", async () => {
    try{
        const resposta = await fetch("/api/flashcards/proximo", {method: "POST"})
        const dados = await resposta.json()
        renderCard(dados.card)
    }catch (erro){
        mostrarmensagem("Erro ao conectar com o server.", "erro")
    }
})

loadCardAtual()
