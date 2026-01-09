def gerar_script(
    hostname,
    ip_loopback,
    uf,
    site,
    ntp_ips,
    ptp_ips,
    processo_ospf,
    area_ospf_formatada,
    bgp,
    rotas_estaticas,
    fibra,
    mwrot,
    movel,
    bateria,
    empresarial,
):
    portas_fo = []
    portas_mwrot = []
    portas_movel = []
    portas_edd = []
    portas_bateria = []
    # Variáveis globais de portas
    portas10 = [
    'GigabitEthernet 0/2/0',
    'GigabitEthernet 0/2/1',
    'GigabitEthernet 0/2/2',
    'GigabitEthernet 0/2/3',
    'GigabitEthernet 0/2/4',
    'GigabitEthernet 0/2/6',
    'GigabitEthernet 0/2/7',
    'GigabitEthernet 0/2/8',
    'GigabitEthernet 0/2/9',
    'GigabitEthernet 0/2/10',
    'GigabitEthernet 0/2/11',
    'GigabitEthernet 0/2/12',
    'GigabitEthernet 0/2/13',
    'GigabitEthernet 0/2/15',
    'GigabitEthernet 0/2/16',
    'GigabitEthernet 0/2/17',
    'GigabitEthernet 0/2/18',
    'GigabitEthernet 0/2/19',
    'GigabitEthernet 0/2/20',
    'GigabitEthernet 0/2/21',
    'GigabitEthernet 0/2/22',
    'GigabitEthernet 0/2/23']
    portas100 = ['100GE0/2/24','100GE0/2/25']
    
    banner = (
        "*****************************ATENCAO**********************************\n"
        "*                                                                    *\n"
        "* EQUIPAMENTO DE ACESSO RESTRITO. SOMENTE PESSOAL AUTORIZADO.        *\n"
        "* QUALQUER TENTATIVA DE ACESSO NAO AUTORIZADO OU INDEVIDO, PODERA    *\n"
        "* SER OBJETO DE PROCESSO                                             *\n"
        "* TODOS OS ACESSOS ESTAO SENDO MONITORADOS E AUDITADOS E TODAS AS    *\n"
        "* INFORMACOES COLETADAS SAO DE PROPRIEDADE DA CLARO.                 *\n"
        "*                                                                    *\n"
        "**********************************************************************\n"
        "*\n"
        "****************************ATENTION**********************************\n"
        "*                                                                    *\n"
        "* RESTRICTED ACCESS EQUIPMENT. ONLY PERSONAL AUTHORIZED.             *\n"
        "* ANY ATTEMPT OF NOT AUTHORIZED OR IMPROPER ACCESS, CAN BE           *\n"
        "* PROCESS OBJECT.                                                    *\n"
        "* ALL ACCESSES ARE BEING MONITORED AND AUDITED AND ALL COLLECTED     *\n"
        "* INFORMATION ARE PROPERTY OF CLARO.                                 *\n"
        "*                                                                    *\n"
        "*********************************************************************\n"
    )
#    with open("scripts/banner.txt", 'w', encoding='utf-8') as arquivo:
#        arquivo.write(banner)
    
    def centralizar(texto):
        return f"*{texto.center(48)}*\n"

    linha1 = f"VOCE ESTA EM : {hostname}"
    linha2 = f"{uf} . {site} . {uf}{site}"

    banner_roteador = (
        "**************************************************\n"
        "*                                                *\n"
        + centralizar(linha1)
        + centralizar(linha2)
        + "*                                                *\n"
        "**************************************************\n"
    )
    
