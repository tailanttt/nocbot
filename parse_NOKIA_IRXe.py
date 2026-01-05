import re
def extrair_dados(backup):
    resultado = {}

# //------- Melhorias -------//
# Fazer o regex único dentro das vprns dentro ddo empresárial e móvel semelhante a captura no regex de bgp community
# Empresarial

# HOSTNAME
    resultado["hostname"] = (next(iter(re.findall(r'name\s+"([^"]+)"', backup)), None) or "").replace("RMA", "RMP")
    resultado["uf"] = resultado["hostname"][:2]
    resultado["site"] = resultado["hostname"][2:].split("-")[0].strip()
# LOOPBACK100
    resultado["loopback100"] = next(iter(re.findall(r'router-id\s+(\d{1,3}(?:\.\d{1,3}){3})', backup)), None)
# OSPF
    resultado["area_formatada"] = next(iter(re.findall(r'area\s+(\d{1,3}(?:\.\d{1,3}){3})', backup)), None)
# NTP
    resultado["ntp"] = re.findall(r'^\s*server\s+(\d+\.\d+\.\d+\.\d+)\s+version\s+\d+',backup,re.MULTILINE)
# PTP Sync-E
    resultado["ptp"] = re.findall(r'^\s*source-port\s+(\S+)', backup, re.MULTILINE)
# BGP
    bgp = {"processo": [],"ddd": [],"ips_vizinhos": [],"community": [],"policy": []}
# Captura o número do peer-as (só um processo)
    match_as = re.search(r'peer-as\s+(\d+)', backup)
    if match_as:
        bgp["processo"] = match_as.group(1)
        bgp["ddd"] = match_as.group(1)[-2:] 
# Neighbor
    vizinhos = re.findall(r'neighbor\s+(\d+\.\d+\.\d+\.\d+)\s+description\s+"(?:TO_)?([^"]+)"', backup, re.MULTILINE)
    bgp["neighbors"] = list(dict.fromkeys(vizinhos))  # remove duplicados     
# Captura hostname do RMC nas policy
    policy = re.findall(r'community add\s+"([A-Za-z0-9]{7}-RM[CD]\d{2})"', backup)
    bgp["policy"] = list(dict.fromkeys(policy))  # remove duplicados mantendo ordem
# Captura hostname do RMC nas community
    community = re.findall(r'community\s+"([A-Za-z0-9]{7}-RM[CD]\d{2})"\s+members\s+"([\d:]+)"', backup, re.MULTILINE)
    bgp["community"] = bgp["community"] = sorted(community, key=lambda x: (x[0] not in bgp["policy"], bgp["policy"].index(x[0]) if x[0] in bgp["policy"] else float('inf')))
    resultado["bgp"] = bgp   
#SAA 
    resultado["saa"] = re.findall(r'test\s+"T1_([A-Z0-9-]+?)(?:-BE)".*?\n[\s\S]*?icmp-ping\s+(\d{1,3}(?:\.\d{1,3}){3})',backup, re.DOTALL)
#TWAMP 
    resultado["twamp"] = re.findall(r'^\s*prefix\s+(\d{1,3}(?:\.\d{1,3}){3}/\d+)\s+create$',backup, re.MULTILINE)
#Portas físicas NNI
    
    portas = re.findall(r'(?m)^\s{4}port\s+\S+[\s\S]*?^\s{4}exit$', backup)
    blocos_interface = re.findall(r'^\s{8}interface\s+"(TO[^"]+)"(.*?)^\s{8}exit\b', backup, re.DOTALL | re.MULTILINE)    
    blocos_lag = list(re.finditer(r'(?m)^ {4}lag (\d+)[\s\S]*?^ {4}exit$', backup))
    blocos_gerencia = re.findall( rf'^(?: {{8}}|\t{{2}})vprn {str(bgp["ddd"]) + "61"}\b.*?^(?: {{8}}|\t{{2}})exit\b', backup, re.DOTALL | re.MULTILINE )
    blocos_int_gerencia = re.findall(r'^(?: {12}|\t{3})interface\s+".+?"\s+create.*?^(?: {12}|\t{3})exit\b', blocos_gerencia[1] if len(blocos_gerencia) > 1 else blocos_gerencia[0] if blocos_gerencia else '', re.DOTALL | re.MULTILINE)
    fibra = []
    mwrot = []
    movel = []
    bateria = []
    empresarial = []    
    vprns = [("ABIS", 103), ("IUB", 1), ("S1", 95), ("GERENCIA", 61)]    
    
    for bloco in portas:
        descricao = re.search(r'\s*description\s+"([^"]+)"', bloco)
        if "description" in bloco:    
