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
    portas1 = ['xgei-1/1/0/1', 
                'xgei-1/1/0/2', 
                'xgei-1/1/0/3', 
                'xgei-1/1/0/4',  
                'xgei-1/1/0/6', 
                'xgei-1/1/0/7', 
                'xgei-1/1/0/8', 
                'xgei-1/1/0/9', 
                'xgei-1/1/0/10',  
                'xxvgei-1/1/0/13',
                'xxvgei-1/1/0/14',
                'xxvgei-1/1/0/15', 
                'xxvgei-1/1/0/16',
                'xxvgei-1/1/0/17',
                'xxvgei-1/1/0/18',
                'xxvgei-1/1/0/19',
                'xxvgei-1/1/0/20',
                'xxvgei-1/1/0/21',
                'xxvgei-1/1/0/22',
                'xxvgei-1/1/0/23',
                'xxvgei-1/1/0/24']
        
    portas10 = ['xxvgei-1/1/0/25',
                'xxvgei-1/1/0/26',
                'xxvgei-1/1/0/27',
                'xxvgei-1/1/0/28',
                'xxvgei-1/1/0/29',
                'xxvgei-1/1/0/30',
                'xxvgei-1/1/0/31',
                'xxvgei-1/1/0/32']
                    
    portas100 = ['cgei-1/1/0/33',
                'cgei-1/1/0/34',
                'cgei-1/1/0/35',
                'cgei-1/1/0/36']