#    with open(f"scripts/{hostname}_banner.txt", 'w', encoding='utf-8') as arquivo:
#        arquivo.write(banner_roteador)
    script = f"""#
# ========================================
# RESET DE FABRICA
# =======================================
#
reset saved-configuration
startup system software
#
# ========================================
# ABERTURA DE CAIXA NA REDE
# =======================================
#
system
stelnet server enable
telnet server enable
commit
aaa
user-password password-force-change disable
local-user suporte password irreversible-cipher claro123
local-user suporte service-type terminal telnet ssh
local-user suporte level 3
local-user suporte state block fail-times 3 interval 5
local-user suporte ftp-directory cfcard:/
local-user suporte user-group manage-ug
commit
stelnet server-source all-interface
telnet server-source all-interface
user-interface vty 0 20
acl ACL_OPERADOR inbound
undo acl inbound
protocol inbound all
commit
#
# ========================================
# HABILITAR FTP
# =======================================
#
system-view
aaa
local-user root service-type ftp terminal telnet ssh
local-user root state block fail-times 3 interval 5
local-user root user-group manage-ug
local-user root ftp-directory cfcard:/
commit
sftp server enable
ftp server enable
ftp server-source all
y
ssh user root service-type all
ssh user root service-type snetconf stelnet sftp
commit
!
# ========================================
# TROCA DO IP DA PORTA ETHERNET
# =======================================
#
interface Ethernet0/0/0
undo shutdown
ip binding vpn-instance __LOCAL_OAM_VPN__
ipv6 enable
ip address 192.168.0.1 255.255.255.0
ipv6 address auto link-local
#
# ========================================
# ATIVAR A LICENÇA
# =======================================
display esn
license active XXXXXXXXXXXXXXXXXXXX.xml
display license
#
# ========================================
# UPDATE PATCH
# =======================================
#
startup patch cfcard:/XXXXXXXXXXXXXXXXXXXXXXXXXX.PAT all
#
# ========================================
# BANNER
# ========================================
#
header login file cfcard:/banner.txt
header shell file cfcard:/{hostname}_Banner.txt
#
#========================================
# SCRIPT DE CONFIGURAÇÃO HUAWEI ATN910D_A_464
#========================================
#
system-view
#
sysname {hostname}
#
multicast routing-enable
#
#========================================
# LOOPBACK GERENCIA
#========================================
interface LoopBack100
description Loopback de Roteamento
ip address {ip_loopback} 255.255.255.255
pim sm
undo shutdown
#
#========================================
# ABRIR ACESSO FTP TELNET
#========================================
bfd
#
cfm enable
#
dhcp server request-packet all-interface disable
#
diffserv domain default
#
dns domain ipran.claro.com.br
#
dot1x-template 1
#
host-packet type management-protocol dscp 48
#
interface NULL0
#
lldp enable
#
local-aaa-server
#
loop-detect trigger enable
#
mpls ldp-srbe convergence enhance
#
pki domain default
#
priority-template default
#
security password
rule admin
forbidden word changeme_123
#
set flow-stat interval 30
#
set inactive-port shutdown
Y
#
soc
#
snetconf server enable
#
telnet server enable
#
stelnet server enable
#
timestamp enable
#
undo dcn
Y
#
undo FTP server
Y
#
undo FTP server-source all-interface
Y
#
undo FTP ipv6 server-source all-interface
#
undo icmp name timestamp-reply send
#
undo pnp enable
#
undo set save-configuration
#
telnet server-source all-interface
y
#
user-interface vty 0 20
undo acl inbound
undo authentication-mode
protocol inbound all
#
undo user-security-policy enable
#
netconf
activate module huawei-ip
#
sftp server enable
#
sftp client-source -i LoopBack100
#
sftp server default-directory cfcard:
#
#========================================
# ATIVAÇÃO DAS PORTAS
#========================================
interface 25GE 0/2/20
shutdown
interface 25GE 0/2/21
shutdown
interface 25GE 0/2/22
shutdown
interface 25GE 0/2/23
shutdown
#
set service-mode card-bandwidth-mode eth-2x100ge-20x10gf-4xgf-mode slot 2
Y
#
license
active port-basic slot 2 port 14-23
active port-service-enhance slot 2 port 14-23
active port-mode-channel slot 2 port 14-23
#
#========================================
# DESATIVANDO TODAS AS PORTAS
#========================================
interface Gi0/2/0
shutdown
quit
interface Gi0/2/1
shutdown
quit
interface Gi0/2/2
shutdown
quit
interface Gi0/2/3
shutdown
quit
interface Gi0/2/4
shutdown
port-mode 1GE
y
quit
interface Gi0/2/5
shutdown
port-mode 1GE
y
quit
interface Gi0/2/6
shutdown
port-mode 1GE
y
quit
interface Gi0/2/7
shutdown
port-mode 1GE
y
quit
interface Gi0/2/8
shutdown
port-mode 1GE
y
quit
interface Gi0/2/9
shutdown
port-mode 1GE
y
quit
interface Gi0/2/10
shutdown
port-mode 1GE
y
quit
interface Gi0/2/11
shutdown
port-mode 1GE
y
quit
interface Gi0/2/12
shutdown
port-mode 1GE
y
quit
interface Gi0/2/13
shutdown
port-mode 1GE
y
quit
interface Gi0/2/14
shutdown
quit
interface Gi0/2/15
shutdown
quit
interface Gi0/2/16
shutdown
quit
interface Gi0/2/17
shutdown
quit
interface Gi0/2/18
shutdown
quit
interface Gi0/2/19
shutdown
quit
interface Gi0/2/20
shutdown
quit
interface Gi0/2/21
shutdown
quit
interface Gi0/2/22
shutdown
quit
interface Gi0/2/23
shutdown
quit
interface 100GE0/2/24
shutdown
quit
interface 100GE0/2/25
shutdown
quit
#
#========================================
# NETSTREAM
#========================================
ip netstream as-mode 32
ip netstream timeout active interval-second 15
ip netstream timeout inactive 5
ip netstream tcp-flag enable
ip netstream export version 9 origin-as
ip netstream export index-switch 32
ip netstream export template timeout-rate 1
ip netstream sampler fix-packets 1000 inbound
ip netstream sampler fix-packets 1000 outbound
ip netstream export source {ip_loopback}
#
#========================================
# NTP
#========================================
clock timezone BR minus 03:00:00
#
acl name NTP basic"""
    if hostname.startswith("RJ"):
        script += """
rule 10 name Server_NTP_RMS_2 permit source 10.120.7.0 0.0.0.255
rule 20 name Server_NTP_RMS_3 permit source 10.120.97.0 0.0.0.255
rule 30 name Server_NTP_RMS_4 permit source 10.123.7.0 0.0.0.255
rule 40 name Server_NTP_RMS_5 permit source 10.125.7.0 0.0.0.255
rule 50 name Server_NTP_RMS_6 permit source 10.128.7.0 0.0.0.255
rule 60 name Server_NTP_RMS_7 permit source 10.129.97.0 0.0.0.255
rule 70 name Server_NTP_RMS_8 permit source 10.221.7.0 0.0.0.255
rule 80 name Server_NTP_RMS_9 permit source 10.221.8.0 0.0.0.255
rule 90 name Server_NTP_RMS_10 permit source 10.222.7.0 0.0.0.255
rule 100 name Server_NTP_RMS_11 permit source 10.90.1.0 0.0.0.255
rule 110 name Clientes_NTP_Roteador_12 permit source 10.204.0.0 0.0.127.255
rule 120 name Clientes_NTP_Roteador_13 permit source 10.205.0.0 0.0.127.255
rule 130 name Clientes_NTP_NodeB_14 permit source 10.204.128.0 0.0.127.255
rule 140 name Clientes_NTP_NodeB_15 permit source 10.205.128.0 0.0.127.255
rule 150 name Clientes_NTP_eNodeB_16 permit source 10.33.0.0 0.0.255.255
rule 160 name Clientes_NTP_BTS_17 permit source 10.94.0.0 0.0.255.255
rule 170 name Clientes_NTP_BTS_18 permit source 10.95.0.0 0.0.255.255
"""
    elif hostname.startswith("ES"):
        script += """
rule 10 name Server_NTP_RMS_2 permit source 10.120.7.0 0.0.0.255
rule 20 name Server_NTP_RMS_3 permit source 10.120.97.0 0.0.0.255
rule 30 name Clientes_NTP_Roteador_4 permit source 10.206.0.0 0.0.127.255
rule 40 name Clientes_NTP_NodeB_5 permit source 10.206.128.0 0.0.127.255
rule 50 name Clientes_NTP_eNodeB_6 permit source 10.38.224.0 0.0.31.255
rule 60 name Clientes_NTP_BTS_7 permit source 10.94.0.0 0.0.255.255
rule 70 name Clientes_NTP_BTS_8 permit source 10.95.0.0 0.0.255.255
"""
    elif hostname.startswith("SI"):
        script += """
rule 10 name Server_NTP_RMS_2 permit source 10.112.7.0 0.0.0.255
rule 20 name Server_NTP_RMS_3 permit source 10.112.97.0 0.0.0.255
rule 30 name Server_NTP_RMS_4 permit source 10.113.7.0 0.0.0.255
rule 40 name Server_NTP_RMS_5 permit source 10.113.8.0 0.0.0.255
rule 50 name Server_NTP_RMS_6 permit source 10.113.97.0 0.0.0.255
rule 60 name Server_NTP_RMS_7 permit source 10.114.7.0 0.0.0.255
rule 70 name Server_NTP_RMS_8 permit source 10.114.8.0 0.0.0.255
rule 80 name Server_NTP_RMS_9 permit source 10.114.97.0 0.0.0.255
rule 90 name Server_NTP_RMS_10 permit source 10.115.7.0 0.0.0.255
rule 100 name Server_NTP_RMS_11 permit source 10.115.8.0 0.0.0.255
rule 110 name Server_NTP_RMS_12 permit source 10.115.97.0 0.0.0.255
rule 120 name Server_NTP_RMS_13 permit source 10.116.7.0 0.0.0.255
rule 130 name Server_NTP_RMS_14 permit source 10.116.8.0 0.0.0.255
rule 140 name Server_NTP_RMS_15 permit source 10.116.97.0 0.0.0.255
rule 150 name Server_NTP_RMS_16 permit source 10.117.7.0 0.0.0.255
rule 160 name Server_NTP_RMS_17 permit source 10.117.97.0 0.0.0.255
rule 170 name Server_NTP_RMS_18 permit source 10.119.7.0 0.0.0.255
rule 180 name Server_NTP_RMS_19 permit source 10.119.97.0 0.0.0.255
rule 190 name Clientes_NTP_Roteador_20 permit source 10.202.0.0 0.0.127.255
rule 200 name Clientes_NTP_Roteador_21 permit source 10.203.0.0 0.0.127.255
rule 210 name Clientes_NTP_NodeB_22 permit source 10.202.128.0 0.0.127.255
rule 220 name Clientes_NTP_NodeB_23 permit source 10.203.128.0 0.0.127.255
rule 230 name Clientes_NTP_eNodeB_24 permit source 10.35.0.0 0.0.255.255
rule 240 name Clientes_NTP_BTS_25 permit source 10.94.0.0 0.0.255.255
"""
    elif hostname.startswith("SM"):
        script += """
rule 10 name Server_NTP_RMS_2 permit source 10.107.7.0 0.0.0.255
rule 20 name Server_NTP_RMS_3 permit source 10.108.97.0 0.0.0.255
rule 30 name Server_NTP_RMS_4 permit source 10.109.7.0 0.0.0.255
rule 40 name Server_NTP_RMS_5 permit source 10.109.8.0 0.0.0.255
rule 50 name Server_NTP_RMS_6 permit source 10.110.7.0 0.0.0.255
rule 60 name Clientes_NTP_Roteador_7 permit source 10.200.0.0 0.0.127.255
rule 70 name Clientes_NTP_Roteador_8 permit source 10.201.0.0 0.0.127.255
rule 80 name Clientes_NTP_NodeB_9 permit source 10.200.128.0 0.0.127.255
rule 90 name Clientes_NTP_NodeB_10 permit source 10.201.128.0 0.0.127.255
rule 100 name Clientes_NTP_eNodeB_11 permit source 10.32.0.0 0.0.255.255
rule 110 name Clientes_NTP_BTS_12 permit source 10.94.0.0 0.0.255.255
rule 120 name Clientes_NTP_BTS_13 permit source 10.95.0.0 0.0.255.255
"""
    else:
        script += """
Inserir manualemnte, pois não se enquandra aos estados de SP, ES ou RJ
"""
    script += f"""rule 10000 deny
#
#
ntp-service server disable
Y
#
ntp-service ipv6 server disable
Y
#
ntp-service server source-interface all disable
ntp-service ipv6 server source-interface all disable
ntp-service authentication enable
ntp-service authentication-keyid 6 authentication-mode md5 cipher NTP6%@backbone
ntp-service reliable authentication-keyid 6
"""
    for ip in ntp_ips:
        script += f"ntp-service unicast-server {ip} source-interface LoopBack100\n"
    script += f"""ntp-service access peer acl-name NTP
ntp-service access server acl-name NTP
ntp-service access synchronization acl-name NTP
#
#
#========================================
# PTP UNICAST
#========================================
ptp-adaptive enable
#
ptp-adaptive domain 0
#
ptp-adaptive dscp 56
#
ptp-adaptive device-type client
#
ptp-adaptive local-ip {ip_loopback}
#
ptp-adaptive request announce-interval 12
#
ptp-adaptive request sync-interval 4
#
ptp-adaptive request delay-resp-interval 6
#
ptp-adaptive acr unicast-negotiate enable
#
"""
    separador_ptp = []
    for i, ip in enumerate(ptp_ips, start=1):
        separador_ptp.append(f"ptp-adaptive remote-server{i}-ip  {ip}")

    script += "\n#\n".join(separador_ptp)
    script += f"""
#
ptp device-type oc
#
clock source ptp synchronization enable
#
clock source ptp priority 5
#
clock source ptp ssm prc
#
#
#========================================
# SNMP
#========================================
acl number 2301
description ACL SNMP OMR/Gerencia NOC-SOC/TrafIP-SLAView/NCE-IP
rule 5 permit source 192.168.32.247 0.0.0.0
rule 6 permit source 192.168.32.248 0.0.0.0
rule 7 permit source 192.168.32.249 0.0.0.0
rule 10 permit source 10.129.97.128 0.0.0.31
rule 15 permit source 10.108.198.0 0.0.0.255
rule 35 permit source 10.129.198.0 0.0.0.255
rule 40 permit source 10.221.198.0 0.0.0.255
rule 45 permit source 10.199.10.0 0.0.0.255
rule 50 permit source 10.199.26.0 0.0.0.255
rule 55 permit source 10.129.71.64 0.0.0.31
rule 60 permit source 10.108.199.0 0.0.0.255
rule 65 permit source 10.129.199.0 0.0.0.255
rule 70 permit source 10.221.199.0 0.0.0.255
rule 75 permit source 10.199.8.0 0.0.0.255
rule 80 permit source 10.199.24.0 0.0.0.255
rule 85 permit source 10.0.10.150 0.255.0.0
rule 90 permit source 10.0.10.152 0.255.0.0
rule 95 permit source 10.129.42.0 0.0.0.255
rule 100 permit source 10.129.197.0 0.0.0.31
rule 105 permit source 10.107.81.0 0.0.0.63
rule 110 permit source 10.0.198.0 0.255.0.255
rule 120 permit source 10.107.12.128 0.0.0.127
rule 125 permit source 10.107.13.0 0.0.0.127
rule 130 permit source 10.107.13.128 0.0.0.127
rule 135 permit source 10.107.81.128 0.0.0.127
rule 140 permit source 10.129.225.128 0.0.0.127
rule 145 permit source 10.129.231.128 0.0.0.127
rule 150 permit source 10.129.237.128 0.0.0.127
rule 155 permit source 10.129.239.128 0.0.0.127
rule 160 permit source 200.255.124.0 0.0.0.31
rule 165 permit source 200.255.124.192 0.0.0.63
rule 10000 deny
#
acl number 2302
description ACL Embratel
rule 5 permit source 200.255.124.0 0.0.0.31
rule 10 permit source 200.255.124.192 0.0.0.63
rule 10000 deny
#
snmp-agent
#
snmp-agent trap enable
#
snmp-agent trap source LoopBack100
#
snmp-agent sys-info version v2c v3
#
snmp-agent sys-info location {hostname}
#
snmp-agent sys-info contact deo-omr-esp.rms@claro.com.br
#
snmp-agent community complexity-check disable
#
snmp-agent community read cipher CLAROIPRAN acl 2301
#
snmp-agent community read cipher IPRAN-EBT acl 2302
#
snmp-agent community read cipher Backbone-EBT acl 2302
#
snmp-agent target-host host-name NCEIP-RJOAM trap address udp-domain 10.129.197.20 source LoopBack100 params securityname cipher CLAROIPRAN v2c
#
snmp-agent target-host host-name NCEIP-SPOMB trap address udp-domain 10.107.81.36 source LoopBack100 params securityname cipher CLAROIPRAN v2c
#
snmp-agent target-host host-name NCEIP-SDN-RJOAM trap address udp-domain 10.107.13.14 source LoopBack100 params securityname cipher CLAROIPRAN v2c
#
snmp-agent target-host host-name NCEIP-SDN-SPOMB trap address udp-domain 10.129.231.142 source LoopBack100 params securityname cipher CLAROIPRAN v2c
#
snmp-agent local-user password complexity-check disable
#
snmp-agent protocol source-status all-interface
#
undo snmp-agent protocol source-status ipv6 all-interface
#
undo snmp-agent proxy protocol source-status all-interface
#
undo snmp-agent proxy protocol source-status ipv6 all-interface
#
#
#========================================
# MPLS
#========================================
#
router id {ip_loopback}
#
mpls lsr-id {ip_loopback}
#
mpls
mpls path-mtu independent
mpls te
mpls rsvp-te
mpls te cspf
#
mpls ldp
accept target-hello all
send-message address all-loopback
mldp p2mp
Y
ipv4-family
#
mpls l2vpn
#
multicast mvpn {ip_loopback}
#
acl name ACL_MCAST_SSM basic
rule 5 permit source 239.233.0.0 0.0.0.255
rule 10 permit source 239.233.0.0 0.0.255.255
rule 10000 deny
#
pim
ssm-policy acl-name ACL_MCAST_SSM
#
#========================================
# VPN INSTANCE (VRF)
#========================================
ip vpn-instance GERENCIA
ipv4-family
route-distinguisher {bgp["processo"]}:61
apply-label per-instance
vpn-target {bgp["processo"]}:61 export-extcommunit
vpn-target {bgp["processo"]}:61 import-extcommunit
#
ip vpn-instance GERL3_EBT_CLARO
ipv4-family
route-distinguisher {bgp["processo"]}:7282
apply-label per-instance
vpn-target {bgp["processo"]}:7282 export-extcommunit
vpn-target {bgp["processo"]}:7281 import-extcommunit
#
ip vpn-instance ABIS
 ipv4-family
route-distinguisher {bgp["processo"]}:103
apply-label per-instance
vpn-target {bgp["processo"]}:103 export-extcommunit
vpn-target {bgp["processo"]}:103 import-extcommunit
#
ip vpn-instance IUB-DADOS
 ipv4-family
route-distinguisher {bgp["processo"]}:1
apply-label per-instance
vpn-target {bgp["processo"]}:1 export-extcommunit
vpn-target {bgp["processo"]}:1 import-extcommunit
#
ip vpn-instance S1
ipv4-family
route-distinguisher {bgp["processo"]}:95
apply-label per-instance
vpn-target {bgp["processo"]}:95 export-extcommunit
vpn-target {bgp["processo"]}:95 import-extcommunit
#
ip vpn-instance __LOCAL_OAM_VPN__
ipv4-family
ipv6-family
#
#"""
    if fibra:
        script += """
#========================================
# QoS NNI FIBRA
#========================================
traffic classifier PHB20_DCR operator or
if-match mpls-exp 2
if-match dscp cs2
if-match dscp af21
#
traffic classifier PHB20_DEFAULT operator or
if-match any
#
traffic classifier PHB20_GPRS operator or
if-match mpls-exp 4
if-match dscp af41
if-match dscp cs4
#
traffic classifier PHB20_MOVEL operator or
if-match mpls-exp 1
if-match dscp cs1
if-match dscp af11
#
traffic classifier PHB20_RT operator or
if-match mpls-exp 5
if-match dscp ef
if-match dscp cs5
#
traffic classifier PHB20_RT_SYNC operator or
if-match mpls-exp 7
if-match dscp cs7
#
traffic classifier PHB20_SIG operator or
if-match mpls-exp 6
if-match dscp cs6
if-match dscp 62
#
traffic classifier PHB20_VIDEO operator or
if-match mpls-exp 3
if-match dscp cs3
if-match dscp af31
#
traffic behavior PHB20_DCR
service-class af2 color green
#
traffic behavior PHB20_DEFAULT
service-class be color green
#
traffic behavior PHB20_GPRS
service-class af4 color green
#
traffic behavior PHB20_MOVEL
service-class af1 color green
#
traffic behavior PHB20_RT
service-class ef color green
#
traffic behavior PHB20_RT_SYNC
service-class cs7 color green
#
traffic behavior PHB20_SIG
service-class cs6 color green
#
traffic behavior PHB20_VIDEO
service-class af3 color green
#
traffic policy CLARO_NNI
statistics enable
classifier PHB20_SIG behavior PHB20_SIG
classifier PHB20_RT behavior PHB20_RT
classifier PHB20_RT_SYNC behavior PHB20_RT_SYNC
classifier PHB20_GPRS behavior PHB20_GPRS
classifier PHB20_VIDEO behavior PHB20_VIDEO
classifier PHB20_DCR behavior PHB20_DCR
classifier PHB20_MOVEL behavior PHB20_MOVEL
classifier PHB20_DEFAULT behavior PHB20_DEFAULT
#
port-wred NNI_PHB20_DEFAULT
queue-depth 10240
color green low-limit 50 high-limit 90 discard-percentage 100
#
#========================================
# INTERFACES NNI FIBRA
#=======================================
# NNI padrão 0/2/20 ao 23 FIBRA
"""
    for i in range(len(fibra)):
        porta_fo = portas10.pop()
        portas_fo.append(porta_fo)
        if "description_bdi" in fibra[i]:
            script += f"""interface {porta_fo}
description {fibra[i]["description"]}
mtu {fibra[i]["mtu"]}
control-flap
lldp enable
undo dcn
undo shutdown
#
interface {porta_fo}.{fibra[i]["bdi"]}
description {fibra[i]['description_bdi']}
ip address {fibra[i]['ip_address']} {fibra[i]['mask']}
pim sm
ospf authentication-mode md5 1 cipher BaCkBoNeOSPF!#@$
ospf cost {fibra[i]['ospf_cost']}
ospf network-type p2p
ospf ldp-sync
mpls
mpls mtu {fibra[i]['mtu']}
mpls te
mpls rsvp-te
mpls ldp
mpls ldp timer igp-sync-delay 5
mpls poison-reverse enable
traffic-policy CLARO_NNI inbound mpls-layer
port-queue be wfq weight 10 port-wred NNI_PHB20_DEFAULT outbound
port-queue af1 wfq weight 40 outbound
port-queue af2 wfq weight 10 outbound
port-queue af3 wfq weight 15 outbound
port-queue af4 wfq weight 10 outbound
port-queue ef pq shaping shaping-percentage 45 outbound
port-queue cs6 wfq weight 15 outbound
port-queue cs7 pq shaping shaping-percentage 5 outbound
statistic enable
undo shutdown
#
"""

        else:
            script += f"""interface {porta_fo}
description {fibra[i]['description']}
mtu {fibra[i]['mtu']}
control-flap
lldp enable
undo dcn
ip address {fibra[i]['ip_address']} {fibra[i]['mask']}
pim sm
ospf authentication-mode md5 1 cipher BaCkBoNeOSPF!#@$
ospf cost {fibra[i]['ospf_cost']}
ospf network-type p2p
ospf ldp-sync
mpls
mpls mtu {fibra[i]['mtu']}
mpls te
mpls rsvp-te
mpls ldp
mpls ldp timer igp-sync-delay 5
mpls poison-reverse enable
traffic-policy CLARO_NNI inbound mpls-layer
port-queue be wfq weight 10 port-wred NNI_PHB20_DEFAULT outbound
port-queue af1 wfq weight 40 outbound
port-queue af2 wfq weight 10 outbound
port-queue af3 wfq weight 15 outbound
port-queue af4 wfq weight 10 outbound
port-queue ef pq shaping shaping-percentage 45 outbound
port-queue cs6 wfq weight 15 outbound
port-queue cs7 pq shaping shaping-percentage 5 outbound
statistic enable
undo shutdown
#
"""
    if any(not i["bnm_ativo"] for i in mwrot):
        script += f"""#========================================
# QOS RADIO - SEM BNM
#=======================================
flow-wred NNI_MW_PHB20_DEFAULT
queue-depth 10240
color green low-limit 50 high-limit 90 discard-percentage 100
#
flow-queue CLARO_MW_NNI
queue be wfq weight 10 flow-wred NNI_MW_PHB20_DEFAULT
queue af1 wfq weight 40
queue af2 wfq weight 10
queue af3 wfq weight 15
queue af4 wfq weight 10
queue ef pq shaping shaping-percentage 45
queue cs6 wfq weight 15
queue cs7 pq shaping shaping-percentage 5
#
#========================================
# SHAPE DO RÁDIO SEM BNM
#========================================
"""
        for i in range(len(mwrot)):
            script += f"""#
qos-profile {mwrot[i]["bandwidth_mbps"]}M-MWBN
description Microwave Link {mwrot[i]["bandwidth_mbps"]}M
user-queue cir {mwrot[i]["bandwidth"]} pir {mwrot[i]["bandwidth"]} flow-queue CLARO_MW_NNI outbound
#"""


    if any(i["bnm_ativo"] for i in mwrot):
            script +=f"""
#========================================
# QOS RADIO - BNM
#=======================================
#
flow-wred NNI_MW_PHB20_BNM
queue-depth 10240
color red low-limit 50 high-limit 90 discard-percentage 100
#
flow-queue NNI_MW_PHB20_BNM
queue be wfq weight 10 flow-wred NNI_MW_PHB20_BNM
queue af1 wfq weight 40
queue af2 wfq weight 10
queue af3 wfq weight 15
queue af4 wfq weight 10
queue ef pq shaping shaping-percentage 45
queue cs6 wfq weight 15
queue cs7 pq shaping shaping-percentage 5
#
qos-profile NNI_MW_PHB20_BNM
description Microwave Link_BNM
user-queue cir-percentage 100 pir-percentage 100 flow-queue NNI_MW_PHB20_BNM
#
traffic classifier TC20_GERENCIA_RT-SYNC_IN operator or
if-match dscp cs7
if-match dscp ef
#
traffic classifier TC20_GERENCIA_DCR_IN operator or
if-match any
#
traffic behavior TC20_GERENCIA_RT-SYNC_IN
remark mpls-exp 7
service-class cs7 color green
#
traffic behavior TC20_GERENCIA_DCR_IN
remark mpls-exp 2
service-class af2 color green
#
traffic policy TC20_GERENCIA_MOVEL_IN
statistics enable
classifier TC20_GERENCIA_RT-SYNC_IN behavior TC20_GERENCIA_RT-SYNC_IN precedence 1
classifier TC20_GERENCIA_DCR_IN behavior TC20_GERENCIA_DCR_IN precedence 2
#
flow-queue TC20_GERENCIA_MOVEL_OUT
queue af2 wfq weight 100
queue cs7 pq shaping shaping-percentage 50
#
#========================================
# SHAPE DO RÁDIO BNM
#========================================
#
qos-profile TC20_GERENCIA_MOVEL_SHAPE_1G_OUT
user-queue cir-percentage 5 pir-percentage 5 flow-queue TC20_GERENCIA_MOVEL_OUT outbound
#
#
qos-profile TC20_GERENCIA_MOVEL_SHAPE_10G_OUT
user-queue cir-percentage 5 pir-percentage 5 flow-queue TC20_GERENCIA_MOVEL_OUT outbound
#"""
    if mwrot:
        script += f"""
#========================================
# INTERFACES NNI RADIO
#=======================================
#
# NNI padrão 0/2/20 E 21 FIBRA
# NO ROTEADOR IPRAN MAIS DISTANTE, NAO E NECESSARIO CONFIGURAR A SUBINTERFACE PARA A GERENCIA DO RADIO."""            
        contadorBNM = 0  # Inicializa o contador
        for x in range(len(mwrot)):
            
            porta_mwrot = portas10.pop()
            portas_mwrot.append(porta_mwrot)

