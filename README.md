# SenFlow

O **SenFlow** é um site de apoio aos estudos pensado para estudantes neurodivergentes. A ideia é ajudar na
organização da rotina de estudo de um jeito simples, sem excesso de informação e no ritmo de cada pessoa.

O projeto foi desenvolvido para a disciplina de Algoritmos e Programação, com o tema **Educação Inclusiva**.
Está em desenvolvimento e hospedado em uma instância **Amazon EC2**, utilizando **SQLite** para armazenar usuários e flashcards.

## Sobre o nome

*Sen (Sensus)* vem do latim e se relaciona com sentido, percepção e sensação. *Flow*, em inglês, significa fluxo,
fluidez, movimento contínuo. Juntando os dois: estudar de um jeito que faz sentido para quem está estudando.

## Funcionalidades atuais

### Cadastro e login

- Cadastro com nome, e-mail e senha, incluindo confirmação de senha e verificação de e-mail já cadastrado.
- Senhas armazenadas como hash com Werkzeug.
- Login por sessão e rota de logout.
- Painel e flashcards acessíveis após o login, com cartões vinculados a cada usuário.

### Metodologias de estudo

A página `/estudo` reúne cinco opções. A página inicial apresenta cards explicativos sobre cada uma delas.

| Metodologia | Como funciona no projeto |
| --- | --- |
| Pomodoro | Ciclos de 25 minutos de foco e 5 minutos de pausa. |
| Foco Curto | Ciclos de 15 minutos de foco e 3 minutos de pausa. |
| Estudo em Blocos | Ciclos de 50 minutos de foco e 10 minutos de pausa. |
| Técnica Feynman | Quatro passos para escolher um tema, explicar com palavras simples, identificar dúvidas e revisar. |
| Repetição Espaçada | Três passos orientativos para revisar o conteúdo, avaliar a dificuldade e organizar a próxima revisão. |

Nos métodos com cronômetro, é possível definir um objetivo opcional, pausar, retomar, avançar de fase e encerrar a sessão.
A interface mostra o tempo restante, os ciclos concluídos e os minutos de foco, com aviso sonoro que pode ser desligado.
Também há notificações de troca de fase quando o navegador oferece suporte e o usuário permite.

Nos métodos em etapas, é possível acompanhar o progresso e avançar até a conclusão. Ao encerrar qualquer método,
um resumo mostra os minutos e ciclos de foco ou a quantidade de passos concluídos.

Os tempos dos ciclos são fixos na versão atual. A repetição espaçada funciona como um roteiro: ainda não registra
a dificuldade escolhida, calcula intervalos ou agenda revisões automaticamente.

### Flashcards

- Criação manual de cartões com matéria, pergunta e resposta.
- Exibição da pergunta na frente e da resposta no verso.
- Sorteio de cartões do usuário para revisão.
- Botões **Acertei**, **Quase** e **Errei**, com contadores durante o uso da página.

Na implementação atual, **Acertei remove do banco o cartão registrado como atual na sessão** e sorteia outro.
**Quase** e **Errei** mantêm o cartão salvo e sorteiam outro, sem alterar sua prioridade ou definir uma data de revisão.
Os contadores são reiniciados ao recarregar a página.

### Partes ainda em desenvolvimento

- Geração de flashcards com IA, mencionada como ideia inicial, ainda não implementada.
- Anotações e Post-its.
- Tarefas e checklist persistente; os elementos exibidos na página inicial são demonstrativos.
- Histórico de estudo e indicadores de horas estudadas e dias consecutivos no painel.
- Agendamento automático de revisões e integração com a dificuldade dos flashcards.

As sessões de estudo ficam na sessão do Flask e podem ser recuperadas ao voltar à página enquanto ela continuar válida.
Ainda não existe histórico de sessões salvo no banco de dados.

## Tecnologias

- Python e Flask, com rotas organizadas em blueprints.
- Werkzeug para geração e verificação de hashes de senha.
- SQLite, acessado pelo módulo `sqlite3` do Python.
- HTML, CSS e JavaScript, com templates Jinja2 e chamadas à API usando `fetch`.
- Amazon EC2 para hospedagem.

## Como rodar localmente

Execute os comandos a partir da pasta do projeto.

1. Clone o repositório:

   ```bash
   git clone https://github.com/th4ylor/Inclusive-Education.git
   cd Inclusive-Education
   ```

2. Crie um ambiente virtual:

   ```bash
   python -m venv venv
   ```

3. Ative o ambiente conforme seu terminal:

   **Windows (PowerShell):**

   ```powershell
   .\venv\Scripts\Activate.ps1
   ```

   **Windows (Prompt de Comando):**

   ```bat
   venv\Scripts\activate.bat
   ```

   **Linux/macOS:**

   ```bash
   source venv/bin/activate
   ```

4. Instale as dependências:

   ```bash
   python -m pip install -r requirements.txt
   ```

5. Inicie o servidor local:

   ```bash
   python -m flask --app app run
   ```

6. Acesse `http://127.0.0.1:5000` no navegador. Use **Comece agora** para acessar o cadastro e o login.

O arquivo `app.py` expõe a aplicação Flask, mas não chama `app.run()`. Por isso, o comando de execução local é o
comando do Flask acima, em vez de `python app.py`.

## Banco de dados e hospedagem

As tabelas de usuários e flashcards são criadas automaticamente ao carregar a aplicação. Não é necessário instalar
um servidor de banco separado ou criar as tabelas manualmente.

O arquivo `banco.db` é aberto com um caminho relativo à pasta em que o processo é iniciado. Mantenha essa pasta
consistente ao executar a aplicação para usar o mesmo banco.

Na instância EC2, preserve o banco nas atualizações do site e mantenha backups regulares. A configuração do serviço
de hospedagem não está incluída neste repositório; o comando da seção anterior é destinado ao desenvolvimento local.

## Estrutura do projeto

```text
Inclusive-Education/
├── app.py                 # configuração da aplicação e registro dos blueprints
├── auth.py                # cadastro, login e verificação de autenticação
├── rotas.py               # páginas principais e endpoints de flashcards
├── metodologias.py        # catálogo de métodos e controle das sessões de estudo
├── card.py                # criação, sorteio e remoção de flashcards
├── db.py                  # conexão SQLite e criação das tabelas
├── requirements.txt       # dependências Python
├── templates/
│   ├── index.html         # apresentação do projeto e das metodologias
│   ├── login.html         # login e cadastro
│   └── home/
│       ├── inicial.html   # painel do usuário
│       ├── estudo.html    # seleção de métodos e sessão de estudo
│       └── flashCards.html
├── static/
│   ├── css/
│   ├── js/
│   └── img/
└── Anotações.md            # anotações do grupo; contém referências históricas
```

## Equipe

Grupo 5 — Faculdade UNA Divinópolis (2026/2)

- Isaak Thaylor
- Alexsander Sales
- Icaro Fernandes
- Cristopher Oliveira