#$ ========================================
#$ Grupos de portas ZTE
#$ =======================================
#$ 11 e 12 - 1G ou 10Gb
#$ 13 e 14 - 1G ou 10Gb
#$ 15 e 16 - 1G ou 10Gb
#$ 17 a 20 - 1G ou 10Gb
#$ 21 a 24 - 1G ou 10Gb
#$ 25 a 32 - 10Gb
#$ 34 e 36 - 100Gb                
    
    script = f"""$    
$ ========================================
$ Grupos de portas ZTE
$ =======================================
$ 11 e 12 - 1G ou 10Gb
$ 13 e 14 - 1G ou 10Gb
$ 15 e 16 - 1G ou 10Gb
$ 17 a 20 - 1G ou 10Gb
$ 21 a 24 - 1G ou 10Gb
$ 25 a 32 - 10Gb
$ 34 e 36 - 100Gb
$
$ ========================================
$ RESET DE FABRICA
$ =======================================
conf t
load-mode noload
commit
end
reload system force
y
$ ========================================
$ ATIVAÇÃO DAS LICENÇAS
$ =======================================
ping vrf mng 192.192.192.10
license download vrf mng ftp //zte@192.192.192.10/6120hs_250XXX.LCS
zte
dir licensedl
$
$
license install 6120hs_250403.LCS
$
license update
$
configure terminal
permit PEL-6100-XG-1G shelf 1 slot 1 subslot 0 port 1-10
permit PEL-6100-QCG-10G shelf 1 slot 1 subslot 0 port 11-32
permit PEL-6100-CG-100G shelf 1 slot 1 subslot 0 port 34,36
commit
exit
write
$
$
$========================================
$ BANNER
$========================================
$
configure terminal
$
banner incoming #
***********************************************
*                                             *      
* VOCE ESTA EM : {hostname}
*                                             *    
***********************************************#
banner login edit
****************************************************************************
* ATENCAO: CLARO - ACESSO RESTRITO -                                       *                                                     
*                                                                          *
* Todas as tentativas de login estao sendo monitoradas.                    *                                            
* ATTENTION: CLARO - RESTRICTED ACCESS -                                   *                                                 
* RESTRICTED ACCESS EQUIPMENT. ONLY PERSONAL AUTHORIZED.                   *                         
* ALL ACCESSES ARE BEING MONITORED.                                        *                                                  
****************************************************************************
!quit
load-mode txt
$
$========================================
$ SCRIPT DE CONFIGURAÇÃO ZTE 6120H
$========================================
$
commit-mode default manual
$
hostname {hostname}
$
$
ip domain name backbone.claro.com.br
$
interface null1
$
load-sharing hash-fields mpls ip-l4
$
load-sharing wtr 5
$
mgmt-eth switch enable
$
nsr service all
$
performance update-interval 30s default
$
dcn
dcn disable
$
$========================================
$ LOOPBACK GERENCIA
$========================================
interface loopback100
description Loopback de Roteamento
ip address {ip_loopback} 255.255.255.255
no shutdown
$
$
$ ========================================
$ DESATIVANDO TODAS AS PORTAS
$ =======================================
interface xgei-1/1/0/1
shutdown
exit           
interface xgei-1/1/0/2
shutdown
exit          
interface xgei-1/1/0/3           
shutdown
exit
interface xgei-1/1/0/4           
shutdown
exit
interface xgei-1/1/0/5           
shutdown
exit
interface xgei-1/1/0/6           
shutdown
exit
interface xgei-1/1/0/7           
shutdown
exit
interface xgei-1/1/0/8           
shutdown
exit
interface xgei-1/1/0/9           
shutdown
exit
interface xgei-1/1/0/10          
shutdown
exit
interface xxvgei-1/1/0/11        
shutdown
exit
interface xxvgei-1/1/0/12        
shutdown
exit
interface xxvgei-1/1/0/13        
shutdown
exit
interface xxvgei-1/1/0/14        
shutdown
exit
interface xxvgei-1/1/0/15        
shutdown
exit
interface xxvgei-1/1/0/16        
shutdown
exit
interface xxvgei-1/1/0/17        
shutdown
exit
interface xxvgei-1/1/0/18        
shutdown
exit
interface xxvgei-1/1/0/19        
shutdown
exit
interface xxvgei-1/1/0/20        
shutdown
exit
interface xxvgei-1/1/0/21        
shutdown
exit
interface xxvgei-1/1/0/22        
shutdown
exit
interface xxvgei-1/1/0/23        
shutdown
exit
interface xxvgei-1/1/0/24        
shutdown
exit
interface xxvgei-1/1/0/25        
shutdown
exit
interface xxvgei-1/1/0/26        
shutdown
exit
interface xxvgei-1/1/0/27        
shutdown
exit
interface xxvgei-1/1/0/28        
shutdown
exit
interface xxvgei-1/1/0/29        
shutdown
exit
interface xxvgei-1/1/0/30        
shutdown
exit
interface xxvgei-1/1/0/31        
shutdown
exit
interface xxvgei-1/1/0/32
shutdown
exit
interface cgei-1/1/0/33          
shutdown
exit
interface cgei-1/1/0/34          
shutdown
exit
interface cgei-1/1/0/35          
shutdown
exit
interface cgei-1/1/0/36          
shutdown
exit
$ ========================================
$ NTP
$ =======================================
$
$
clock timezone BRZ -3
$
$
ipv4-access-list NTP
rule 5 permit 10.108.64.242 0.0.0.0
rule 10 permit 10.129.64.242 0.0.0.0
rule 15 permit 127.127.7.1 0.0.0.0"""
    if hostname.startswith("RS"):
        script += """
rule 20 permit 10.150.7.0 0.0.0.255
rule 25 permit 10.150.8.0 0.0.0.255
rule 30 permit 10.151.7.0 0.0.0.255
rule 35 permit 10.152.7.0 0.0.0.255
rule 40 permit 10.155.7.0 0.0.0.255
rule 45 permit 10.207.0.0 0.0.127.255
rule 50 permit 10.208.0.0 0.0.127.255
rule 55 permit 10.207.128.0 0.0.127.255
rule 60 permit 10.208.128.0 0.0.127.255
rule 55 permit 10.207.128.0 0.0.127.255
rule 65 permit 10.34.0.0 0.0.255.255
rule 70 permit 10.94.0.0 0.0.255.255
rule 75 permit 10.95.0.0 0.0.255.255
"""
    elif hostname.startswith("PR") or hostname.startswith("SC"):
        script += """
rule 20 permit 10.147.7.0 0.0.0.255
rule 25 permit 10.148.7.0 0.0.0.255
rule 30 permit 10.210.0.0 0.0.127.255
rule 35 permit 10.210.128.0 0.0.127.255
rule 40 permit 10.37.192.0 0.0.63.255
rule 45 permit 10.94.0.0 0.0.255.255
rule 50 permit 10.95.0.0 0.0.255.255
"""
    else:
        script += """
Inserir manualemnte, pois não se enquandra aos estados de RS, PR ou SC
"""
    script += f"""rule 500 deny any
$
ntp enable
ntp authenticate
ntp source interface loopback100
ntp access-group ipv4-access-list NTP
ntp authentication-key 6 md5 clear NTP6%@backbone
ntp trusted-key 6
ntp master 12
"""
    for i, ip in enumerate(ntp_ips, start=1):
        script += f"ntp server {ip} priority {i} key 6\n"

    script += """
$
$ ========================================
$ PTP UNICAST
$ ========================================
$
ptp
enable
domain 0
state-algorithm bmc
free-mode
port interface loopback100 portnum 2
enable
network-protocol ipv4
transmit-mode unicast
manual-port-state slave
sync-interval -6
delay-req-interval -6
"""
    separador_ptp = []
    for i, ip in enumerate(ptp_ips, start=1):
        separador_ptp.append(f"acceptmasterip {ip}")

    script += "\n".join(separador_ptp)
    script += f""" 
$
$
$
ssm
usessm
synchronization-clock 1588
priority 1588 1
port-receive-mode manual-ssm 1588
receive-quality 1588 2
$
$
$ ========================================
$ SNMP / SYSLOG / NETCONF
$ ========================================
$
ipv4-access-list 1301
rule 5 permit 192.168.32.247 0.0.0.0
rule 6 permit 192.168.32.248 0.0.0.0
rule 7 permit 192.168.32.249 0.0.0.0
rule 10 permit 10.129.97.128 0.0.0.31
rule 15 permit 10.108.198.0 0.0.0.255
rule 20 permit 10.129.198.0 0.0.0.255
rule 25 permit 10.221.198.0 0.0.0.255
rule 30 permit 10.199.10.0 0.0.0.255
rule 35 permit 10.199.26.0 0.0.0.255
rule 40 permit 10.129.71.64 0.0.0.31
rule 45 permit 10.108.199.0 0.0.0.255
rule 50 permit 10.129.199.0 0.0.0.255
rule 55 permit 10.221.199.0 0.0.0.255
rule 60 permit 10.199.8.0 0.0.0.255
rule 65 permit 10.199.24.0 0.0.0.255
rule 70 permit 10.0.10.150 0.255.0.0
rule 75 permit 10.0.10.152 0.255.0.0
rule 80 permit 10.129.72.0 0.0.0.255
rule 500 deny any
$
ipv4-access-list 1302
rule 10 permit 200.255.124.0 0.0.0.31
rule 20 permit 200.255.124.192 0.0.0.63
rule 500 deny any
$
snmp-server trap-source interface loopback100
snmp-server version v2c enable
snmp-server enable inform
snmp-server enable trap
snmp-server community CLAROIPRAN showclear view AllView ro ipv4-access-list 1301
snmp-server community ZENICONE-IP showclear view AllView ro ipv4-access-list 1301
snmp-server community IPRAN-EBT showclear view AllView ro ipv4-access-list 1302
snmp-server community Backbone-EBT showclear view AllView ro ipv4-access-list 1302
snmp-server host 10.129.72.179 trap version 2c ZENICONE-IP showclear udp-port 162
$
snetconf server enable
netconf agent enable
$
alarm netconf-report informational
logging trap-enable informational
syslog level warnings
syslog-server facility syslog
syslog-server host 10.221.199.31
syslog-server host 200.255.124.9
syslog-server host 200.255.124.25
syslog-server source interface loopback100
$
$
$ ========================================
$  VRF
$ =======================================
ip vrf GERENCIA
rd {bgp["processo"]}:61
mpls label mode per-vrf
address-family ipv4
route-target import {bgp["processo"]}:61
route-target export {bgp["processo"]}:61
  $
$
ip vrf ABIS
rd {bgp["processo"]}:103
  mpls label mode per-vrf
  address-family ipv4
route-target import {bgp["processo"]}:103
route-target export {bgp["processo"]}:103
  $
$
ip vrf IUB-DADOS
rd {bgp["processo"]}:1
  mpls label mode per-vrf
  address-family ipv4
route-target import {bgp["processo"]}:1
route-target export {bgp["processo"]}:1
  $
$        
ip vrf S1
rd {bgp["processo"]}:95
  mpls label mode per-vrf
  address-family ipv4
route-target import {bgp["processo"]}:95
route-target export {bgp["processo"]}:95
  $
$
ip vrf GERL3_EBT_CLARO
rd {bgp["processo"]}:7282
 mpls label mode per-vrf
address-family ipv4
route-target import {bgp["processo"]}:7281
route-target export {bgp["processo"]}:7282
  $
$
"""
    if fibra:
        script += """
$ ========================================
$ QoS NNI
$ =======================================
class-map child match-any
match child
$
class-map PHB20_DEFAULT_IN traffic-based match-any
match dscp reserved-words default
match mpls-exp 0
$
class-map PHB20_MOVEL_IN traffic-based match-any
match dscp reserved-words af11
match dscp reserved-words cs1
match mpls-exp 1
$
class-map PHB20_DCR_IN traffic-based match-any
match dscp reserved-words af21
match dscp reserved-words cs2
match mpls-exp 2
$
class-map PHB20_VIDEO_IN traffic-based match-any
match dscp reserved-words af31
match dscp reserved-words cs3
match mpls-exp 3
$
class-map PHB20_GPRS_IN traffic-based match-any
match dscp reserved-words af41
match dscp reserved-words cs4
match mpls-exp 4
$
class-map PHB20_RT_IN traffic-based match-any
match dscp reserved-words ef
match dscp reserved-words cs5
match mpls-exp 5
$
class-map PHB20_SIG_IN traffic-based match-any
match dscp range 62
match dscp reserved-words cs6
match mpls-exp 6
$
class-map PHB20_RT_SYNC_IN traffic-based match-any
match dscp reserved-words cs7
match mpls-exp 7
$
class-map PHB20_RT_SYNC_OUT match-any
match service-class cs7
$
class-map PHB20_SIG_OUT match-any
match service-class cs6
$
class-map PHB20_RT_OUT match-any
match service-class ef
$
class-map PHB20_GPRS_OUT match-any
match service-class af4
$
class-map PHB20_VIDEO_OUT match-any
match service-class af3
$
class-map PHB20_DCR_OUT match-any
match service-class af2
$
class-map PHB20_MOVEL_OUT match-any
match service-class af1
$
class-map PHB20_DEFAULT_OUT match-any
match service-class be
$
$
policy-map PHB20_IN traffic-based unshared
class PHB20_DEFAULT_IN
set service-class be
statistics enable
$
class PHB20_MOVEL_IN
set service-class af1
statistics enable
$
class PHB20_DCR_IN
set service-class af2
statistics enable
$
class PHB20_VIDEO_IN
set service-class af3
statistics enable
$
class PHB20_GPRS_IN
set service-class af4
statistics enable
$
class PHB20_RT_IN
set service-class ef
statistics enable
$
class PHB20_SIG_IN
set service-class cs6
statistics enable
$
class PHB20_RT_SYNC_IN
set service-class cs7
statistics enable
$
$
$
policy-map PHB20_1G_OUT
class PHB20_RT_SYNC_OUT
police cir percentage 5
priority-level 1
$
class PHB20_RT_OUT
police cir percentage 45
priority-level 1
$
class PHB20_SIG_OUT
bandwidth-remaining percent 15
priority-level 7
queue-limit 7500
$
class PHB20_VIDEO_OUT
bandwidth-remaining percent 15
priority-level 7
queue-limit 7500
$
class PHB20_GPRS_OUT
bandwidth-remaining percent 10
priority-level 7
queue-limit 12500
$
class PHB20_DCR_OUT
bandwidth-remaining percent 10
priority-level 7
queue-limit 12500
$
class PHB20_MOVEL_OUT
bandwidth-remaining percent 40
priority-level 7
queue-limit 12500
$
class PHB20_DEFAULT_OUT
bandwidth-remaining percent 10
priority-level 7
random-detect enable
random-detect color green 2500 7500 50
random-detect color red 2500 7500 50
random-detect color yellow 2500 7500 50
$
$
$
policy-map PHB20_10G_OUT
class PHB20_RT_SYNC_OUT
police cir percentage 5
priority-level 1
$
class PHB20_RT_OUT
police cir percentage 45
priority-level 1
$
class PHB20_SIG_OUT
bandwidth-remaining percent 15
priority-level 7
queue-limit 75000
$
class PHB20_VIDEO_OUT
bandwidth-remaining percent 15
priority-level 7
queue-limit 75000
$
class PHB20_GPRS_OUT
bandwidth-remaining percent 10
priority-level 7
queue-limit 125000
$
class PHB20_DCR_OUT
bandwidth-remaining percent 10
priority-level 7
queue-limit 125000
$
class PHB20_MOVEL_OUT
bandwidth-remaining percent 40
priority-level 7
queue-limit 125000
$
class PHB20_DEFAULT_OUT
bandwidth-remaining percent 10
priority-level 7
random-detect enable
random-detect color green 25000 75000 50
random-detect color red 25000 75000 50
random-detect color yellow 25000 75000 50
$
$
$
policy-map PHB20_100G_OUT
class PHB20_RT_SYNC_OUT
police cir percentage 5
priority-level 1
$
class PHB20_RT_OUT
police cir percentage 45
priority-level 1
$
class PHB20_SIG_OUT
bandwidth-remaining percent 15
priority-level 7
queue-limit 750000
$
class PHB20_VIDEO_OUT
bandwidth-remaining percent 15
priority-level 7
queue-limit 750000
$
class PHB20_GPRS_OUT
bandwidth-remaining percent 10
priority-level 7
queue-limit 1250000
$
class PHB20_DCR_OUT
bandwidth-remaining percent 10
priority-level 7
queue-limit 1250000
$
class PHB20_MOVEL_OUT
bandwidth-remaining percent 40
priority-level 7
queue-limit 1250000
$
class PHB20_DEFAULT_OUT
bandwidth-remaining percent 10
priority-level 7
random-detect enable
random-detect color green 250000 750000 50
random-detect color red 250000 750000 50
random-detect color yellow 250000 750000 50
$
$
$ ========================================
$ INTERFACES NNI FIBRA
$ =======================================
$
"""
    for i in range(len(fibra)):
            porta_fo = (portas10 if fibra[i].get('speed') == '10000' else portas1).pop(0 if fibra[i].get('speed') == '10000' else -1)
            portas_fo.append(porta_fo)
            if "description_bdi" in fibra[i]:
                script += f"""interface {porta_fo}
description {fibra[i]["description"]}
mtu {fibra[i]["mtu"]}
ip mtu {fibra[i]["mtu"]}
mpls mtu {fibra[i]["mtu"]}
negotiation negotiation-force
speed speed-{'10' if fibra[i].get('speed') == '10000'else '1'}G
no shutdown
$
interface {porta_fo}.{fibra[i]["bdi"]}
ip mtu {fibra[i]["mtu"]}
ip address {fibra[i]['ip_address']} {fibra[i]['mask']}
mpls mtu {fibra[i]["mtu"]}
no shutdown
$
$
service-policy {porta_fo} output PHB20_{ '10' if fibra[i].get('speed') == '10000' else '1'}G_OUT
traffic-policy interface {porta_fo} input PHB20_IN
$
qos-statistics switch on {porta_fo} output
traffic-policy-statistics switch on interface {porta_fo} input
$
$
"""
            else:
                script += f"""interface {porta_fo}
description {fibra[i]["description"]}
mtu {fibra[i]["mtu"]}
ip mtu {fibra[i]["mtu"]}
ip address {fibra[i]['ip_address']} {fibra[i]['mask']}
mpls mtu {fibra[i]["mtu"]}
negotiation negotiation-force
speed speed-{'10' if fibra[i].get('speed') == '10000'else '1'}G
no shutdown
$
$
service-policy {porta_fo} output PHB20_{ '10' if fibra[i].get('speed') == '10000' else '1'}G_OUT
traffic-policy interface {porta_fo} input PHB20_IN
$
qos-statistics switch on {porta_fo} output
traffic-policy-statistics switch on interface {porta_fo} input
$
$
"""
    if any(not i["bnm_ativo"] for i in mwrot):
        script += f"""$ ========================================
$ QOS RADIO - SEM BNM
$ ======================================="""

    for i in range(len(mwrot)):
        if not mwrot[i]["bnm_ativo"]:
            script += f"""
policy-map PHB20_{mwrot[i]["bandwidth_mbps"]}M_OUT
class child
police cir {mwrot[i]["bandwidth"]} pir {mwrot[i]["bandwidth"]}
service-policy PHB20_{'10' if mwrot[i].get('speed') == '10000' else '1'}G_OUT
$
$
$"""
    if any(i["bnm_ativo"] for i in mwrot):
            script += f"""
$ ========================================
$ QOS RADIO - COM BNM
$ =======================================
policy-map PHB20_BNM_1G_OUT
class child
police cir percentage 95
service-policy PHB20_1G_OUT
$
$
policy-map PHB20_BNM_10G_OUT
class child
police cir percentage 95
service-policy PHB20_10G_OUT
$"""
    if mwrot:
        script += f"""
$========================================
$ INTERFACES NNI RADIO
$=======================================
$"""
        contadorBNM = 0  # Inicializa o contador
        for x in range(len(mwrot)):
            porta_mwrot = (portas10 if mwrot[x].get('speed') == '10000' else portas1).pop(0 if mwrot[x].get('speed') == '10000' else -1)
            portas_mwrot.append(porta_mwrot)

