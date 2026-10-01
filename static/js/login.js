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

document.addEventListener("DOMContentLoaded", () => {
    const msg = document.querySelector(".msg")
    if (msg.classList.contains("sucesso")){
        card.classList.remove("CadastroActive")
        card.classList.add("LoginActive")
    }
    if (msg){
        setTimeout(() =>{
            msg.classList.add("show")
        },100)
        setTimeout(() => {
            msg.classList.remove("show")
        },3000)
    }
})