import csv
import json
import os
import sqlite3
from pathlib import Path

from dotenv import load_dotenv
from google import genai


BASE_DIR = Path(__file__).resolve().parent
CSV_PATH = BASE_DIR / "avaliacoes.csv"
DB_PATH = BASE_DIR / "avaliacoes.db"

load_dotenv(BASE_DIR / ".env")
api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    raise SystemExit("GEMINI_API_KEY não encontrada. Confira o arquivo .env.")

client = genai.Client(api_key=api_key)

with sqlite3.connect(DB_PATH) as conn:
    conn.execute("""
        CREATE TABLE IF NOT EXISTS analises (
            id INTEGER PRIMARY KEY,
            texto TEXT NOT NULL,
            sentimento TEXT NOT NULL,
            tema TEXT NOT NULL,
            acao_sugerida TEXT NOT NULL
        )
    """)

print("Banco de dados e tabela prontos.")

with CSV_PATH.open("r", encoding="utf-8-sig", newline="") as csv_file:
    reader = csv.DictReader(csv_file)

    for avaliacao in reader:
        prompt = f"""Analise esta avaliação e responda somente com JSON válido.
Use as chaves sentimento, tema e acao_sugerida.
Sentimento deve ser positivo, neutro ou negativo.

Avaliação: {avaliacao['texto']}
"""

        response = client.models.generate_content(
            model="gemini-3.5-flash-lite",
            contents=prompt,
        )

        print(f"Avaliação {avaliacao['id']}:")
        texto_json = response.text
        if not isinstance(texto_json, str) or not texto_json.strip():
            print(f"Resposta vazia ou inválida para a avaliação {avaliacao['id']}; pulando.")
            continue
        texto_json = texto_json.strip()

        if texto_json.startswith("```"):
            partes = texto_json.split("\n", 1)
            if len(partes) == 1:
                print(f"Formato inesperado na avaliação {avaliacao['id']}; pulando.")
                continue
            texto_json = partes[1]
            texto_json = texto_json.removesuffix("```").strip()

        try:
            resultado = json.loads(texto_json)
            if not isinstance(resultado, dict):
                raise ValueError("a resposta JSON não é um objeto")
            campos_obrigatorios = {"sentimento", "tema", "acao_sugerida"}
            if not campos_obrigatorios.issubset(resultado):
                raise ValueError("faltam campos obrigatórios no JSON")
        except (json.JSONDecodeError, TypeError, ValueError) as error:
            print(f"JSON inválido para a avaliação {avaliacao['id']}: {error}; pulando.")
            continue
        with sqlite3.connect(DB_PATH) as conn:
            conn.execute(
                """
                INSERT OR REPLACE INTO analises
                (id, texto, sentimento, tema, acao_sugerida)
                VALUES (?, ?, ?, ?, ?)
                """,
                (
                    int(avaliacao["id"]),
                    avaliacao["texto"],
                    resultado["sentimento"],
                    resultado["tema"],
                    resultado["acao_sugerida"],
                ),
        )

        with sqlite3.connect(DB_PATH) as conn:
            linhas = conn.execute("""
                SELECT sentimento, COUNT(*)
                FROM analises
                GROUP BY sentimento
            """).fetchall()

    for sentimento, quantidade in linhas:
        print(f"{sentimento}: {quantidade}")