#FO            
            if descricao and "NNI" in descricao.group(1) and not ("MW-ROT" in descricao.group(1) or "MWROT" in descricao.group(1)):
                interfaces_nni = []
                porta = re.search(r'^\s*port\s+(\S+)', bloco, re.MULTILINE)
                speed = re.search(r'\s*speed\s+(\S+)', bloco)
# Verifica se a porta está em algum LAG
                lag = None
                dot1q = None
                if porta:
                    for match in blocos_lag:
                        bloco_lag = match.group(0)
                        lag_num = match.group(1)
                        portas_lag = re.findall(r'port\s+(\S+)', bloco_lag)
                        if porta.group(1) in portas_lag:
                            lag = int(lag_num)
                            break
# Verifica as porta Logicas (Interfaces)    
                
                for interface, bloco_logico in blocos_interface:
                    if lag is not None:
                        porta_logica = re.search(r'port\s+lag-{}:(\d+)'.format(lag), bloco_logico)
                    else:
                        porta_logica = re.search(r'port\s+{}\s*(?::\s*(\d+))?'.format(re.escape(porta.group(1))), bloco_logico)
                    if porta_logica:
                        dot1q = porta_logica.group(1) if porta_logica and porta_logica.group(1) else None
                        ip = re.search(r'address\s+(\d{1,3}(?:\.\d{1,3}){3}/\d+)', bloco_logico)
                        descricao_logica = re.search(r'description\s+"([^"]+)"', bloco_logico)
                        bfd_match = re.search(r'\bbfd\b', bloco_logico, re.IGNORECASE)
                        bfd_exists = bfd_match is not None

                        interfaces_nni.append({
                            "interface": interface,
                            "ip": ip.group(1) if ip else None,
                            "descricao": descricao_logica.group(1) if descricao_logica else None,
                            "porta": porta.group(1) if porta else None,
                            "dot1q": dot1q,
                            "bfd": bfd_exists
                        })
                fibra.append({
                    "porta": porta.group(1) if porta else None,
                    "descricao": descricao.group(1),
                    "speed": speed.group(1) if speed else "100000" if "c" in porta.group(1) else "10000",
                    "interfaces": interfaces_nni,
                    "lag": lag
                })
              
# MWROT
            elif descricao and "NNI" in descricao.group(1) and ("MW-ROT" in descricao.group(1) or "MWROT" in descricao.group(1)):
                interfaces_mwrot = []
                gerencia_mwrot = None
                porta = re.search(r'^\s*port\s+(\d+/\d+/\d+)', bloco, re.MULTILINE)
                speed = re.search(r'\s*speed\s+(\S+)', bloco)    
                bandwidth = re.search(r'\s*egress-rate\s+(\S+)', bloco)
                bnm_ativo = 'cfm' in bloco.lower()            
#LAG
                lag = None
                if porta:
                    for match in blocos_lag:
                        bloco_lag = match.group(0)
                        lag_num = match.group(1)
                        portas_lag = re.findall(r'port (\d+/\d+/\d+)', bloco_lag)
                        if porta.group(1) in portas_lag:
                            lag = int(lag_num)
                            break
            
                for interface, bloco_logico in blocos_interface:
                    porta_logica = re.search(r'port\s+(\d+/\d+/\d+):(\d+)', bloco_logico)
                    lag_logico = re.search(r'port\s+lag-(\d+):(\d+)', bloco_logico)
            
                    match_por_porta = porta and porta_logica and porta_logica.group(1) == porta.group(1)
                    match_por_lag = lag_logico and lag and int(lag_logico.group(1)) == lag
            
                    if match_por_porta or match_por_lag:
                        ip = re.search(r'address\s+(\d{1,3}(?:\.\d{1,3}){3}/\d+)', bloco_logico)
                        descricao_logica = re.search(r'description\s+"([^"]+)"', bloco_logico)
                        bfd_match = re.search(r'\bbfd\b', bloco_logico, re.IGNORECASE)
                        bfd_exists = bfd_match is not None
