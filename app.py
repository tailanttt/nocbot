import streamlit as st
from pagina_swap import pagina_swap
from pagina_integracao import pagina_integracao

def main():
    # Cabeçalho
    st.markdown("<h2 style='text-align: left;'>NOC BOT</h2>", unsafe_allow_html=True)
    st.markdown("<h3 style='text-align: center;'>GERADOR DE SCRIPT - NOC CONFIGURAÇÃO</h3>", unsafe_allow_html=True)

    # Menu lateral
    escolha = st.sidebar.radio("📑 Escolha:", ["Swap", "Integração"])

    # Chama a página escolhida
    if escolha == "Swap":
        pagina_swap()
    elif escolha == "Integração":
        pagina_integracao()

if __name__ == "__main__":
    main()