#Se tiver dot1q vai adicionar o IP na logica

            if mwrot[x]["porta_logica"]:
                if mwrot[x]["porta_logica"]["bdi"] in mwrot[x]["dot1qs"]:
                    script += f"""
interface {porta_mwrot}
description {mwrot[x]["porta_logica"]["description"]}
mtu {mwrot[x]["mtu"]}
ip mtu {mwrot[x]["porta_logica"]["mtu"]}
mpls mtu {mwrot[x]["porta_logica"]["mtu"]}
negotiation negotiation-force
speed speed-{'10' if mwrot[x].get('speed') == '10000' else '1'}G
no shutdown
$
interface {porta_mwrot}.{mwrot[x]["porta_logica"]["bdi"]}
description {mwrot[x]["porta_logica"]["description"]}
mtu {mwrot[x]["porta_logica"]["mtu"]}
ip address {mwrot[x]["porta_logica"]["ip_address"]} {mwrot[x]["porta_logica"]["mask"]}
ip mtu {mwrot[x]["porta_logica"]["mtu"]}
mpls mtu {mwrot[x]["porta_logica"]["mtu"]}
no shutdown
$
$
vlan-configuration
interface {porta_mwrot}.{mwrot[x]["porta_logica"]["bdi"]}
encapsulation-dot1q {mwrot[x]["porta_logica"]["bdi"]}
$
$
$
intf-statistics
interface {porta_mwrot}.{mwrot[x]["porta_logica"]["bdi"]}
traffic-statistics enable
$
$
$
service-policy {porta_mwrot}.{mwrot[x]["porta_logica"]["bdi"]} output PHB20_BNM_{ '10' if mwrot[x].get('speed') == '10000' else '1'}G_OUT
traffic-policy interface {porta_mwrot}.{mwrot[x]["porta_logica"]["bdi"]} input PHB20_IN
$
qos-statistics switch on {porta_mwrot}.{mwrot[x]["porta_logica"]["bdi"]} output
traffic-policy-statistics switch on interface {porta_mwrot}.{mwrot[x]["porta_logica"]["bdi"]} input
$"""            
                else:
                    script += f"""
interface {porta_mwrot}
description {mwrot[x]["porta_logica"]["description"]}
mtu {mwrot[x]["mtu"]}
ip address {mwrot[x]["porta_logica"]["ip_address"]} {mwrot[x]["porta_logica"]["mask"]}
ip mtu {mwrot[x]["porta_logica"]["mtu"]}
mpls mtu {mwrot[x]["porta_logica"]["mtu"]}
negotiation negotiation-force
speed speed-{'10' if mwrot[x].get('speed') == '10000' else '1'}G
no shutdown
$
$
intf-statistics
interface {porta_mwrot}
traffic-statistics enable
$
$
$
service-policy {porta_mwrot} output PHB20_BNM_{ '10' if mwrot[x].get('speed') == '10000' else '1'}G_OUT
traffic-policy interface {porta_mwrot} input PHB20_IN
$
qos-statistics switch on {porta_mwrot} output
traffic-policy-statistics switch on interface {porta_mwrot} input"""
            if mwrot[x]["porta_gerencia"]:
                script += f"""
interface {porta_mwrot}.{mwrot[x]["porta_gerencia"]["bdi"]}
description {mwrot[x]["porta_gerencia"]["description"]}
ip vrf forwarding GERENCIA
ip address {mwrot[x]["porta_gerencia"]["ip_address"]} {mwrot[x]["porta_gerencia"]["mask"]}
no shutdown
$
$
vlan-configuration
interface {porta_mwrot}.{mwrot[x]["porta_gerencia"]["bdi"]}
encapsulation-dot1q {mwrot[x]["porta_gerencia"]["dot1q"]}
$
$
$
intf-statistics
interface {porta_mwrot}.{mwrot[x]["porta_gerencia"]["bdi"]}
traffic-statistics enable
$
$"""
            if mwrot[x]["bnm_ativo"]:
                contadorBNM += 1
                if mwrot[x]["porta_logica"]:
                    if mwrot[x]["porta_logica"]["bdi"] in mwrot[x]["dot1qs"]:
                        script += f"""
$========================================
$ BNM   
$=======================================
cfm
set cfm enable
create md index {contadorBNM} name-format 4 name {mwrot[x]["bridge_domains"][0]} level 3
md index {contadorBNM}
create ma index {contadorBNM} name-format 2 name ACM{mwrot[x]["bridge_domains"][0]} vid {mwrot[x]["bridge_domains"][0]}
ma index {contadorBNM}
set ccminterval 5
create rmep mepid {int(mwrot[x]["bridge_domains"][0]) - 1}
set mep {int(mwrot[x]["bridge_domains"][0]) - 1} state enable
create mep mepid {mwrot[x]["porta_logica"]["bdi"]} direction down interface {porta_mwrot}.{mwrot[x]["porta_logica"]["bdi"]}
set mep {mwrot[x]["bridge_domains"][0]} state enable
set mep {mwrot[x]["bridge_domains"][0]} bnm service-policy-adjust enable
set mep {mwrot[x]["bridge_domains"][0]} ccm-send enable
set mep {mwrot[x]["bridge_domains"][0]} client-level 4
$
$"""
                    else:
# Interface física (sem dot1q)
                        script += f"""
$========================================
$ BNM   
$=======================================
cfm
set cfm enable
create md index {contadorBNM} name-format 4 name {mwrot[x]["bridge_domains"][0]} level 3
md index {contadorBNM}
create ma index {contadorBNM} name-format 2 name ACM{mwrot[x]["bridge_domains"][0]} vid {mwrot[x]["bridge_domains"][0]}
ma index {contadorBNM}
set ccminterval 5
create rmep mepid {int(mwrot[x]["bridge_domains"][0]) - 1}
set mep {int(mwrot[x]["bridge_domains"][0]) - 1} state enable
create mep mepid {mwrot[x]["bridge_domains"][0]} direction down interface {porta_mwrot}
set mep {mwrot[x]["bridge_domains"][0]} state enable
set mep {mwrot[x]["bridge_domains"][0]} bnm service-policy-adjust enable
set mep {mwrot[x]["bridge_domains"][0]} ccm-send enable
set mep {mwrot[x]["bridge_domains"][0]} client-level 4
$
$"""
    script += f"""
$========================================
$ OSPF
$========================================
$
router ospf {processo_ospf}
router-id {ip_loopback}
timers throttle spf 10 100 1000
timers throttle lsa-arrival 0 25 1000
timers throttle lsa 1 25 1000
timers lsa-group-pacing 10
passive-interface default"""
    for x in range(len(portas_fo)):
        script += f"""
passive-interface {portas_fo[x]} disable"""
    for x in range(len(portas_mwrot)):
        if mwrot[x]["porta_logica"]:
            mwrot[x]["porta_logica"]["bdi"] = mwrot[x]["porta_logica"]["bdi"]
            if mwrot[x]["porta_logica"]["bdi"] in mwrot[x]["dot1qs"]:
