import streamlit as st
from output_HUAWEI_ATN910D import gerar_script as gerar_huawei
from output_ZTE_6120H import gerar_script as gerar_zte
from output_NOKIA_IXRe2 import gerar_script as gerar_nokia

def pagina_integracao():
    st.markdown("<h3 style='text-align: center;'>INTEGRAÇÃO DE ROTEADOR</h3>", unsafe_allow_html=True)
    
    DDD_POR_UF = {
        "AC": 68, "AL": 82, "AM": 92, "AP": 96, "BA": 71, "CE": 85, "DF": 61, "ES": 27,
        "GO": 62, "MA": 98, "MG": 31, "MS": 67, "MT": 65, "PA": 91, "PB": 83, "PE": 81,
        "PI": 86, "PR": 41, "RJ": 21, "RN": 84, "RO": 69, "RR": 95, "RS": 51, "SC": 48,
        "SE": 79, "TO": 63,
        "SM": 11, "SI": 19
    }
    
    def ddd_por_uf(uf: str) -> int | None:
        if not uf:
            return None
        return DDD_POR_UF.get(uf.upper())
        
    def calcular_area_ospf(processo: int) -> str:
        if processo is None:
            return ""
        parte3 = processo // 256
        parte4 = processo if processo < 256 else processo - (parte3 * 256)
        return f"0.0.{parte3}.{parte4}"

    # Seleção do modelo de saída logo no topo
    modelos_saida = ["HUAWEI ATN910D_A", "ZTE 6120H_S", "NOKIA IXR-e2"]
    modelo_destino = st.selectbox("Modelo de saída", modelos_saida)

    # Linha 1: Hostname e Loopback
    col1, col2, col3 = st.columns(3)
    with col1:
        hostname_input = st.text_input("Hostname", help="Ex.: SIPRF14-RMP01 (RMA será convertido para RMP automaticamente)")
    with col2:
        ip_loopback = st.text_input("Loopback100 (IP)", help="Ex.: 10.100.0.1")
    with col3:
        processo_ospf_str = st.text_input("OSPF (nº)", value="")
        processo_ospf = int(processo_ospf_str) if processo_ospf_str.strip().isdigit() else None

    # Deriva UF e Site do hostname
    uf_auto, site_auto, hostname = ("", "", "")
    if hostname_input.strip():
        hn = hostname_input.replace("RMA", "RMP")
        uf_auto = hn[:2]
        site_auto = hn[2:].split("-")[0].strip() if len(hn) > 2 else ""
        hostname = hn

    # Linha única com 5 campos: BGP, UF, Site, OSPF
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        ddd = ddd_por_uf(uf_auto)
        bgp_proc_auto = "650" + str(ddd) if ddd is not None else ""
        bgp_processo_str = st.text_input("BGP (650+DDD)", value=bgp_proc_auto)
        bgp_processo = int(bgp_processo_str) if bgp_processo_str.strip().isdigit() else None
    with col2:
        uf = st.text_input("UF", value=uf_auto)
    with col3:
        site = st.text_input("Site", value=site_auto)
    with col4:
        area_ospf_sugestao = calcular_area_ospf(processo_ospf)
        area_ospf = st.text_input("OSPF (IP)", value=area_ospf_sugestao)

    # PTP, NTP e BGP peers (campos de uma linha)
    ptp_ips_raw = st.text_input("PTP IPs (separados por espaço)")
    ntp_ips_raw = st.text_input("NTP IPs (separados por espaço)")
    bgp_peers_raw = st.text_input("BGP Peers IPs (separados por espaço)")
    
