import streamlit as st
import pandas as pd
import os
from datetime import date

# =========================
# CONFIG
# =========================
ARQUIVO = "gastos.csv"
ARQUIVO_SALARIO = "salario.txt"

st.set_page_config(
    page_title="Controle Financeiro 💸",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# =========================
# DARK MODE + DESIGN
# =========================
st.markdown("""
<style>
.stApp {
    background-color: #0f1117;
    color: #ffffff;
}

h1, h2, h3 {
    color: #f8f9fa;
}

div[data-testid="metric-container"] {
    background-color: #1c1f26;
    border-radius: 16px;
    padding: 20px;
    box-shadow: 0 4px 12px rgba(0,0,0,0.4);
}

button {
    border-radius: 12px !important;
    background-color: #6c63ff !important;
    color: white !important;
    font-weight: 600 !important;
}

input, select {
    border-radius: 10px !important;
    background-color: #1c1f26 !important;
    color: white !important;
}

footer, #MainMenu {
    visibility: hidden;
}
</style>
""", unsafe_allow_html=True)

st.title("💜 Controle Financeiro do Casal")

# =========================
# SALÁRIO
# =========================
st.subheader("💰 Salário")

if os.path.exists(ARQUIVO_SALARIO):
    salario = float(open(ARQUIVO_SALARIO).read())
else:
    salario = 0.0

novo_salario = st.number_input(
    "Digite seu salário",
    min_value=0.0,
    step=100.0,
    value=salario
)

if novo_salario != salario:
    with open(ARQUIVO_SALARIO, "w") as f:
        f.write(str(novo_salario))
    salario = novo_salario

# =========================
# CARREGAR DADOS
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
st.subheader("➕ Adicionar gasto")

with st.form("add_gasto"):
    data = st.date_input("Data", date.today())
    descricao = st.text_input("Descrição")
    categoria = st.selectbox(
        "Categoria",
        ["Alimentação", "Transporte", "Investimento", "Lazer", "Outros"]
    )
    valor = st.number_input("Valor", min_value=0.0, step=0.01)

    adicionar = st.form_submit_button("Adicionar gasto")

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
st.subheader("🔍 Filtros")

categorias = sorted(df["categoria"].unique())
categorias_filtro = st.multiselect(
    "Categorias",
    categorias,
    default=categorias
)

df_filtrado = df[df["categoria"].isin(categorias_filtro)]

# =========================
# LISTA DE GASTOS
# =========================
st.subheader("📋 Gastos")

if df_filtrado.empty:
    st.info("Nenhum gasto registrado.")
else:
    for i, row in df_filtrado.iterrows():
        c1, c2, c3, c4, c5 = st.columns([2, 4, 3, 2, 1])

        c1.write(row["data"].date())
        c2.write(row["descricao"])
        c3.write(row["categoria"])
        c4.write(f"R$ {row['valor']:.2f}")

        if c5.button("❌", key=f"del_{i}"):
            st.session_state["excluir"] = i

# =========================
# CONFIRMAR EXCLUSÃO
# =========================
if "excluir" in st.session_state:
    st.warning("Deseja excluir este gasto?")
    a, b = st.columns(2)

    if a.button("Sim"):
        df = df.drop(st.session_state["excluir"])
        df.to_csv(ARQUIVO, index=False)
        del st.session_state["excluir"]
        st.rerun()

    if b.button("Cancelar"):
        del st.session_state["excluir"]
        st.rerun()

# =========================
# RESUMO FINANCEIRO
# =========================
st.subheader("📊 Resumo")

total_gastos = df_filtrado["valor"].sum()
saldo = salario - total_gastos

c1, c2, c3 = st.columns(3)

c1.metric("💰 Salário", f"R$ {salario:.2f}")
c2.metric("💸 Gastos", f"R$ {total_gastos:.2f}")
c3.metric(
    "🟢 Saldo disponível" if saldo >= 0 else "🔴 Saldo negativo",
    f"R$ {saldo:.2f}"
)

# =========================
# GRÁFICO
# =========================
if not df_filtrado.empty:
    resumo = df_filtrado.groupby("categoria")["valor"].sum()
    st.bar_chart(resumo)






