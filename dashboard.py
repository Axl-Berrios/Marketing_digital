import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns

# Configuración inicial
st.set_page_config(layout="wide")
st.title("📊 Dashboard de Análisis de Marketing")

# Cargar datos
archivo = 'Practica_Analisis_Marketing.xlsx'
funnels = pd.read_excel(archivo, sheet_name='Funnels')
campañas = pd.read_excel(archivo, sheet_name='Campañas')
benchmark = pd.read_excel(archivo, sheet_name='Benchmark')

# --- Análisis de Funnels ---
st.header("🔄 Análisis de Funnels")
usuarios_por_etapa = funnels.groupby('Página_Visitada')['ID_Usuario'].nunique().sort_values(ascending=False)

fig1, ax1 = plt.subplots()
sns.barplot(x=usuarios_por_etapa.values, y=usuarios_por_etapa.index, ax=ax1, palette='viridis')
ax1.set_title('Usuarios únicos por etapa del funnel')
st.pyplot(fig1)

conversion_total = funnels[funnels['Conversión'] == 'Sí']['ID_Usuario'].nunique()
usuarios_totales = funnels['ID_Usuario'].nunique()
tasa_conversion = round((conversion_total / usuarios_totales) * 100, 2)
st.metric("Tasa de Conversión General", f"{tasa_conversion}%")

# --- Análisis de Campañas ---
st.header("📣 Análisis de Campañas de Performance")
campañas_grouped = campañas.groupby('Campaña').agg({
    'Impresiones': 'sum',
    'Clics': 'sum',
    'Conversiones': 'sum',
    'Inversión ($)': 'sum'
}).reset_index()
campañas_grouped['CTR (%)'] = round((campañas_grouped['Clics'] / campañas_grouped['Impresiones']) * 100, 2)
campañas_grouped['CPA ($)'] = round(campañas_grouped['Inversión ($)'] / campañas_grouped['Conversiones'], 2)

col1, col2 = st.columns(2)
with col1:
    st.subheader("CTR por campaña")
    fig2, ax2 = plt.subplots()
    sns.barplot(data=campañas_grouped, x='CTR (%)', y='Campaña', ax=ax2, palette='Blues_d')
    st.pyplot(fig2)

with col2:
    st.subheader("CPA por campaña")
    fig3, ax3 = plt.subplots()
    sns.barplot(data=campañas_grouped, x='CPA ($)', y='Campaña', ax=ax3, palette='Oranges')
    st.pyplot(fig3)

# --- Análisis de Benchmark ---
st.header("📊 Benchmark de Competencia")
precio_promedio = benchmark.groupby('Competidor')['Precio'].mean().sort_values()

fig4, ax4 = plt.subplots()
sns.barplot(x=precio_promedio.values, y=precio_promedio.index, ax=ax4, palette='coolwarm')
ax4.set_title("Precio Promedio por Competidor")
st.pyplot(fig4)
