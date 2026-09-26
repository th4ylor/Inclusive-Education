let card = document.querySelector(".card")
let loginButton = document.querySelector(".loginButton")
let cadastroButton = document.querySelector(".cadastroButton")


loginButton.onclick = () => {
    card.classList.remove("CadastroActive")
    card.classList.add("LoginActive")
}

cadastroButton.onclick = () => {
    card.classList.remove("LoginActive")
    card.classList.add("CadastroActive")
}