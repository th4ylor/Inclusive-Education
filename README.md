# SenFlow 
Um fluxo que faz sentido para você.

O **SenFlow** é um site de apoio aos estudos pensado para estudantes neurodivergentes. A ideia é ajudar na
organização da rotina de estudo de um jeito simples, sem excesso de informação e no ritmo de cada pessoa.

O projeto foi desenvolvido para a disciplina de Algoritmos e Programação, com o tema **Educação Inclusiva**.

## Sobre o nome

*Sen (Sensus)* vem do latim e se relaciona com sentido, percepção e sensação. *Flow*, em inglês, significa fluxo, 
fluidez, movimento contínuo. Juntando os dois: estudar de um jeito que faz sentido para quem está estudando.

## O que o site tem (ou terá)

- Login e cadastro de usuários
- Flashcards criados manualmente ou automaticamente com IA (pergunta na frente, resposta no verso)
- Aba de metodologias de estudo: Pomodoro, estudo em blocos, técnica de Feynman e repetição espaçada
- Aba de anotações
- Checklist de tarefas, se der tempo

> O projeto ainda está em construção, então algumas dessas partes podem não estar prontas.

## Tecnologias

- Python com Flask
- HTML, CSS e JavaScript
- SQLite

## Como rodar o projeto

1. Clone o repositório:
```bash
   git clone https://github.com/th4ylor/Inclusive-Education.git
   cd Inclusive-Education
```

2. Crie e ative um ambiente virtual:
```bash
   python -m venv venv

   # Windows
   venv\Scripts\activate

   # Linux/macOS
   source venv/bin/activate
```

3. Instale o Flask:
```bash
   pip install flask
```

4. Rode o projeto:
```bash
   python app.py
```

5. O terminal vai mostrar uma URL (algo como `http://127.0.0.1:5000`). É só copiar e colar no navegador.

## Estrutura do projeto

```
Inclusive-Education/
├── app.py          # aplicação principal (rotas do Flask)
├── auth.py         # login e cadastro
├── templates/      # páginas HTML
├── static/         # CSS, JavaScript e imagens
└── Annotations.md  # anotações do grupo
```

## Equipe

Grupo 5 — Faculdade UNA Divinópolis (2026/2)

- Isaak Thaylor
- Alexsander Sales
- Icaro Fernandes
- Cristopher Oliveira
