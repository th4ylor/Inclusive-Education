const botaoAdicionar = document.getElementById("adicionar-postit");
const campoTitulo = document.getElementById("titulo-postit");
const campoTexto = document.getElementById("texto-postit");
const areaPostits = document.querySelector(".area-postits");

const cores = ["#f6d73ef2", "#1f4b93", "rgb(47, 175, 124)", "#e475bb"];

// Função para criar os botões de cada Post-it
function adicionarBotoes(postit, tituloPostit, textoPostit) {

    // Cria o rodapé
    const rodapePostit = document.createElement("div");
    rodapePostit.classList.add("rodape-postit");

    // Cria a área das cores
    const areaCores = document.createElement("div");

    for (const cor of cores) {
        const botaoCor = document.createElement("button");

        botaoCor.style.backgroundColor = cor;
        botaoCor.classList.add("botao-cor");

        botaoCor.addEventListener("click", async function() {

            const notaId = postit.dataset.id;

            const resposta = await fetch(`/api/notas/${notaId}`, {
                method: "PUT",
                headers: {"Content-Type": "application/json"},
                body: JSON.stringify({
                    titulo: tituloPostit.textContent,
                    conteudo: textoPostit.textContent,
                    cor: cor
                })
            });

            const dados = await resposta.json();

            if (!resposta.ok) {
                alert(dados.erro || "Não foi possível alterar a cor.");
                return;
            }

            postit.style.backgroundColor = cor;
        });

        areaCores.appendChild(botaoCor);
    }

    rodapePostit.appendChild(areaCores);

    // Cria o botão Editar
    const botaoEditar = document.createElement("button");
    botaoEditar.textContent = "Editar";
    botaoEditar.classList.add("botao-editar");

    botaoEditar.addEventListener("click", async function() {

        const novoTitulo = prompt(
            "Digite o novo título:",
            tituloPostit.textContent
        );

        if (novoTitulo === null) {
            return;
        }

        const novoTexto = prompt(
            "Digite o novo conteúdo:",
            textoPostit.textContent
        );

        if (novoTexto === null) {
            return;
        }

        const tituloLimpo = novoTitulo.trim();
        const textoLimpo = novoTexto.trim();

        if (!tituloLimpo || !textoLimpo) {
            alert("O título e o conteúdo não podem ficar vazios!");
            return;
        }

        try {
            const notaId = postit.dataset.id;

            const resposta = await fetch(`/api/notas/${notaId}`, {
                method: "PUT",
                headers: {"Content-Type": "application/json"},
                body: JSON.stringify({
                    titulo: tituloLimpo,
                    conteudo: textoLimpo,
                    cor: postit.style.backgroundColor
                })
            });

            const dados = await resposta.json();

            if (!resposta.ok) {
                alert(dados.erro || "Não foi possível atualizar a anotação.");
                return;
            }

            tituloPostit.textContent = tituloLimpo;
            textoPostit.textContent = textoLimpo;

        } catch (erro) {
            alert("Não foi possível conectar ao servidor. Tente novamente.");
            console.error(erro);
        }
    });

    rodapePostit.appendChild(botaoEditar);

    // Cria o botão Excluir
    const botaoExcluir = document.createElement("button");
    botaoExcluir.textContent = "Excluir";
    botaoExcluir.classList.add("botao-excluir");

    botaoExcluir.addEventListener("click", async function() {

        try {
        const notaId = postit.dataset.id;

        const resposta = await fetch(`/api/notas/${notaId}`, {
            method: "DELETE"
        });

        const dados = await resposta.json();

        if (!resposta.ok) {
            alert(dados.erro || "Não foi possível excluir a anotação.");
            return;
        }

        postit.remove();

    } catch (erro) {
        alert("Não foi possível conectar ao servidor. Tente novamente.");
        console.error(erro);
    }
    });

    rodapePostit.appendChild(botaoExcluir);

    // Coloca o rodapé dentro do Post-it
    postit.appendChild(rodapePostit);
}

function criarPostitNaTela(nota) {

    const novoPostit = document.createElement("article");
    novoPostit.classList.add("postit");
    novoPostit.dataset.id = nota.id;

    novoPostit.style.backgroundColor = nota.cor;

    const tituloPostit = document.createElement("h3");
    tituloPostit.textContent = nota.titulo;

    const textoPostit = document.createElement("p");
    textoPostit.textContent = nota.conteudo;

    novoPostit.appendChild(tituloPostit);
    novoPostit.appendChild(textoPostit);

    adicionarBotoes(novoPostit, tituloPostit, textoPostit);

    areaPostits.appendChild(novoPostit);
}

async function carregarNotas() {

    try {
        const resposta = await fetch("/api/notas");

        const dados = await resposta.json();

        if (!resposta.ok) {
            alert(dados.erro || "Não foi possível carregar suas anotações.");
            return;
        }

        for (const nota of dados.notas) {
            criarPostitNaTela(nota);
        }

    } catch (erro) {
        alert("Não foi possível carregar as anotações. Verifique sua conexão.");
        console.error(erro);
    }
}

// Criar novos Post-its
botaoAdicionar.addEventListener("click", async function() {

    const titulo = campoTitulo.value.trim();
    const texto = campoTexto.value.trim();

    if (titulo === "") {
        alert("Digite um título para sua anotação!");
        return;
    }

    if (texto === "") {
        alert("Digite o conteúdo da sua anotação!");
        return;
    }

    try {
        const resposta = await fetch("/api/notas", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                titulo: titulo,
                conteudo: texto,
                cor: cores[0]
            })
        });

        const dados = await resposta.json();

        if (!resposta.ok) {
            alert(dados.erro || "Não foi possível salvar a anotação.");
            return;
        }

        criarPostitNaTela(dados.nota);

        campoTitulo.value = "";
        campoTexto.value = "";

    } catch (erro) {
        alert("Não foi possível conectar ao servidor. Tente novamente.");
        console.error(erro);
    }
});

carregarNotas();

//getElementById() procura um elemento pelo ID.
//querySelector() permite procurar por ID, classe ou outros seletores CSS.
//appendChild = coloca um elemento dentro de outro
// async: indica que a função trabalha com operações assíncronas.
//await: espera uma operação assíncrona terminar.
//.trim(): remove os espaços vazios do começo e do final de um texto