# ------------------- FIBRA -------------------
    if "qtd_fibra" not in st.session_state:
        st.session_state.qtd_fibra = 0
    
    col1, col2, col3 = st.columns([8,1,1])
    with col1:
        st.markdown("**NNI Fibra**")
    with col2:
        if st.button("➕", key="add_fibra"):
            st.session_state.qtd_fibra += 1
    with col3:
        if st.button("➖", key="remove_fibra") and st.session_state.qtd_fibra > 0:
            st.session_state.qtd_fibra -= 1
    
    fibra = []
    
    for i in range(st.session_state.qtd_fibra):
        # valor default de speed
        speed_default = st.session_state.get(f"fibra_speed_{i}", "10")
    
        with st.expander(f"Fibra {i+1} - Porta reservada automaticamente de acordo com a speed escolhida.", expanded=True):
            col1, col2, col3 = st.columns([1,1,1])
            with col1:
                speed = st.selectbox(
                    "Speed (Gbps)",
                    ["100", "10", "1"],
                    index=["100","10","1"].index(speed_default),
                    key=f"fibra_speed_{i}"
                )
            with col2:
                mtu = st.text_input(
                    "MTU",
                    value="9208",
                    key=f"fibra_mtu_{i}_{modelo_destino}_{speed}"
                )
            with col3:
                custo_map = {"1": "1000", "10": "100", "100": "10"}
                ospf_cost = st.text_input(
                    "Cost OSPF",
                    value=custo_map.get(speed, ""),
                    key=f"fibra_cost_{i}_{modelo_destino}_{speed}"
                )
    
            # Segunda linha: IP e Mask
            col4, col5 = st.columns([2,1])
            with col4:
                ip_address = st.text_input(
                    "IP Address",
                    key=f"fibra_ip_{i}_{modelo_destino}_{speed}"
                )
            with col5:
                mask = st.selectbox(
                    "Mask",
                    ["255.255.255.252","255.255.255.254"],
                    key=f"fibra_mask_{i}_{modelo_destino}_{speed}"
                )
    
            # Terceira linha: Vizinho | Porta | Anel
            col6, col7, col8 = st.columns(3)
            with col6:
                router_vizinho = st.text_input(
                    "Roteador vizinho",
                    key=f"fibra_router_{i}_{modelo_destino}_{speed}"
                )
            with col7:
                porta_vizinho = st.text_input(
                    "Porta vizinho",
                    key=f"fibra_porta_{i}_{modelo_destino}_{speed}"
                )
            with col8:
                anel_topologia = st.text_input(
                    "Anel topologia",
                    key=f"fibra_anel_{i}_{modelo_destino}_{speed}"
                )
    
            description = f"NNI | {router_vizinho} {porta_vizinho} | FO | CLARO | {anel_topologia}"
    
            fibra.append({
                "interface": f"{router_vizinho} {porta_vizinho}" or None,
                "speed": f"{speed*1000}",
                "mtu": mtu or None,
                "ospf_cost": ospf_cost or None,
                "ip_address": ip_address or None,
                "mask": mask,
                "description": description.strip() if description else None
            })
    
