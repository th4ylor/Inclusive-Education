let card = document.querySelector(".card")
let loginButoon = document.querySelector(".loginButton")
let cadastroButton = document.querySelector(".cadastroButton")
let text = document.querySelector(".corText")

function activeLogin() {
    card.classList.remove("CadastroActive")
    card.classList.add("LoginActive")
    text.classList.add("Xactive")

}
function activeCadastro(){
    card.classList.remove("LoginActive")
    card.classList.add("CadastroActive")
    text.classList.remove("Xactive")
}
loginButoon.addEventListener("click", activeLogin)
cadastroButton.addEventListener("click", activeCadastro)

document.addEventListener("DOMContentLoaded", () => {
    const msg = document.querySelector(".msg")
    const parametros = new URLSearchParams(window.location.search)
    const modo = parametros.get("modo")
    if (modo === "login"){
        activeLogin()

    }else{
        activeCadastro()
    }

    if (msg && msg.classList.contains("sucesso")){
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