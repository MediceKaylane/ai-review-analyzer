import sqlite3
from pathlib import Path

import pandas as pd
import streamlit as st


DB_PATH = Path(__file__).resolve().parent / "avaliacoes.db"

st.set_page_config(page_title="Análise de avaliações", layout="wide")
st.title("Análise de avaliações de clientes")
st.caption("Resumo das avaliações processadas e salvas no SQLite.")

if not DB_PATH.exists():
    st.error("O banco avaliacoes.db ainda não foi criado. Rode py m2.py primeiro.")
    st.stop()

with sqlite3.connect(DB_PATH) as conn:
    dados = pd.read_sql_query(
        "SELECT id, texto, sentimento, tema, acao_sugerida FROM analises ORDER BY id",
        conn,
    )

if dados.empty:
    st.warning("Ainda não há análises no banco. Rode py m2.py primeiro.")
    st.stop()

contagens = dados["sentimento"].value_counts()
colunas = st.columns(3)
for coluna, sentimento in zip(colunas, ["positivo", "neutro", "negativo"]):
    coluna.metric(sentimento.capitalize(), int(contagens.get(sentimento, 0)))

st.subheader("Avaliações por sentimento")
por_sentimento = dados["sentimento"].value_counts().rename("quantidade")
st.bar_chart(por_sentimento)

st.subheader("Temas das avaliações negativas")
negativas = dados[dados["sentimento"] == "negativo"]
if negativas.empty:
    st.info("Não há avaliações negativas no banco.")
else:
    por_tema = negativas["tema"].value_counts().rename("quantidade")
    st.bar_chart(por_tema)

st.subheader("Todas as análises")
st.dataframe(dados, hide_index=True, width="stretch")

