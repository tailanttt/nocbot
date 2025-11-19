import re
def extrair_dados(backup):
    resultado = {}

# Hostname
    match = re.search(r'^hostname\s+(\S+)', backup, re.MULTILINE)
    if match:
        hostname = match.group(1).replace('RMA', 'RMP')
        resultado["hostname"] = hostname
        resultado["uf"] = hostname[:2]
        resultado["site"] = hostname[2:].split('-')[0].strip()

# Loopback100
    match = re.search(r'interface Loopback100[\s\S]*?ip address (\d+\.\d+\.\d+\.\d+)', backup)
    resultado["loopback100"] = match.group(1) if match else None

# OSPF
    match = re.search(r'^router ospf (\d+)', backup, re.MULTILINE)
    if match:
        processo = int(match.group(1))
        parte3 = processo // 256
        parte4 = processo if processo < 256 else processo - (parte3 * 256)
        resultado["ospf"] = {
            "processo": processo,
            "area_formatada": f"0.0.{parte3}.{parte4}"
        }
    else:
        resultado["ospf"] = None

# BGP
    match_bgp = re.search(r'router bgp (\d+)', backup)
    bgp = {"processo": None, "ips_vizinhos": []}
    if match_bgp:
        bgp["processo"] = match_bgp.group(1)
    bgp_filtered = re.findall(r'neighbor\s+(\d+\.\d+\.\d+\.\d+)\s+inherit', backup)
    bgp["ips_vizinhos"] = list(dict.fromkeys(bgp_filtered))
    resultado["bgp"] = bgp

# ROUTER STATIC
    rotas_estaticas = []
    padrao = re.findall( r'^ip route(?: vrf (\S+))?\s+(\d{1,3}(?:\.\d{1,3}){3})\s+(\d{1,3}(?:\.\d{1,3}){3})\s+(\d{1,3}(?:\.\d{1,3}){3})', backup, re.MULTILINE)
    
    for vrf, ip_origem, mask, ip_destino in padrao:
        rotas_estaticas.append({
            "vrf": vrf if vrf else None,
            "ip_origem": ip_origem,
            "mask": mask,
            "ip_destino": ip_destino
        })
    resultado["rotas_estaticas"] = rotas_estaticas
# NTP
    resultado["ntp"] = re.findall(r'^ntp server (\d+\.\d+\.\d+\.\d+)', backup, re.MULTILINE)

# PTP
    resultado["ptp"] = re.findall(r'clock source (\d+\.\d+\.\d+\.\d+)', backup)

# Interfaces
    interfaces = re.findall(r'(^interface [\s\S]+?)(?=^interface|\Z)', backup, re.MULTILINE)
    
# NNI FO
    fibra = []
    mwrot = []
    bateria = []
    empresarial = []
    movel = []
    for bloco in interfaces:
        if bloco.startswith("interface") and not bloco.startswith("interface BDI") and 'NNI' in bloco and 'FO' in bloco:
            bridge_domain = re.search(r'bridge-domain (\d+)', bloco)
            porta = re.search(r'^interface (\S+)', bloco, re.MULTILINE)
            mtu = re.search(r'\s+mtu (\d+)', bloco)
            descricao = re.search(r'description (.+)', bloco)
            speed = re.search(r'\s+speed (\d+)', bloco)

            if bridge_domain:
                bdi_bloco = next((b for b in interfaces if f"interface BDI{bridge_domain.group(1)}" in b), None)
                if bdi_bloco:
                    descricao_bdi = re.search(r'description (.+)', bdi_bloco)
                    ip_mask = re.search(r'ip address (\d+\.\d+\.\d+\.\d+)\s+(\d+\.\d+\.\d+\.\d+)', bdi_bloco)
                    ospf_cost = re.search(r'ip ospf cost (\d+)', bdi_bloco)
                    fibra.append({
                        "interface": porta.group(1) if porta else None,
                        "mtu": mtu.group(1) if mtu else None,
                        "description": descricao.group(1).strip() if descricao else None,
                        "bdi": bridge_domain.group(1).strip(),
                        "description_bdi": descricao_bdi.group(1).strip() if descricao_bdi else None,
                        "ip_address": ip_mask.group(1) if ip_mask else None,
                        "mask": ip_mask.group(2) if ip_mask else None,
                        "ospf_cost": ospf_cost.group(1) if ospf_cost else None
                    })
            else:
                ip_mask = re.search(r'ip address (\d+\.\d+\.\d+\.\d+)\s+(\d+\.\d+\.\d+\.\d+)', bloco)
                ospf_cost = re.search(r'ip ospf cost (\d+)', bloco)
                fibra.append({
                    "interface": porta.group(1) if porta else None,
                    "description": descricao.group(1).strip() if descricao else None,
                    "mtu": mtu.group(1) if mtu else None,
                    "speed": speed.group(1) if speed else "10000" if porta.group(1).startswith("Ten") else "1000",
                    "ip_address": ip_mask.group(1) if ip_mask else None,
                    "mask": ip_mask.group(2) if ip_mask else None,
                    "ospf_cost": ospf_cost.group(1) if ospf_cost else None
                })

        resultado["fibra"] = fibra