# ------------------- RÁDIO MWROT -------------------
    if "qtd_mwrot" not in st.session_state:
        st.session_state.qtd_mwrot = 0
    
    col1, col2, col3 = st.columns([8,1,1])
    with col1:
        st.markdown("**NNI Rádio MWROT**")
    with col2:
        if st.button("➕", key="add_mwrot"):
            st.session_state.qtd_mwrot += 1
    with col3:
        if st.button("➖", key="remove_mwrot") and st.session_state.qtd_mwrot > 0:
            st.session_state.qtd_mwrot -= 1
    
    mwrot = []
    
    for j in range(st.session_state.qtd_mwrot):
        # valor default de speed
        speed_default = st.session_state.get(f"mwrot_speed_{j}", "10")
    
        with st.expander(f"Rádio {j+1} - Porta reservada automaticamente de acordo com a speed escolhida.", expanded=True):
            col1, col2, col3 = st.columns([1,1,1])
            with col1:
                speed = st.selectbox(
                    "Speed (Gbps)",
                    ["10", "1"],
                    index=["10","1"].index(speed_default),
                    key=f"mwrot_speed_{j}"
                )
            with col2:
                mtu = st.text_input(
                    "MTU",
                    value="9208",
                    key=f"mwrot_mtu_{j}_{modelo_destino}_{speed}"
                )
            with col3:
                custo_map = {"1": "1000", "10": "100"}
                ospf_cost = st.text_input(
                    "Cost OSPF",
                    value=custo_map.get(speed, ""),
                    key=f"mwrot_cost_{j}_{modelo_destino}_{speed}"
                )
    
            # Segunda linha: Bandwidth + BNM + Tipo da porta
            col4, col5, col6 = st.columns([2,1,1])
            with col4:
                bandwidth = st.text_input("Bandwidth (Mbps)", value="1000", key=f"mwrot_bw_{j}")
            with col5:
                bnm_ativo = st.checkbox("BNM ativo", value=True, key=f"mwrot_bnm_{j}")
            with col6:
                porta_logica = st.checkbox("Porta Lógica", value=True, key=f"mwrot_logica_{j}")
    
            # Terceira linha: IP, Mask e VLAN principal
            col7, col8, col9 = st.columns([2,2,1])
            with col7:
                ip_address = st.text_input("IP Address", key=f"mwrot_ip_{j}_{modelo_destino}_{speed}")
            with col8:
                mask = st.selectbox("Mask", ["255.255.255.252","255.255.255.254"],
                                    key=f"mwrot_mask_{j}_{modelo_destino}_{speed}")
            with col9:
                vlan = st.text_input("VLAN", key=f"mwrot_vlan_{j}_{modelo_destino}_{speed}")
    
            # Quarta linha: IP, Mask e VLAN de Gerência
            col10, col11, col12 = st.columns([2,2,1])
            with col10:
                ip_gerencia = st.text_input("IP Gerência", key=f"mwrot_ip_g_{j}_{modelo_destino}_{speed}")
            with col11:
                mask_gerencia = st.selectbox("Mask Gerência",
                                            ["255.255.255.248","255.255.255.252","255.255.255.254"],
                                            key=f"mwrot_mask_g_{j}_{modelo_destino}_{speed}")
            with col12:
                vlan_gerencia = st.text_input("VLAN Gerência", key=f"mwrot_vlan_g_{j}_{modelo_destino}_{speed}")
    
            # Quinta linha: Vizinho | Porta | Anel
            col13, col14, col15 = st.columns(3)
            with col13:
                router_vizinho = st.text_input("Roteador vizinho", key=f"mwrot_router_{j}_{modelo_destino}_{speed}")
            with col14:
                porta_vizinho = st.text_input("Porta vizinho", key=f"mwrot_porta_{j}_{modelo_destino}_{speed}")
            with col15:
                anel_topologia = st.text_input("Anel topologia", key=f"mwrot_anel_{j}_{modelo_destino}_{speed}")
    
            # Monta automaticamente as descrições
            description   = f"NNI | {router_vizinho} {porta_vizinho} | MW-ROT | {anel_topologia}"
            description_gerencia = f"NNI | {router_vizinho} {porta_vizinho} | MW-ROT | GERENCIA | {anel_topologia}"
    
            # Monta a estrutura final
            mwrot.append({
                "interface": f"{router_vizinho} {porta_vizinho}" or None,
                "description": description.strip(),
                "mtu": mtu or None,
                "bandwidth_mbps": bandwidth,
                "bandwidth": str(int(bandwidth) * 1000) if bandwidth and bandwidth.isdigit() else None,
                "speed": f"{speed*1000}",
                "bridge_domains": [vlan] if vlan else [],
                "dot1qs": [vlan] if porta_logica and vlan else [],
                "bnm_ativo": bnm_ativo,
                "porta_logica": {
                    "bdi": vlan,
                    "description": description.strip(),
                    "ip_address": ip_address or None,
                    "mask": mask,
                    "mtu": mtu or None,
                    "ospf_cost": ospf_cost or None
                } if vlan else None,
                "porta_gerencia": {
                    "bdi": vlan_gerencia,
                    "description": description_gerencia.strip(),
                    "ip_address": ip_gerencia or None,
                    "mask": mask_gerencia,
                    "dot1q": vlan_gerencia
                } if vlan_gerencia else None
            })

