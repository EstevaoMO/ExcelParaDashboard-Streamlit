import pandas as pd
import plotly.express as px
import streamlit as st

st.set_page_config(
    page_title="Vendas Dashboard",
    page_icon=":bar-_chart:"
)

@st.cache_data
def extrair_dados_excel():
    dataframe = pd.read_excel(
        io="supermarkt_sales.xlsx",
        engine="openpyxl",
        sheet_name="Sales",
        skiprows=3,
        usecols="B:R",
        nrows=1000
    )

    # Adicionar coluna de hora para o dataframe
    dataframe["Hour"] = pd.to_datetime(dataframe["Time"], format="%H:%M:%S").dt.hour
    return dataframe

dataframe = extrair_dados_excel()

# Aba de Filtragem
st.sidebar.header("Filtros:")

cidade = st.sidebar.multiselect(
    "Cidade:",
    options=dataframe["City"].unique(),
    default=dataframe["City"].unique(),
)

tipo_consumidor = st.sidebar.multiselect(
    "Publico Alvo:",
    options=dataframe["Customer_type"].unique(),
    default=dataframe["Customer_type"].unique(),
)

genero = st.sidebar.multiselect(
    "Gênero:",
    options=dataframe["Gender"].unique(),
    default=dataframe["Gender"].unique(),
)

dataframe_filtrado = dataframe.query(
    "City == @cidade & Customer_type == @tipo_consumidor & Gender == @genero"
)

# Página Principal
st.title(":bar_chart: Dashboard de Vendas")
st.markdown("##")

total_vendas = int(dataframe_filtrado["Total"].sum())
avaliacao_media = round(dataframe_filtrado["Rating"].mean(), 1)
media_receita_por_transacao = round(dataframe_filtrado["Total"].mean(), 2)

coluna_esquerda, coluna_meio, coluna_direita = st.columns(3)

with coluna_esquerda:
    st.subheader("Vendas Totais:")
    st.subheader(f"US $ {total_vendas:,}")

with coluna_meio:
    st.subheader("Média de Avaliações:")
    st.subheader(f"{avaliacao_media}:star:")

with coluna_direita:
    st.subheader("Média de Receita por Transação:")
    st.subheader(f"US $ {media_receita_por_transacao:,}")

st.markdown("---")

# Gráfico de Vendas por Linha de Produto
vendas_por_linha_produto = (
    dataframe_filtrado.groupby(by=["Product line"]).sum(numeric_only=True)[["Total"]].sort_values(by="Total")
)

graf_produto_vendas = px.bar(
    vendas_por_linha_produto,
    x="Total",
    y=vendas_por_linha_produto.index,
    orientation="h",
    title="<b>Vendas por Linha de Produto</br>",
    color_discrete_sequence=["#0083B8"] * len(vendas_por_linha_produto),
    template="plotly_white"
)

graf_produto_vendas.update_layout(
    plot_bgcolor="rgba(0,0,0,0)",
    xaxis=(dict(showgrid=False))
)

# Gráfico de Vendas por Hora
vendas_por_hora = (
    dataframe_filtrado.groupby(by=["Hour"]).sum(numeric_only=True)[["Total"]]
)

grafico_venda_hora = px.bar(
    vendas_por_hora,
    x=vendas_por_hora.index,
    y="Total",
    title="<b>Vendas por Hora</br>",
    color_discrete_sequence=["#0083B8"] * len(vendas_por_hora),
    template="plotly_white"
)

grafico_venda_hora.update_layout(
    plot_bgcolor="rgba(0,0,0,0)",
    xaxis=(dict(tickmode="linear")),
    yaxis=(dict(showgrid=False))
)

coluna_esquerda, coluna_direita = st.columns(2)

coluna_esquerda.plotly_chart(grafico_venda_hora, use_container_width=True)
coluna_direita.plotly_chart(graf_produto_vendas, use_container_width=True)

# CSS
estilo_st = """
                <style>
                #MainMenu {visibility: hidden;}
                footer {visibility: hidden;}
                header {visibility: hidden;}
                </style>
                """

st.markdown(estilo_st, unsafe_allow_html=True)