#Se tiver dot1q vai adicionar o IP na logica

            if mwrot[x]["porta_logica"]:
                if mwrot[x]["porta_logica"]["bdi"] in mwrot[x]["dot1qs"]:
                    script += f"""#
interface {porta_mwrot}
description {mwrot[x]["description"]}
mtu {mwrot[x]["mtu"]}
control-flap
lldp enable
undo dcn
undo shutdown
#
interface {porta_mwrot}.{mwrot[x]["porta_logica"]["bdi"]}
description {mwrot[x]["porta_logica"]["description"]}
mtu {mwrot[x]["porta_logica"]["mtu"]}
vlan-type dot1q {mwrot[x]["porta_logica"]["bdi"]}
ip address {mwrot[x]["porta_logica"]["ip_address"]} {mwrot[x]["porta_logica"]["mask"]}
pim sm
ospf authentication-mode md5 1 cipher BaCkBoNeOSPF!#@$
ospf cost {mwrot[x]["porta_logica"]["ospf_cost"]}
ospf network-type p2p
ospf ldp-sync
mpls
mpls mtu {mwrot[x]["porta_logica"]["mtu"]}
mpls te
mpls rsvp-te
mpls ldp
mpls ldp timer igp-sync-delay 5
mpls poison-reverse enable
traffic-policy CLARO_NNI inbound mpls-layer
qos-profile { "NNI_MW_PHB20_BNM" if mwrot[x]["bnm_ativo"] else str(mwrot[x]["bandwidth_mbps"] or 10000) + "M-MWBN" } outbound
statistic enable
undo shutdown
#
"""
#Se não tiver dot1q vai adicionar o IP na fisica

                else:
                    script += f"""
interface {porta_mwrot}
description {mwrot[x]["porta_logica"]["description"]}
mtu {mwrot[x]["porta_logica"]["mtu"]}
ip address {mwrot[x]["porta_logica"]["ip_address"]} {mwrot[x]["porta_logica"]["mask"]}
pim sm
control-flap
lldp enable
undo dcn
ospf authentication-mode md5 1 cipher BaCkBoNeOSPF!#@$
ospf cost {mwrot[x]["porta_logica"]["ospf_cost"]}
ospf network-type p2p
ospf ldp-sync
mpls
mpls mtu {mwrot[x]["porta_logica"]["mtu"]}
mpls te
mpls rsvp-te
mpls ldp
mpls ldp timer igp-sync-delay 5
mpls poison-reverse enable
traffic-policy CLARO_NNI inbound mpls-layer
qos-profile { "NNI_MW_PHB20_BNM" if mwrot[x]["bnm_ativo"] else mwrot[x]["bandwidth_mbps"] + "M-MWBN" } outbound
statistic enable
undo shutdown
#
"""
            if mwrot[x]["porta_gerencia"]:
                script += f"""interface {porta_mwrot}.{mwrot[x]["porta_gerencia"]["bdi"]}
description {mwrot[x]["porta_gerencia"]["description"]}
vlan-type dot1q {mwrot[x]["porta_gerencia"]["dot1q"]}
ip address {mwrot[x]["porta_gerencia"]["ip_address"]} {mwrot[x]["porta_gerencia"]["mask"]}
ip binding vpn-instance GERENCIA
traffic-policy TC20_GERENCIA_MOVEL_IN inbound
qos-profile TC20_GERENCIA_MOVEL_SHAPE_{"10" if mwrot[x]["speed"] == "10000" else "1"}G_OUTG_OUT outbound
statistic enable
undo shutdown
#
"""
            if mwrot[x]["bnm_ativo"]:
                contadorBNM += 1 
                script += f"""#========================================
# BNM
#=======================================
cfm md md1 level 7
ma ma{contadorBNM}
{(
    f"mep mep-id {contadorBNM} interface {porta_mwrot}.{mwrot[x]['porta_logica']['bdi']} vlan {mwrot[x]['porta_logica']['bdi']} outward"
                if mwrot[x]["porta_logica"] and mwrot[x]["porta_logica"]["bdi"] in mwrot[x]["dot1qs"]
                else f"mep mep-id {contadorBNM} interface {porta_mwrot} outward"
)}
mep ccm-send mep-id {contadorBNM} enable
mep mep-id {contadorBNM} eth-bn receive enable
#
"""

    script += f"""#========================================
# OSPF
#========================================
#
ospf {processo_ospf} router-id {ip_loopback}
bfd all-interfaces enable
bfd all-interfaces min-tx-interval 100 min-rx-interval 100 frr-binding
silent-interface all
Y
"""
    for x in range(len(portas_fo)):
        script += f"""undo silent-interface {portas_fo[x]}
"""
    for x in range(len(portas_mwrot)):
        if mwrot[x]["porta_logica"]:
            mwrot[x]["porta_logica"]["bdi"] = mwrot[x]["porta_logica"]["bdi"]
            if mwrot[x]["porta_logica"]["bdi"] in mwrot[x]["dot1qs"]:
