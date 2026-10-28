const formCard = document.getElementById("formCard")
const areaCard = document.getElementById("flashcard")
const botaoAcerto = document.getElementById("acertei")
const parag = document.getElementById("parag")


function mostrarmensagem(texto = "teste", tipo = "erro"){
    console.log("executou")
    if (texto == "" || tipo == ""){
        parag.innerHTML= ""
        console.log("deu ERRADO")
        return   
    }
    const mensagem = document.createElement("p")
        mensagem.textContent = texto
        mensagem.className = `msg ${tipo}`
        parag.appendChild(mensagem)

        mensagem.getBoundingClientRect()
        mensagem.classList.add("show")
        console.log("add essa bosta")

        setTimeout(() => {
            mensagem.classList.remove("show")
            setTimeout(() => mensagem.remove(), 200)
        }, 4000)
}


function criarFace(classe, idText, rotulo, materia, text, dica){
    let face = document.createElement("face")
    face.className = "face" + classe

    let small = document.createElement("small")
    small.textContent = rotulo + " . " + materia

    let h3 = document.createElement("h3")
    h3.id = idText
    h3.textContent = text

    let span = document.createElement("span")
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

    let flip = document.createElement("div")
    flip.className = "flipInner"
    flip.append(
        criarFace(" Frente", "perguntaC", "PERGUNTA", card.materia, card.pergunta, "Passe o mouse para virar ->"),
        criarFace(" Verso", "respostaC", "RESPOSTA", card.materia, card.resposta, "<- Passe o mouse para voltar ")
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
        mostrarmensagem("Card adicionado", "sucesso")
        formCard.reset()
        renderCard(dados.card)
    }catch (erro) {
        mostrarmensagem("Erro ao conectar com  Python", "erro")
        return
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