#GERENCIA
                        for interface_gerencia in blocos_int_gerencia:
                            if porta and porta.group(1) in interface_gerencia:
                                description_gerencia = re.search(r'description\s+"([^"]+)"', interface_gerencia)
                                ip_gerencia = re.search(r'address\s+(\d{1,3}(?:\.\d{1,3}){3}/\d+)', interface_gerencia)
                                sap = re.search(r'sap\s+(\d+/\d+/\d+):(\d+)', interface_gerencia)
                                interface_nome = re.search(r'interface\s+"([^"]+)"', interface_gerencia)
            
                                gerencia_mwrot = {
                                    "interface": interface_nome.group(1) if interface_nome else None,
                                    "descricao": description_gerencia.group(1) if description_gerencia else None,
                                    "ip": ip_gerencia.group(1) if ip_gerencia else None,
                                    "porta": sap.group(1) if sap else None,
                                    "dot1q": sap.group(2) if sap else None
                                }
                        interfaces_mwrot.append({
                            "interface": interface,
                            "ip": ip.group(1) if ip else None,
                            "descricao": descricao_logica.group(1) if descricao_logica else None,
                            "porta": porta_logica.group(1) if porta_logica else (f"lag-{lag}" if lag else None),                            
                            "dot1q": porta_logica.group(2) if porta_logica else (lag_logico.group(2) if lag_logico else None),
                            "gerencia": gerencia_mwrot,
                            "bfd": bfd_exists
                        })
            
                mwrot.append({
                    "porta": porta.group(1) if porta else None,
                    "descricao": descricao.group(1),
                    "speed": speed.group(1) if speed else "10000",
                    "bandwidth": bandwidth.group(1) if bandwidth else None,
                    "bnm_ativo": bnm_ativo,
                    "interfaces": interfaces_mwrot,
                    "lag": lag
                })          
# EDD
            elif descricao and "UNI" in descricao.group(1) and ("EDD" in descricao.group(1) or "EoMPLS" in descricao.group(1)):
                porta = re.search(r'^\s*port\s+(\d+/\d+/\d+)', bloco, re.MULTILINE)
                speed = re.search(r'\s*speed\s+(\S+)', bloco)
                mtu = re.search(r'mtu\s+(\d+)', bloco)
                if not porta:
                    continue
            
                item_edd = {
                    "porta": porta.group(1),
                    "descricao": descricao.group(1),
                    "speed": speed.group(1) if speed else None,
                    "mtu": mtu.group(1) if mtu else None,
                    "epipe": [],
                    "gerencia": None
                }
                empresarial.append(item_edd)     
# GERÊNCIA L3 — busca no segundo bloco vprn
                blocos_vprn_edd = re.findall(rf'^(?: {{8}}|\t{{2}})vprn {bgp["ddd"]}7281\b.*?^(?: {{8}}|\t{{2}})exit\b',backup,re.DOTALL | re.MULTILINE)
                if blocos_vprn_edd:
                    
                    bloco_gerencia = blocos_vprn_edd[1]
            
                    interfaces_gerencia = re.findall(r'^(?: {12}|\t{3})interface\s+".+?"\s+create.*?^(?: {12}|\t{3})exit\b', bloco_gerencia, re.DOTALL | re.MULTILINE)
            
                    for interface_bloco in interfaces_gerencia:
                        porta_match = re.search(r'sap\s+(\d+/\d+/\d+):(\d+)', interface_bloco)
                        descricao_g = re.search(r'description\s+"([^"]+)"', interface_bloco)
                        ip = re.search(r'address\s+(\S+)', interface_bloco)
                       
                        if not porta_match:
                            continue
            
                        if porta_match.group(1) == porta.group(1):
                            item_edd["gerencia"] = { 
                                "porta": porta_match.group(1),
                                "descricao": descricao_g.group(1) if descricao_g else None,
                                "ip": ip.group(1) if ip else None,
                                "dot1q": porta_match.group(2)
                            }
