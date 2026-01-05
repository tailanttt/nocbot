import streamlit as st
from ptp_multicast import coletar_dados

# ------------------- PÁGINA PTP -------------------
def pagina_ptp():
    st.markdown("<h3 style='text-align: center;'>PTP Multicast Sync-E</h3>", unsafe_allow_html=True)

    # Etapa 1: selecionar modelo e IP na mesma linha
    col_modelo, col_ip = st.columns(2)
    modelos = ["HUAWEI ATN910D_A", "ZTE 6120H_S", "NOKIA IXR-e2", "CISCO NCS 540"]
    modelo = col_modelo.selectbox("Modelo do roteador", modelos)
    ip = col_ip.text_input("IP do roteador")

    # Etapa 2: inserir usuário e senha na mesma linha
    col_user, col_pass = st.columns(2)
    username = col_user.text_input("Usuário")
    password = col_pass.text_input("Senha", type="password")

    # Linha de botões
    col1, col2 = st.columns(2)
    gerar_btn = col1.button("🚀 Gerar Script")

    # Se clicar em gerar
    if gerar_btn:
        if ip and username and password:
            try:
                script = coletar_dados(ip, username, password)
                st.session_state["script"] = script
                st.session_state["hostname"] = ip  # pode ajustar se coletar_dados retornar hostname
                st.session_state["modelo"] = modelo
            except Exception as e:
                st.error(f"⚠️ Erro ao coletar dados: {e}")
        else:
            st.warning("Preencha IP, usuário e senha.")

    # Botões de download e exibição
    if "script" in st.session_state:
        col2.download_button("⬇️ Script",
                             st.session_state["script"],
                             file_name=f"{st.session_state['hostname']}_{st.session_state['modelo']}_PTP.txt",
                             mime="text/plain")

        st.subheader("📄 Script Gerado")
        st.code(st.session_state["script"], language="bash")