# Subinterface com dot1q
                    script += f"""
passive-interface {portas_mwrot[x]}.{mwrot[x]["porta_logica"]["bdi"]} disable"""
            else:
# Interface física (sem dot1q)
                script += f"""
passive-interface {portas_mwrot[x]} disable"""
    script += f"""
max-metric router-lsa on-startup timeout 240
ispf
auto-cost reference-bandwidth 100000
nsf
maximum-paths 16
mpls ldp auto-config
segment-routing mpls enable
te-link-bandwidth enable
te-link-delay enable
area {area_ospf_formatada}
authentication message-digest
mpls traffic-eng
mpls ldp sync
interface loopback100
$"""
    for x in range(len(portas_fo)):
        script += f"""
interface {portas_fo[x]}
bfd interval 100 min-rx 100 multiplier 3
network point-to-point
message-digest-key 1 md5 BaCkBoNeOSPF!#@$
cost {fibra[x]["ospf_cost"]}
mtu-ignore
$"""
    for x in range(len(portas_mwrot)):
        if mwrot[x]["porta_logica"]:
            mwrot[x]["porta_logica"]["bdi"] = mwrot[x]["porta_logica"]["bdi"]
            if mwrot[x]["porta_logica"]["bdi"] in mwrot[x]["dot1qs"]:
# Subinterface com dot1q
                    script += f"""
interface {portas_mwrot[x]}.{mwrot[x]["porta_logica"]["bdi"]}
bfd interval 100 min-rx 100 multiplier 3
network point-to-point
message-digest-key 1 md5 BaCkBoNeOSPF!#@$
cost {mwrot[x]["porta_logica"]["ospf_cost"]}
mtu-ignore
$"""
            else:
# Interface física (sem dot1q)
                script += f"""
interface {portas_mwrot[x]}
bfd interval 100 min-rx 100 multiplier 3
network point-to-point
message-digest-key 1 md5 BaCkBoNeOSPF!#@$
cost {mwrot[x]["porta_logica"]["ospf_cost"]}
mtu-ignore
$"""
    script += f"""
$ ========================================
$ BGP
$ =======================================
route-map MARCA-COMMUNITY-REGIAO-IPV4 permit 10
set community additive {bgp["processo"]}:{processo_ospf}
set mpls-label
$
$
router bgp {bgp["processo"]}
bgp router-id {ip_loopback}
synchronization disable
bgp graceful-restart
bgp nexthop trigger delay 1
maximum-paths 2
network {ip_loopback} 255.255.255.255 route-map MARCA-COMMUNITY-REGIAO-IPV4
neighbor CSG-AGG peer-group
neighbor CSG-AGG remote-as {bgp["processo"]}
neighbor CSG-AGG activate
neighbor CSG-AGG next-hop-self
neighbor CSG-AGG send-community
neighbor CSG-AGG send-label
neighbor CSG-AGG update-source loopback100
neighbor CSG-AGG password BaCkBoNeBGP!#@$
neighbor CSG-AGG tracking"""
    for i in range(len(bgp["ips_vizinhos"])):
        script += f"""
neighbor {bgp["ips_vizinhos"][i]} peer-group CSG-AGG"""
    script += f"""
address-family vpnv4
bgp nexthop recursive-lookup default-route disable
neighbor CSG-AGG activate
neighbor CSG-AGG send-community
$
address-family vpnv6
bgp nexthop recursive-lookup default-route disable
neighbor CSG-AGG activate
neighbor CSG-AGG send-community
$
address-family ipv4 mdt"""
    for i in range(len(bgp["ips_vizinhos"])):
        script += f"""
neighbor {bgp["ips_vizinhos"][i]} activate
neighbor {bgp["ips_vizinhos"][i]} send-community"""
#Rota estática
    if rotas_estaticas:
        script += """
$====================================================================
$ ROTAS ESTATICAS
$===================================================================="""
        for rota in rotas_estaticas:
            if rota["vrf"]:
                script += f"""
ip route vrf {rota["vrf"]} {rota["ip_origem"]} {rota["mask"]} {rota["ip_destino"]}"""
            else:
                script += f"""
ip route {rota["ip_origem"]} {rota["mask"]} {rota["ip_destino"]}"""
    script += f"""
$
$ ========================================
$ MPLS / MULTICAST / TRAFFIC-EN
$ =======================================
$
mpls ldp instance 1
access-fec ip-prefix host-route-only
graceful-restart
igp sync delay 5
session protection duration 86400
router-id loopback100
mldp
$
"""
    for x in range(len(portas_fo)):
        script += f"""interface {portas_fo[x]}
$
"""
    for x in range(len(portas_mwrot)):
        if mwrot[x]["porta_logica"]:
            mwrot[x]["porta_logica"]["bdi"] = mwrot[x]["porta_logica"]["bdi"]
            if mwrot[x]["porta_logica"]["bdi"] in mwrot[x]["dot1qs"]:
# Subinterface com dot1q
                    script += f"""interface {portas_mwrot[x]}.{mwrot[x]["porta_logica"]["bdi"]}
$
"""
            else:
# Interface física (sem dot1q)
                script += f"""interface {portas_mwrot[x]}
$
"""
    script += f"""$
$
$
mpls l2vpn enable
$
$
ipv4-access-list ACL_MCAST_SSM
rule 5 permit 239.233.0.0 0.0.255.255
description rule 5 "MDT DEFAULT"
rule 10 permit 239.233.0.0 0.0.0.255
description rule 10 "MDT DATA"
rule 100 deny any
$
$
ip multicast-routing
multipath s-g-hash next-hop-based
router pim
ssm enable
ssm range group-list ACL_MCAST_SSM
interface loopback100
pimsm
$
"""
    for x in range(len(portas_fo)):
        script += f"""interface {portas_fo[x]}
pimsm
hello-interval 1
$
"""
    for x in range(len(portas_mwrot)):
        if mwrot[x]["porta_logica"]:
            mwrot[x]["porta_logica"]["bdi"] = mwrot[x]["porta_logica"]["bdi"]
            if mwrot[x]["porta_logica"]["bdi"] in mwrot[x]["dot1qs"]:
# Subinterface com dot1q
                    script += f"""interface {portas_mwrot[x]}.{mwrot[x]["porta_logica"]["bdi"]}
pimsm
hello-interval 1
$
"""
            else:
# Interface física (sem dot1q)
                script += f"""interface {portas_mwrot[x]}
pimsm
hello-interval 1
$
"""
    script += f"""$
$
mpls traffic-eng
router-id {ip_loopback}
cspf delay link-up 30
cspf delay switch-over 30
reoptimize events link-up
reoptimize timers delay installation-delay-time 60
reoptimize timers frequency 3600
unactive timer 30
interface loopback100
$
"""
    for x in range(len(portas_fo)):
        script += f"""interface {portas_fo[x]}
$
"""
    for x in range(len(portas_mwrot)):
        if mwrot[x]["porta_logica"]:
            mwrot[x]["porta_logica"]["bdi"] = mwrot[x]["porta_logica"]["bdi"]
            if mwrot[x]["porta_logica"]["bdi"] in mwrot[x]["dot1qs"]:
# Subinterface com dot1q
                    script += f"""interface {portas_mwrot[x]}.{mwrot[x]["porta_logica"]["bdi"]}
$
"""
            else:
