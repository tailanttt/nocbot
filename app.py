import streamlit as st
from parse_CISCO_ASR920 import extrair_dados as extrair_cisco
from parse_NOKIA_IRXe import extrair_dados as extrair_nokia
from output_HUAWEI_ATN910D import gerar_script as gerar_huawei
from output_ZTE_6120H import gerar_script as gerar_zte
from output_NOKIA_IXRe2 import gerar_script as gerar_nokia

# Função auxiliar para normalizar nome do modelo
def modelo_destino_nome(md: str) -> str:
    if "HUAWEI ATN910D_A" in md:
        return "HUAWEI_ATN910D"
    if "ZTE 6120H_S" in md:
        return "ZTE_6120H"
    if "NOKIA IXR-e2" in md:
        return "NOKIA_IXRe2"
    return md.replace(" ", "_")

def main():
    # Palavra CLAREOU separada e alinhada à esquerda
    st.markdown("<h2 style='text-align: left;'>NOC BOT</h2>", unsafe_allow_html=True)

    # Título menor para GERADOR DE SCRIPT
    st.markdown("<h3 style='text-align: center;'>GERADOR DE SCRIPT - NOC CONFIGURAÇÃO</h3>", unsafe_allow_html=True)

    # Etapa 1: escolher modelos
    st.markdown("<h4 style='font-size:20px;'>Selecione o modelo de entrada:</h4>", unsafe_allow_html=True)
    modelos_entrada = ["CISCO_ASR920", "NOKIA IXR-e"]
    modelo_entrada = st.selectbox("", modelos_entrada)

    if modelo_entrada == "CISCO_ASR920":
        modelos_saida = ["HUAWEI ATN910D_A", "ZTE 6120H_S"]
    elif modelo_entrada == "NOKIA IXR-e":
        modelos_saida = ["NOKIA IXR-e2"]
    else:
        modelos_saida = []

    st.markdown("<h4 style='font-size:20px;'>Selecione o modelo de saída:</h4>", unsafe_allow_html=True)
    modelo_destino = st.selectbox("", modelos_saida)

    # Etapa 2: inserir arquivo
    st.subheader("📥 Arquivo de configuração do Roteador")
    st.markdown("<h4 style='font-size:20px;'>Como deseja fornecer o arquivo?</h4>", unsafe_allow_html=True)
    opcao = st.radio("", ["Colar texto", "Upload de arquivo"])

    backup = None
    if opcao == "Colar texto":
        backup = st.text_area("Cole aqui o conteúdo", height=300)
    else:
        arquivo = st.file_uploader("Upload (.txt ou .cfg)", type=["txt", "cfg"])
        if arquivo:
            raw_bytes = arquivo.getvalue()
            backup = raw_bytes.decode("utf-8", errors="ignore")
            backup = backup.replace("\r\n", "\n")

    # Etapa 3: processar
    if backup:
        # Extrair dados
        if modelo_entrada == "CISCO_ASR920":
            dados = extrair_cisco(backup)
        elif modelo_entrada == "NOKIA IXR-e":
            dados = extrair_nokia(backup)
        else:
            st.error(f"⚠️ Modelo {modelo_entrada} não implementado.")
            return

        hostname = dados["hostname"]
        modelo_nome = modelo_destino_nome(modelo_destino)

        # Linha de botões
        col1, col2, col3, col4 = st.columns(4)
        gerar_btn = col1.button("🚀 Gerar Script")

        # Se clicar em gerar, salva no session_state
        if gerar_btn:
            if "HUAWEI ATN910D_A" in modelo_destino:
                script, banner, banner_roteador = gerar_huawei(
                    hostname=hostname,
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
                st.session_state["script"] = script
                st.session_state["banner"] = banner
                st.session_state["banner_roteador"] = banner_roteador
                st.session_state["modelo_nome"] = modelo_nome
                st.session_state["hostname"] = hostname

            elif "ZTE 6120H_S" in modelo_destino:
                script = gerar_zte(
                    hostname=hostname,
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
                st.session_state["script"] = script
                st.session_state["modelo_nome"] = modelo_nome
                st.session_state["hostname"] = hostname

            elif "NOKIA IXR-e2" in modelo_destino:
                script = gerar_nokia(
                    hostname=dados["hostname"],
                    ip_loopback=dados["loopback100"],
                    uf=dados["uf"],
                    site=dados["site"],
                    saa=dados["saa"],
                    ntp_ips=dados["ntp"],
                    ptp=dados["ptp"],
                    processo_ospf=dados["ospf"]["processo"] if dados.get("ospf") else None,
                    area_ospf_formatada=dados["area_formatada"] if dados.get("area_formatada") else None,
                    bgp=dados["bgp"],
                    rotas_estaticas=dados["rotas_estaticas"],
                    twamp=dados["twamp"],
                    fibra=dados["fibra"],
                    mwrot=dados["mwrot"],
                    movel=dados["movel"],
                    bateria=dados["bateria"],
                    empresarial=dados["empresarial"],
                )
                st.session_state["script"] = script
                st.session_state["modelo_nome"] = modelo_nome
                st.session_state["hostname"] = hostname

        # Botões de download permanecem fixos se já existe script
        if "script" in st.session_state:
            if "HUAWEI ATN910D_A" in modelo_destino:
                col2.download_button("⬇️ Script", st.session_state["script"],
                                     file_name=f"{st.session_state['hostname']}_{st.session_state['modelo_nome']}.txt",
                                     mime="text/plain")
                col3.download_button("⬇️ Banner", st.session_state["banner"],
                                     file_name="banner.txt", mime="text/plain")
                col4.download_button("⬇️ Banner Roteador", st.session_state["banner_roteador"],
                                     file_name=f"{st.session_state['hostname']}_banner.txt", mime="text/plain")

                # Mostrar resultados
                st.subheader("📄 Script Gerado")
                st.code(st.session_state["script"], language="bash")
                st.subheader("📄 Banner Institucional")
                st.code(st.session_state["banner"], language="bash")
                st.subheader(f"📄 Banner do Roteador ({st.session_state['hostname']})")
                st.code(st.session_state["banner_roteador"], language="bash")

            else:
                col2.download_button("⬇️ Script", st.session_state["script"],
                                     file_name=f"{st.session_state['hostname']}_{st.session_state['modelo_nome']}.txt",
                                     mime="text/plain")

                # Mostrar script
                st.subheader("📄 Script Gerado")
                st.code(st.session_state["script"], language="bash")

if __name__ == "__main__":
    main()