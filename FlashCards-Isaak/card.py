from flask import Flask, request

formCard = request.form["formCard"]
baralho = []
posicao = 0

def guardarCard():
    baralho.append({
        "materia": request.form["materia"].upper,
        "pergunta": request.form["pergunta"],
        "resposta": request.form["resposta"]
    })
    u = len(baralho) - 1
    return baralho[u]


def gerarCard(posicao):
    c = baralho[posicao]
    return f"""
        <div class="face Frente">
            <small>PERGUNTA . {baralho[c]["materia"]}</small>
                <h3 id="perguntaC">{baralho[c]["pergunta"]}</h3>
            <span class="dica">Passe o mouse para virar -></span>
        </div>

        <div class="face Verso">
            <small>RESPOSTA . {baralho[c]["materia"]}</small>
                <h3 id="respostaC"> {baralho[c]["resposta"]}</h3>
            <span class="dica"><-Passe o mouse para voltar</span>
        </div>`
    """


