import streamlit as st
import pandas as pd
import os
from datetime import date
# =========================
# PROTEÇÃO POR SENHA
# =========================
SENHA_CORRETA = "momor123"  # troca por algo de vocês 😌

senha = st.text_input("🔒 Digite a senha para acessar", type="password")

if senha != SENHA_CORRETA:
    st.warning("Acesso restrito 💕")
    st.stop()

ARQUIVO = "gastos.csv"

st.set_page_config(page_title="Controle de Gastos do Momor", layout="wide")
st.title("Controle de Gastos da Belle❤️")

# =========================
# CARREGAR / CRIAR DADOS
# =========================
if os.path.exists(ARQUIVO):
    df = pd.read_csv(ARQUIVO)
    df["data"] = pd.to_datetime(df["data"], format="mixed", errors="coerce")
    df = df.dropna(subset=["data"])
else:
    df = pd.DataFrame(columns=["data", "descricao", "categoria", "valor"])

df["categoria"] = df["categoria"].fillna("Outros")

# =========================
# ADICIONAR GASTO
# =========================
st.subheader("🍣 Adicionar gasto")

with st.form("add_gasto"):
    data = st.date_input("Data", date.today())
    descricao = st.text_input("Descrição")
    categoria = st.selectbox(
        "Categoria",
        ["Alimentação", "Transporte", "Investimento", "Lazer", "Outros"]
    )
    valor = st.number_input("Valor", min_value=0.0, step=0.01)

    adicionar = st.form_submit_button("Adicionar")

if adicionar:
    novo = {
        "data": data,
        "descricao": descricao,
        "categoria": categoria,
        "valor": valor
    }

    df = pd.concat([df, pd.DataFrame([novo])], ignore_index=True)
    df.to_csv(ARQUIVO, index=False)
    st.success("Gasto adicionado 🚀")
    st.rerun()

# =========================
# FILTROS
# =========================
st.subheader("😲 Filtros")

if not df.empty:
    categorias_unicas = sorted(df["categoria"].unique())

    categorias_filtro = st.multiselect(
        "Categorias",
        options=categorias_unicas,
        default=categorias_unicas
    )

    df_filtrado = df[df["categoria"].isin(categorias_filtro)]
else:
    df_filtrado = df

# =========================
# LISTA DE GASTOS
# =========================
st.subheader("📋 Gastos registrados")

if df_filtrado.empty:
    st.info("Nenhum gasto encontrado.")
else:
    for i, row in df_filtrado.iterrows():
        col1, col2, col3, col4, col5 = st.columns([2, 4, 3, 2, 1])

        col1.write(row["data"].date())
        col2.write(row["descricao"])
        col3.write(row["categoria"])
        col4.write(f"R$ {row['valor']:.2f}")

        if col5.button("❌", key=f"del_{i}"):
            st.session_state["confirmar"] = i

# =========================
# CONFIRMAÇÃO DE EXCLUSÃO
# =========================
if "confirmar" in st.session_state:
    st.warning("⚠️ Tem certeza que deseja excluir este gasto?")
    c1, c2 = st.columns(2)

    if c1.button("Sim, excluir"):
        df = df.drop(st.session_state["confirmar"])
        df.to_csv(ARQUIVO, index=False)
        del st.session_state["confirmar"]
        st.success("Gasto excluído 🗑️")
        st.rerun()

    if c2.button("Cancelar"):
        del st.session_state["confirmar"]
        st.rerun()

# =========================
# RESUMO + GRÁFICO (AGORA SEMPRE VISÍVEL)
# =========================
st.subheader("📊 Resumo")

if not df_filtrado.empty:
    total = df_filtrado["valor"].sum()
    st.metric("💸 Total gasto", f"R$ {total:.2f}")

    resumo_categoria = (
        df_filtrado
        .groupby("categoria")["valor"]
        .sum()
        .reset_index()
    )

    st.bar_chart(resumo_categoria.set_index("categoria"))





