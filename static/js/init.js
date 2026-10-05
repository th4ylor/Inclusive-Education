//Pomodoro
const btn = document.getElementById("btnPausar")
const foco = 25 * 60 //duracao do bloco em segundos
const tempo = document.getElementById("tempo")

let restante = foco
let ciclos = 0
let timer = null
let fim = 0 //horario que o bloco termina

const doisDG = (n) => String(n).padStart(2, '0') // transforma o numero em string e coloca um 0 antes dele sempre pra transformar ele em padrao 2 digtos
const formatar = (s) => `${doisDG(Math.floor(s / 60))}:${doisDG(Math.floor(n % 60))}` //Formata tipo assim: 00:00


function desenhar(){
    
}

//Parte do carrocel

let prevButton = document.getElementById('prev')
let nextButton = document.getElementById('next')
let container = document.querySelector('.sobre')
let itens = container.querySelectorAll('.lista .item')
let indicators = document.querySelector('.indicators')
let dots = indicators.querySelectorAll('ul li')
let list = container.querySelector('.lista')
let section = document.querySelector('section')

let active = 0
let firstPosition = 0
let lastPosition = itens.length - 1

function setSlider(){
    section.classList.remove("bg1", "bg2", "bg3")
    section.classList.add(`bg${active + 1}`)

    let itemOld = container.querySelector('.lista .item.active')
    itemOld.classList.remove('active')

     let dotsOld = indicators.querySelector('ul li.active')
    dotsOld.classList.remove('active')
    dots[active].classList.add('active')

    indicators.querySelector('.number').innerHTML = '0' + (active + 1)
}

nextButton.onclick = () => {
    list.style.setProperty('--calculation', 1)

    if (active + 1 > lastPosition) {
        active = 0
    }
    else{
        active = active + 1
    }
    setSlider()
    itens[active].classList.add('active')
}


prevButton.onclick = () => {
    list.style.setProperty('--calculation', -1)

    if (active - 1 < firstPosition) {
        active = lastPosition
    }
    else{
        active = active - 1
    }
    setSlider()
    itens[active].classList.add('active')
  

}