# SERVIÇOS EPIPE EMPRESARIAL
                blocos_epipe = re.findall(r'^(?: {8}|\t{2})epipe\s+\d+\s+name\s+".*?".*?^(?: {8}|\t{2})exit\b', backup, re.DOTALL | re.MULTILINE)
            
                for bloco_epipe in blocos_epipe:
                    porta_match = re.search(r'sap\s+(\d+/\d+/\d+):(\d+)(?:\.(\d+))?', interface_bloco)
                    if not porta_match or porta_match.group(1) != porta.group(1):
                        continue
                    epipe_match = re.search(r'epipe\s+(\d+)', bloco_epipe)
                    descricao_match = re.search(r'name\s+"([^"]+)"', bloco_epipe)
                    mtu_match = re.search(r'service-mtu\s+(\d+)', bloco_epipe)
                    sdp_match = re.search(r'spoke-sdp\s+(\d+):\d+', bloco_epipe)
                    velocidade_match = re.search(r'aggregate-policer-rate\s+(\d+)', bloco_epipe)
                
#PROCURA BLOCO SDP
                    descricao_sdp, ip_sdp = None, None
                    if sdp_match:
                        blocos_sdp = re.findall(rf'^(?: {{8}}|\t{{2}})sdp {sdp_match.group(1)} .*?^(?: {{8}}|\t{{2}})exit\b',backup,re.DOTALL | re.MULTILINE)
                        for bloco_sdp in blocos_sdp:
                            desc_match = re.search(r'description\s+"([^"]+)"', bloco_sdp)
                            ip_match   = re.search(r'far-end\s+([\d\.]+)', bloco_sdp)
                            descricao_sdp = desc_match.group(1) if desc_match else None
                            ip_sdp        = ip_match.group(1) if ip_match else None
                
                    item_edd["epipe"].append({
                        "epipe": epipe_match.group(1) if epipe_match else None,
                        "descricao": descricao_match.group(1) if descricao_match else None,
                        "porta": porta_match.group(1),
                        "vlan": porta_match.group(2),
                        "vlan2": porta_match.group(3),
                        "mtu": mtu_match.group(1) if mtu_match else None,
                        "sdp": sdp_match.group(1) if sdp_match else None,
                        "velocidade": velocidade_match.group(1) if velocidade_match else None,
                        "descricao_sdp": descricao_sdp,
                        "ip_sdp": ip_sdp
                    })

# BATERIA
            elif descricao and "UNI" in descricao.group(1) and ("LITIO" in descricao.group(1) or "FONTE" in descricao.group(1) or "PWR" in descricao.group(1)):
                porta = re.search(r'^\s*port\s+(\d+/\d+/\d+)', bloco, re.MULTILINE)
                speed = re.search(r'\s*speed\s+(\S+)', bloco)
                
                for interface_gerencia in blocos_int_gerencia:
                    if porta and porta.group(1) in interface_gerencia:
                        description_gerencia = re.search(r'description\s+"([^"]+)"', interface_gerencia)
                        ip_gerencia = re.search(r'address\s+(\d{1,3}(?:\.\d{1,3}){3}/\d+)', interface_gerencia)
                        sap = re.search(r'sap\s+(\d+/\d+/\d+):(\d+)', interface_gerencia)
                        interface_nome = re.search(r'interface\s+"([^"]+)"', interface_gerencia)
                    
                        gerencia_bateria = {
                            "interface": interface_nome.group(1) if interface_nome else None,
                            "descricao": description_gerencia.group(1) if description_gerencia else None,
                            "ip": ip_gerencia.group(1) if ip_gerencia else None,
                            "porta": sap.group(1) if sap else None,
                            "dot1q": sap.group(2) if sap else None
                        }
                bateria.append({
                            "descricao": descricao.group(1) if descricao else None,                            
                            "porta": porta.group(1) if porta else None,
                            "speed": speed.group(1) if speed else None,
                            "gerencia": gerencia_bateria
                })
                
    resultado["fibra"] = fibra
    resultado["mwrot"] = mwrot
    resultado["bateria"] = bateria
    resultado["empresarial"] = empresarial

