import os 
from dotenv import load_dotenv
from google import genai

load_dotenv()
client = genai.Client(api_key=os.getenv("GENAI_API_KEY"))

resposta = client.models.generate_content(
    model="gemini-3.5-flash-lite",
    contents="Em uma frase, o que é uma nota de serviço?"
)

print(resposta.text)