# MW-ROT

        if bloco.startswith("interface") and not bloco.startswith("interface BDI") and 'NNI' in bloco and 'MW-ROT' in bloco:
            porta = re.search(r'^interface (\S+)', bloco, re.MULTILINE)
            descricao = re.search(r'description (.+)', bloco)
            mtu = re.search(r'^\s*mtu\s+(\d+)', bloco, re.MULTILINE)
            bandwidth = re.search(r'\s+bandwidth (\d+)', bloco)
            speed = re.search(r'\s+speed (\d+)', bloco)
            bridge_domains = re.findall(r'bridge-domain (\d+)', bloco)
            dot1qs = re.findall(r'encapsulation dot1q (\d+)', bloco, re.IGNORECASE)
            bnm_ativo = 'cfm' in bloco.lower()

            mwrot.append({
                "interface": porta.group(1) if porta else None,
                "description": descricao.group(1).strip() if descricao else None,
                "mtu": mtu.group(1) if mtu else None,
                "bandwidth": bandwidth.group(1) if bandwidth else None,
                "bandwidth_mbps": str(int(bandwidth.group(1)) // 1000) if bandwidth else None,
                "speed": speed.group(1) if speed else "10000" if porta.group(1).startswith("Ten") else "1000",
                "bridge_domains": bridge_domains,
                "dot1qs": dot1qs,
                "bnm_ativo": bnm_ativo,
                "porta_logica": None,
                "porta_gerencia": None
            })

        if bloco.startswith("interface BDI") and 'NNI' in bloco and 'MW-ROT' in bloco:
            bdi_id = re.search(r'^interface BDI(\d+)', bloco)
            if not bdi_id:
                continue
            bdi_num = bdi_id.group(1)

            for interface in mwrot:
                if bdi_num in interface["bridge_domains"]:
                    if "GERENCIA" in bloco:
                        descricao_bdi_gerencia = re.search(r'description (.+)', bloco)
                        ip_match_gerencia = re.search(r'ip address (\d+\.\d+\.\d+\.\d+)\s+(\d+\.\d+\.\d+\.\d+)', bloco)
                        dot1q_gerencia = re.search(r'encapsulation dot1q (\d+)', bloco, re.IGNORECASE)

                        interface["porta_gerencia"] = {
                            "bdi": bdi_num,
                            "description": descricao_bdi_gerencia.group(1).strip() if descricao_bdi_gerencia else None,
                            "ip_address": ip_match_gerencia.group(1) if ip_match_gerencia else None,
                            "mask": ip_match_gerencia.group(2) if ip_match_gerencia else None,
                            "dot1q": dot1q_gerencia.group(1) if dot1q_gerencia else None
                        }
                    else:
                        descricao_bdi = re.search(r'description (.+)', bloco)
                        ip_match = re.search(r'ip address (\d+\.\d+\.\d+\.\d+)\s+(\d+\.\d+\.\d+\.\d+)', bloco)
                        ospf_match = re.search(r'ip ospf cost (\d+)', bloco)
                        mtu_bdi = re.search(r'\s+ip mtu (\d+)', bloco)

                        interface["porta_logica"] = {
                            "bdi": bdi_num,
                            "description": descricao_bdi.group(1).strip() if descricao_bdi else None,
                            "ip_address": ip_match.group(1) if ip_match else None,
                            "mask": ip_match.group(2) if ip_match else None,
                            "mtu": mtu_bdi.group(1) if mtu_bdi else None,
                            "ospf_cost": ospf_match.group(1) if ospf_match else None
                        }

        resultado["mwrot"] = mwrot

# BATERIA LÍTIO

        if ('UNI' in bloco and 'BATERIA' in bloco) or ('UNI' in bloco and 'ELTEK' in bloco):
            porta = re.search(r'^interface (\S+)', bloco, re.MULTILINE)
            descricao = re.search(r'description (.+)', bloco)
            mtu = re.search(r'\s+mtu (\d+)', bloco)
            vrf_match = re.search(r'vrf forwarding (\S+)', bloco)
            ip_match = re.search(r'ip address (\d+\.\d+\.\d+\.\d+)\s+(\d+\.\d+\.\d+\.\d+)', bloco)
            speed = re.search(r'\s+speed (\d+)', bloco)

            bateria.append({
                'interface': porta.group(1) if porta else None,
                'description': descricao.group(1).strip() if descricao else None,
                'speed': speed.group(1) if speed else None,
                'mtu': mtu.group(1) if mtu else None,
                'vrf': vrf_match.group(1) if vrf_match else None,
                'ip_address': ip_match.group(1) if ip_match else None,
                'mask': ip_match.group(2) if ip_match else None,
            })

        resultado["bateria"] = bateria

# SERVIÇO MÓVEL 2G/3G/4G/5G

        if not bloco.startswith("interface BDI") and 'UNI' in bloco and not 'EDD' in bloco:
            porta = re.search(r'^interface (\S+)', bloco, re.MULTILINE)
            description = re.search(r'description (.+)', bloco)
            speed = re.search(r'\s+speed (\d+)', bloco)

            dot1q_ids = re.findall(r'encapsulation dot1q (\d+)', bloco)
            bd_ids = re.findall(r'bridge-domain (\d+)', bloco)

            bdi_info = []
            for bd_id in bd_ids:
                for bdi_bloco in interfaces:
                    if f'interface BDI{bd_id}' in bdi_bloco:
                        ip_match = re.search(r'ip address (\d+\.\d+\.\d+\.\d+)\s+(\d+\.\d+\.\d+\.\d+)', bdi_bloco)
                        descricao_bdi = re.search(r'description (.+)', bdi_bloco)
                        vrf_match = re.search(r'vrf forwarding (\S+)', bdi_bloco)
                        ip_helper = re.findall(r'ip helper-address (\S+)', bdi_bloco)

                        tipo_servico = None
                        if vrf_match:
                            vrf = vrf_match.group(1).upper()
                            if 'ABIS' in vrf:
                                tipo_servico = '2G'
                            elif 'IUB-DADOS' in vrf:
                                tipo_servico = '3G'
                            elif 'S1' in vrf:                                
                                tipo_servico = '5G' if '5G' in descricao_bdi.group(1) else '4G'
                            elif 'GERENCIA' in vrf:
                                tipo_servico = 'GERENCIA'
                            else:
                                continue

                            bdi_info.append({
                                "dot1q": bd_id if bd_id in dot1q_ids else "não encontrado",
                                "bridge_domain": bd_id,
                                "description": descricao_bdi.group(1).strip() if descricao_bdi else "Descrição não encontrada",
                                "ip_address": ip_match.group(1) if ip_match else None,
                                "mask": ip_match.group(2) if ip_match else None,
                                "tipo_servico": tipo_servico,
                                "dhcp": ip_helper
                            })
                        break

            if bdi_info:
                movel.append({
                    "interface": porta.group(1) if porta else None,
                    "description": description.group(1).strip() if description else None,
                    "speed": speed.group(1) if speed else "10000" if porta.group(1).startswith("Ten") else "1000",
                    "dot1q_ids": dot1q_ids,
                    "bridge_domains": bd_ids,
                    "bdis": bdi_info
                })

        resultado["movel"] = movel

# SERVIÇO EMPRESARIAL

        if 'UNI' in bloco and ('EDD' in bloco or 'EoMPLS' in bloco):
            porta = re.search(r'^interface (\S+)', bloco, re.MULTILINE)
            description = re.search(r'description (.+)', bloco)
            mtu = re.search(r'\s+mtu (\d+)', bloco)
            speed = re.search(r'\s+speed (\d+)', bloco)

            dados_base = {
                "interface": porta.group(1) if porta else None,
                "description": description.group(1).strip() if description else None,
                "mtu": mtu.group(1) if mtu else None,
                "speed": speed.group(1) if speed else "10000" if porta.group(1).startswith("Ten") else "1000",
                "servicos": []
            }

            service_instances = re.findall(r'(service instance[\s\S]+?)\s*!', bloco)
            for bloco_servico in service_instances:
                if "bridge-domain" in bloco_servico:
                    dot1qs = re.findall(r'encapsulation dot1q (\d+)', bloco_servico)
                    bd_ids = re.findall(r'bridge-domain (\d+)', bloco_servico)

                    for bd_id in bd_ids:
                        for bdi_bloco in interfaces:
                            if f'interface BDI{bd_id}' in bdi_bloco:
                                ip_match = re.search(r'ip address (\d+\.\d+\.\d+\.\d+)\s+(\d+\.\d+\.\d+\.\d+)', bdi_bloco)
                                descricao_bdi = re.search(r'description (.+)', bdi_bloco)

                                dados_servico = {
                                    "tipo_servico": "gerencia",
                                    "dot1q": dot1qs[0] if dot1qs else None,
                                    "bridge_domain": bd_id,
                                    "bdi_description": descricao_bdi.group(1).strip() if descricao_bdi else None,
                                    "ip_address": ip_match.group(1) if ip_match else None,
                                    "mask": ip_match.group(2) if ip_match else None
                                }

                                dados_base["servicos"].append(dados_servico)

                elif "second-dot1q" in bloco_servico:
                    descricao_svc = re.search(r'description (.+)', bloco_servico)
                    service_policy = re.search(r'(\d+)(?=KBPS)', bloco_servico)
                    dot1q_match = re.search(r'encapsulation\s+dot1q\s+(\d+)\s+second-dot1q\s+(\d+)', bloco_servico)
                    ip_pw = re.search(r'xconnect (\d+\.\d+\.\d+\.\d+)\s+(\d+)', bloco_servico)
                    mtu_svc = re.search(r'\bmtu (\d+)', bloco_servico)

                    dados_servico = {
                        "tipo_servico": "servico_q",
                        "mtu": mtu_svc.group(1) if mtu_svc else dados_base["mtu"],
                        "dot1q_1": dot1q_match.group(1) if dot1q_match else None,
                        "dot1q_2": dot1q_match.group(2) if dot1q_match else None,
                        "service_policy": service_policy.group(1) if service_policy else None,
                        "xconnect_ip": ip_pw.group(1) if ip_pw else None,
                        "xconnect_vcid": ip_pw.group(2) if ip_pw else None,
                        "service_description": descricao_svc.group(1).strip() if descricao_svc else None
                    }

                    dados_base["servicos"].append(dados_servico)

                else:
                    descricao_svc = re.search(r'description (.+)', bloco_servico)
                    dot1q = re.search(r'encapsulation dot1q (\d+)', bloco_servico)
                    service_policy = re.search(r'(\d+)(?=KBPS)', bloco_servico)
                    ip_pw = re.search(r'xconnect (\d+\.\d+\.\d+\.\d+)\s+(\d+)', bloco_servico)
                    mtu_svc = re.search(r'\bmtu (\d+)', bloco_servico)

                    dados_servico = {
                        "tipo_servico": "servico",
                        "mtu": mtu_svc.group(1) if mtu_svc else dados_base["mtu"],
                        "dot1q": dot1q.group(1) if dot1q else None,
                        "service_policy": service_policy.group(1) if service_policy else None,
                        "xconnect_ip": ip_pw.group(1) if ip_pw else None,
                        "xconnect_vcid": ip_pw.group(2) if ip_pw else None,
                        "service_description": descricao_svc.group(1).strip() if descricao_svc else None
                    }

                    dados_base["servicos"].append(dados_servico)

            if dados_base["servicos"]:
                empresarial.append(dados_base)

        resultado["empresarial"] = empresarial

    return resultado