# MOVEL
    lista_interfaces_Movel = []

# Percorre apenas VPRNs móveis (exclui GERENCIA = 61)
    for servico, vprn in [item for item in vprns if item[1] != 61]:
        blocos_vprn = re.findall(rf'(?m)^\s*vprn\s+{bgp.get("ddd","")}{vprn}\b[\s\S]*?^\s*exit\b',backup)
        if not blocos_vprn:
            continue
    
        # Itera sobre todos os blocos encontrados (não usa índice fixo [1])
        for bloco_vprn in blocos_vprn:
            blocos_int_movel = re.findall(r'(?m)^\s*interface\s+".+?"\s+create[\s\S]*?^\s*exit\b',bloco_vprn)
            for interface_bloco in blocos_int_movel:
                porta_logica = re.search(r'sap\s+(\d+/\d+/\d+):(\d+)', interface_bloco)
                if porta_logica:  # só adiciona se encontrou
                    lista_interfaces_Movel.append(porta_logica.group(1))

#Removendo as portas duplicadas
    lista_interfaces_Movel = list(dict.fromkeys(lista_interfaces_Movel))
    
    for porta in lista_interfaces_Movel:
        interfaces_movel = []
        for bloco in portas:
            if re.search(rf'^ {{4}}port {re.escape(porta)}\b', bloco, re.MULTILINE):
                descricao = re.search(r'\s*description\s+"([^"]+)"', bloco)
                porta_fisica = re.search(r'^\s*port\s+(\d+/\d+/\d+)', bloco, re.MULTILINE)
                speed = re.search(r'\s*speed\s+(\S+)', bloco)
        
# Todas vrfs incluindo gerencia para identificar todos os serviços
        for servico, vprn in vprns:       
            blocos_vprn = re.findall(rf'^(?: {{8}}|\t{{2}})vprn {bgp["ddd"]}{vprn}\b.*?^(?: {{8}}|\t{{2}})exit\b', backup,re.DOTALL | re.MULTILINE)
            if not blocos_vprn:
                continue
            blocos_int_movel = re.findall(r'^(?: {12}|\t{3})interface\s+".+?"\s+create.*?^(?: {12}|\t{3})exit\b', blocos_vprn[1], re.DOTALL | re.MULTILINE)                    
            
            for interface_bloco in blocos_int_movel:
                
                if re.search(rf'^ {{16}}sap {re.escape(porta)}:\d+\b', interface_bloco, re.MULTILINE):
                    interface = re.search(r'^(?: {12}|\t{3})interface\s+"(.+?)"\s+create', interface_bloco)
                    description = re.search(r'(?: {16}|\t{4})description\s+"(.+?)"', interface_bloco)                        
                    ip = re.search(r'address\s+(\d{1,3}(?:\.\d{1,3}){3}/\d+)', interface_bloco)
                    porta_logica_all = re.search(r'sap\s+(\d+/\d+/\d+):(\d+)', interface_bloco)                    
                    dhcp = re.search(r'server\s+(\d{1,3}(?:\.\d{1,3}){3})', interface_bloco)             
                    tipo_servico = servico
                    
                    interfaces_movel.append({
                        "interface": interface.group(1) if interface else None,
                        "description": description.group(1) if description else None,
                        "porta": porta_logica_all.group(1) if porta_logica_all else None,
                        "dot1q": porta_logica_all.group(2) if porta_logica_all else None,
                        "ip": ip.group(1) if ip else None,
                        "dhcp": dhcp.group(1) if dhcp else None,
                        "vprn": f'{vprn}',
                        "tipo_servico": servico
                    })                
                                
        movel.append({
            "porta": porta_fisica.group(1) if porta_fisica else None,
            "descricao": descricao.group(1) if descricao else None,
            "speed": speed.group(1) if speed else "10000",
            "interfaces_movel": interfaces_movel
        })
    resultado["movel"] = movel
    

