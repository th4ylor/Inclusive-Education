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
