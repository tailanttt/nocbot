import re
import time
from netmiko import ConnectHandler

def normaliza_iface(nome):
    # Converte para formato aceito no modo sys
    if nome.startswith("100GE"):
        return nome.replace("100GE", "100G", 1)
    nome = nome.replace("GigabitEthernet", "G")
    nome = nome.replace("25GigabitEthernet", "25G")
    if nome.startswith("GE"):
        nome = nome.replace("GE", "G", 1)
    if nome.startswith("25GE"):
        nome = nome.replace("25GE", "25G", 1)
    return nome

def is_radio_iface(net_connect, iface):
    """Verifica se a interface é via rádio pelo campo description"""
    output = net_connect.send_command(f"display current-configuration interface {iface}")
    desc_match = re.search(r"description\s+(.*)", output)
    if desc_match:
        desc = desc_match.group(1).upper()
        if any(tag in desc for tag in ["RADIO", "MW", "MW-ROT"]):
            return True
    return False

def coletar_dados(ip, username, password):
    device = {
        "device_type": "huawei",
        "ip": ip,
        "username": username,
        "password": password,
        "fast_cli": True,
        "session_log": "saida.log"
    }
    net_connect = ConnectHandler(**device)

    # 1. Captura todos os peers BGP em Established
    bgp_output = net_connect.send_command("display bgp peer")
    bgp_peers = re.findall(r"(\d+\.\d+\.\d+\.\d+).*?Established", bgp_output)
    print("\n=== Cabeças BGP (Established) ===")
    print(bgp_peers)

    if not bgp_peers:
        print("Nenhum peer BGP em Established.")
        net_connect.disconnect()
        return

    # 2. Descobre cabeça mais próximo via traceroute
    hops = {}
    for peer in bgp_peers:
        net_connect.write_channel(f"tracert -w 1000 -q 1 -m 10 {peer}\n")
        tracert_out, start = "", time.time()
    
        while time.time() - start < 5:  # limite de 5s
            time.sleep(0.5)
            chunk = net_connect.read_channel()
            if chunk:
                tracert_out += chunk
                if "*" in chunk:  # aborta no primeiro '*'
                    net_connect.write_channel("\x03")
                    tracert_out += net_connect.read_channel()
                    break
            if net_connect.base_prompt in chunk:  # comando terminou
                break
    
        linhas = tracert_out.splitlines()
        saida_filtrada = []
        for linha in linhas:
            saida_filtrada.append(linha)
            if "*" in linha:
                break
    
        qtd = len(re.findall(r"^\s*\d+\s", "\n".join(saida_filtrada), re.MULTILINE))
        hops[peer] = qtd if qtd else 9999
    
    menor = min(hops.values())
    cabeca_proximo = [p for p, h in hops.items() if h == menor][0]
    
    print("\n=== Hops por peer ===")
    for p, h in hops.items():
        print(f"{p}: {h} hops")
    print(f"Cabeça mais próximo: {cabeca_proximo}")
    
    # 3. Interfaces OSPF Full
    ospf_output = net_connect.send_command("display ospf peer brief")
    ospf_full = [normaliza_iface(x) for x in re.findall(r"\s+(\S+)\s+\S+\s+Full", ospf_output)]

    # 4. Filtra interfaces via rádio
    ospf_filtradas = []
    for iface in ospf_full:
        if not is_radio_iface(net_connect, iface):
            ospf_filtradas.append(iface)

    print("\n=== Interfaces OSPF Full (sem rádio) ===")
    print(ospf_filtradas)

    principais = []
    backups = []
    ordem_final = []

    # 5. Ordem das Interfaces
    if len(ospf_filtradas) == 2:
        rt_verbose = net_connect.send_command(f"display ip routing-table {cabeca_proximo} verbose")
        interfaces = [normaliza_iface(x) for x in re.findall(r"Interface:\s+(\S+)", rt_verbose)]
        if interfaces:
            iface1 = interfaces[0]
            principais.append(iface1)
            iface2 = ospf_filtradas[0] if ospf_filtradas[1] == iface1 else ospf_filtradas[1]
            backups.append(iface2)
        ordem_final = principais + backups
        print("\n=== Ordem das Interfaces (2 OSPF Full) ===")
        for idx, iface in enumerate(ordem_final, start=1):
            print(f"{idx}ª: {iface}")

    elif len(ospf_filtradas) == 3:
        for peer in bgp_peers:
            rt_verbose = net_connect.send_command(f"display ip routing-table {peer} verbose")
            interfaces = [normaliza_iface(x) for x in re.findall(r"Interface:\s+(\S+)", rt_verbose)]
            if interfaces:
                principais.append(interfaces[0])
                if len(interfaces) > 1:
                    backups.append(interfaces[1])
        ordem_final = []
        if principais:
            ordem_final.append(principais[0])
        if backups:
            ordem_final.append(backups[0])
        interface_3 = [iface for iface in ospf_filtradas if iface not in principais and iface not in backups]
        if interface_3:
            ordem_final.append(interface_3[0])
        print("\n=== Ordem das Interfaces (3 OSPF Full) ===")
        for idx, iface in enumerate(ordem_final, start=1):
            print(f"{idx}ª: {iface}")

    elif len(ospf_filtradas) > 3:
        for peer in bgp_peers:
            rt_verbose = net_connect.send_command(f"display ip routing-table {peer} verbose")
            interfaces = [normaliza_iface(x) for x in re.findall(r"Interface:\s+(\S+)", rt_verbose)]
            if interfaces:
                principais.append(interfaces[0])
                if len(interfaces) > 1:
                    backups.append(interfaces[1])

        exclui = "|".join(["Loop", *principais, *backups])
        ospf_int = net_connect.send_command(f"display ospf interface | exclude {exclui}")
        custos = re.findall(r"^(?:\s*)(\S+)\s+\S+\s+\S+\s+\S+\s+(\d+)", ospf_int, re.MULTILINE)
        custos_ordenados = sorted(custos, key=lambda x: int(x[1]))
        ordem_final = principais + backups + [normaliza_iface(iface) for iface, _ in custos_ordenados]
        print("\n=== Ordem das Interfaces (>3 OSPF Full) ===")
        for idx, iface in enumerate(ordem_final, start=1):
            print(f"{idx}ª: {iface}")

    else:
        if ospf_filtradas:
            ordem_final = [ospf_filtradas[0]]
            print("\nMenos de 2 OSPF Full — sem ordenação especial.")
            print(f"1ª: {ospf_filtradas[0]}")

    # 6. Interfaces 4G/5G (ARP S1)
    arp_s1 = net_connect.send_command("display arp vpn-instance S1")
    arp_ifaces = [normaliza_iface(x) for x in re.findall(r"(GE\d+/\d+/\d+(?:\.\d+)?|25G\d+/\d+/\d+(?:\.\d+)?)", arp_s1)]
    arp_fisicas = list({iface.split('.')[0] for iface in arp_ifaces})
    print("\n=== Interfaces 4G/5G (ARP S1) ===")
    print(arp_fisicas)

    # 7. Gerar o Script do Sync-e
    script = f"""
system-view
clock ssm-control on
clock wtr 0
clock ethernet-synchronization enable
undo ptp-adaptive acr
clock source ptp priority 100
clock source ptp synchronization enable
clock source ptp ssm prc
ptp profile g-8275-1 enable
ptp enable
ptp device-type t-bc
ptp asymmetry-measure enable
ptp domain 24"""
    vistas = set()
    nni_unicas = []
    for iface in ordem_final:
        if iface not in vistas:
            nni_unicas.append(iface)
            vistas.add(iface)

    for idx, iface in enumerate(nni_unicas, start=1):
        prioridade = idx * 10
        script += f"""
interface {iface}
clock synchronization enable
clock priority {prioridade}
ptp notslave disable
ptp enable
quit"""
    for iface in arp_fisicas:
        script += f"""
interface {iface}
clock synchronization enable
clock priority 255
ptp enable
quit"""

    script +="""
commit
return
save
display ptp all
display clock source
"""
    net_connect.disconnect()
    return script