#ROTAS ESTÁTICAS
    rotas_estaticas = []
    
# Captura blocos das VPRNs desejadas
    vprn_blocos = re.findall(r'(?ms)^(?: {8}|\t{2})vprn\s+\d{2}(61|103|1|95)\s+name\s+"[^"]+"\s+customer\s+\d+\s+create([\s\S]*?^(?: {8}|\t{2})exit\b)',backup)
    for vrf_numero, bloco in vprn_blocos:
        rotas_static = re.findall(r'(?s)static-route-entry\s+(\d{1,3}(?:\.\d{1,3}){3})/(\d+).*?next-hop\s+(\d{1,3}(?:\.\d{1,3}){3})', bloco)
        for ip_origem, mask, ip_destino in rotas_static:
            nome_vprn = next((nome for nome, num in vprns if str(num) == vrf_numero), None)
            rotas_estaticas.append({
                "vrf_nome": nome_vprn,
                "vrf_numero": vrf_numero,
                "ip_origem": ip_origem,
                "mask": mask,
                "ip_destino": ip_destino
            })
    resultado["rotas_estaticas"] = rotas_estaticas
    
#    print(f"Hostname: {resultado['hostname']}")
#    print(f"Loopback100: {resultado['loopback100']}")
#    print(f"Area OSPF: {resultado['area_formatada']}")
#    print(f"NTP: {resultado["ntp"]}")
#    print(f"Processo     : {bgp['processo']}")
#    print(resultado["bgp"]["community"])
#    print(f"Vizinhos     : {', '.join([f"{neighbor_ip} - {neighbor}" for neighbor_ip, neighbor in bgp["neighbors"]]) if bgp["neighbors"] else '-'}")
#    print(f"Communities  : {', '.join([f"{community} - {members}" for community, members in bgp["community"]]) if bgp["community"] else '-'}")
#    print(f"Policies     : {', '.join(bgp['policy']) if bgp['policy'] else '-'}")
#    for rmc, ip in resultado["saa"]:
#        print("RMC:", rmc)
#        print("IP:", ip)
#    for ip in twamp:
#        print(f"TWAMP - {ip}")
#
#    print("\n=== PTP Sync-E ===")
#    if resultado["ptp"]:
#        for i, porta in enumerate(resultado["ptp"], start=1):
#            print(f"Ref{i} -> Porta: {porta}")
#    else:
#        print("Nenhuma porta PTP encontrada.")
#
##NNI FO
#    for item in fibra:
#        print("\n=== Interface Física FO ===")
#        print(f"Porta        : {item['porta']}")
#        print(f"Descrição    : {item['descricao']}")
#        print(f"Speed        : {item['speed'] if item['speed'] else '-'}")
#        print(f"LAG          : {item['lag']}")
#        
#        
## Interface Lógica NNI FO (router interface)
#        print(f"portas vinculadas: {len(item["interfaces"])}")
#        for interface in item["interfaces"]:
#            print(f"Nome         : {interface['interface']}")
#            print(f"IP           : {interface['ip']}")
#            print(f"Descrição    : {interface['descricao']}")
#            print(f"Porta        : {interface['porta']}")
#            print(f"Vlan         : {interface['dot1q']}")
#            
##MWROT              
#    for item in mwrot:
#        print("\n=== Interface Física MWROT ===")
#        print(f"Porta        : {item['porta']}")
#        print(f"Descrição    : {item['descricao']}")
#        print(f"Speed        : {item['speed']}")
#        print(f"Bandwidth    : {item['bandwidth']}")
#        print(f"BNM          : {item['bnm_ativo']}")
#        print(f"LAG          : {item['lag']}")
#        
#        for interface in item["interfaces"]:
#            print(f"Porta        : {interface['porta']}")
#            print(f"Nome         : {interface['interface']}")
#            print(f"IP           : {interface['ip']}")
#            print(f"Descrição    : {interface['descricao']}")
#            print(f"Vlan         : {interface['dot1q']}")                                  
#            if interface.get("gerencia"):
#                print(f"Interface    : {interface['gerencia']['interface']}")
#                print(f"Porta        : {interface['gerencia']['porta']}")
#                print(f"Descrição    : {interface['gerencia']['descricao']}")
#                print(f"IP           : {interface['gerencia']['ip']}")
#                print(f"Vlan         : {interface['gerencia']['dot1q']}")
#                
#    
##MOVEL
#    for item in movel:
#        print("\n=== Interface Física UNI MOVEL ===")
#        print(f"Porta        : {item['porta']}")
#        print(f"Descrição    : {item['descricao']}")
#        print(f"Speed        : {item['speed'] if item['speed'] else '-'}")
#
#        for interface in item["interfaces_movel"]:
#            print(f"Serviço : {interface['tipo_servico']}")  
#            print(f"Descrição    : {interface['description']}")
#            print(f"IP           : {interface['ip']}")
#            print(f"Porta Física : {interface['porta']}")
#            print(f"Vlan         : {interface['dot1q']}")            
#            print(f"VRF          : {interface['vprn']}")
#            
#            if "dhcp" in interface:
#                print(f"DHCP         : {interface['dhcp']}")
##Bateria
#    for item in bateria:
#        print("\n=== UNI Bateria ===")
#        print(f"Porta        : {item['porta']}")
#        print(f"Descrição    : {item['descricao']}")
#        print(f"Speed        : {item['speed'] if item['speed'] else '-'}")
#
#        if item.get("gerencia"):
#                print(f"Interface    : {item['gerencia']['interface']}")
#                print(f"Porta        : {item['gerencia']['porta']}")
#                print(f"Descrição    : {item['gerencia']['descricao']}")
#                print(f"IP           : {item['gerencia']['ip']}")
#                print(f"Vlan         : {item['gerencia']['dot1q']}")
#
## EDD
#    for item in empresarial:
#        print("\n=== Interface Física UNI EDD ===")
#        print(f"Porta        : {item['porta']}")
#        print(f"Descrição    : {item['descricao']}")
#        print(f"Speed        : {item['speed'] if item['speed'] else '-'}")
#        print(f"MTU          : {item['mtu'] if item['speed'] else '-'}")
#        
#        if item["gerencia"]:
#            print(f"\n--- Gerência L3 ---")
#            print(f"Porta        : {item['gerencia']['porta']}")
#            print(f"Descrição    : {item['gerencia']['descricao']}")
#            print(f"IP           : {item['gerencia']['ip']}")
#            print(f"Vlan         : {item['gerencia']['dot1q']}")
#            
#        if item["epipe"]:
#            for ep in item["epipe"]:
#                print(f"\n--- Serviço ---")
#                print(f"Porta        : {ep['porta']}")
#                print(f"PW           : {ep['epipe']}")
#                print(f"Descrição    : {ep['descricao']}")
#                print(f"MTU          : {ep['mtu']}")
#                print(f"Vlan         : {ep['vlan']}")
#                print(f"Velocidade   : {ep['velocidade'] if ep['velocidade'] else '-'}")
#                print(f"SDP          : {ep['sdp'] if ep['sdp'] else '-'}")
#                print(f"Desc SDP     : {ep['descricao_sdp'] if ep['descricao_sdp'] else '-'}")
#                print(f"IP SDP       : {ep['ip_sdp'] if ep['ip_sdp'] else '-'}")
#
#
##ROUTER STATIC
#print(f"\n[RESUMO] Total de rotas estáticas: {len(rotas_estaticas)}")
#    for r in rotas_estaticas:
#        print(f'- VPRN {r["vrf_numero"]} ({r["vrf_nome"]}): {r["ip_origem"]}/{r["mask"]} -> {r["ip_destino"]}')
#
    return resultado

