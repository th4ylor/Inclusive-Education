# cpa essa bomba vai ser integrada nos flashcards
# https://console.groq.com/docs/quickstart
from dotenv import load_dotenv
import os
from groq import Groq
load_dotenv()


#API de chat deu boa
"""
client = Groq(
    api_key=os.environ.get("GROQ_API_KEY"),
    bese_url="https://api.groq.com/openai/v1"
)
resposta = client.responses.create(
    messages=[
        {
            "role": "user",
            "content": "me de um ola se funcionou"
        }],
    model="openai/gpt-oss-120b",
)
json_fmt = resposta.model_dump_json(indent=2)
#print(json_fmt)
"""

#Teste com a API de resposta estruturada
import openai
import json

texto = """s baleias possuem uma característica surpreendente na hora de dormir: elas descansam apenas metade do cérebro por vez. Esse fenômeno, conhecido como sono uni-hemisférico, permite que esses gigantes marinhos continuem nadando devagar e subindo à superfície para respirar sem o risco de se afogarem.
Enquanto o lado esquerdo do cérebro desliga para recuperar as energias, o lado direito permanece alerta e atento aos predadores e ao ambiente ao redor. Além disso, o olho oposto ao hemisfério que está dormindo permanece aberto para vigiar o oceano. Depois de algumas horas, os lados se alternam para que o cérebro inteiro consiga descansar completamente.
Essa adaptação incrível mostra como esses mamíferos evoluíram para sobreviver no fundo do mar, já que, ao contrário dos peixes, as baleias precisam subir à tona de forma consciente para puxar o ar pelos seus espiráculos.
Se você quiser me contar para qual finalidade ou público-alvo precisa desse conteúdo, posso adaptar esse texto ou criar uma série de curiosidades personalizadas sobre o mundo marinho para você."""

client = openai.OpenAI(
    api_key=os.environ.get("GROQ_API_KEY"),
    base_url="https://api.groq.com/openai/v1"
)

resposta = client.responses.create(
    model="openai/gpt-oss-20b",
    instructions=("Extraia conteúdos do texto. O intuito é criar um flashcard com pergunta e resposta sobre o tema afins de estudo"),
    input= texto,
    text={
        "format": {
            "type": "json_schema",
            "name": "flashcards",
            "strict": True,
            "schema": {
                "type": "object",
                "properties": {
                    "materia": {"type": "string"},
                    "pergunta": {"type": "string"},
                    "resposta": {"type": "string"}
                },
                "required": ["materia", "pergunta", "resposta"],
                "additionalProperties": False
            }
        }
    }
)
flashcards = json.loads(resposta.output_text)

print(json.dumps(flashcards, indent=2, ensure_ascii=False))