# Subinterface com dot1q
                    script += f"""undo silent-interface {portas_mwrot[x]}.{mwrot[x]["porta_logica"]["bdi"]}
"""
            else:
# Interface física (sem dot1q)
                script += f"""undo silent-interface {portas_mwrot[x]}
"""
    script += f"""opaque-capability enable
stub-router on-startup 300 external-lsa summary-lsa
bandwidth-reference 100000
maximum load-balancing 8
enable traffic-adjustment
metric-delay advertisement enable
avoid-microloop frr-protected
frr
loop-free-alternate
remote-lfa tunnel ldp
area {area_ospf_formatada}
network {ip_loopback} 0.0.0.0 description Loopback 100
"""
    for x in range(len(fibra)):
            script += f"""network {fibra[x]["ip_address"]} 0.0.0.0 description {fibra[x]["description"]}
"""

    for x in range(len(mwrot)):
        script += f"""network {mwrot[x]["porta_logica"]["ip_address"]} 0.0.0.0 description {mwrot[x]["porta_logica"]["description"]}
"""
    script += f"""mpls-te enable
#
"""
    script += f"""#========================================
# BGP
#========================================
#
ip ip-prefix FILTRA32 permit 0.0.0.0 0 greater-equal 32
#
route-policy VERIFICA-NEXTHOP permit node 10
if-match ip-prefix FILTRA32
#
route-policy MARCA-COMMUNITY-REGIAO-IPV4 permit node 10
apply community {bgp["processo"]}:{processo_ospf} additive
apply mpls-label
#
bgp {bgp["processo"]}
router-id {ip_loopback}
private-4-byte-as disable
group CSG-AGG internal
peer CSG-AGG description PEERS RRs
peer CSG-AGG connect-interface LoopBack100
peer CSG-AGG password cipher BaCkBoNeBGP!#@$"""

    for i in range(len(bgp["ips_vizinhos"])):
        script += f"""
peer {bgp["ips_vizinhos"][i]} as-number {bgp["processo"]}
peer {bgp["ips_vizinhos"][i]} group CSG-AGG"""

    script += f"""
ipv4-family unicast
undo synchronization
network {ip_loopback} 255.255.255.255
auto-frr
nexthop recursive-lookup route-policy VERIFICA-NEXTHOP
ingress-lsp protect-mode bgp-frr
bestroute nexthop-resolved tunnel
bestroute add-path path-number 2
nexthop recursive-lookup delay 1
peer CSG-AGG enable
peer CSG-AGG route-policy MARCA-COMMUNITY-REGIAO-IPV4 export
peer CSG-AGG next-hop-local
peer CSG-AGG label-route-capability
peer CSG-AGG advertise-community
peer CSG-AGG capability-advertise add-path both
peer CSG-AGG advertise add-path path-number 2"""
    for i in range(len(bgp["ips_vizinhos"])):
        script += f"""
peer {bgp["ips_vizinhos"][i]} enable
peer {bgp["ips_vizinhos"][i]} group CSG-AGG"""
    script += f"""
ipv4-family vpnv4
policy vpn-target
auto-frr
nexthop recursive-lookup route-policy VERIFICA-NEXTHOP
bestroute nexthop-resolved tunnel
bestroute add-path path-number 2
nexthop recursive-lookup delay 1
peer CSG-AGG enable
peer CSG-AGG advertise-community
peer CSG-AGG capability-advertise add-path both
peer CSG-AGG advertise add-path path-number 2"""
    for i in range(len(bgp["ips_vizinhos"])):
        script += f"""
peer {bgp["ips_vizinhos"][i]} enable
Y
peer {bgp["ips_vizinhos"][i]} group CSG-AGG"""

    script += """
ipv6-family vpnv6
policy vpn-target
auto-frr
nexthop recursive-lookup route-policy VERIFICA-NEXTHOP
bestroute nexthop-resolved tunnel
bestroute add-path path-number 2
nexthop recursive-lookup delay 1
peer CSG-AGG enable
peer CSG-AGG advertise-community
peer CSG-AGG capability-advertise add-path both
peer CSG-AGG advertise add-path path-number 2
 """
    for i in range(len(bgp["ips_vizinhos"])):
        script += f"""
peer {bgp["ips_vizinhos"][i]} enable
Y
peer {bgp["ips_vizinhos"][i]} group CSG-AGG"""
    script += f"""
ipv4-family mdt
undo policy vpn-target
peer CSG-AGG enable
peer CSG-AGG advertise-community"""
    for i in range(len(bgp["ips_vizinhos"])):
        script += f"""
peer {bgp["ips_vizinhos"][i]} enable
Y
peer {bgp["ips_vizinhos"][i]} group CSG-AGG"""

    script+="""
quit
bgp yang-mode enable
Y
#
#"""
#Rota estática
    if rotas_estaticas:
        script += """
$====================================================================
$ ROTAS ESTATICAS
$====================================================================
"""
        for rota in rotas_estaticas:
            if rota["vrf"]:
                script += f"""ip route vrf {rota["vrf"]} {rota["ip_origem"]} {rota["mask"]} {rota["ip_destino"]}
"""
            else:
                script += f"""ip route {rota["ip_origem"]} {rota["mask"]} {rota["ip_destino"]}
"""
    if movel:
        script +=f"""
#
#========================================
# BGP - SERVICO MOVEL
#========================================
bgp {bgp["processo"]}
vpn-instance ABIS
quit
vpn-instance GERENCIA
quit
vpn-instance GERL3_EBT_CLARO
quit
vpn-instance IUB-DADOS
quit
vpn-instance S1
quit
ipv4-family vpn-instance ABIS
import-route direct
quit
ipv4-family vpn-instance GERENCIA
import-route direct
{"import-route static" if any(rota["vrf"] == "GERENCIA" for rota in rotas_estaticas) else ""}
quit
ipv4-family vpn-instance GERL3_EBT_CLARO
import-route direct
quit
ipv4-family vpn-instance IUB-DADOS
import-route direct
quit
ipv4-family vpn-instance S1
import-route direct
quit
#
#====================================================================
# QoS 2G ABIS
#====================================================================
#
traffic classifier TC20_2G_SIG_IN operator or
if-match dscp cs6
if-match dscp 62
#
traffic classifier TC20_2G_RT_IN operator or
if-match dscp cs5
if-match dscp ef
#
traffic classifier TC20_2G_GPRS_IN operator or
if-match any
#
#
traffic behavior TC20_2G_SIG_IN
remark mpls-exp 6
service-class cs6 color green
#
traffic behavior TC20_2G_RT_IN
remark mpls-exp 5
service-class ef color green
#
traffic behavior TC20_2G_GPRS_IN
remark mpls-exp 4
service-class af4 color green
#
#
traffic policy TC20_2G_IN
statistics enable
classifier TC20_2G_SIG_IN behavior TC20_2G_SIG_IN Precedence 1
classifier TC20_2G_RT_IN behavior TC20_2G_RT_IN Precedence 2
classifier TC20_2G_GPRS_IN behavior TC20_2G_GPRS_IN Precedence 3
#
#
flow-queue TC20_2G_OUT
queue cs6 wfq weight 15
queue ef pq shaping shaping-percentage 50
queue af4 wfq weight 85
#
qos-profile TC20_2G_SHAPE_1G_OUT
user-queue cir-percentage 95 pir-percentage 95 flow-queue TC20_2G_OUT outbound
#
qos-profile TC20_2G_SHAPE_10G_OUT
user-queue cir-percentage 95 pir-percentage 95 flow-queue TC20_2G_OUT outbound
#
#====================================================================
# QoS 3G IUB-DADOS
#====================================================================
#
traffic classifier TC20_3G_SIG_IN operator or
if-match dscp cs6
if-match dscp 62
#
traffic classifier TC20_3G_RT_IN operator or
if-match dscp cs5
if-match dscp ef
#
traffic classifier TC20_3G_GPRS_IN operator or
if-match any
#
#
traffic behavior TC20_3G_SIG_IN
remark mpls-exp 6
service-class cs6 color green
#
traffic behavior TC20_3G_RT_IN
remark mpls-exp 5
service-class ef color green
#
traffic behavior TC20_3G_GPRS_IN
remark mpls-exp 4
service-class af4 color green
#
#
traffic policy TC20_3G_IN
statistics enable
classifier TC20_3G_SIG_IN behavior TC20_3G_SIG_IN Precedence 1
classifier TC20_3G_RT_IN behavior TC20_3G_RT_IN Precedence 2
classifier TC20_3G_GPRS_IN behavior TC20_3G_GPRS_IN Precedence 3
#
#
flow-queue TC20_3G_OUT
queue cs6 wfq weight 15
queue ef pq shaping shaping-percentage 50
queue af4 wfq weight 85
#
qos-profile TC20_3G_SHAPE_1G_OUT
user-queue cir-percentage 95 pir-percentage 95 flow-queue TC20_3G_OUT outbound
#
qos-profile TC20_3G_SHAPE_10G_OUT
user-queue cir-percentage 95 pir-percentage 95 flow-queue TC20_3G_OUT outbound
#
#====================================================================
# QoS 4G S1
#====================================================================
#
traffic classifier TC20_4G_SIG_IN operator or
if-match dscp cs5
if-match dscp cs6
if-match dscp 62
#
traffic classifier TC20_4G_RT_IN operator or
if-match dscp ef
#
traffic classifier TC20_4G_VIDEO_IN operator or
if-match dscp cs4
if-match dscp af41
if-match dscp af42
if-match dscp af43
#
traffic classifier TC20_4G_MOVEL_IN operator or
if-match any
#
#
traffic behavior TC20_4G_SIG_IN
remark mpls-exp 6
service-class cs6 color green
#
traffic behavior TC20_4G_RT_IN
remark mpls-exp 5
service-class ef color green
#
traffic behavior TC20_4G_VIDEO_IN
remark mpls-exp 3
service-class af3 color green
#
traffic behavior TC20_4G_MOVEL_IN
remark mpls-exp 1
service-class af1 color green
#
#
traffic policy TC20_4G_IN
statistics enable
classifier TC20_4G_SIG_IN behavior TC20_4G_SIG_IN Precedence 1
classifier TC20_4G_RT_IN behavior TC20_4G_RT_IN Precedence 2
classifier TC20_4G_VIDEO_IN behavior TC20_4G_VIDEO_IN Precedence 3
classifier TC20_4G_MOVEL_IN behavior TC20_4G_MOVEL_IN Precedence 4
#
#
flow-queue TC20_4G_OUT
queue cs6 wfq weight 10
queue ef pq shaping shaping-percentage 50
queue af3 wfq weight 20
queue af1 wfq weight 70
#
qos-profile TC20_4G_SHAPE_1G_OUT
user-queue cir-percentage 95 pir-percentage 95 flow-queue TC20_4G_OUT outbound
#
qos-profile TC20_4G_SHAPE_10G_OUT
user-queue cir-percentage 95 pir-percentage 95 flow-queue TC20_4G_OUT outbound
#
#====================================================================
# QoS 5G S1
#====================================================================
#
traffic classifier TC20_5G_SIG_IN operator or
if-match dscp cs5
if-match dscp cs6
if-match dscp 62
#
traffic classifier TC20_5G_RT_IN operator or
if-match dscp ef
#
traffic classifier TC20_5G_VIDEO_IN operator or
if-match dscp cs4
if-match dscp af41
if-match dscp af42
if-match dscp af43
#
traffic classifier TC20_5G_MOVEL_IN operator or
if-match any
#
#
traffic behavior TC20_5G_SIG_IN
remark mpls-exp 6
service-class cs6 color green
#
traffic behavior TC20_5G_RT_IN
remark mpls-exp 5
service-class ef color green
#
traffic behavior TC20_5G_VIDEO_IN
remark mpls-exp 3
service-class af3 color green
#
traffic behavior TC20_5G_MOVEL_IN
remark mpls-exp 1
service-class af1 color green
#
#
traffic policy TC20_5G_IN
statistics enable
classifier TC20_5G_SIG_IN behavior TC20_5G_SIG_IN Precedence 1
classifier TC20_5G_RT_IN behavior TC20_5G_RT_IN Precedence 2
classifier TC20_5G_VIDEO_IN behavior TC20_5G_VIDEO_IN Precedence 3
classifier TC20_5G_MOVEL_IN behavior TC20_5G_MOVEL_IN Precedence 4
#
#
flow-queue TC20_5G_OUT
queue cs6 wfq weight 10
queue ef pq shaping shaping-percentage 50
queue af3 wfq weight 20
queue af1 wfq weight 70
#
qos-profile TC20_5G_SHAPE_1G_OUT
user-queue cir-percentage 95 pir-percentage 95 flow-queue TC20_5G_OUT outbound
#
qos-profile TC20_5G_SHAPE_10G_OUT
user-queue cir-percentage 95 pir-percentage 95 flow-queue TC20_5G_OUT outbound
#
#====================================================================
# QoS GERENCIA
#====================================================================
#
traffic classifier TC20_GERENCIA_RT-SYNC_IN operator or
if-match dscp cs7
if-match dscp ef
#
traffic classifier TC20_GERENCIA_DCR_IN operator or
if-match any
#
#
traffic behavior TC20_GERENCIA_RT-SYNC_IN
remark mpls-exp 7
service-class cs7 color green
#
traffic behavior TC20_GERENCIA_DCR_IN
remark mpls-exp 2
service-class af2 color green
#
#
traffic policy TC20_GERENCIA_MOVEL_IN
statistics enable
classifier TC20_GERENCIA_RT-SYNC_IN behavior TC20_GERENCIA_RT-SYNC_IN precedence 1
classifier TC20_GERENCIA_DCR_IN behavior TC20_GERENCIA_DCR_IN precedence 2
#
#
flow-queue TC20_GERENCIA_MOVEL_OUT
queue af2 wfq weight 100
queue cs7 pq shaping shaping-percentage 50
#
qos-profile TC20_GERENCIA_MOVEL_SHAPE_1G_OUT
user-queue cir-percentage 5 pir-percentage 5 flow-queue TC20_GERENCIA_MOVEL_OUT outbound
#
qos-profile TC20_GERENCIA_MOVEL_SHAPE_10G_OUT
user-queue cir-percentage 5 pir-percentage 5 flow-queue TC20_GERENCIA_MOVEL_OUT outbound
#
"""
    for x in range(len(movel)):        
        porta_movel = portas10.pop(0)
        portas_movel.append(porta_movel)
        script += f"""#====================================================================
# SERVIÇOS MOVEIS INTERFACE FISICA
#====================================================================
interface {porta_movel}
description {movel[x]["description"]}
undo shutdown
undo lldp enable
undo dcn {"\n" + "speed " + movel[x]["speed"] if movel[x]["speed"] else "" }
duplex full
#
"""
        for y in range(len(movel[x]["bdis"])):
            if movel[x]["bdis"][y]["tipo_servico"] == "2G":
                script += f"""#====================================================================
# CONFIGURAÇÃO 2G ABIS
#====================================================================
interface {porta_movel}.{movel[x]["bdis"][y]["bridge_domain"]}
vlan-type dot1q {movel[x]["bdis"][y]["dot1q"]}
description {movel[x]["bdis"][y]["description"]}
ip binding vpn-instance ABIS
ip address {movel[x]["bdis"][y]["ip_address"]} {movel[x]["bdis"][y]["mask"]}
statistic enable
traffic-policy TC20_2G_IN inbound
qos-profile TC20_2G_SHAPE_{"10" if  "Ten" in movel[x]["interface"] else "1" }G_OUT outbound
undo shutdown
#
"""
            if movel[x]["bdis"][y]["tipo_servico"] == "3G":
                script += f"""#====================================================================
# CONFIGURAÇÃO 3G IUB-DADOS
#====================================================================
interface {porta_movel}.{movel[x]["bdis"][y]["bridge_domain"]}
vlan-type dot1q {movel[x]["bdis"][y]["dot1q"]}
description {movel[x]["bdis"][y]["description"]}
ip binding vpn-instance IUB-DADOS
ip address {movel[x]["bdis"][y]["ip_address"]} {movel[x]["bdis"][y]["mask"]}
statistic enable
traffic-policy TC20_3G_IN inbound
qos-profile TC20_3G_SHAPE_{"10" if  "Ten" in movel[x]["interface"] else "1" }G_OUT outbound
undo shutdown
#
"""
            if movel[x]["bdis"][y]["tipo_servico"] == "4G":
                script += f"""#====================================================================
# CONFIGURAÇÃO 4G S1
#====================================================================
interface {porta_movel}.{movel[x]["bdis"][y]["bridge_domain"]}
vlan-type dot1q {movel[x]["bdis"][y]["dot1q"]}
description {movel[x]["bdis"][y]["description"]}
ip binding vpn-instance S1
ip address {movel[x]["bdis"][y]["ip_address"]} {movel[x]["bdis"][y]["mask"]}
statistic enable
traffic-policy TC20_4G_IN inbound
qos-profile TC20_4G_SHAPE_{"10" if  "Ten" in movel[x]["interface"] else "1" }G_OUT outbound
undo shutdown
#
"""
            if movel[x]["bdis"][y]["tipo_servico"] == "5G":           
                script += f"""#====================================================================
# CONFIGURAÇÃO 5G S1
#====================================================================
interface GigabitEthernet0/2/14.{movel[x]["bdis"][y]["bridge_domain"]}
vlan-type dot1q {movel[x]["bdis"][y]["dot1q"]}
description {movel[x]["bdis"][y]["description"]}
ip binding vpn-instance S1
ip address {movel[x]["bdis"][y]["ip_address"]} {movel[x]["bdis"][y]["mask"]}
statistic enable
traffic-policy TC20_5G_IN inbound
qos-profile TC20_5G_SHAPE_{"10" if  "Ten" in movel[x]["interface"] else "1" }G_OUT outbound
undo shutdown
#
"""
            if movel[x]["bdis"][y]["tipo_servico"] == "GERENCIA":
                script += f"""#====================================================================
# Configuracao Sub-interface GERENCIA e DHCP
#====================================================================
interface {porta_movel}.{movel[x]["bdis"][y]["bridge_domain"]}
vlan-type dot1q {movel[x]["bdis"][y]["dot1q"]}
description {movel[x]["bdis"][y]["description"]}
ip binding vpn-instance GERENCIA
ip address {movel[x]["bdis"][y]["ip_address"]} {movel[x]["bdis"][y]["mask"]}
statistic enable
traffic-policy TC20_GERENCIA_MOVEL_IN inbound
"""
                if movel[x]["bdis"][y]["dhcp"]:
                    script += "dhcp select relay\n"
                    for z in range(len(movel[x]["bdis"][y]["dhcp"])):
                        script += f"ip relay address {movel[x]["bdis"][y]["dhcp"][z]}\n"
                        script += f"""ip relay source-ip-address {movel[x]["bdis"][y]["ip_address"]} vpn-instance GERENCIA\n"""
                    script += f"""qos-profile TC20_GERENCIA_MOVEL_SHAPE_{"10" if  "Ten" in movel[x]["interface"] else "1" }G_OUT outbound
undo shutdown
#
"""
    if bateria:
        script += f"""#========================================
# QoS BATERIA
#========================================
traffic classifier TC20_GERENCIA_IN operator or
if-match any
#
traffic behavior TC20_GERENCIA_IN
remark mpls-exp 2
service-class af2 color green
#
traffic policy TC20_GERENCIA_IN
statistics enable
classifier TC20_GERENCIA_IN behavior TC20_GERENCIA_IN precedence 2
#
#========================================
# BATERIA
#========================================"""
    for x in range(len(bateria)):
        porta_bateria = "GigabitEthernet 0/2/5" if x == 0 else portas10.pop(0)
        portas_bateria. append(porta_bateria)
        script += f"""
interface {porta_bateria}
speed {bateria[x]["speed"]}
mtu {bateria[x]["mtu"]}
description {bateria[x]["description"]}
ip binding vpn-instance GERENCIA
ip address {bateria[x]["ip_address"]} {bateria[x]["mask"]}
ip relay address 10.119.68.18
ip relay address 10.119.68.19
dhcp select relay
traffic-policy TC20_GERENCIA_IN inbound
set flow-stat interval 30
statistic enable
undo shutdown
undo lldp enable
undo dcn
#"""
    if empresarial:
        script += f"""
# ====================================================================
# QoS EMPRESARIAL
# ====================================================================
#
#
traffic classifier TC20_RUD_MPLS_ROUTING operator or
if-match dscp cs6
#
traffic classifier TC20_RUD_MPLS_RT operator or
if-match dscp ef
#
traffic classifier TC20_RUD_MPLS_VIDEO operator or
if-match dscp af41
if-match dscp af42
if-match dscp af43
#
traffic classifier TC20_RUD_MPLS_DCR-1 operator or
if-match dscp CS1
if-match dscp AF11
if-match dscp AF12
if-match dscp AF13
if-match dscp CS2
if-match dscp AF21
if-match dscp AF22
if-match dscp AF23
#
traffic classifier TC20_RUD_MPLS_DCR-2 operator or
if-match dscp CS3
if-match dscp AF31
if-match dscp AF32
if-match dscp AF33
#
traffic classifier TC20_RUD_MPLS_DEFAULT operator or
if-match any
#
traffic behavior TC20_RUD_MPLS_ROUTING
remark mpls-exp 6
service-class cs6 color green
#
traffic behavior TC20_RUD_MPLS_RT
remark mpls-exp 5
service-class ef color green
#
traffic behavior TC20_RUD_MPLS_VIDEO
remark mpls-exp 3
service-class af3 color green
#
traffic behavior TC20_RUD_MPLS_DCR-1
remark mpls-exp 2
service-class af2 color green
#
traffic behavior TC20_RUD_MPLS_DCR-2
remark mpls-exp 2
service-class af2 color yellow
#
traffic behavior TC20_RUD_MPLS_DEFAULT
remark mpls-exp 0
service-class be color green
#
traffic policy TC20_EoMPLS_IN
statistics enable
classifier TC20_RUD_MPLS_ROUTING behavior TC20_RUD_MPLS_ROUTING
classifier TC20_RUD_MPLS_RT behavior TC20_RUD_MPLS_RT
classifier TC20_RUD_MPLS_VIDEO behavior TC20_RUD_MPLS_VIDEO
classifier TC20_RUD_MPLS_DCR-1 behavior TC20_RUD_MPLS_DCR-1
classifier TC20_RUD_MPLS_DCR-2 behavior TC20_RUD_MPLS_DCR-2
classifier TC20_RUD_MPLS_DEFAULT behavior TC20_RUD_MPLS_DEFAULT
#
#
traffic classifier TC20_GERENCIA_CORP operator or
if-match any
#
traffic behavior TC20_GERENCIA_CORP
service-class af2 color green
#
#
traffic policy TC20_GERENCIA_CORP_IN
statistics enable
classifier TC20_GERENCIA_CORP behavior TC20_GERENCIA_CORP
#
#
flow-queue CIRCUITO-512KBPS
queue be wfq weight 100
#
qos-profile CIRCUITO-512KBPS
user-queue cir 512 pir 512 flow-queue CIRCUITO-512KBPS inbound
#
#"""
        valores_usados = set()
        for item in empresarial:
            for svc in item.get("servicos", []):
                valor = svc.get("service_policy")
                if valor and valor not in valores_usados:
                    valores_usados.add(valor)
                    script += f"""
#
flow-queue CIRCUITO-{valor}KBPS
queue be wfq weight 100
#
#
qos-profile EoMPLS-CIRCUITO-{valor}KBPS-IN
user-queue cir {valor} pir {valor} flow-queue CIRCUITO-{valor}KBPS inbound
#
#"""
        script += """
# ========================================
# EMPRESARIAL
# ========================================"""

    for x in range(len(empresarial)):
        porta_edd = portas10.pop(0)
        portas_edd.append(porta_edd)

