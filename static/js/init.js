
let prevButton = document.getElementById('prev')
let nextButton = document.getElementById('next')
let container = document.querySelector('.sobre')

let itens = container.querySelectorAll('.lista .item')
let indicators = document.querySelector('.indicators')
let dots = indicators.querySelectorAll('.pontos button')
let btnEquipe = container.querySelectorAll(".equipe-nav button")
let number = container.querySelector(".number")
let list = container.querySelector('.lista')
let section = document.querySelector('section')

let active = 0


function mostrarIntegrante(newPosition){
    itens[active].classList.remove('active')
    dots[active].classList.remove('active')
    btnEquipe[active].classList.remove('active')
    
    active = newPosition

    itens[active].classList.add('active')
    dots[active].classList.add('active')
    btnEquipe[active].classList.add('active')

    number.textContent = (active + 1) + ' / ' + itens.length
}

nextButton.onclick = () => {
    list.style.setProperty('--calculation', -1)

    if (active == itens.length - 1) {
        mostrarIntegrante(0)
    }
    else{
        mostrarIntegrante(active + 1)
}}

prevButton.onclick = () => {
    list.style.setProperty('--calculation', 1)

    if (active == 0) {
        mostrarIntegrante(itens.length - 1)
    }
    else{
        mostrarIntegrante(active - 1)
}}


