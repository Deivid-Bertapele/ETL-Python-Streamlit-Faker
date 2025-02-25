import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from data_generator import generate_fake_data
from utils import convert_df_to_excel

# Gerar DataFrame fake
df = generate_fake_data()

# Sidebar
st.sidebar.header("Filtros")
artigocor_filter = st.sidebar.text_input("Filtrar por ArtigoCor")
cod_cota_filter = st.sidebar.text_input("Filtrar por Cod Cota")

# Filtro adicional para os dashboards
st.sidebar.header("Filtros do Dashboard")
visualization_type = st.sidebar.selectbox(
    "Visualizar por:",
    ["ArtigoCor", "Produto"]
)

# Limitar número de itens no gráfico
top_n = st.sidebar.slider(
    "Mostrar top N itens", 
    min_value=5, 
    max_value=50, 
    value=10
)

# Aplicar filtros principais
filtered_df = df.copy()
if artigocor_filter:
    filtered_df = filtered_df[filtered_df["ArtigoCor"].str.contains(
        artigocor_filter, case=False, na=False)]
if cod_cota_filter:
    filtered_df = filtered_df[filtered_df["Cod Cota"].astype(
        str).str.contains(cod_cota_filter, case=False, na=False)]

# Exibir tabela filtrada
st.write("### Dados Filtrados")
st.dataframe(filtered_df)

# Preparar dados para os dashboards
dashboard_df = filtered_df.groupby(visualization_type).agg({
    'Receita Total': 'sum',
    'Peças Total': 'sum'
}).reset_index()

# Ordenar e pegar top N
dashboard_df_receita = dashboard_df.nlargest(top_n, 'Receita Total')
dashboard_df_pecas = dashboard_df.nlargest(top_n, 'Peças Total')

# Criar dashboards
st.write(f"### Dashboard de Receita e Peças (Top {top_n})")

# Gráfico de Receita
fig, ax = plt.subplots(figsize=(12, 6))
sns.barplot(data=dashboard_df_receita, x=visualization_type, y="Receita Total", ax=ax)
plt.xticks(rotation=45, ha='right')
plt.title(f'Receita Total por {visualization_type}')
plt.tight_layout()
st.pyplot(fig)

# Gráfico de Peças
fig, ax = plt.subplots(figsize=(12, 6))
sns.barplot(data=dashboard_df_pecas, x=visualization_type, y="Peças Total", ax=ax)
plt.xticks(rotation=45, ha='right')
plt.title(f'Peças Total por {visualization_type}')
plt.tight_layout()
st.pyplot(fig)

# Botão para download do Excel
st.sidebar.write("### Exportar Dados")
data_xlsx = convert_df_to_excel(filtered_df)
st.sidebar.download_button(
    label="Baixar Excel",
    data=data_xlsx,
    file_name="dados_filtrados.xlsx",
    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
)