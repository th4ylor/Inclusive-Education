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

        botaoCor.addEventListener("click", function() {
            postit.style.backgroundColor = cor;
        });

        areaCores.appendChild(botaoCor);
    }

    rodapePostit.appendChild(areaCores);

    // Cria o botão Editar
    const botaoEditar = document.createElement("button");
    botaoEditar.textContent = "Editar";

    botaoEditar.addEventListener("click", function() {

        const novoTitulo = prompt("Digite o novo título:", tituloPostit.textContent);

        if (novoTitulo === null) {
            return;
        }

        const novoTexto = prompt("Digite o novo conteúdo:", textoPostit.textContent);

        if (novoTexto === null) {
            return;
        }

        tituloPostit.textContent = novoTitulo;
        textoPostit.textContent = novoTexto;
    });

    rodapePostit.appendChild(botaoEditar);

    // Cria o botão Excluir
    const botaoExcluir = document.createElement("button");
    botaoExcluir.textContent = "Excluir";
    botaoExcluir.classList.add("botao-excluir");

    botaoExcluir.addEventListener("click", function() {
        postit.remove();
    });

    rodapePostit.appendChild(botaoExcluir);

    // Coloca o rodapé dentro do Post-it
    postit.appendChild(rodapePostit);
}

// Criar novos Post-its
botaoAdicionar.addEventListener("click", function() {

    const titulo = campoTitulo.value;
    const texto = campoTexto.value;

    if (titulo === "") {
        alert("Digite um título para sua anotação!");
        return;
    }

    if (texto === "") {
        alert("Digite o conteúdo da sua anotação!");
        return;
    }

    // Cria o artigo
    const novoPostit = document.createElement("article");
    novoPostit.classList.add("postit");
    novoPostit.style.backgroundColor = cores[0];

    // Cria o título
    const tituloPostit = document.createElement("h3");
    tituloPostit.textContent = titulo;

    // Cria o texto
    const textoPostit = document.createElement("p");
    textoPostit.textContent = texto;

    novoPostit.appendChild(tituloPostit);
    novoPostit.appendChild(textoPostit);

    // Adiciona os botões
    adicionarBotoes(novoPostit, tituloPostit, textoPostit);

    // Adiciona o Post-it à página
    areaPostits.appendChild(novoPostit);

    // Limpa os campos
    campoTitulo.value = "";
    campoTexto.value = "";
});

// Adicionar botões aos Post-its antigos
const postitsIniciais = document.querySelectorAll(".postit");

for (const postit of postitsIniciais) {

    const tituloPostit = postit.querySelector("h3");
    const textoPostit = postit.querySelector("p");

    adicionarBotoes(postit, tituloPostit, textoPostit);
}


//getElementById() procura um elemento pelo ID.
//querySelector() permite procurar por ID, classe ou outros seletores CSS.
//appendChild = coloca um elemento dentro de outro