# Interface física
        script += f"""
interface {porta_edd}
mtu {empresarial[x]['mtu']}
description {empresarial[x]['description']}
undo shutdown
undo lldp enable
undo dcn
statistic enable
#"""

# GERENCIA
        for y in range (len(empresarial[x].get("servicos"))):
            if empresarial[x]["servicos"][y].get("tipo_servico") == "gerencia":
                script += f"""
interface {porta_edd}.{empresarial[x]["servicos"][y]['bridge_domain']}
vlan-type dot1q {empresarial[x]["servicos"][y]['dot1q']}
mtu {empresarial[x]['mtu']}
description {empresarial[x]["servicos"][y]['bdi_description']}
ip binding vpn-instance GERL3_EBT_CLARO
ip address {empresarial[x]["servicos"][y]['ip_address']} {empresarial[x]["servicos"][y]['mask']}
traffic-policy TC20_GERENCIA_CORP_IN inbound link-layer
qos-profile CIRCUITO-512KBPS inbound
#"""
# SERVIÇO Q IN Q
            elif empresarial[x]["servicos"][y].get("tipo_servico") == "servico_q":
                vcid_formatado = str(empresarial[x]["servicos"][y]['xconnect_vcid'])[-8:]
                script += f"""
interface {porta_edd}.{vcid_formatado}
mtu {empresarial[x]["servicos"][y].get('mtu', empresarial[x]['mtu'])}
description {empresarial[x]["servicos"][y]['service_description']}
set flow-stat interval 30
statistic enable
encapsulation qinq-termination
qinq termination pe-vid {empresarial[x]["servicos"][y]["dot1q_1"]} ce-vid {empresarial[x]["servicos"][y]["dot1q_2"]}
mpls l2vc {empresarial[x]["servicos"][y]['xconnect_ip']} {empresarial[x]["servicos"][y]['xconnect_vcid']} raw
qos-profile EoMPLS-CIRCUITO-{empresarial[x]["servicos"][y]['service_policy']}KBPS-IN inbound pe-vid {empresarial[x]["servicos"][y]["dot1q_1"]} ce-vid {empresarial[x]["servicos"][y]["dot1q_2"]}
traffic-policy TC20_EoMPLS_IN inbound pe-vid {empresarial[x]["servicos"][y]["dot1q_1"]} ce-vid {empresarial[x]["servicos"][y]["dot1q_2"]}
#"""
# SERVIÇO 
            elif empresarial[x]["servicos"][y].get("tipo_servico") == "servico":
                vcid_formatado = str(empresarial[x]["servicos"][y]['xconnect_vcid'])[-8:]
                script += f"""
interface {porta_edd}.{vcid_formatado}
vlan-type dot1q {empresarial[x]["servicos"][y]['dot1q']}
mtu {empresarial[x]["servicos"][y].get('mtu', item['mtu'])}
description {empresarial[x]["servicos"][y]['service_description']}
set flow-stat interval 30
statistic enable
traffic-policy TC20_EoMPLS_IN inbound link-layer
mpls l2vc {empresarial[x]["servicos"][y]['xconnect_ip']} {empresarial[x]["servicos"][y]['xconnect_vcid']} raw
qos-profile EoMPLS-CIRCUITO-{empresarial[x]["servicos"][y]['service_policy']}KBPS-IN inbound
#"""
    script += f"""
#========================================
# PUBLIC KEY
#========================================
rsa peer-public-key 10.107.13.15
 public-key-code begin
 3082018A
  02820181
    00C32B1E 2FACE6E7 9FBFE852 973EF7AC 687B7467 C3624C1F F760D853 9D8B273C
    ACBE78A2 23BC9A33 14BEC7D8 7DAD9A93 7B22F98F 1078733C 5561EF4B 55B95968
    F0A3A59F 64729396 254F5ABF 6E453DB8 117265C9 B1F52924 464E2778 EF48ACF8
    DDDA5CB8 64454885 AA566E68 723A4D9F 79B9171D 6219BDAF 63F2BEB0 A080DD05
    26BC8CF7 0FF0A782 FAF3F39E 28ED3280 6E4E0BEE 0E5F28FA 2FCE06EC 4CB244D8
    715A7F32 F9F697FD 02530CEA B70F97F8 3E9A9E89 2ACFCB65 7F427FEE 9C252FB6
    FD36974D 234523AC 06B9C283 14FF5D01 80F729A2 2BEC96ED C887F8EA 0DCAF317
    CD60BF89 2C8CC750 AA487E79 9875B6B9 3626ADC9 9EC51A4B 2879CDA5 29420DF8
    2AB330EA 32A0A092 E087BD96 7D349CA6 0AF60655 3A90D14E F50E0DBD 77D4C207
    27890242 6A62FEBE 6E8954A4 E9A7A38C 2BCF2FDC 127915FD 96339E54 434A14EA
    E423370B 97308F45 5A3238F8 0ECD4857 C318D8AD F9932B12 947DBC6D BCB344AF
    ED29541F D22C1878 7295F9DB 2A7B7725 4497236D 2F90B7EB 06F98980 7158B15E
    C3
  0203
    010001
 public-key-code end
 peer-public-key end
#
rsa peer-public-key 10.129.197.20
 public-key-code begin
 3082018A
  02820181
    00C8E912 3DB62C96 1B647611 D1300895 18315C20 DAA0E31D 12F619B3 15A3E814
    AF1D1C7A 01229343 E561D634 54C20EC3 E9DE0EB0 1C632B2C BDCA004B ABE8FC3B
    43BC7DA6 F8232511 FA8AEB4E 343B40CF FDB64845 7E170451 D048246E E7D785AD
    C4FF1DF1 7105D680 6D5F1FC6 4C9C62AB E27046A6 B1C50220 575E55EF F034B580
    07360793 25CBAC35 DCB2A24B 6B7F46AF 8941436F 536D2640 9D291B9F 883FAFC2
    2691D53F 091035FF F20FA7E2 4974BF8D F2EA3F3B 2C6ABF60 5F459BD4 5E57DBE6
    DC960061 D4AFD160 88FFD669 584D8104 5BF4E8B7 4E3BA736 D4892398 7232CF4C
    3DC865B5 B25F46BC 1AAA8C41 0C53029F 24DA0253 2B03D28C 6244652D 32F1A7DC
    F325798E 18E33F30 D07F2017 09ED9AB1 7FB19C96 739D4500 6BFF4171 D57BCEBD
    838C9F18 26E2E160 2DB933E0 D1C26696 46C0B99E 58CA2CAB 47A6769F 8DD8B1FC
    AB4A3052 6ACADF59 E8E76727 0668D7D5 5BF33F4D 1DE33415 DFAD8D4D DA89971C
    1871CC53 D8359C70 D0182D8A FCC0EEE8 32D1BDB9 6062F3B6 0DFFECA0 96CDDC80
    01
  0203
    010001
 public-key-code end
 peer-public-key end
#
rsa peer-public-key 10.129.231.138
 public-key-code begin
 3082018A
  02820181
    00C113E0 8928E6F3 57E949B0 92BABDB3 1A276AC0 7875FF91 91386693 D4D78B44
    11635798 7F596F6A 92F307D7 A0B1B832 75BC9DEB B14F1BD5 A05BC36C 31950F19
    CBB86CC4 9C5459B7 6F593980 487BFBD4 DBFC49A7 4CB079DA 6DA19991 F54CB87D
    586E7CA2 531EBC06 662E33F7 DE7B3AEE 52E8D4D4 1177FDE6 E3B32F53 FBE53DCA
    6CD578C1 908FE62A 32E6E8A2 4F65751B 529BA59A 871A309C 0E319479 72BFC4F2
    AECB3EC7 F423114A 39F605B3 08A48668 D981BC72 4D3CC82D BD9290A5 C88962EC
    7CC9810C 7CE2DA09 2DEB0190 CCEF3351 F4093809 5D9CEB07 28751CC5 531669EF
    5DCC28BB 8E76444A C97F6B3D 94799A49 27A7412B 078A5A86 C1530E23 E22F7FF1
    A16FA7EB 3EF8188C 32868B16 E6B9035B FB4653A2 30AFBB9F F1E94BE8 43D499E7
    936B8A8D 29C2D152 0640D8BF 0BAE24F0 FBA991CF 1FA0F335 7C933259 393763CD
    622628CC 5577F110 8246BE83 640EA0F1 0D01BEA1 125A5905 888F6BDE 54F079C4
    487F1DF4 1C362E13 80882729 28CF85C0 78661A76 F6037C9E 12227655 F7C614F2
    D7
  0203
    010001
 public-key-code end
 peer-public-key end
#
rsa peer-public-key 10.129.231.139
 public-key-code begin
 3082018A
  02820181
    00AB3EEC C8826CCA 49E1A2ED ECC64728 48E43B14 7C629BC3 E42036CD C70DDE21
    A5191F12 5DE12C41 700DE5A5 0338AB07 F20B7D4E 89419092 36031E67 7B6F6091
    641F8E23 7CB96AB1 1BF647E5 53AFD467 C4B698B2 9C4B9024 10C8D0A5 CC885D44
    5B7BB420 A9E42BA7 6A2C89D6 08C8259D F037D093 2D8896B2 61781F50 C2C10321
    5E5042E8 C60B9B47 1D65632F 233390F1 F7066C5B E83AED50 1C3843C5 DC300A51
    031F7032 0771AE46 08EC51EF BBAD2251 23F25EAB 32932495 E17BA7BA 7F64AD05
    3E724405 E1EF7BB6 D34CB22A 656EBEA7 CD4AC3EA 9A8CD56D 1A7A421E 6F277F46
    5A4E4509 FA5F5504 0F9BF676 661FF735 E8906C15 9E81C4A9 90536838 A09A7390
    D406F67C 55FCDE74 C824F0E2 C9F3472B 2C2471B3 15D99056 B093EA6B 8895A65D
    53C6354B 94514DFC 3C81645F 49B3EAD7 75AA4217 190059A3 1A2E53B1 DE2DCAD4
    D06C3293 3EC27553 C095B050 C8C9B683 71A1C85B 062E32CF 3BA27035 4B771089
    9746EEB3 D7B94EA7 AC93451D A33C2ED2 30F40A66 BEBF76A1 4EEB172E EB99BC09
    0B
  0203
    010001
 public-key-code end
 peer-public-key end
#
rsa peer-public-key 10.129.231.142
 public-key-code begin
 3082018A
  02820181
    00BAA116 9A130DF4 F20EBC7D 6A4C997B 66F5A6CF 1544ECDE 2D88B167 85038C71
    E5FB4059 5D115590 3724B53E 7FBDDFE1 CB828C4C E2E3BE4E 44B1E283 64F3D4E5
    35CD61F3 109563B2 D7271843 6B494A3A DB8FA60D 7BEBC81D 14B7806E 612D1207
    0F199871 F673973B 9C5DDCCA 357BCEB0 B16B7074 D0B86C7B 4AFB2A6A 77AAFC1C
    15923F5E 5C7C9556 D0743960 AE297450 7172FCD6 965BA0F7 75E65E14 4CBA5937
    CBF2F4C1 AC263E68 351F2D63 F53AB6F9 885A90F7 82809B9B 8455A1B3 61A9EB10
    FF451E9A C4111417 2C80CB07 1CC2C88C B67A4DA3 7E2D5C0C 420B3C70 4A12D6A7
    5A366679 2D1D29F9 2D77EDAA 5E7D1504 22DD1D06 55D538C3 27AB9637 1114216B
    B46E630C CCBB88FB 4619D245 21A4EA06 BE961E54 5BB230EE E20BEEAF 31AA2256
    B06A690E C1AA0B11 990FEC02 BEEBEDAA 8DB73675 2C4FC1F2 ED2ACD38 43A10225
    D173054C D744D03B 84B81BA5 A4046DEF 93D276FE FCA939D0 6502F352 B3B2D095
    886D84F0 51BCCA5D 7536C970 B06922E2 EA2149BD E4DF7FE3 C79FC02C 7D3BCFCD
    4B
  0203
    010001
 public-key-code end
 peer-public-key end
#
rsa peer-public-key 10.129.231.143
 public-key-code begin
 3082018A
  02820181
    00C113E0 8928E6F3 57E949B0 92BABDB3 1A276AC0 7875FF91 91386693 D4D78B44
    11635798 7F596F6A 92F307D7 A0B1B832 75BC9DEB B14F1BD5 A05BC36C 31950F19
    CBB86CC4 9C5459B7 6F593980 487BFBD4 DBFC49A7 4CB079DA 6DA19991 F54CB87D
    586E7CA2 531EBC06 662E33F7 DE7B3AEE 52E8D4D4 1177FDE6 E3B32F53 FBE53DCA
    6CD578C1 908FE62A 32E6E8A2 4F65751B 529BA59A 871A309C 0E319479 72BFC4F2
    AECB3EC7 F423114A 39F605B3 08A48668 D981BC72 4D3CC82D BD9290A5 C88962EC
    7CC9810C 7CE2DA09 2DEB0190 CCEF3351 F4093809 5D9CEB07 28751CC5 531669EF
    5DCC28BB 8E76444A C97F6B3D 94799A49 27A7412B 078A5A86 C1530E23 E22F7FF1
    A16FA7EB 3EF8188C 32868B16 E6B9035B FB4653A2 30AFBB9F F1E94BE8 43D499E7
    936B8A8D 29C2D152 0640D8BF 0BAE24F0 FBA991CF 1FA0F335 7C933259 393763CD
    622628CC 5577F110 8246BE83 640EA0F1 0D01BEA1 125A5905 888F6BDE 54F079C4
    487F1DF4 1C362E13 80882729 28CF85C0 78661A76 F6037C9E 12227655 F7C614F2
    D7
  0203
    010001
 public-key-code end
 peer-public-key end
#
#========================================
# TACACS / AAA / LOCAL USER
#========================================
#
# Aplicar apos a conclusao da SSD de Integracao na Gerencia.
# Pegar as rsa peer-public-key de outro RMP
#
hwtacacs-server template acsclaro
hwtacacs-server authentication 10.129.199.25
hwtacacs-server authentication 10.108.199.25 secondary
hwtacacs-server authorization 10.129.199.25
hwtacacs-server authorization 10.108.199.25 secondary
hwtacacs-server accounting 10.129.199.25
hwtacacs-server accounting 10.108.199.25 secondary
hwtacacs-server source-ip {ip_loopback}
hwtacacs-server shared-key cipher CLAROSECkey$321
hwtacacs-server timer response-timeout 10
hwtacacs-server user-name original
#
#
aaa
user-password password-force-change disable
local-user root password irreversible-cipher Changeme_123
local-user root service-type terminal ssh
local-user root level 3
local-user root state block fail-times 3 interval 5
local-user root ftp-directory cfcard:/
local-user root user-group manage-ug
local-user nsvcadm password irreversible-cipher #Hu@We1#CI@ro#
local-user nsvcadm service-type terminal ssh
local-user nsvcadm level 3
local-user nsvcadm state block fail-times 3 interval 5
local-user nsvcadm ftp-directory cfcard:/
local-user nsvcadm user-group manage-ug
authentication-scheme default0
authentication-mode local
authentication-scheme default1
authentication-mode hwtacacs local
authentication-scheme default
authentication-mode local radius
authentication-scheme hwtacacs
authentication-mode hwtacacs local
authorization-scheme hwtacacs
authorization-mode hwtacacs local
authorization-cmd 1 hwtacacs local
authorization-cmd 3 hwtacacs local
authorization-cmd 15 hwtacacs local
authorization-scheme default
accounting-scheme hwtacacs
accounting-mode none
accounting start-fail online
accounting-scheme default0
accounting-scheme default1
domain default_admin
authentication-scheme hwtacacs
authorization-scheme hwtacacs
accounting-scheme hwtacacs
hwtacacs-server acsclaro
domain default0
domain default1
recording-scheme hwtacacs
recording-mode hwtacacs acsclaro
cmd recording-scheme hwtacacs
#
#
acl name ACL_OPERADOR advance
description ACL-120
rule 5 permit ip source 10.0.1.7 0.255.0.0
rule 10 permit ip source 10.0.7.0 0.255.0.255
rule 15 permit ip source 10.0.55.0 0.255.0.255
rule 20 permit ip source 10.0.56.0 0.255.0.255
rule 25 permit ip source 10.108.7.0 0.0.0.255
rule 30 permit ip source 10.108.97.0 0.0.0.255
rule 35 permit ip source 10.108.198.0 0.0.0.255
rule 40 permit ip source 10.108.199.0 0.0.0.255
rule 45 permit ip source 10.129.71.64 0.0.0.31
rule 50 permit ip source 10.119.97.0 0.0.0.255
rule 55 permit ip source 10.129.7.0 0.0.0.255
rule 60 permit ip source 10.129.97.0 0.0.0.255
rule 65 permit ip source 10.129.198.0 0.0.0.255
rule 70 permit ip source 10.129.199.0 0.0.0.255
rule 75 permit ip source 10.129.251.80 0.0.0.15
rule 80 permit ip source 10.197.120.0 0.0.7.255
rule 85 permit ip source 10.198.1.0 0.0.0.255
rule 90 permit ip source 10.198.120.0 0.0.7.255
rule 95 permit ip source 10.199.8.0 0.0.0.255
rule 100 permit ip source 10.199.10.0 0.0.0.255
rule 105 permit ip source 10.199.24.0 0.0.0.255
rule 110 permit ip source 10.199.26.0 0.0.0.255
rule 115 permit ip source 10.200.0.0 0.0.0.255
rule 120 permit ip source 10.201.0.0 0.0.0.255
rule 125 permit ip source 10.202.0.0 0.0.0.255
rule 130 permit ip source 10.203.0.0 0.0.0.255
rule 135 permit ip source 10.204.0.0 0.0.0.255
rule 140 permit ip source 10.205.0.0 0.0.0.255
rule 145 permit ip source 10.206.0.0 0.0.0.255
rule 150 permit ip source 10.207.0.0 0.0.0.255
rule 155 permit ip source 10.208.0.0 0.0.0.255
rule 160 permit ip source 10.209.0.0 0.0.0.255
rule 165 permit ip source 10.210.0.0 0.0.0.255
rule 170 permit ip source 10.221.198.0 0.0.0.255
rule 175 permit ip source 10.221.199.0 0.0.0.255
rule 180 permit ip source 10.230.0.0 0.0.0.255
rule 185 permit ip source 10.231.0.0 0.0.0.255
rule 190 permit ip source 10.232.0.0 0.0.0.255
rule 195 permit ip source 10.233.0.0 0.0.0.255
rule 200 permit ip source 10.234.0.0 0.0.0.255
rule 205 permit ip source 10.235.0.0 0.0.0.255
rule 210 permit ip source 10.236.0.0 0.0.0.255
rule 215 permit ip source 10.237.0.0 0.0.0.255
rule 220 permit ip source 10.238.0.0 0.0.0.255
rule 225 permit ip source 10.239.0.0 0.0.0.255
rule 230 permit ip source 10.240.0.0 0.0.0.255
rule 235 permit ip source 10.241.0.0 0.0.0.255
rule 240 permit ip source 10.242.0.0 0.0.0.255
rule 245 permit ip source 10.243.0.0 0.0.0.255
rule 250 permit ip source 10.244.0.0 0.0.0.255
rule 255 permit ip source 10.245.0.0 0.0.0.255
rule 260 permit ip source 10.246.0.0 0.0.0.255
rule 265 permit ip source 10.247.0.0 0.0.0.255
rule 270 permit ip source 10.248.0.0 0.0.0.255
rule 275 permit ip source 10.249.0.0 0.0.0.255
rule 280 permit ip source 10.250.0.0 0.0.0.255
rule 285 permit ip source 10.251.0.0 0.0.0.255
rule 290 permit ip source 10.252.0.0 0.0.0.255
rule 295 permit ip source 172.31.176.0 0.0.0.255
rule 300 permit ip source 172.31.177.0 0.0.0.255
rule 305 permit ip source 172.31.178.0 0.0.0.255
rule 310 permit ip source 172.31.180.0 0.0.0.255
rule 315 permit ip source 172.31.181.0 0.0.0.255
rule 320 permit ip source 172.31.182.0 0.0.0.255
rule 325 permit ip source 172.31.183.0 0.0.0.255
rule 330 permit ip source 172.31.224.0 0.0.0.255
rule 335 permit ip source 172.31.225.0 0.0.0.255
rule 340 permit ip source 172.31.226.0 0.0.0.255
rule 345 permit ip source 172.31.227.0 0.0.0.255
rule 350 permit ip source 172.31.228.0 0.0.0.255
rule 355 permit ip source 172.31.229.0 0.0.0.255
rule 360 permit ip source 172.31.230.0 0.0.0.255
rule 365 permit ip source 172.31.240.0 0.0.0.255
rule 370 permit ip source 10.197.4.1 0.0.0.0
rule 375 permit ip source 200.255.124.9 0.0.0.0
rule 380 permit ip source 200.255.124.25 0.0.0.0
rule 385 permit ip source 10.108.211.129 0.0.0.0
rule 386 permit ip source 10.108.211.128 0.0.0.31
rule 387 permit ip source 10.108.210.33 0.0.0.255
rule 390 permit ip source 10.108.210.82 0.0.0.0
rule 395 permit ip source 10.129.197.0 0.0.0.31
rule 400 permit ip source 10.107.81.0 0.0.0.63
rule 405 permit ip source 200.255.124.0 0.0.0.31
rule 410 permit ip vpn-instance __LOCAL_OAM_VPN__ source 192.168.0.0 0.0.0.255
rule 411 permit ip source 192.168.32.247 0.0.0.0
rule 412 permit ip source 192.168.32.248 0.0.0.0
rule 413 permit ip source 192.168.32.249 0.0.0.0
rule 425 permit ip source 10.107.12.128 0.0.0.127
rule 430 permit ip source 10.107.13.0 0.0.0.127
rule 435 permit ip source 10.107.13.128 0.0.0.127
rule 440 permit ip source 10.107.81.128 0.0.0.127
rule 445 permit ip source 10.129.225.128 0.0.0.127
rule 450 permit ip source 10.129.231.128 0.0.0.127
rule 455 permit ip source 10.129.237.128 0.0.0.127
rule 460 permit ip source 10.129.239.128 0.0.0.127
rule 10000 deny ip
#
user-interface maximum-vty 21
#
user-interface con 0
authentication-mode aaa
set authentication password cipher #Hu@We1#Cl@r0#
history-command max-size 50
#
user-interface vty 0 20
acl ACL_OPERADOR inbound
authentication-mode aaa
user privilege level 3
history-command max-size 50
idle-timeout 15 0
protocol inbound ssh
#
ssh server timeout 60
#
ssh server authentication-retries 2
#
ssh user nsvcadm
#
ssh user nsvcadm authentication-type password
#
ssh user nsvcadm service-type snetconf stelnet
#
ssh user nsvcadm sftp-directory cfcard:
#
ssh user root
#
ssh user root authentication-type password
#
ssh user root service-type snetconf stelnet
#
ssh user root sftp-directory cfcard:
#
ssh server-source all-interface
Y
#
undo ssh ipv6 server-source all-interface
Y
#
ssh authorization-type default aaa
#
ssh server cipher aes256_gcm aes128_gcm aes256_ctr aes192_ctr aes128_ctr aes256_cbc aes128_cbc 3des_cbc
#
ssh server hmac sha2_512 sha2_256_96 sha2_256 sha1 sha1_96 md5 md5_96
#
ssh server key-exchange dh_group_exchange_sha256 dh_group_exchange_sha1 ecdh_sha2_nistp256 ecdh_sha2_nistp384 ecdh_sha2_nistp521 sm2_kep
#
ssh server publickey ecc rsa rsa_sha2_256 rsa_sha2_512
#
ssh server dh-exchange min-len 1024
#
ssh server acl ACL_OPERADOR
#
ssh client first-time enable
#
ssh client publickey ecc rsa rsa_sha2_256 rsa_sha2_512
#
ssh client cipher aes256_gcm aes128_gcm aes256_ctr aes192_ctr aes128_ctr
#
ssh client hmac sha2_512 sha2_256
#
ssh client key-exchange dh_group_exchange_sha256 dh_group_exchange_sha1 dh_group14_sha1 ecdh_sha2_nistp256 ecdh_sha2_nistp384 ecdh_sha2_nistp521 dh_group16_sha512
#
ssh client peer 10.129.197.20 assign rsa-key 10.107.13.15
#
ssh client peer 10.107.81.36 assign rsa-key 10.129.197.20
#
ssh client peer 10.107.81.36 assign rsa-key 10.129.231.138
#
ssh client peer 10.129.197.20 assign rsa-key 10.129.231.139
#
ssh client peer 10.129.197.20 assign rsa-key 10.129.231.142
#
ssh client peer 10.107.81.36 assign rsa-key 10.129.231.143
#
#
#====================================================================
# REMOÇÃO DO TELNET
#====================================================================
undo telnet server enable
Y
undo telnet server-source all-interface
y
#
#
#
commit
#
save
#
"""
# DE PARA

    de_para_fo = []
    de_para_mwrot = []
    de_para_movel = []
    de_para_bateria = []
    de_para_empresarial = []

    de_para_texto = "\n### DE PARA ###\n"