# Interface física (sem dot1q)
                script += f"""interface {portas_mwrot[x]}
$
"""
#QOS MOVEL
    if movel:
        script += f"""$====================================================================
$ BGP - SERVICO MOVEL
$====================================================================
router bgp {bgp["processo"]}
address-family ipv4 vrf GERL3_EBT_CLARO
redistribute connected
$
address-family ipv4 vrf GERENCIA
redistribute connected
{"redistribute static" if any(rota["vrf"] == "GERENCIA" for rota in rotas_estaticas) else ""}
$
address-family ipv4 vrf ABIS
redistribute connected
$
address-family ipv4 vrf IUB-DADOS
redistribute connected
$
address-family ipv4 vrf S1
redistribute connected
$
$
$====================================================================
$ QoS 2G
$====================================================================
$
class-map child match-any
match child
$
class-map TC20_2G_SIG_IN traffic-based match-any
match dscp range 48,62
match dscp reserved-words cs6
$
class-map TC20_2G_RT_IN traffic-based match-any
match dscp range 40,46
match dscp reserved-words ef
match dscp reserved-words cs5
$
class-map TC20_2G_GPRS_IN traffic-based match-any
match dscp range 0-63
$
$
class-map TC20_2G_SIG_OUT match-any
match service-class cs6
$
class-map TC20_2G_RT_OUT match-any
match service-class ef
$
class-map TC20_2G_GPRS_OUT match-any
match service-class af4
$
$
policy-map TC20_2G_IN traffic-based unshared
class TC20_2G_SIG_IN
set service-class cs6
statistics enable
$
class TC20_2G_RT_IN
set service-class ef
statistics enable
$
class TC20_2G_GPRS_IN
set service-class af4
statistics enable
$
$
policy-map TC20_2G_1G_OUT1
class TC20_2G_RT_OUT
police cir percentage 50
priority-level 1
$
class TC20_2G_SIG_OUT
bandwidth-remaining percent 15
priority-level 3
queue-limit 7500
$
class TC20_2G_GPRS_OUT
bandwidth-remaining percent 85
priority-level 3
queue-limit 12500
$
$
policy-map TC20_2G_1G_OUT
class child
police cir percentage 95
service-policy TC20_2G_1G_OUT1
$
$
policy-map TC20_2G_10G_OUT1
class TC20_2G_RT_OUT
police cir percentage 50
priority-level 1
$
class TC20_2G_SIG_OUT
bandwidth-remaining percent 15
priority-level 3
queue-limit 75000
$
class TC20_2G_GPRS_OUT
bandwidth-remaining percent 85
priority-level 3
queue-limit 125000
$
$
policy-map TC20_2G_10G_OUT
class child
police cir percentage 95
service-policy TC20_2G_10G_OUT1
$
$
$====================================================================
$ QoS 3G
$====================================================================
$
class-map child match-any
match child
$
class-map TC20_3G_SIG_IN traffic-based match-any
match dscp range 48,62
match dscp reserved-words cs6
$
class-map TC20_3G_RT_IN traffic-based match-any
match dscp range 40,46
match dscp reserved-words ef
match dscp reserved-words cs5
$
class-map TC20_3G_GPRS_IN traffic-based match-any
match dscp range 0-63
$
$
class-map TC20_3G_SIG_OUT match-any
match service-class cs6
$
class-map TC20_3G_RT_OUT match-any
match service-class ef
$
class-map TC20_3G_GPRS_OUT match-any
match service-class af4
$
$
policy-map TC20_3G_IN traffic-based unshared
class TC20_3G_SIG_IN
set service-class cs6
statistics enable
$
class TC20_3G_RT_IN
set service-class ef
statistics enable
$
class TC20_3G_GPRS_IN
set service-class af4
statistics enable
$
$
policy-map TC20_3G_1G_OUT1
class TC20_3G_RT_OUT
police cir percentage 50
priority-level 1
$
class TC20_3G_SIG_OUT
bandwidth-remaining percent 15
priority-level 3
queue-limit 7500
$
class TC20_3G_GPRS_OUT
bandwidth-remaining percent 85
priority-level 3
queue-limit 12500
$
$
policy-map TC20_3G_1G_OUT
class child
police cir percentage 95
service-policy TC20_3G_1G_OUT1
$
$
policy-map TC20_3G_10G_OUT1
class TC20_3G_RT_OUT
police cir percentage 50
priority-level 1
$
class TC20_3G_SIG_OUT
bandwidth-remaining percent 15
priority-level 3
queue-limit 75000
$
class TC20_3G_GPRS_OUT
bandwidth-remaining percent 85
priority-level 3
queue-limit 125000
$
$
policy-map TC20_3G_10G_OUT
class child
police cir percentage 95
service-policy TC20_3G_10G_OUT1
$
$
$====================================================================
$ QoS 4G
$====================================================================
$
class-map child match-any
match child
$
class-map TC20_4G_SIG_IN traffic-based match-any
match dscp range 40,48,62
match dscp reserved-words cs5
match dscp reserved-words cs6
$
class-map TC20_4G_RT_IN traffic-based match-any
match dscp range 46
match dscp reserved-words ef
$
class-map TC20_4G_VIDEO_IN traffic-based match-any
match dscp range 32,34,36,38
match dscp reserved-words cs4
match dscp reserved-words af41
match dscp reserved-words af42
match dscp reserved-words af43
$
class-map TC20_4G_MOVEL_IN traffic-based match-any
match dscp range 0-63
$
$
class-map TC20_4G_SIG_OUT match-any
match service-class cs6
$
class-map TC20_4G_RT_OUT match-any
match service-class ef
$
class-map TC20_4G_VIDEO_OUT match-any
match service-class af3
$
class-map TC20_4G_MOVEL_OUT match-any
match service-class af1
$
$
policy-map TC20_4G_IN traffic-based unshared
class TC20_4G_SIG_IN
set service-class cs6
statistics enable
$
class TC20_4G_RT_IN
set service-class ef
statistics enable
$
class TC20_4G_VIDEO_IN
set service-class af3
statistics enable
$
class TC20_4G_MOVEL_IN
set service-class af1
statistics enable
$
$
policy-map TC20_4G_1G_OUT1
class TC20_4G_RT_OUT
police cir percentage 50
priority-level 1
$
class TC20_4G_SIG_OUT
bandwidth-remaining percent 10
priority-level 3
queue-limit 12500
$
class TC20_4G_VIDEO_OUT
bandwidth-remaining percent 20
priority-level 3
queue-limit 12500
$
class TC20_4G_MOVEL_OUT
bandwidth-remaining percent 70
priority-level 3
queue-limit 12500
$
$
policy-map TC20_4G_1G_OUT
class child
police cir percentage 95
service-policy TC20_4G_1G_OUT1
$
$
policy-map TC20_4G_10G_OUT1
class TC20_4G_RT_OUT
police cir percentage 50
priority-level 1
$
class TC20_4G_SIG_OUT
bandwidth-remaining percent 10
priority-level 3
queue-limit 125000
$
class TC20_4G_VIDEO_OUT
bandwidth-remaining percent 20
priority-level 3
queue-limit 125000
$
class TC20_4G_MOVEL_OUT
bandwidth-remaining percent 70
priority-level 3
queue-limit 125000
$
$
policy-map TC20_4G_10G_OUT
class child
police cir percentage 95
service-policy TC20_4G_10G_OUT1
$
$
$====================================================================
$ QoS 5G
$====================================================================
$
class-map child match-any
match child
$
class-map TC20_5G_SIG_IN traffic-based match-any
match dscp range 40,48,62
match dscp reserved-words cs5
match dscp reserved-words cs6
$
class-map TC20_5G_RT_IN traffic-based match-any
match dscp range 46
match dscp reserved-words ef
$
class-map TC20_5G_VIDEO_IN traffic-based match-any
match dscp range 32,34,36,38
match dscp reserved-words cs4
match dscp reserved-words af41
match dscp reserved-words af42
match dscp reserved-words af43
$
class-map TC20_5G_MOVEL_IN traffic-based match-any
match dscp range 0-63
$
$
class-map TC20_5G_SIG_OUT match-any
match service-class cs6
$
class-map TC20_5G_RT_OUT match-any
match service-class ef
$
class-map TC20_5G_VIDEO_OUT match-any
match service-class af3
$
class-map TC20_5G_MOVEL_OUT match-any
match service-class af1
$
$
policy-map TC20_5G_IN traffic-based unshared
class TC20_5G_SIG_IN
set service-class cs6
statistics enable
$
class TC20_5G_RT_IN
set service-class ef
statistics enable
$
class TC20_5G_VIDEO_IN
set service-class af3
statistics enable
$
class TC20_5G_MOVEL_IN
set service-class af1
statistics enable
$
$
policy-map TC20_5G_1G_OUT1
class TC20_5G_RT_OUT
police cir percentage 50
priority-level 1
$
class TC20_5G_SIG_OUT
bandwidth-remaining percent 10
priority-level 3
queue-limit 12500
$
class TC20_5G_VIDEO_OUT
bandwidth-remaining percent 20
priority-level 3
queue-limit 12500
$
class TC20_5G_MOVEL_OUT
bandwidth-remaining percent 70
priority-level 3
queue-limit 12500
$
$
policy-map TC20_5G_1G_OUT
class child
police cir percentage 95
service-policy TC20_5G_1G_OUT1
$
$
policy-map TC20_5G_10G_OUT1
class TC20_5G_RT_OUT
police cir percentage 50
priority-level 1
$
class TC20_5G_SIG_OUT
bandwidth-remaining percent 10
priority-level 3
queue-limit 125000
$
class TC20_5G_VIDEO_OUT
bandwidth-remaining percent 20
priority-level 3
queue-limit 125000
$
class TC20_5G_MOVEL_OUT
bandwidth-remaining percent 70
priority-level 3
queue-limit 125000
$
$
policy-map TC20_5G_10G_OUT
class child
police cir percentage 95
service-policy TC20_5G_10G_OUT1
$
$
$ ====================================================================
$ QoS GERENCIA MOVEL
$ ====================================================================
$
class-map TC20_GERENCIA_MOVEL_RT_SYNC_IN traffic-based match-any
  match dscp range 46,56
  match dscp reserved-words ef
  match dscp reserved-words cs7
$
class-map TC20_GERENCIA_MOVEL_DCR_IN traffic-based match-any
  match dscp range 0-63
$
$
class-map TC20_GERENCIA_MOVEL_RT-SYNC_OUT match-any
  match service-class cs7
$
class-map TC20_GERENCIA_MOVEL_DCR_OUT match-any
  match service-class af2
$
$
policy-map TC20_GERENCIA_MOVEL_IN traffic-based unshared
  class TC20_GERENCIA_MOVEL_RT_SYNC_IN
    set service-class cs7
    statistics enable
  $
  class TC20_GERENCIA_MOVEL_DCR_IN
    set service-class af2
    statistics enable
  $
$
policy-map TC20_GERENCIA_MOVEL_50M_OUT1
class TC20_GERENCIA_MOVEL_RT-SYNC_OUT
police cir percentage 50
priority-level 1
$
class TC20_GERENCIA_MOVEL_DCR_OUT
queue-limit 625
$
$
policy-map TC20_GERENCIA_MOVEL_50M_OUT
class child
police cir percentage 5
service-policy TC20_GERENCIA_MOVEL_50M_OUT1
$
$
policy-map TC20_GERENCIA_MOVEL_500M_OUT1
class TC20_GERENCIA_MOVEL_RT-SYNC_OUT
police cir percentage 50
priority-level 1
$
class TC20_GERENCIA_MOVEL_DCR_OUT
queue-limit 6250
$
$
policy-map TC20_GERENCIA_MOVEL_500M_OUT
class child
police cir percentage 5
service-policy TC20_GERENCIA_MOVEL_500M_OUT1
$
$
"""
    for x in range(len(movel)):
        porta_movel = (portas10 if movel[x].get('speed') == '10000' else portas1).pop(0)
        portas_movel.append(porta_movel)
        script += f"""$====================================================================
$ SERVIÇOS MOVEIS INTERFACE FISICA
$====================================================================
$
interface {porta_movel}
description {movel[x]["description"]}
negotiation negotiation-force
speed speed-{'10' if movel[x].get('speed') == '10000'else '1'}G
no shutdown
$
"""
        for y in range(len(movel[x]["bdis"])):
            if movel[x]["bdis"][y]["tipo_servico"] == "2G":
                script += f"""$====================================================================
$ CONFIGURAÇÃO 2G ABIS
$====================================================================
interface {porta_movel}.{movel[x]["bdis"][y]["bridge_domain"]}
description {movel[x]["bdis"][y]["description"]}
ip vrf forwarding ABIS
ip address {movel[x]["bdis"][y]["ip_address"]} {movel[x]["bdis"][y]["mask"]}
no shutdown
$
vlan-configuration
interface {porta_movel}.{movel[x]["bdis"][y]["bridge_domain"]}
encapsulation-dot1q {movel[x]["bdis"][y]["dot1q"]}
$
$
traffic-policy interface {porta_movel}.{movel[x]["bdis"][y]["bridge_domain"]} input TC20_2G_IN
$
service-policy {porta_movel}.{movel[x]["bdis"][y]["bridge_domain"]} output TC20_2G_{'100M' if movel[x].get('speed') == '100' else f"{str(int(movel[x].get('speed')) // 1000)}G"}_OUT
$
intf-statistics
interface {porta_movel}.{movel[x]["bdis"][y]["bridge_domain"]}
traffic-statistics enable
$
$
qos-statistics switch on {porta_movel}.{movel[x]["bdis"][y]["bridge_domain"]} output
$
traffic-policy-statistics switch on interface {porta_movel}.{movel[x]["bdis"][y]["bridge_domain"]} input
$
$
$
"""        
            if movel[x]["bdis"][y]["tipo_servico"] == "3G":
                script += f"""$====================================================================
$ CONFIGURAÇÃO 3G IUB-DADOS
$====================================================================
interface {porta_movel}.{movel[x]["bdis"][y]["bridge_domain"]}
description {movel[x]["bdis"][y]["description"]}
ip vrf forwarding IUB-DADOS
ip address {movel[x]["bdis"][y]["ip_address"]} {movel[x]["bdis"][y]["mask"]}
no shutdown
$
vlan-configuration
interface {porta_movel}.{movel[x]["bdis"][y]["bridge_domain"]}
encapsulation-dot1q {movel[x]["bdis"][y]["dot1q"]}
$
$
traffic-policy interface {porta_movel}.{movel[x]["bdis"][y]["bridge_domain"]} input TC20_3G_IN
$
service-policy {porta_movel}.{movel[x]["bdis"][y]["bridge_domain"]} output TC20_3G_{'100M' if movel[x].get('speed') == '100' else f"{str(int(movel[x].get('speed')) // 1000)}G"}_OUT
$
intf-statistics
interface {porta_movel}.{movel[x]["bdis"][y]["bridge_domain"]}
traffic-statistics enable
$
$
qos-statistics switch on {porta_movel}.{movel[x]["bdis"][y]["bridge_domain"]} output
$
traffic-policy-statistics switch on interface {porta_movel}.{movel[x]["bdis"][y]["bridge_domain"]} input
$
$
$
"""        
            if movel[x]["bdis"][y]["tipo_servico"] == "4G":
                script += f"""$====================================================================
$ CONFIGURAÇÃO 4G S1
$====================================================================
interface {porta_movel}.{movel[x]["bdis"][y]["bridge_domain"]}
description {movel[x]["bdis"][y]["description"]}
ip vrf forwarding S1
ip address {movel[x]["bdis"][y]["ip_address"]} {movel[x]["bdis"][y]["mask"]}
no shutdown
$
vlan-configuration
interface {porta_movel}.{movel[x]["bdis"][y]["bridge_domain"]}
encapsulation-dot1q {movel[x]["bdis"][y]["dot1q"]}
$
$
traffic-policy interface {porta_movel}.{movel[x]["bdis"][y]["bridge_domain"]} input TC20_4G_IN
$
service-policy {porta_movel}.{movel[x]["bdis"][y]["bridge_domain"]} output TC20_4G_{'100M' if movel[x].get('speed') == '100' else f"{str(int(movel[x].get('speed')) // 1000)}G"}_OUT
$
intf-statistics
interface {porta_movel}.{movel[x]["bdis"][y]["bridge_domain"]}
traffic-statistics enable
$
$
qos-statistics switch on {porta_movel}.{movel[x]["bdis"][y]["bridge_domain"]} output
$
traffic-policy-statistics switch on interface {porta_movel}.{movel[x]["bdis"][y]["bridge_domain"]} input
$
$
$
"""
            if movel[x]["bdis"][y]["tipo_servico"] == "5G":
                script += f"""$====================================================================
$ CONFIGURAÇÃO 5G S1
$====================================================================
interface xxvgei-1/1/0/11.{movel[x]["bdis"][y]["bridge_domain"]}
description {movel[x]["bdis"][y]["description"]}
ip vrf forwarding S1
ip address {movel[x]["bdis"][y]["ip_address"]} {movel[x]["bdis"][y]["mask"]}
no shutdown
$
vlan-configuration
interface {porta_movel}.{movel[x]["bdis"][y]["bridge_domain"]}
encapsulation-dot1q {movel[x]["bdis"][y]["dot1q"]}
$
$
traffic-policy interface {porta_movel}.{movel[x]["bdis"][y]["bridge_domain"]} input TC20_5G_IN
$
service-policy {porta_movel}.{movel[x]["bdis"][y]["bridge_domain"]} output TC20_5G_{'100M' if movel[x].get('speed') == '100' else f"{str(int(movel[x].get('speed')) // 1000)}G"}_OUT
$
intf-statistics
interface {porta_movel}.{movel[x]["bdis"][y]["bridge_domain"]}
traffic-statistics enable
$
$
qos-statistics switch on {porta_movel}.{movel[x]["bdis"][y]["bridge_domain"]} output
$
traffic-policy-statistics switch on interface {porta_movel}.{movel[x]["bdis"][y]["bridge_domain"]} input
$
$
$
"""
            if movel[x]["bdis"][y]["tipo_servico"] == "GERENCIA":
                script += f"""$ ====================================================================
$ Configuracao Sub-interface GERENCIA e DHCP
$ ====================================================================
$
interface {porta_movel}.{movel[x]["bdis"][y]["bridge_domain"]}
description {movel[x]["bdis"][y]["description"]}
ip vrf forwarding GERENCIA
ip address {movel[x]["bdis"][y]["ip_address"]} {movel[x]["bdis"][y]["mask"]}
no shutdown
$
vlan-configuration
interface {porta_movel}.{movel[x]["bdis"][y]["bridge_domain"]}
encapsulation-dot1q {movel[x]["bdis"][y]["dot1q"]}
$
$
traffic-policy interface {porta_movel}.{movel[x]["bdis"][y]["bridge_domain"]} input TC20_GERENCIA_MOVEL_IN
$
service-policy {porta_movel}.{movel[x]["bdis"][y]["bridge_domain"]} output TC20_GERENCIA_MOVEL_{"500M" if str(int(movel[x]["speed"])//1000 ) == "10"  else "50M" }_OUT
$
intf-statistics
interface {porta_movel}.{movel[x]["bdis"][y]["bridge_domain"]}
traffic-statistics enable
$
$
traffic-policy-statistics switch on interface {porta_movel}.{movel[x]["bdis"][y]["bridge_domain"]} input
$
qos-statistics switch on {porta_movel}.{movel[x]["bdis"][y]["bridge_domain"]} output
$
"""
            if movel[x]["bdis"][y]["dhcp"]:
                script += "ip dhcp relay server group 1\n"
                for z in range(len(movel[x]["bdis"][y]["dhcp"])):
                    script +=f"server {z+1} {movel[x]["bdis"][y]["dhcp"][z]} vrf GERENCIA\n"
                script += f"""$       
dhcp
enable
interface {porta_movel}.{movel[x]["bdis"][y]["bridge_domain"]}
mode relay
relay server group 1
relay agent {movel[x]["bdis"][y]["ip_address"]}
$
$
"""
    if bateria:
        script += f"""$====================================================================
$ QoS GERENCIA BATERIA
$====================================================================
class-map TC20_ALL traffic-based match-any
match dscp range 0-63
$
policy-map TC20_GERENCIA_IN traffic-based unshared
class TC20_ALL
set service-class af2
statistics enable
$
$
class-map TC20_GERENCIA_OUT match-any
match service-class af2
$
policy-map TC20_GERENCIA_OUT
class TC20_GERENCIA_OUT
queue-limit 1250
$
$
policy-map TC20_GERENCIA_SHAPE_95Mbps_OUT
class child
police cir percentage 95
service-policy TC20_GERENCIA_OUT
$
$ 
$ ====================================================================
$ BATERIA
$ ====================================================================
"""
        for x in range(len(bateria)):
            porta_bateria = "xgei-1/1/0/5" if x == 0 else portas1.pop(0)
            portas_bateria. append(porta_bateria)
            script += f"""interface {porta_bateria}
description {bateria[x]["description"]}
mtu {bateria[x]["mtu"]}
ip vrf forwarding GERENCIA
ip address {bateria[x]["ip_address"]} {bateria[x]["mask"]}
pemode media-copper
negotiation negotiation-auto
speed speed-{'100M' if bateria[x].get('speed') == '100' else f"{str(int(bateria[x].get('speed')) // 1000)}G"}
no shutdown
$
traffic-policy interface {porta_bateria} input TC20_GERENCIA_IN
traffic-policy-statistics switch on interface {porta_bateria} input
service-policy {porta_bateria} output TC20_GERENCIA_SHAPE_95Mbps_OUT
qos-statistics switch on {porta_bateria} output
$
$
"""
    if empresarial:
        script += f"""$====================================================================
$ QoS EMPRESARIAL
$====================================================================
$
class-map VPN-GERENCIA match-any
match service-class af3
$
policy-map VPN-GERENCIA-512KBPS-IN
class VPN-GERENCIA
$
$
policy-map TC20-VPN-GERENCIA-512KBPS-IN
class child
police cir 517 pir 517
service-policy VPN-GERENCIA-512KBPS-IN
$
$
class-map TC20_GERL3_ALL traffic-based match-any
match dscp range 0-63
$
policy-map TC20-VPN-GERENCIA-CORP-IN traffic-based unshared
class TC20_GERL3_ALL
set service-class af3
statistics enable
$
$
$
$
class-map TC20_EoMPLS_ROUTING_IN traffic-based match-any
match dscp reserved-words cs6
$
class-map TC20_EoMPLS_RT_IN traffic-based match-any
match dscp reserved-words ef
$
class-map TC20_EoMPLS_VIDEO_IN traffic-based match-any
match dscp reserved-words cs4
match dscp reserved-words af41
match dscp reserved-words af42
match dscp reserved-words af43
$
class-map TC20_EoMPLS_DCR-2_IN traffic-based match-any
match dscp reserved-words cs3
match dscp reserved-words af31
match dscp reserved-words af32
match dscp reserved-words af33
$
class-map TC20_EoMPLS_DCR-1_IN traffic-based match-any
match dscp reserved-words cs1
match dscp reserved-words af11
match dscp reserved-words af12
match dscp reserved-words af13
match dscp reserved-words cs2
match dscp reserved-words af21
match dscp reserved-words af22
match dscp reserved-words af23
$
class-map TC20_EoMPLS_DEFAULT_IN traffic-based match-any
match dscp reserved-words default
$
$
policy-map TC20-EoMPLS-CIRCUITO-MARCA-IN traffic-based unshared
class TC20_EoMPLS_ROUTING_IN
set service-class cs6
statistics enable
$
class TC20_EoMPLS_RT_IN
set service-class ef
statistics enable
$
class TC20_EoMPLS_VIDEO_IN
set service-class af3
statistics enable
$
class TC20_EoMPLS_DCR-2_IN
set service-class af2
statistics enable
$
class TC20_EoMPLS_DCR-1_IN
set service-class af1
statistics enable
$
class TC20_EoMPLS_DEFAULT_IN
set service-class be
statistics enable
$
$
$
"""
        for x in range (len(empresarial)):  
            porta_edd = (portas10 if empresarial[i].get('speed') == '10000' else portas1).pop(0)
            portas_edd.append(porta_edd)
