const { createElement } = require("react");

formCard = document.getElementById("formCard")
baralho = []

formCard.addEventListener('submit', (e) => {
    e.preventDefault()

    baralho.push({
        materia: document.getElementById("materia").value || 'GERAL',
        pergunta: document.getElementById("pergunta").value,
        resposta: document.getElementById("resposta").value,
    });console.log(baralho)
    
    formCard.reset()
    renderList()
    irPara(baralho.length - 1);
} )


function renderList(){
    const ul = document.getElementById("listCards")
    ul.innerHTML= ""
    baralho.forEach((c,i) =>{
        const li = createElement("li")
        li.innerHTML = `<span>${c.tag} · ${c.pergunta}</span>`
        ul.appendChild(li)
    })
}
