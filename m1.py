import csv
import json
import os
from pathlib import Path

from dotenv import load_dotenv
from google import genai


BASE_DIR = Path(__file__).resolve().parent
CSV_PATH = BASE_DIR / "avaliacoes.csv"

load_dotenv(BASE_DIR / ".env")
api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    raise SystemExit("GEMINI_API_KEY não encontrada. Confira o arquivo .env.")

with CSV_PATH.open("r", encoding="utf-8-sig", newline="") as csv_file:
    reader = csv.DictReader(csv_file)
    avaliacao = next((row for row in reader if row["id"] == "1"), None)

if avaliacao is None:
    raise SystemExit("Não encontrei a avaliação com id 1 em avaliacoes.csv.")

prompt = f"""Analise a avaliação de cliente abaixo e responda somente com um objeto JSON válido.

Use exatamente estas chaves:
- sentimento: uma opção entre "positivo", "neutro" e "negativo"
- tema: o principal assunto da avaliação, em poucas palavras
- acao_sugerida: uma ação prática para a empresa, em uma frase

Não inclua markdown nem texto fora do JSON.

Avaliação: {avaliacao['texto']}
"""

client = genai.Client(api_key=api_key)
response = client.models.generate_content(
    model="gemini-3.5-flash-lite",
    contents=prompt,
)

try:
    resultado = json.loads(response.text)
except (json.JSONDecodeError, TypeError) as error:
    raise SystemExit(f"O modelo não retornou JSON válido: {response.text!r}") from error

print(json.dumps(resultado, ensure_ascii=False, indent=2))
