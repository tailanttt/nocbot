import streamlit as st
from parse_CISCO_ASR920 import extrair_dados as extrair_cisco
from parse_NOKIA_IRXe import extrair_dados as extrair_nokia
from output_HUAWEI_ATN910D import gerar_script as gerar_huawei
from output_ZTE_6120H import gerar_script as gerar_zte
from output_NOKIA_IXRe2 import gerar_script as gerar_nokia_out

def main():
    # Palavra CLAREOU separada e alinhada à esquerda
    st.markdown("<h2 style='text-align: left;'>CLAREOU AI</h2>", unsafe_allow_html=True)

    # Título menor para GERADOR DE SCRIPT
    st.markdown("<h3 style='text-align: center;'>GERADOR DE SCRIPT - NOC CONFIGURAÇÃO</h3>", unsafe_allow_html=True)

    # Etapa 1: escolher modelos com fonte maior
    st.markdown("<h4 style='font-size:20px;'>Selecione o modelo de entrada:</h4>", unsafe_allow_html=True)
    modelos_entrada = ["CISCO_ASR920", "NOKIA IXR-e"]
    modelo_entrada = st.selectbox("", modelos_entrada)

    modelos_saida = []
    if modelo_entrada == "CISCO_ASR920":
        modelos_saida = ["HUAWEI ATN910D_A", "ZTE 6120H_S"]
    elif modelo_entrada == "NOKIA IXR-e":
        modelos_saida = ["NOKIA IXR-e2"]

    st.markdown("<h4 style='font-size:20px;'>Selecione o modelo de saída:</h4>", unsafe_allow_html=True)
    modelo_destino = st.selectbox("", modelos_saida)

    # Etapa 2: inserir backup → texto atualizado
    st.subheader("📥 Arquivo de configuração do Roteador")
    st.markdown("<h4 style='font-size:20px;'>Como deseja fornecer o arquivo?</h4>", unsafe_allow_html=True)
    opcao = st.radio("", ["Colar texto", "Upload de arquivo"])

    backup = None
    if opcao == "Colar texto":
        backup = st.text_area("Cole aqui o conteúdo do arquivo", height=300)
    else:
        arquivo = st.file_uploader("Faça upload do arquivo de configuração (.txt ou .cfg)", type=["txt", "cfg"])
        if arquivo is not None:
            backup = arquivo.read().decode("utf-8")

    # Etapa 3: processar backup
    if backup:
        col1, col2 = st.columns([1,1])
        gerar = col1.button("🚀 Gerar Script")
        baixar = None

        if gerar:
            # Extrair dados
            if modelo_entrada == "CISCO_ASR920":
                dados = extrair_cisco(backup)
            elif modelo_entrada == "NOKIA IXR-e":
                dados = extrair_nokia(backup)
            else:
                st.error(f"⚠️ Modelo {modelo_entrada} não implementado.")
                return

            # Gerar script conforme destino
            script = None
            if "HUAWEI ATN910D_A" in modelo_destino:
                script = gerar_huawei(
                    hostname=dados["hostname"],
                    ip_loopback=dados["loopback100"],
                    uf=dados["uf"],
                    site=dados["site"],
                    ntp_ips=dados["ntp"],
                    ptp_ips=dados["ptp"],
                    processo_ospf=dados["ospf"]["processo"] if dados["ospf"] else None,
                    area_ospf_formatada=dados["ospf"]["area_formatada"] if dados["ospf"] else None,
                    bgp=dados["bgp"],
                    rotas_estaticas=dados["rotas_estaticas"],
                    fibra=dados["fibra"],
                    mwrot=dados["mwrot"],
                    movel=dados["movel"],
                    bateria=dados["bateria"],
                    empresarial=dados["empresarial"],
                )
            elif "ZTE 6120H_S" in modelo_destino:
                script = gerar_zte(
                    hostname=dados["hostname"],
                    ip_loopback=dados["loopback100"],
                    uf=dados["uf"],
                    site=dados["site"],
                    ntp_ips=dados["ntp"],
                    ptp_ips=dados["ptp"],
                    processo_ospf=dados["ospf"]["processo"] if dados["ospf"] else None,
                    area_ospf_formatada=dados["ospf"]["area_formatada"] if dados["ospf"] else None,
                    bgp=dados["bgp"],
                    rotas_estaticas=dados["rotas_estaticas"],
                    fibra=dados["fibra"],
                    mwrot=dados["mwrot"],
                    movel=dados["movel"],
                    bateria=dados["bateria"],
                    empresarial=dados["empresarial"],
                )
            elif "NOKIA IXR-e2" in modelo_destino:
                script = gerar_nokia_out(
                    hostname=dados["hostname"],
                    ip_loopback=dados["loopback100"],
                    uf=dados["uf"],
                    site=dados["site"],
                    ntp_ips=dados["ntp"],
                    ptp=dados["ptp"],
                    processo_ospf=dados["ospf"]["processo"] if dados.get("ospf") else None,
                    area_ospf_formatada=dados["area_formatada"] if dados.get("area_formatada") else None,
                    bgp=dados["bgp"],
                    twamp=dados["twamp"],
                    fibra=dados["fibra"],
                    mwrot=dados["mwrot"],
                    movel=dados["movel"],
                    empresarial=dados["empresarial"],
                )
            else:
                st.error(f"⚠️ Conversão de {modelo_entrada} para {modelo_destino} ainda não implementada.")
                return

            # Mostrar resultado
            st.subheader("📄 Script Gerado")
            st.code(script, language="bash")

            # Botão de download ao lado do Gerar
            baixar = col2.download_button(
                label="⬇️ Baixar Script",
                data=script,
                file_name=f"script_{modelo_destino}.txt",
                mime="text/plain"
            )

if __name__ == "__main__":
    main()