# ------------------- BATERIA DE LÍTIO -------------------
    if "qtd_bateria" not in st.session_state:
        st.session_state.qtd_bateria = 0
    
    col1, col2, col3 = st.columns([8,1,1])
    with col1:
        st.markdown("**UNI Bateria de Lítio**")
    with col2:
        if st.button("➕", key="add_bateria"):
            st.session_state.qtd_bateria += 1
    with col3:
        if st.button("➖", key="remove_bateria") and st.session_state.qtd_bateria > 0:
            st.session_state.qtd_bateria -= 1
    
    bateria = []
    
    for i in range(st.session_state.qtd_bateria):
        with st.expander(f"Bateria {i+1} - Porta reservada automaticamente de acordo com a speed escolhida.", expanded=True):
            # Primeira linha: Speed + MTU
            col1, col2 = st.columns([1,1])
            with col1:
                speed = st.selectbox(
                    "Speed (Mbps)",
                    ["1000","100"],
                    key=f"bateria_speed_{i}"
                )
            with col2:
                mtu = st.text_input(
                    "MTU",
                    value="9208",
                    key=f"bateria_mtu_{i}_{modelo_destino}"
                )
    
            # Segunda linha: IP + Mask + CRQ
            col3, col4, col5 = st.columns([2,2,2])
            with col3:
                ip_address = st.text_input(
                    "IP Address",
                    key=f"bateria_ip_{i}_{modelo_destino}"
                )
            with col4:
                mask = st.selectbox(
                    "Mask",
                    ["255.255.255.254","255.255.255.252"],
                    key=f"bateria_mask_{i}_{modelo_destino}"
                )
            with col5:
                crq_id = st.text_input(
                    "CRQID (para startup do RMP)",
                    key=f"bateria_crq_{i}_{modelo_destino}"
                )
    
            # Monta automaticamente a descrição
            description = f"UNI | FCC - GERENCIA BATERIA LITIO | {crq_id}"
    
            # Estrutura final
            bateria.append({
                "interface": f"BATERIA",
                "speed": speed,
                "mtu": mtu or None,
                "ip_address": ip_address or None,
                "mask": mask,
                "description": description.strip() if description else None
            })
    
    # Processa listas
    ptp_ips = [ip.strip() for ip in ptp_ips_raw.split(" ") if ip.strip()]
    ntp_ips = [ip.strip() for ip in ntp_ips_raw.split(" ") if ip.strip()]
    bgp_peers = [ip.strip() for ip in bgp_peers_raw.split(" ") if ip.strip()]
    
    # Estrutura BGP final
    bgp = {"processo": bgp_processo, "ips_vizinhos": bgp_peers}
    
    # Botão de gerar
    if st.button("🚀 Gerar Script"):
        if not hostname or not ip_loopback:
            st.error("Informe hostname e Loopback100.")
            return
        if processo_ospf is None:
            st.error("Informe um Processo OSPF válido (inteiro).")
            return
        if not area_ospf.strip():
            st.error("Informe a Área OSPF (ex.: 0.0.X.Y).")
            return
        if bgp_processo is None:
            st.error("Informe um Processo BGP válido (inteiro).")
            return
    
        # Geração conforme modelo
        if "HUAWEI ATN910D_A" in modelo_destino:
            script, banner, banner_roteador = gerar_huawei(
                hostname=hostname,
                ip_loopback=ip_loopback,
                uf=uf,
                site=site,
                ntp_ips=ntp_ips,
                ptp_ips=ptp_ips,
                processo_ospf=processo_ospf,
                area_ospf_formatada=area_ospf,
                bgp=bgp,
                fibra=fibra,
                mwrot=mwrot,
                movel=[],
                bateria=bateria,
                empresarial=[],
                rotas_estaticas=[],
            )
            st.session_state["script"] = script
            st.session_state["banner"] = banner
            st.session_state["banner_roteador"] = banner_roteador
    
        elif "ZTE 6120H_S" in modelo_destino:
            script = gerar_zte(
                hostname=hostname,
                ip_loopback=ip_loopback,
                uf=uf,
                site=site,
                ntp_ips=ntp_ips,
                ptp_ips=ptp_ips,
                processo_ospf=processo_ospf,
                area_ospf_formatada=area_ospf,
                bgp=bgp,
                fibra=fibra,
                mwrot=mwrot,
                movel=[],
                bateria=bateria,
                empresarial=[],
                rotas_estaticas=[],
            )
            st.session_state["script"] = script
    
        elif "NOKIA IXR-e2" in modelo_destino:
            script = gerar_nokia(
                hostname=hostname,
                ip_loopback=ip_loopback,
                uf=uf,
                site=site,
                saa=[],
                ntp_ips=ntp_ips,
                ptp=ptp_ips,
                processo_ospf=processo_ospf,
                area_ospf_formatada=area_ospf,
                bgp=bgp,
                twamp=[],
                fibra=fibra,
                mwrot=mwrot,
                movel=[],
                bateria=bateria,
                empresarial=[],
                rotas_estaticas=[],
            )
            st.session_state["script"] = script
    
        st.session_state["hostname"] = hostname
        st.session_state["modelo_nome"] = modelo_destino
    
    # >>> Botões de download e exibição
    if "script" in st.session_state:
        if "HUAWEI ATN910D_A" in modelo_destino:
            col2, col3, col4 = st.columns(3)
            col2.download_button("⬇️ Script", st.session_state["script"],
                                file_name=f"{st.session_state['hostname']}_{st.session_state['modelo_nome']}.txt",
                                mime="text/plain")
            col3.download_button("⬇️ Banner", st.session_state["banner"],
                                file_name="banner.txt", mime="text/plain")
            col4.download_button("⬇️ Banner Roteador", st.session_state["banner_roteador"],
                                file_name=f"{st.session_state['hostname']}_banner.txt", mime="text/plain")
    
            st.subheader("📄 Script Gerado")
            st.code(st.session_state["script"], language="bash")
            st.subheader("📄 Banner Institucional")
            st.code(st.session_state["banner"], language="bash")
            st.subheader(f"📄 Banner do Roteador ({st.session_state['hostname']})")
            st.code(st.session_state["banner_roteador"], language="bash")
    
        else:
            col2 = st.columns(1)[0]
            col2.download_button("⬇️ Script", st.session_state["script"],
                                file_name=f"{st.session_state['hostname']}_{st.session_state['modelo_nome']}.txt",
                                mime="text/plain")
            st.subheader("📄 Script Gerado")
            st.code(st.session_state["script"], language="bash")