# NNI FO
    for i in range(len(fibra or [])):
        porta_antiga = fibra[i]['interface']
        porta_nova = f"{portas_fo[i]}"
        de_para_texto += f"De {porta_antiga} → Para {porta_nova} - NNI FIBRA\n"

# NNI MW-ROT
    for i in range(len(mwrot or [])):
        porta_antiga = mwrot[i]['interface']
        porta_nova = f"{portas_mwrot[i]}"
        de_para_texto += f"De {porta_antiga} → Para {porta_nova} - NNI RADIO\n"

# UNI MOVEL
    for i in range(len(movel or [])):
        porta_antiga = movel[i]['interface']
        porta_nova = f"{portas_movel[i]}"
        de_para_texto += f"De {porta_antiga} → Para {porta_nova} - UNI MOVEL\n"

# BATERIA
    for i in range(len(bateria or [])):
        porta_antiga = bateria[i]['interface']
        porta_nova = f"{portas_bateria[i]}"
        de_para_texto += f"De {porta_antiga} → Para {porta_nova} - BATERIA LÍTIO\n"

# EMPRESARIAL
    for i in range(len(empresarial or [])):
        porta_antiga = empresarial[i]['interface']
        porta_nova = f"{portas_edd[i]}"
        de_para_texto += f"De {porta_antiga} → Para {porta_nova} - EMPRESARIAL\n"

# Insere o DE PARA no topo do script
    script = de_para_texto + script

# Salva o script final
    with open(f"scripts/{hostname}_HUAWEI_ATN910D.txt", 'w', encoding='utf-8') as arquivo:
        arquivo.write(script)

    print(f"✅ Script e banners gerados com sucesso para {hostname}_HUAWEI_ATN910D")

#    return script, banner, banner_roteador

