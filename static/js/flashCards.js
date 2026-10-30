const formCard = document.getElementById("formCard")
const areaCard = document.getElementById("flashcard")
const botaoAcerto = document.getElementById("acertei")
const parag = document.getElementById("parag")
const quase = document.getElementById("quase")
const errei = document.getElementById("errei")
let acerto = 0
let erro = 0
let quaseX = 0


function mostrarmensagem(texto, tipo){
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
    let face = document.createElement("div")
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
    console.log("valor do acertei " + acerto)
    console.log("valor do Quase " + quaseX)
    console.log("valor do Errei " + erro)
    areaCard.replaceChildren()

    if (!card){
        const aviso = document.createElement("div")
        aviso.className = "avisoCard"
        aviso.innerHTML= `
        <h2>Nenhum card ainda.<br> Crie o primeiro no formulario ao lado.</h2>
        <img src='../../static/img/Learning-amico.svg' ></img>`
        areaCard.appendChild(aviso)
        botaoAcerto.hidden = true
        quase.hidden = true
        errei.hidden = true
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
    quase.hidden = false
    errei.hidden = false
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

//Acoes dos botoes de Acerto, Quase e erro
botaoAcerto.addEventListener("click", async () => {
    const resposta = await fetch("/api/flashcards/1", {method: "POST"})
    const dados = await resposta.json()
    const innerAcerto  = document.getElementById("numeroAcerto")
    acerto = addCount(innerAcerto, acerto )
    renderCard(dados.card)
})
quase.addEventListener("click", async () => {
    const resposta = await fetch("/api/flashcards/2", {method: "PATCH"})
    const dados = await resposta.json()
    const innerQuase = document.getElementById("numeroQuase")
    quaseX = addCount(innerQuase, quaseX )
    renderCard(dados.card)  
})
errei.addEventListener("click", async () => {
    const resposta = await fetch("/api/flashcards/2", {method: "PATCH"})
    const dados = await resposta.json()
    const innerErro = document.getElementById("numeroErro")
    erro = addCount(innerErro, erro )
    renderCard(dados.card)
})

function addCount(html,num){
    num = num + 1
    html.innerHTML = `<h3>${num}</h3>`
    return num
}

loadCardAtual()