# Interface física
            script += f"""interface {porta_edd}
description {empresarial[x]['description']}
mtu {empresarial[x]['mtu']}
no shutdown
negotiation negotiation-auto
speed speed-{ '10' if empresarial[x].get('speed') == '10000' else '1'}G
$
$
"""
# GERENCIA
            for y in range (len(empresarial[x].get("servicos"))):
                if empresarial[x]["servicos"][y].get("tipo_servico") == "gerencia":
                    script += f"""interface {porta_edd}.{empresarial[x]["servicos"][y]['bridge_domain']}
description {empresarial[x]["servicos"][y]['bdi_description']}
ip vrf forwarding GERL3_EBT_CLARO
ip address {empresarial[x]["servicos"][y]['ip_address']} {empresarial[x]["servicos"][y]['mask']}
no shutdown
$
vlan-configuration
interface {porta_edd}.{empresarial[x]["servicos"][y]['bridge_domain']}
encapsulation-dot1q {empresarial[x]["servicos"][y]['dot1q']}
$
$
intf-statistics
interface {porta_edd}.{empresarial[x]["servicos"][y]['bridge_domain']}
traffic-statistics enable
$
$
qos-statistics switch on {porta_edd}.{empresarial[x]["servicos"][y]['bridge_domain']} output
service-policy {porta_edd}.{empresarial[x]["servicos"][y]['bridge_domain']} input TC20-VPN-GERENCIA-512KBPS-IN
traffic-policy interface {porta_edd}.{empresarial[x]["servicos"][y]['bridge_domain']} input TC20-VPN-GERENCIA-CORP-IN
traffic-policy-statistics switch on interface {porta_edd}.{empresarial[x]["servicos"][y]['bridge_domain']} input
$
$
"""
# SERVIÇO Q IN Q                
                elif empresarial[x]["servicos"][y].get("tipo_servico") == "servico_q":
                    vcid_formatado = str(empresarial[x]["servicos"][y]['xconnect_vcid'])[-8:]
                    script += f"""pw pw{str(empresarial[x]["servicos"][y]['xconnect_vcid'])}
$
interface {porta_edd}.{vcid_formatado}
description {empresarial[x]["servicos"][y]['service_description']}
mtu {empresarial[x]["servicos"][y].get('mtu', empresarial[x]['mtu'])}
$
qos
interface {porta_edd}.{vcid_formatado}"""
                    if empresarial[x]["servicos"][y].get("service_policy") is not None:
                        script += f"""
rate-limit input localport cir {int(float(empresarial[x]['servicos'][y]['service_policy']) * 1.01)} kbps pir {int(float(empresarial[x]['servicos'][y]['service_policy']) * 1.01)} kbps conform-action transmit exceed-action drop violate-action drop
$"""

                    script += f"""
vlan-configuration
interface {porta_edd}.{vcid_formatado} 
qinq internal-vlanid {empresarial[x]["servicos"][y]["dot1q_2"]} external-vlanid {empresarial[x]["servicos"][y]["dot1q_1"]}
$
$
intf-statistics
interface {porta_edd}.{vcid_formatado}
traffic-statistics enable
$
$
mpls ldp instance 1
target-session {empresarial[x]["servicos"][y]['xconnect_ip']}
$
$
vpws {str(empresarial[x]["servicos"][y]['xconnect_vcid'])}
mtu 1546
access-point {porta_edd}.{vcid_formatado}
access-params ethernet
$
$
pseudo-wire pw{str(empresarial[x]["servicos"][y]['xconnect_vcid'])}
neighbour {empresarial[x]["servicos"][y]['xconnect_ip']} vcid {str(empresarial[x]["servicos"][y]['xconnect_vcid'])}
$
$
$
traffic-policy interface {porta_edd}.{vcid_formatado} input TC20-EoMPLS-CIRCUITO-MARCA-IN
traffic-policy-statistics switch on interface {porta_edd}.{vcid_formatado} input
$
$                    
"""
# SERVIÇO COM APENAS UMA DOT1Q
                elif empresarial[x]["servicos"][y].get("tipo_servico") == "servico":
                    vcid_formatado = str(empresarial[x]["servicos"][y]['xconnect_vcid'])[-8:]
                    script += f"""pw pw{str(empresarial[x]["servicos"][y]['xconnect_vcid'])}
$
interface {porta_edd}.{vcid_formatado}
description {empresarial[x]["servicos"][y]['service_description']}
mtu {empresarial[x]["servicos"][y].get('mtu', empresarial[x]["mtu"])}
$
qos
interface {porta_edd}.{vcid_formatado}"""
                    if empresarial[x]["servicos"][y].get("service_policy") is not None:
                        script += f"""
rate-limit input localport cir {int(float(empresarial[x]['servicos'][y]['service_policy']) * 1.01)} kbps pir {int(float(empresarial[x]['servicos'][y]['service_policy']) * 1.01)} kbps conform-action transmit exceed-action drop violate-action drop
$"""

                    script += f"""
vlan-configuration
interface {porta_edd}.{vcid_formatado} 
encapsulation-dot1q {empresarial[x]["servicos"][y]["dot1q"]}
$
$
intf-statistics
interface {porta_edd}.{vcid_formatado}
traffic-statistics enable
$
$
mpls ldp instance 1
target-session {empresarial[x]["servicos"][y]['xconnect_ip']}
$
$
vpws {str(empresarial[x]["servicos"][y]['xconnect_vcid'])}
mtu 1546
access-point {porta_edd}.{vcid_formatado}
access-params ethernet
$
$
pseudo-wire pw{str(empresarial[x]["servicos"][y]['xconnect_vcid'])}
neighbour {empresarial[x]["servicos"][y]['xconnect_ip']} vcid {str(empresarial[x]["servicos"][y]['xconnect_vcid'])}
$
$
$
traffic-policy interface {porta_edd}.{vcid_formatado} input TC20-EoMPLS-CIRCUITO-MARCA-IN
traffic-policy-statistics switch on interface {porta_edd}.{vcid_formatado} input
$
$                    
"""
    script += f"""
$ ====================================================================
$ CONFIGURAÇÃO TACACS
$ ====================================================================
tacacs enable
tacacs-client source-interface loopback100
tacacs-server deadtime 0
tacacs-server timeout 30
tacacs-server host 10.129.199.25 key CLAROSECkey$321
tacacs-server host 10.108.199.25 key CLAROSECkey$321
tacplus group-server ACSCLARO
server 10.129.199.25
server 10.108.199.25
$
$
aaa-authentication-template 1
aaa-authentication-type local
$
aaa-authentication-template 2020
aaa-authentication-type tacacs-local
authentication-tacacs-group ACSCLARO
$
aaa-authorization-template 1
aaa-authorization-type local
$
aaa-authorization-template 2020
aaa-authorization-type tacacs-local
authorization-tacacs-group ACSCLARO
$
aaa-accounting-template 2020
aaa-accounting-type tacacs
accounting-tacacs-group ACSCLARO
$
$
system-user
authentication-template 1
bind aaa-authentication-template 1
$
authentication-template 127
bind aaa-authentication-template 2020
$
authorization-template 1
bind aaa-authorization-template 1
local-privilege-level 7
login-sametime-max 60
$
authorization-template 127
bind aaa-authorization-template 2020
local-privilege-level 15
login-type-allowed console ssh ftp
login-sametime-max 60
$
login ascii authentication-template 127 authortication-template 127
strong-password check disable
user-authen-restriction fail-time 5 lock-minute 5
user-name claroadmin
bind authentication-template 127
bind authorization-template 127
password claroadmin@1q2w3e
$
user-name suporteipran
bind authentication-template 127
bind authorization-template 127
password encrypted *21*Cd9FBNz0tjJfcP3wzoPKJs6DyibOg8omzoPKJtkpzlZN38Vg19Y5fPgy6fQUld4H/haIb3jPx5G1NBxoWzZGV7y7tXqSYgbH95TndUebzYFPe10xhODI6HEguEGTY0Q+8sHgn7uYmGwu7mAD
$
$
$
command-authorization 15 config-command 2020
privilege show all level 7 show
privilege exec all level 7 copy
$
$
login authentication
y
$
$
ipv4-access-list 120
rule 5 permit ip 192.168.32.247 0.0.0.0 any
rule 6 permit ip 192.168.32.248 0.0.0.0 any
rule 7 permit ip 192.168.32.249 0.0.0.0 any
rule 10 permit ip 10.0.55.0 0.255.0.255 any
rule 15 permit ip 10.0.56.0 0.255.0.255 any
rule 20 permit ip 10.0.7.0 0.255.0.255 any
rule 25 permit ip 10.0.1.7 0.255.0.0 any
rule 30 permit ip 10.108.198.0 0.0.0.255 any
rule 35 permit ip 10.129.198.0 0.0.0.255 any
rule 40 permit ip 10.221.198.0 0.0.0.255 any
rule 45 permit ip 10.199.10.0 0.0.0.255 any
rule 50 permit ip 10.197.4.1 0.0.0.0 any
rule 54 permit ip 200.255.124.0 0.0.0.31 any
rule 55 permit ip 200.255.124.9 0.0.0.0 any
rule 60 permit ip 200.255.124.25 0.0.0.0 any
rule 65 permit ip 10.129.71.64 0.0.0.31 any
rule 70 permit ip 10.199.26.0 0.0.0.255 any
rule 75 permit ip 10.108.199.0 0.0.0.255 any
rule 80 permit ip 10.129.199.0 0.0.0.255 any
rule 85 permit ip 10.221.199.0 0.0.0.255 any
rule 90 permit ip 10.199.8.0 0.0.0.255 any
rule 95 permit ip 10.199.24.0 0.0.0.255 any
rule 100 permit ip 10.108.7.0 0.0.0.255 any
rule 105 permit ip 10.129.7.0 0.0.0.255 any
rule 110 permit ip 10.108.97.0 0.0.0.255 any
rule 115 permit ip 10.129.97.0 0.0.0.255 any
rule 120 permit ip 10.129.251.80 0.0.0.15 any
rule 125 permit ip 10.119.97.0 0.0.0.255 any
rule 130 permit ip 172.31.224.0 0.0.0.255 any
rule 135 permit ip 172.31.225.0 0.0.0.255 any
rule 140 permit ip 172.31.226.0 0.0.0.255 any
rule 145 permit ip 172.31.227.0 0.0.0.255 any
rule 150 permit ip 172.31.228.0 0.0.0.255 any
rule 155 permit ip 172.31.229.0 0.0.0.255 any
rule 160 permit ip 172.31.230.0 0.0.0.255 any
rule 165 permit ip 10.198.120.0 0.0.7.255 any
rule 170 permit ip 10.197.120.0 0.0.7.255 any
rule 175 permit ip 10.198.1.0 0.0.0.255 any
rule 180 permit ip 172.31.176.0 0.0.0.255 any
rule 185 permit ip 172.31.177.0 0.0.0.255 any
rule 190 permit ip 172.31.178.0 0.0.0.255 any
rule 195 permit ip 172.31.180.0 0.0.0.255 any
rule 200 permit ip 172.31.181.0 0.0.0.255 any
rule 205 permit ip 172.31.182.0 0.0.0.255 any
rule 210 permit ip 172.31.183.0 0.0.0.255 any
rule 215 permit ip 172.31.240.0 0.0.0.255 any
rule 220 permit ip 10.200.0.0 0.0.0.255 any
rule 225 permit ip 10.201.0.0 0.0.0.255 any
rule 230 permit ip 10.202.0.0 0.0.0.255 any
rule 235 permit ip 10.203.0.0 0.0.0.255 any
rule 240 permit ip 10.204.0.0 0.0.0.255 any
rule 245 permit ip 10.205.0.0 0.0.0.255 any
rule 250 permit ip 10.206.0.0 0.0.0.255 any
rule 255 permit ip 10.207.0.0 0.0.0.255 any
rule 260 permit ip 10.208.0.0 0.0.0.255 any
rule 265 permit ip 10.209.0.0 0.0.0.255 any
rule 270 permit ip 10.210.0.0 0.0.0.255 any
rule 275 permit ip 10.230.0.0 0.0.0.255 any
rule 280 permit ip 10.231.0.0 0.0.0.255 any
rule 285 permit ip 10.232.0.0 0.0.0.255 any
rule 290 permit ip 10.233.0.0 0.0.0.255 any
rule 295 permit ip 10.234.0.0 0.0.0.255 any
rule 300 permit ip 10.235.0.0 0.0.0.255 any
rule 305 permit ip 10.236.0.0 0.0.0.255 any
rule 310 permit ip 10.237.0.0 0.0.0.255 any
rule 315 permit ip 10.238.0.0 0.0.0.255 any
rule 320 permit ip 10.239.0.0 0.0.0.255 any
rule 325 permit ip 10.240.0.0 0.0.0.255 any
rule 330 permit ip 10.241.0.0 0.0.0.255 any
rule 335 permit ip 10.242.0.0 0.0.0.255 any
rule 340 permit ip 10.243.0.0 0.0.0.255 any
rule 345 permit ip 10.244.0.0 0.0.0.255 any
rule 350 permit ip 10.245.0.0 0.0.0.255 any
rule 355 permit ip 10.246.0.0 0.0.0.255 any
rule 360 permit ip 10.247.0.0 0.0.0.255 any
rule 365 permit ip 10.248.0.0 0.0.0.255 any
rule 370 permit ip 10.249.0.0 0.0.0.255 any
rule 375 permit ip 10.250.0.0 0.0.0.255 any
rule 380 permit ip 10.251.0.0 0.0.0.255 any
rule 385 permit ip 10.252.0.0 0.0.0.255 any
rule 390 permit ip 10.108.211.129 0.0.0.0 any
rule 395 permit ip 10.108.210.33 0.0.0.255 any
rule 400 permit ip 10.129.72.0 0.0.0.255 any
rule 410 permit ip 192.192.192.0 0.0.0.255 any
rule 415 permit ip 10.108.211.128 0.0.0.31 any
rule 421 permit ip 10.107.215.96 0.0.0.31 any
rule 422 permit ip 10.129.246.96 0.0.0.31 any
rule 1000 deny any
$
$
$ ====================================================================
$ REMOÇÃO DO TELNET
$ ====================================================================
$
line console absolute-timeout 30
line console idle-timeout 5
line telnet server disable
yes
line telnet absolute-timeout 0
line telnet idle-timeout 5
$
$
ssh server version 2
ssh server encryption none disable
ssh server hmac none disable
ssh server access-class ipv4 120
$
$
commit
$
$
end
$
$
write
$
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
#    with open(f"scripts/{hostname}_ZTE_6120H.txt", 'w', encoding='utf-8') as arquivo:
#        arquivo.write(script)
#
#    print(f"✅ Script gerado com sucesso para {hostname}_ZTE_6120H.")
    return script