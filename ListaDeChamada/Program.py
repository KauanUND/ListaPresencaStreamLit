import streamlit as st
import pandas as pd
from datetime import datetime
import io

st.set_page_config(page_title="Controle de Evento", layout="wide")
st.title("📋 Controle de Entrada e Saída do Evento")

# Upload do arquivo Excel
arquivo = st.file_uploader("📁 Envie a lista de participantes (.xlsx)", type=["xlsx"])

if arquivo:
    df = pd.read_excel(arquivo)

    # Detecta a coluna de nome
    col_nome = None
    for col in df.columns:
        if "nome" in col.lower():
            col_nome = col
            break

    if not col_nome:
        st.error("❌ O arquivo precisa ter uma coluna com os nomes dos participantes.")
    else:
        # Inicializa o estado da sessão
        if 'registro' not in st.session_state:
            df['Entrada'] = None
            df['Saída'] = None
            df['Falta'] = None
            st.session_state.registro = df.copy()

        # Campo de busca
        st.subheader("🔍 Buscar participante")
        busca = st.text_input("Digite o nome para buscar")

        # Filtra os participantes
        if busca:
            filtro = st.session_state.registro[st.session_state.registro[col_nome].str.contains(busca, case=False, na=False)]
        else:
            filtro = st.session_state.registro

        st.subheader("👥 Participantes")
        for i, row in filtro.iterrows():
            col1, col2, col3, col4, col5 = st.columns([3, 2, 2, 2, 2])
            col1.write(f"**{row[col_nome]}**")

            if col2.button("✅ Entrada", key=f"entrada_{i}"):
                st.session_state.registro.at[i, 'Entrada'] = datetime.now().strftime("%H:%M:%S")
                st.session_state.registro.at[i, 'Falta'] = None  # limpa falta se entrar

            if col3.button("🚪 Saída", key=f"saida_{i}"):
                st.session_state.registro.at[i, 'Saída'] = datetime.now().strftime("%H:%M:%S")

            if col4.button("❌ Falta", key=f"falta_{i}"):
                st.session_state.registro.at[i, 'Falta'] = "Sim"
                st.session_state.registro.at[i, 'Entrada'] = None
                st.session_state.registro.at[i, 'Saída'] = None

        st.subheader("📊 Resumo")
        st.dataframe(st.session_state.registro)

        # Gera arquivo Excel para download
        buffer = io.BytesIO()
        st.session_state.registro.to_excel(buffer, index=False)
        buffer.seek(0)

        st.download_button(
            label="📥 Baixar registro atualizado",
            data=buffer,
            file_name="registro_evento.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )

else:
    st.info("Envie o arquivo Excel para começar.")
