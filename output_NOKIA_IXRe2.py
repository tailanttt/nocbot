import os 
from dotenv import load_dotenv 
load_dotenv()

def gerar_script(
    hostname,
    ip_loopback,
    uf,
    site,
    ntp_ips,
    processo_ospf,
    area_ospf_formatada,
    bgp,
    saa,
    twamp,
    fibra,
    mwrot,
    movel,
    bateria,
    empresarial,
    ptp,
    rotas_estaticas
):

#PENDENCIAS BFD e EMPRESARIAL DHCP GERENCIA61

    portas_fo = []
    portas_mwrot = []
    portas_movel = []
    portas_edd = []
    portas_bateria = []
    bnm_id = 0

    portas10 = ["1/1/c5",
                "1/1/c6",
                "1/1/c7",
                "1/1/c8",
                "1/1/c9",
                "1/1/c10",
                "1/1/c12",
                "1/1/c13",
                "1/1/c14",
                "1/1/c15",
                "1/1/c16",
                "1/1/c17",
                "1/1/c18",
                "1/1/c19",
                "1/1/c20",
                "1/1/c21",
                "1/1/c22",
                "1/1/c23",
                "1/1/c24",
                "1/1/c25",
                "1/1/c26",
                "1/1/c27",
                "1/1/c28"]
    portas100 =["1/1/c1","1/1/c2","1/1/c3","1/1/c4"]

    script = f"""
#--------------------------------------------------
# Criação do Diretório de Rollback
#--------------------------------------------------
#
file
    md rollback_directory
    md rescue_directory
exit all
#
#
#--------------------------------------------------
# SCRIPT DE CONFIGURAÇÃO NOKIA IXRe2
#--------------------------------------------------
#
configure system
        name {hostname}
        management-interface
            yang-modules
                no nokia-combined-modules
                nokia-submodules
                openconfig-modules
            exit
        exit
        rollback
            rollback-location "cf3:/rollback_directory/rollback"
            rescue-location "cf3:/rescue_directory/rescue"
        exit
        netconf
            listen
                no shutdown
            exit
        exit
        grpc
            allow-unsecure-connection
            no shutdown
        exit
        snmp
            streaming
                no shutdown
            exit
            packet-size 9216
            no shutdown
        exit
        time
            ntp"""
    for ip in ntp_ips:
        script+=f"\n              server {ip} version 3"
    script+=f"""
              no shutdown
            exit
            sntp
                shutdown
            exit
            zone BRZ -03
        exit
exit all
#
#
#--------------------------------------------------
# System Security Configuration
#--------------------------------------------------
#
#
configure system
        security
            ftp-server
            management-access-filter
                ip-filter
                    default-action permit
                    entry 1
                        description "permit SSH"
                        protocol tcp
                        dst-port 22 65535
                        action permit
                    exit
                    entry 2
                        description "permit SSH originated from router"
                        protocol tcp
                        l4-src-port 22 65535
                        action permit
                    exit
                    entry 7
                        description "permit Protocol ICMP"
                        protocol icmp
                        action permit
                    exit
                    entry 8
                        description "permit Protocolo LDP Sessao"
                        protocol tcp
                        l4-src-port 646 65535
                        action permit
                    exit
                    entry 9
                        description "permit Protocolo LDP Sessao"
                        protocol tcp
                        dst-port 646 65535
                        action permit
                    exit
                    entry 10
                        description "permit Protocolo LDP Hello"
                        protocol udp
                        l4-src-port 646 65535
                        action permit
                    exit
                    entry 11
                        description "permit Protocolo LDP Hello"
                        protocol udp
                        dst-port 646 65535
                        action permit
                    exit
                    entry 12
                        description "permit UDP Echo"
                        protocol udp
                        l4-src-port 7 65535
                        action permit
                    exit
                    entry 13
                        description "permit UDP Echo"
                        protocol udp
                        dst-port 7 65535
                        action permit
                    exit
                    entry 14
                        description "permit RSVP"
                        protocol rsvp
                        action permit
                    exit
                    entry 15
                        description "permit FTP_SRC"
                        protocol tcp
                        l4-src-port 21 65535
                        action permit
                    exit
                    entry 16
                        description "permit FTP_DST"
                        protocol tcp
                        dst-port 21 65535
                        action permit
                    exit
                    entry 17
                        description "permit FTP_SRC"
                        protocol tcp
                        l4-src-port 20 65535
                        action permit
                    exit
                    entry 18
                        description "permit FTP_DST"
                        protocol tcp
                        dst-port 20 65535
                        action permit
                    exit
                    entry 19
                        description "permit OSPF over IPV4"
                        protocol ospf-igp
                        action permit
                    exit
                    entry 20
                        description "PERMIT_BGP"
                        protocol tcp
                        dst-port 179 65535
                        action permit
                    exit
                    entry 21
                        description "PERMIT_BGP"
                        protocol tcp
                        l4-src-port 179 65535
                        action permit
                    exit
                    entry 24
                        description "permit BFD"
                        protocol udp
                        dst-port 3784 65535
                        action permit
                    exit
                    entry 28
                        description "Permite Traceroute"
                        protocol udp
                        dst-port 33408 65408
                        action permit
                    exit
                    entry 34
                        description "PERMIT_VRRP"
                        protocol vrrp 
                        action permit
                    exit
                    entry 40
                        description "PERMITIR PTP"
                        protocol udp
                        dst-port 319 65535
                        action permit
                    exit
                    entry 41
                        description "PERMITIR PTP"
                        protocol udp
                        dst-port 320 65535
                        action permit
                    exit
                    entry 50
                        description "PERMIT_RIP"
                        protocol udp
                        dst-port 520 65535
                        action permit
                    exit
                    entry 51
                        description "PERMIT_MC_LAG"
                        protocol udp
                        dst-port 1025 65535
                        action permit
                    exit
                    entry 55
                        description "PERMIT_TACACS_SERVER1"
                        protocol tcp
                        src-ip 10.129.199.25/32
                        l4-src-port 49 65535
                        action permit
                    exit
                    entry 56
                        description "PERMIT_TACACS_SERVER2"
                        protocol tcp
                        src-ip 10.108.199.25/32
                        l4-src-port 49 65535
                        action permit
                    exit
                    entry 59
                        description "PROTOCOLO PIM"
                        protocol pim
                        action permit
                    exit
                    entry 60
                        description "PERMIT_NTP_SERVER1"
                        protocol udp
                        src-ip {ntp_ips[0]}/32
                        dst-port 123 65535
                        action permit
                    exit
                    entry 61
                        description "PERMIT_NTP_SERVER2"
                        protocol udp
                        src-ip {ntp_ips[1]}/32
                        dst-port 123 65535
                        action permit
                    exit
                    entry 62
                       description "SLAVIEW SNMP"
                       protocol udp
                       dst-port 161 65535
                       src-ip 10.0.0.0/8
                       action permit
                    exit
                    entry 63
                       description "permit NTP originated from access router"
                       protocol udp
                       dst-port 123 65535
                       src-ip 10.0.0.0/8
                       action permit
                    exit
                    entry 70
                        description "permit Telemetria NSP 24.11 - SPOMB"
                        src-ip 10.101.70.0/25
                        protocol tcp
                        dst-port 57400 65535
                        action permit
                    exit
                    entry 71
                        description "permit Telemetria NSP 24.11 - RJOAM"
                        src-ip 10.199.70.0/25
                        protocol tcp
                        dst-port 57400 65535
                        action permit
                    exit
                    entry 72
                        description "permit Telemetria - TELCO"
                        src-ip 200.244.182.192/26
                        protocol tcp
                        dst-port 57400 65535
                        action permit
                    exit
                    entry 80
                        description "permit NETCONF TCP NSP 24.11 - SPOMB"
                        src-ip 10.101.70.0/25
                        protocol tcp
                        dst-port 830 65535
                        action permit
                    exit
                    entry 81
                        description "permit NETCONF TCP NSP 24.11 - RJOAM"
                        src-ip 10.199.70.0/25
                        protocol tcp
                        dst-port 830 65535
                        action permit
                    exit
                    entry 82
                        description "permit NETCONF UDP NSP 24.11 - SPOMB"
                        src-ip 10.101.70.0/25
                        protocol udp
                        dst-port 830 65535
                        action permit
                    exit
                    entry 83
                        description "permit NETCONF UDP NSP 24.11 - RJOAM"
                        src-ip 10.199.70.0/25
                        protocol udp
                        dst-port 830 65535
                        action permit
                    exit
                    entry 84
                        description "permit TWAMP-SRC"
                        protocol udp
                        l4-src-port 862 65535
                        action permit
                    exit
                    entry 85
                        description "permit TWAMP-DST"
                        protocol udp
                        dst-port 862 65535
                        action permit
                    exit
                    entry 86
                        description "permit SNMP Servidor NSP 24.11 - SPOMB"
                        src-ip 10.101.70.0/25
                        protocol udp
                        dst-port 161 65535
                        action permit
                    exit
                    entry 87
                        description "permit SNMP Servidor NSP 24.11 - RJOAM"
                        src-ip 10.199.70.0/25
                        protocol udp
                        dst-port 161 65535
                        action permit
                    exit
                    entry 100
                        description "SLAVIEW SPJAG01"
                        src-ip 10.108.10.144/28
                        protocol udp
                        action permit
                    exit
                    entry 101
                        description "SLAVIEW SPCAS01"
                        src-ip 10.119.10.144/28
                        protocol udp
                        action permit
                    exit
                    entry 102
                        description "SLAVIEW RJMCK01"
                        src-ip 10.129.10.144/28
                        protocol udp
                        action permit
                    exit
                    entry 103
                        description "SLAVIEW MGBHE01"
                        src-ip 10.130.10.144/28
                        protocol udp
                        action permit
                    exit
                    entry 104
                        description "SLAVIEW MGBHE02"
                        src-ip 10.131.10.144/28
                        protocol udp
                        action permit
                    exit
                    entry 105
                        description "SLAVIEW PRCTA02"
                        src-ip 10.140.10.144/28
                        protocol udp
                        action permit
                    exit
                    entry 106
                        description "SLAVIEW PRCTA01"
                        src-ip 10.141.10.144/28
                        protocol udp
                        action permit
                    exit
                    entry 107
                        description "SLAVIEW RSMOV01"
                        src-ip 10.150.10.144/28
                        protocol udp
                        action permit
                    exit
                    entry 108
                        description "SLAVIEW RSPAE01"
                        src-ip 10.151.10.144/28
                        protocol udp
                        action permit
                    exit
                    entry 109
                        description "SLAVIEW DFBSA02"
                        src-ip 10.160.10.144/28
                        protocol udp
                        action permit
                    exit
                    entry 110
                        description "SLAVIEW GOGNA01"
                        src-ip 10.162.10.144/28
                        protocol udp
                        action permit
                    exit
                    entry 111
                        description "SLAVIEW BASDR02"
                        src-ip 10.170.10.144/28
                        protocol udp
                        action permit
                    exit
                    entry 112
                        description "SLAVIEW PERCE02"
                        src-ip 10.180.10.144/28
                        protocol udp
                        action permit
                    exit
                    entry 113
                        description "SLAVIEW CONSOLIDADORA"
                        src-ip 10.221.198.40/30
                        protocol udp
                        action permit
                    exit
                    entry 666
                        description "permitir SNMP servidor GRB-EBT"
                        src-ip 200.255.124.0/27
                        protocol udp
                        dst-port 161 65535
                        action permit
                    exit
                    entry 668
                        description "permitir SNMP servidor GRB-EBT"
                        src-ip 200.255.124.192/26
                        protocol udp
                        dst-port 161 65535
                        action permit
                    exit
                    default-action deny
                    no shutdown 
                exit
            exit
            profile "default"
                entry 10
                    match "exec"
                    action permit
                exit
                entry 20
                    match "exit"
                    action permit
                exit
                entry 30
                    match "help"
                    action permit
                exit
                entry 40
                    match "logout"
                    action permit
                exit
                entry 50
                    match "password"
                    action permit
                exit
                entry 66
                    match "clear li"
                    action deny
                exit
                entry 67
                    match "tools dump li"
                    action deny
                exit
                entry 75
                    match "state"
                    action permit
                exit
                entry 90
                    match "enable"
                    action permit
                exit
                no entry 60
                no entry 65
                no entry 70
                no entry 80
                no entry 100
            exit
            profile "administrative"
                netconf
                    base-op-authorization
                        action
                        cancel-commit
                        close-session
                        commit
                        copy-config
                        create-subscription
                        delete-config
                        discard-changes
                        edit-config
                        get
                        get-config
                        get-data
                        get-schema
                        kill-session
                        lock
                        validate
                    exit
                exit
                entry 10
                    match "configure system security"
                    action permit
                exit
                entry 20
                    match "show system security"
                    action permit
                exit
                entry 30
                    match "tools perform security"
                    action permit
                exit
                entry 40
                    match "tools dump security"
                    action permit
                exit
                entry 42
                    match "tools dump system security"
                    action permit
                exit
                entry 50
                    match "admin system security"
                    action permit
                exit
                entry 100
                    match "configure li"
                    action deny
                exit
                entry 110
                    match "show li"
                    action deny
                exit
                entry 111
                    match "clear li"
                    action deny
                exit
                entry 112
                    match "tools dump li"
                    action deny
                exit
            exit
            password
                authentication-order tacplus local radius exit-on-reject
            exit
            radius
                shutdown
            exit
            tacplus
                accounting
                authorization
                timeout 10
                server 1 address 10.129.199.25 secret "R9O4drd76p2iRxoOfZG2kiG354o+8V35w3LNS0CkBg==" hash2
                server 2 address 10.108.199.25 secret "R9O4drd76p2iRxoOfZG2ki8GmYroNMVO+ONTcWoccw==" hash2
            exit
            user-template "tacplus_default"
                access console ftp netconf grpc
                no restricted-to-home
                no save-when-restricted
            exit
            user "backbone"
                password "$2y$10$Gs/s6vQzlfjG1BC7ihOBk.5w8GfvLV97GzWeDKkoMS8vKNCVS/KVO"
                access console
                no restricted-to-home
                no save-when-restricted
                console
                    member "administrative"
                    member "default"
                exit
            exit
            user "sam"
                password "$2y$10$ULwWT3FuJh96N1o6vSYTw.zfp3EGSHxp86OSxE5WjiSBMKZS3NPMK"
                access console ftp netconf grpc
                no restricted-to-home
                no save-when-restricted
                console
                    cannot-change-password
                    member "administrative"
                    no member "default"
                exit
            exit
            user "Nokia_Tele"
                access netconf grpc
                password "{os.getenv("NOKIA_TELE")}"
            exit
            snmp
                community "hLzZnt2IMTNE6JGDGpglKMUpygVp/NOhWJc=" hash2 rwa version v2c
            exit
            ssh
                preserve-key
            exit
            per-peer-queuing
exit all
#
#
#--------------------------------------------------
# System Login Control Configuration
#--------------------------------------------------
#
configure system
        login-control
            motd text Login Successful
            ftp
                inbound-max-sessions 1
            exit
            idle-timeout 15
pre-login-message"""
    script += r"""
"$##############################################################################$\n# ATENCAO: CLARO - ACESSO RESTRITO
#\n# Proibido o acesso de pessoas nao autorizadas.
#\n# Todas as tentativas de login estao sendo monitoradas.
#\n# ATTENTION: CLARO - RESTRICTED ACCESS –
#\n# RESTRICTED ACCESS EQUIPMENT. ONLY PERSONAL AUTHORIZED.
#\n# ALL ACCESSES ARE BEING MONITORED.
#\n$############################################################################$\n\n\n”"""
    script += f"""
    exit
exit all
#
#
#--------------------------------------------------
# Log Configuration
#--------------------------------------------------
#
configure log
        file-id 1
            description "ALARM_LOG_FILE"
            location cf3:
            rollover 2880 retention 360
        exit
        file-id 12
            description "ServiceEGRroll60minRet72h_7250"
            location cf3:
            rollover 60 retention 72
        exit
        accounting-policy 12
            description "ServiceEGR_7250"
            record service-egress-octets
            collection-interval 60
            to file 12
            no shutdown
        exit
        throttle-rate 10 interval 30
        event-control "igmp" 2005 suppress
        event-control "vrtr" 2034 generate
        event-control "system" 2052 suppress
        event-control "system" 2053 suppress
        event-control "system" 2101 suppress
        event-control "system" 2102 suppress
        event-control "system" 2103 suppress
        event-control "system" 2104 suppress
        event-control "svcmgr" sdpBindPwPeerStatusBitsChanged suppress
        event-control "logger" tmnxLogFileDeleted suppress
        syslog 1
            description "SYSLOG1_Claro"
            address 10.221.199.37
            facility local1
        exit
        syslog 2
            description "clsyslog01.bkb.embratel.net.br"
            address 200.255.124.9
            level warning
        exit
        syslog 3
            description "clsyslog02.bkb.embratel.net.br"
            address 200.255.124.25
            level debug
        exit
        snmp-trap-group 98
           description "5620sam"
        exit
        log-id 1
            time-format local
            from main security change
            to syslog 1
            no shutdown
        exit
        log-id 2
            time-format local
            to syslog 2
            no shutdown
        exit
        log-id 5
            time-format local
            from main security change
            no shutdown
        exit
        log-id 98
            time-format local
            from main security change
            to snmp 1024
            no shutdown
        exit
        log-id 99
            time-format local
            no shutdown
        exit
        log-id 100
            time-format local
            no shutdown
        exit
exit all
#
#
#--------------------------------------------------
# QoS Policy Configuration
#--------------------------------------------------
#
#
configure qos
        queue-mgmt-policy "queue-1" create
            high-slope
                shutdown
            exit
            low-slope
                shutdown
            exit
            mbs 71526
        exit
       queue-mgmt-policy "queue-2" create
            high-slope
                shutdown
            exit
            low-slope
                shutdown
            exit
            mbs 119209
        exit
        queue-mgmt-policy "queue-3" create
            high-slope
                shutdown
            exit
            low-slope
                shutdown
            exit
            mbs 119209
        exit
        queue-mgmt-policy "queue-4" create
            high-slope
                shutdown
            exit
            low-slope
                shutdown
            exit
            mbs 71526
        exit
       queue-mgmt-policy "queue-5" create
            high-slope
                shutdown
            exit
            low-slope
                shutdown
            exit
            mbs 119209
        exit
        queue-mgmt-policy "queue-6" create
            high-slope
                shutdown
            exit
            low-slope
                shutdown
            exit
            mbs 53644
        exit
       queue-mgmt-policy "queue-7" create 
            high-slope
                shutdown
            exit
            low-slope
                shutdown
            exit
            mbs 71526
        exit
        queue-mgmt-policy "queue-8" create
            high-slope
                shutdown
            exit
            low-slope
                shutdown
            exit
            mbs 1192
        exit
exit all
#
#
#
configure qos
        port-qos-policy "QOS_PORT_BACKBONE_CLARO" create
            description "QOS_NETWORK_CLARO_PL2020"
            queue "1" create
                adaptation-rule pir min cir min
                queue-mgmt "queue-1"
                scheduler-mode wfq
                    percent-rate 100.00 cir 5.00
                exit
            exit
           queue "2" create
               adaptation-rule pir min cir min
                queue-mgmt "queue-2"
                scheduler-mode wfq
                   percent-rate 100.00 cir 20.00
               exit
            exit
            queue "3" create
                adaptation-rule pir min cir min
                queue-mgmt "queue-3"
                scheduler-mode wfq
                    percent-rate 100.00 cir 5.00
                exit
            exit
            queue "4" create
                adaptation-rule pir min cir min
                queue-mgmt "queue-4"
                scheduler-mode wfq
                    percent-rate 100.00 cir 7.00
                exit
            exit
           queue "5" create
               adaptation-rule pir min cir min
                queue-mgmt "queue-5"
                scheduler-mode wfq
                   percent-rate 100.00 cir 5.00
               exit
            exit
            queue "6" create
                adaptation-rule pir min cir min
                queue-mgmt "queue-6"
                scheduler-mode wfq
                    percent-rate 45.00 cir 45.00
                exit
            exit
           queue "7" create
               adaptation-rule pir min cir min
                queue-mgmt "queue-7"
                scheduler-mode wfq
                   percent-rate 100.00 cir 8.00
               exit
            exit
            queue "8" create
                adaptation-rule pir min cir min
                queue-mgmt "queue-8"
                scheduler-mode wfq
                    percent-rate 5.00 cir 5.00
                exit
            exit
exit all
#
#
#
configure qos
        vlan-qos-policy "QOS_BACKBONE_CLARO" create
            description "QOS_NETWORK_CLARO_PL2020"
            stat-mode enqueued-with-discards
            queue "1" create
                adaptation-rule pir min cir min
                queue-mgmt "queue-1"
                percent-rate 100.00 cir 5.00
                scheduling-priority 1
            exit
           queue "2" create
               adaptation-rule pir min cir min
               queue-mgmt "queue-2"
               percent-rate 100.00 cir 20.00
                scheduling-priority 1
            exit
            queue "3" create
                adaptation-rule pir min cir min
                queue-mgmt "queue-3"
                percent-rate 100.00 cir 5.00
                scheduling-priority 1
            exit
            queue "4" create
                adaptation-rule pir min cir min
                queue-mgmt "queue-4"
                percent-rate 100.00 cir 7.00
                scheduling-priority 1
            exit
           queue "5" create
               adaptation-rule pir min cir min
               queue-mgmt "queue-5"
               percent-rate 100.00 cir 5.00
                scheduling-priority 3
            exit
            queue "6" create
                adaptation-rule pir min cir min
                queue-mgmt "queue-6"
                percent-rate 45.00 cir 45.00
                scheduling-priority 3
            exit
           queue "7" create
               adaptation-rule pir min cir min
               queue-mgmt "queue-7"
               percent-rate 100.00 cir 8.00
                scheduling-priority 6
            exit
            queue "8" create
                adaptation-rule pir min cir min
                queue-mgmt "queue-8"
                percent-rate 5.00 cir 5.00
                scheduling-priority 6
            exit
exit all
#
#
configure qos
        fc-dot1p-map "NETWORK-EGRESS-dot1p" create
            fc af create
                dot1p 2
            exit
            fc be create
                dot1p 0
            exit
            fc ef create
                dot1p 5
            exit
            fc h1 create
                dot1p 6
            exit
            fc h2 create
                dot1p 4
            exit
            fc l1 create
                dot1p 3
            exit
            fc l2 create
                dot1p 1
            exit
            fc nc create
                dot1p 7
            exit
exit all
#
#
configure qos
        fc-lsp-exp-map "NETWORK-EGRESS-exp" create
            fc af create
                lsp-exp 2
            exit
            fc be create
                lsp-exp 0
            exit
            fc ef create
                lsp-exp 5
            exit
            fc h1 create
                lsp-exp 6
            exit
            fc h2 create
                lsp-exp 4
            exit
            fc l1 create
                lsp-exp 3
            exit
            fc l2 create
                lsp-exp 1
            exit
            fc nc create
                lsp-exp 7
            exit
exit all
#
#
configure qos
        egress-remark-policy "NETWORK-EGRESS" create
            description "QOS_NETWORK_CLARO_PL2020"
            fc-dot1p-map "NETWORK-EGRESS-dot1p"
            fc-lsp-exp-map "NETWORK-EGRESS-exp"
        exit
exit all
#
#
configure qos
        dscp-fc-map "IN_DSCP_1000" create
            dscp "be" fc "be" profile out
            dscp "ef" fc "ef"
            dscp "af12" fc "l1"
            dscp "af13" fc "l1"
            dscp "af21" fc "af"
            dscp "af22" fc "af"
            dscp "af23" fc "af"
            dscp "af41" fc "l1"
            dscp "af42" fc "l1"
            dscp "af43" fc "af"
            dscp "cp51" fc "nc"
            dscp "cp62" fc "nc"
        exit
exit all
#
#
configure qos
        ingress-classification-policy "IN_DSCP_1000" allow-attachment any create
            description "CLASSIFiCACAO_DSCP_NTW_QOS_NETWORK_CLARO"
            dscp-fc-map "IN_DSCP_1000"
        exit
exit all
#
#
configure qos
       dot1p-fc-map "IN_EXP_1000_EXP-dot1p" create
           default-action fc "be" profile out
           dot1p 0 fc "be" profile out
           dot1p 1 fc "l2"
           dot1p 2 fc "af"
           dot1p 3 fc "l1"
           dot1p 4 fc "h2"
           dot1p 5 fc "ef"
           dot1p 6 fc "h1"
            dot1p 7 fc "nc"
        exit
exit all
#
#
configure qos
       lsp-exp-fc-map "IN_EXP_1000_EXP-lsp-exp" create
            lsp-exp 0 fc "be" profile out
            lsp-exp 1 fc "l2"
            lsp-exp 2 fc "af"
            lsp-exp 3 fc "l1"
           lsp-exp 4 fc "h2"
            lsp-exp 5 fc "ef"
            lsp-exp 6 fc "h1"
            lsp-exp 7 fc "nc"
        exit
exit all
#
#
configure qos
        ingress-classification-policy "IN_EXP_1000_EXP" allow-attachment any create
            description "CLASSIFICACAO_DOT1P_EXP_NTW_QOS_NETWORK_CLARO_PL2020"
           dot1p-fc-map "IN_EXP_1000_EXP-dot1p"
           lsp-exp-fc-map "IN_EXP_1000_EXP-lsp-exp"
        exit
exit all
#
#
configure qos
        network-ingress "QOS_BACKBONE_CLARO" policer-allocation per-fc create
            description "QOS_NETWORK_CLARO_PL2020"
            ingress-classification-policy "IN_EXP_1000_EXP"
            policer 1
                stat-mode offered-profile-with-discards
            exit
            policer 2
                stat-mode offered-profile-with-discards
            exit
            policer 3
                stat-mode offered-profile-with-discards
            exit
            policer 4
                stat-mode offered-profile-with-discards
            exit
            policer 5
                stat-mode offered-profile-with-discards
            exit
            policer 6
                stat-mode offered-profile-with-discards
            exit
            policer 7
                stat-mode offered-profile-with-discards
            exit
            policer 8
                stat-mode offered-profile-with-discards
            exit
        exit
exit all
#
#
configure router sgt-qos
            application dns dscp nc1
            application ftp dscp nc1
            application snmp dscp nc1
            application snmp-notification dscp nc1
            application ssh dscp nc1
            application syslog dscp nc1
            application tacplus dscp nc1
            application telnet dscp nc1
            application tftp dscp nc1
            application ptp dscp nc2
            application bmp dscp nc1
            application grpc dscp nc1
            application http dscp nc1
            application arp dot1p 6
            application isis dot1p 6
            dscp nc1 fc h1
exit all
#
#
#--------------------------------------------------
# Card Configuration
#--------------------------------------------------
#
configure card 1
        card-type imm2-qsfpdd+2-qsfp28+24-sfp28
        mda 1
            sync-e
            no shutdown
        exit
        no shutdown
    exit
#
#
#--------------------------------------------------
# DESATIVANDO TODAS AS PORTAS
#--------------------------------------------------
configurate port 1/1/c1   
    shutdown
exit all
configurate port 1/1/c2   
    shutdown
exit all
configurate port 1/1/c3   
    shutdown
exit all
configurate port 1/1/c4   
    shutdown
exit all
configurate port 1/1/c5   
    shutdown
exit all
configurate port 1/1/c6   
    shutdown
exit all
configurate port 1/1/c7   
    shutdown
exit all
configurate port 1/1/c8   
    shutdown
exit all
configurate port 1/1/c9   
    shutdown
exit all
configurate port 1/1/c10  
    shutdown
exit all
configurate port 1/1/c11  
    shutdown
exit all
configurate port 1/1/c12  
    shutdown
exit all
configurate port 1/1/c13  
    shutdown
exit all
configurate port 1/1/c14  
    shutdown
exit all
configurate port 1/1/c15  
    shutdown
exit all
configurate port 1/1/c16  
    shutdown
exit all
configurate port 1/1/c17  
    shutdown
exit all
configurate port 1/1/c18  
    shutdown
exit all
configurate port 1/1/c19  
    shutdown
exit all
configurate port 1/1/c20  
    shutdown
exit all
configurate port 1/1/c21  
    shutdown
exit all
configurate port 1/1/c22  
    shutdown
exit all
configurate port 1/1/c23  
    shutdown
exit all
configurate port 1/1/c24  
    shutdown
exit all
configurate port 1/1/c25  
    shutdown
exit all
configurate port 1/1/c26  
    shutdown
exit all
configurate port 1/1/c27  
    shutdown
exit all
configurate port 1/1/c28  
    shutdown
exit all
#
#--------------------------------------------------
# LOOPBACK
#--------------------------------------------------
#
configure router
    interface system
        address {ip_loopback}/32
        description LOOPBACK_DE_GERENCIA 
        no shutdown
    exit
    autonomous-system {bgp["processo"]}
    router-id {ip_loopback}
exit all
#
configure router
    ecmp 8
exit all
#
configure system
    load-balancing lsr-load-balancing lbl-eth-ip-l4-teid
    load-balancing hash-poly ecmp poly5 lag poly2
exit all
#
#"""

    if fibra:  
        script += """
#--------------------------------------------------
# NNI FIBRA
#--------------------------------------------------"""

    for port in fibra:
        porta_fo = portas100.pop() if port["speed"] == "100000" else portas10.pop()
        portas_fo.append(porta_fo)
        script += f"""
configure port {porta_fo}
    connector
        breakout c1-{int(port["speed"])//1000}g
    exit
    no shutdown
exit all
#
#
configure port {porta_fo}/1
    description "{port["description"]}"
    ethernet
        mode network
        mtu 9212
        collect-stats
        lldp
            dest-mac nearest-bridge
                admin-status tx-rx
                notification
                tx-tlvs port-desc sys-name sys-desc sys-cap
                tx-mgmt-address system
            exit
            dest-mac nearest-customer
                admin-status tx-rx
                notification
                tx-tlvs port-desc sys-name sys-desc sys-cap
                tx-mgmt-address system
            exit
        exit
        hold-time up 5
        egress-port-qos-policy "QOS_PORT_BACKBONE_CLARO"
        ssm
            no shutdown
        exit
        rs-fec-mode cl91-514-528
    exit
    no shutdown
exit all
#
#
#"""
        if port["lag"]:
            script+=f"""
configure lag {port["lag"]}
    description "{port["description"]}"
    mode network
    lacp active
    port {porta_fo}/1        
    no shutdown
exit all
#
#"""
        for interface in port["interfaces"]:
            if port["lag"]:
                script += f""" 
#
configure router
    interface {interface["interface"]}
    description "{interface["description"]}"
    address {interface["ip"]}
    port lag-{port["lag"]}
exit
no shutdown
exit
exit all
#
#"""
            else:
                script += f"""
configure router
    interface {interface["interface"]}
    description "{interface["description"]}"
    address {interface["ip"]}
    port {porta_fo}/1
    egress
        vlan-qos-policy "QOS_BACKBONE_CLARO"
    exit
    ingress
        qos "QOS_BACKBONE_CLARO"
    exit
    egress
        agg-rate
            rate max cir max
        exit
        egress-remark-policy "NETWORK-EGRESS"
    exit"""
                if interface["bfd"]:
                    script += f"""
    bfd 100 receive 100 multiplier 3
        if-attribute
            delay
                delay-selection dynamic
                dynamic
                    measurement-template "LINK_DELAY_V4"
                    twamp-light
                        ipv4
                            no shutdown
                        exit
                    exit
                exit
            exit
        exit
        no shutdown
    exit"""

                script += """
exit all
#"""

    if any(interface.get("gerencia") for item in mwrot for interface in item["interfaces"]):
        script += f"""
#--------------------------------------------------
# QoS MWROT GERENCIA
#--------------------------------------------------
configure qos
        dscp-fc-map "32" create
            default-action fc "af" profile in
        exit
exit all
#
#
configure qos
        ingress-classification-policy "32" allow-attachment any create
            description "TC20_QOS_GERENCIA_IN"
            dscp-fc-map "32"
        exit
exit all
#
#
configure qos
        sap-ingress 32 name "TC20_QOS_GERENCIA_IN" policer-allocation per-fc create
            description "TC20_QOS_GERENCIA_IN"
            ingress-classification-policy "32"
            policer 3 create
                stat-mode offered-profile-with-discards
            exit
        exit
exit all
#
#"""
    if mwrot:  
        script += """
#--------------------------------------------------
# NNI MWROT
#--------------------------------------------------
"""
    for port in mwrot:
        porta_mwrot = portas10.pop()
        portas_mwrot.append(porta_mwrot)
        if port["bnm_ativo"]:
            bnm_id +=1
            script += f"""
configure eth-cfm domain 1 format none level 0 admin-name 1
    association {bnm_id} format icc-based name "01-000000010{bnm_id}" admin-name {bnm_id}
    exit        
exit all
#
"""
        script += f"""#
configure port {porta_mwrot}
    connector
        breakout c1-{int(port["speed"])//1000}g
    exit
    no shutdown
exit all
#
#
configure port {porta_mwrot}/1
    description "{port["description"]}"
    ethernet
        mode hybrid
        encap-type dot1q
        mtu 9212
        collect-stats
        hold-time up 5
        egress-port-qos-policy "QOS_PORT_BACKBONE_CLARO"
        egress-rate {port["bandwidth"]}"""
			
        if port["bnm_ativo"]:                
            script +=f"""
        eth-bn-egress-rate-changes
        eth-cfm
            mep 1 domain 1 association {bnm_id}
                install-mep
                no shutdown
                eth-bn
                    receive
                    rx-update-pacing 1
                exit
            exit
        exit"""
			
        script+= """
        ssm
            no shutdown
        exit
    exit
    no shutdown
exit all
#
#"""
        for interface in port["interfaces"]:
            script += f"""
configure router
    interface {interface["interface"]}
    description "{interface["description"]}"
    address {interface["ip"]}
    port {porta_mwrot}/1:{interface["dot1q"]}
    egress
        vlan-qos-policy "QOS_BACKBONE_CLARO"
    exit
    ingress
        qos "QOS_BACKBONE_CLARO"
    exit
    egress
        agg-rate
            rate max cir max
        exit
        egress-remark-policy "NETWORK-EGRESS"
    exit"""
            if interface["bfd"]:
                script += f"""
    bfd 100 receive 100 multiplier 3
        if-attribute
            delay
                delay-selection dynamic
                dynamic
                    measurement-template "LINK_DELAY_V4"
                    twamp-light
                        ipv4
                            no shutdown
                        exit
                    exit
                exit
            exit
        exit
        no shutdown
    exit"""
            
            script += """
exit all
#
#"""

        if interface["gerencia"]: 
            script += f"""
configure service vprn {bgp["ddd"]}61
    interface "{interface["gerencia"]["interface"]}" create
        description "{interface["gerencia"]["description"]}"
        address {interface["gerencia"]["ip"]}
        sap {porta_mwrot}/1:{interface["gerencia"]["dot1q"]} create
            ingress
                qos 32
            exit
            collect-stats
            accounting-policy 12
            no shutdown
        exit
        no shutdown
    exit
exit all
#
#"""
    if twamp: 
        script += f"""
#--------------------------------------------------
# Router TWAMP-LIGHT Configuration
#--------------------------------------------------
#
configure router twamp-light
    reflector udp-port 862 create"""
        for ip in twamp:
            script += f"""
        prefix {ip} create
        exit"""
        script +="""
        no shutdown
    exit
exit all
#
#
#--------------------------------------------------
# OAM Tests Configuration
#--------------------------------------------------
#
configure test-oam
        link-measurement
            measurement-template "LINK_DELAY_V4" create
                description "TWAMP probe for dynamic link delay IPv4"
                delay avg
                interval 10
                aggregate-sample-window
                    multiplier 12
                    threshold
                        relative 10
                    exit
                exit
                sample-window
                    multiplier 6
                    window-integrity 80
                    threshold
                        relative 10
                    exit
                exit
                twamp-light
                    dscp "be"
                    fc "be"
                exit
                no shutdown
            exit
        exit
        twamp
            twamp-test-pdu
                ipv4-timestamping fp
            exit
        exit
exit all
#
#
"""
    script += f"""
#--------------------------------------------------
# Router OSPFv2 Configuration
#--------------------------------------------------
#
configure router ospf
    router-id {ip_loopback}
    reference-bandwidth 100000000
    timers
        spf-wait 1000 spf-initial-wait 50 spf-second-wait 100
        lsa-generate 1000 lsa-initial-wait 10 lsa-second-wait 25
    exit
    export "OSPF_EXPORT_RMD"
    traffic-engineering-options
        advertise-delay
    exit
    traffic-engineering
    area {area_ospf_formatada}
        nssa
        exit
        interface "system"
            no shutdown
        exit"""
    for port in fibra:
        if port.get("interfaces") and len(port["interfaces"]) > 0:
            script += f"""
            interface "{port["interfaces"][0]["interface"]}"
                interface-type point-to-point
                mtu 1500"""
            if port["lag"]:
                script += """
                authentication-type password
                authentication-key {os.getenv("OSPF_NOKIA")}"""
            else:
                if port["interfaces"][0].get("bfd"):
                    script += """
                bfd-enable remain-down-on-failure"""
                script += """
                authentication-type password
                authentication-key {os.getenv("OSPF_NOKIA")}"""
            script += """
                no shutdown
            exit"""
    
    for port in mwrot:
        if port.get("interfaces") and len(port["interfaces"]) > 0:
            script += f"""
            interface "{port["interfaces"][0]["interface"]}"
                interface-type point-to-point
                mtu 1500"""
            if port["lag"]:
                script += """
                authentication-type password
                authentication-key {os.getenv("OSPF_NOKIA")}"""
            else:
                if port["interfaces"][0].get("bfd"):
                    script += """
                bfd-enable remain-down-on-failure"""
                script += """
                authentication-type password
                authentication-key {os.getenv("OSPF_NOKIA")}"""
            script += """
                no shutdown
            exit"""
    script += """
    exit
    no shutdown
exit all
#
#
"""
    script += """#--------------------------------------------------
# Router LDP Configuration
#--------------------------------------------------
#
configure router ldp
            graceful-restart
            exit
            tunnel-down-damp-time 0
            import-pmsi-routes
            exit
            tcp-session-parameters
            exit
            interface-parameters"""

    for port in fibra:
        if port.get("interfaces") and len(port["interfaces"]) > 0:
            script +=f"""
                interface "{port["interfaces"][0]["interface"]}" dual-stack
                    ipv4
                        local-lsr-id interface
                        fec-type-capability
                            prefix-ipv6 disable
                        exit
                        transport-address interface
                        no shutdown
                    exit
                    no shutdown
                exit"""
    for port in mwrot:
        if port.get("interfaces") and len(port["interfaces"]) > 0:
            script +=f"""
                interface "{port["interfaces"][0]["interface"]}" dual-stack
                    ipv4
                        local-lsr-id interface
                        fec-type-capability
                            prefix-ipv6 disable
                        exit
                        transport-address interface
                        no shutdown
                    exit
                    no shutdown
                exit"""
    script += """
            exit
            targeted-session
        exit
        no shutdown
exit all
#
#
#--------------------------------------------------
# Router MPLS Configuration
#--------------------------------------------------
#
configure router mpls
    interface "system"
        no shutdown
    exit"""            
    for port in fibra:
        if port.get("interfaces") and len(port["interfaces"]) > 0:
            script += f""" 
    interface "{port["interfaces"][0]["interface"]}"
        no shutdown
    exit"""
    for port in mwrot: 
        if port.get("interfaces") and len(port["interfaces"]) > 0:
            script += f""" 
    interface "{port["interfaces"][0]["interface"]}"
        no shutdown
    exit"""
    script += f"""
    no shutdown
exit all
#
#
#--------------------------------------------------
# Router RSVP Configuration
#--------------------------------------------------
#
configure router rsvp
    interface "system"
        no shutdown
    exit"""            
    for port in fibra:
        if port.get("interfaces") and len(port["interfaces"]) > 0:        
            script += f""" 
    interface "{port["interfaces"][0]["interface"]}"
        no shutdown
    exit"""
    for port in mwrot: 
        if port.get("interfaces") and len(port["interfaces"]) > 0:
            script += f""" 
    interface "{port["interfaces"][0]["interface"]}"
        no shutdown
    exit"""
    script += f"""
    no shutdown
exit all
#  
"""
    script += f"""
#--------------------------------------------------
# Router-Policy Configuration
#--------------------------------------------------
#
# EM CASO DE SWAP, DEVEM SER MANTIDAS AS CONFIGURACOES
# ADICIONAIS DE <ROUTER POLICY-OPTIONS> EXISTENTES.
#
# DEVEM SER INDICADAS AS COMMUNITIES DE TODOS OS RMCs 01
# E DE TODOS O RMCs 02 DO DOMINIO IPRAN, CONFORME RELACAO
# DA ENGENHARIA (PLANILHA “INTER-AS-community BGP”).
#
configure router policy-options
    begin
    community "VPN-DADOS" members "target:{bgp["processo"]}:1"
    community "VPN-GERENCIA" members "target:{bgp["processo"]}:61"
    community "VPN-LTE" members "target:{bgp["processo"]}:95"
    community "VPN-ABIS" members "target:{bgp["processo"]}:103"
    community "VPN-GBIU" members "target:{bgp["processo"]}:71"
    community "VPN-VIDEOSURV" members "target:{bgp["processo"]}:93"
"""
    for community, member in bgp["community"]:
        script += f'    community "{community}" members "{member}\n'
    script += f"""
    prefix-list "SYSTEM"
        prefix {ip_loopback}/32 exact
    exit
    community "ANUNCIA_PARA_RMA" members "{bgp["processo"]}:3"
    community "ANUNCIA_PARA_RMP" members "{bgp["processo"]}:2"
    community "ANUNCIA_PARA_RMC_RMD" members "{bgp["processo"]}:1"
    community "INTER-AS-RMS" members "22085:64"
        policy-statement "EXPORT_BGP_GLOBAL"
            entry 991
                from
                    protocol direct
                    prefix-list "SYSTEM"
                exit
                action next-entry
                    community add "ANUNCIA_PARA_RMC_RMD"
                exit
            exit
# A entry 992 so deve ser configurada se houver necessidade de SDP com RMP.
            entry 992
                from
                    protocol direct
                    prefix-list "SYSTEM"
                exit
                action next-entry
                    community add "ANUNCIA_PARA_RMP"
                exit
            exit
# A entry 993 so deve ser configurada se houver necessidade de SDP com RMA.
            entry 993
                from
                    protocol direct
                    prefix-list "SYSTEM"
                exit
                action next-entry
                    community add "ANUNCIA_PARA_RMA"
                exit
            exit
            entry 1000
                from
                    protocol direct
                    prefix-list "SYSTEM"
                exit
                action next-entry
                    community add "INTER-AS-RMS"
                exit
            exit
            entry 1001
                from
                    protocol direct
                    prefix-list "SYSTEM"
                exit
                action next-entry
                    community add "{bgp["policy"][0]}"
                exit
            exit
            entry 1002
                from
                    protocol direct
                    prefix-list "SYSTEM"
                exit
                action accept
                    community add "{bgp["policy"][1]}"
                exit
            exit
        exit
#
            policy-statement "OSPF_EXPORT_RMD"
                entry 10
                    from
                        protocol static
                    exit
                    to
                    exit
                    action accept
                    exit
                exit
                entry 20
                    from
                        protocol direct
                    exit
                    to
                    exit
                    action accept
                    exit
                exit
                default-action drop
                exit
            exit
            policy-statement "VPN_EXPORT_VPN-LTE"
                entry 5
                    from
                        protocol direct
                    exit
                    to
                        protocol bgp-vpn
                    exit
                    action next-entry
                        community add "{bgp["policy"][0]}"
                    exit
                exit
                entry 6
                    from
                        protocol direct
                    exit
                    to
                        protocol bgp-vpn
                    exit
                    action next-entry
                        community add "{bgp["policy"][1]}"
                    exit
                exit
                entry 10
                    from
                        protocol direct
                    exit
                    to
                        protocol bgp-vpn
                    exit
                    action accept
                        community add "VPN-LTE"
                    exit
                exit
                entry 15
                    from
                        protocol static
                    exit
                    to
                        protocol bgp-vpn
                    exit
                    action next-entry
                        community add "{bgp["policy"][0]}"
                    exit
                exit
                entry 16
                    from
                        protocol static
                    exit
                    to
                        protocol bgp-vpn
                    exit
                    action next-entry
                        community add "{bgp["policy"][1]}"
                    exit
                exit
                entry 20
                    from
                        protocol static
                    exit
                    to
                        protocol bgp-vpn
                    exit
                    action accept
                        community add "VPN-LTE"
                    exit
                exit
                entry 25
                    from
                        protocol bgp
                    exit
                    to
                        protocol bgp-vpn
                    exit
                    action next-entry
                        community add "{bgp["policy"][0]}"
                    exit
                exit
                entry 26
                    from
                        protocol bgp
                    exit
                    to
                        protocol bgp-vpn
                    exit
                    action next-entry
                        community add "{bgp["policy"][1]}"
                    exit
                exit
                entry 30
                    from
                        protocol bgp
                    exit
                    to
                        protocol bgp-vpn
                    exit
                    action accept
                        community add "VPN-LTE"
                    exit
                exit
                default-action drop
                exit
            exit
            policy-statement "VPN_IMPORT_VPN-LTE"
                entry 10
                    from
                        protocol bgp-vpn
                        community "VPN-LTE"
                    exit
                    action accept
                    exit
                exit
                default-action drop
                exit
            exit
            policy-statement "VPN_EXPORT_VPN-ABIS"
                entry 5
                    from
                        protocol direct
                    exit
                    to
                        protocol bgp-vpn
                    exit
                    action next-entry
                        community add "{bgp["policy"][0]}"
                    exit
                exit
                entry 6
                    from
                        protocol direct
                    exit
                    to
                        protocol bgp-vpn
                    exit
                    action next-entry
                        community add "{bgp["policy"][1]}"
                    exit
                exit
                entry 10
                    from
                        protocol direct
                    exit
                    to
                        protocol bgp-vpn
                    exit
                    action accept
                        community add "VPN-ABIS"
                    exit
                exit
                entry 15
                    from
                        protocol static
                    exit
                    to
                        protocol bgp-vpn
                    exit
                    action next-entry
                        community add "{bgp["policy"][0]}"
                    exit
                exit
                entry 16
                    from
                        protocol static
                    exit
                    to
                        protocol bgp-vpn
                    exit
                    action next-entry
                        community add "{bgp["policy"][1]}"
                    exit
                exit
                entry 20
                    from
                        protocol static
                    exit
                    to
                        protocol bgp-vpn
                    exit
                    action accept
                        community add "VPN-ABIS"
                    exit
                exit
                entry 25
                    from
                        protocol bgp
                    exit
                    to
                        protocol bgp-vpn
                    exit
                    action next-entry
                        community add "{bgp["policy"][0]}"
                    exit
                exit
                entry 26
                    from
                        protocol bgp
                    exit
                    to
                        protocol bgp-vpn
                    exit
                    action next-entry
                        community add "{bgp["policy"][1]}"
                    exit
                exit
                entry 30
                    from
                        protocol bgp
                    exit
                    to
                        protocol bgp-vpn
                    exit
                    action accept
                        community add "VPN-ABIS"
                    exit
                exit
                default-action drop
                exit
            exit
            policy-statement "VPN_IMPORT_VPN-ABIS"
                entry 10
                    from
                        protocol bgp-vpn
                        community "VPN-ABIS"
                    exit
                    action accept
                    exit
                exit
                default-action drop
                exit
            exit
            policy-statement "VPN_EXPORT_VPN-GBIU"
                entry 5
                    from
                        protocol direct
                    exit
                    to
                        protocol bgp-vpn
                    exit
                    action next-entry
                        community add "{bgp["policy"][0]}"
                    exit
                exit
                entry 6
                    from
                        protocol direct
                    exit
                    to
                        protocol bgp-vpn
                    exit
                    action next-entry
                        community add "{bgp["policy"][1]}"
                    exit
                exit
                entry 10
                    from
                        protocol direct
                    exit
                    to
                        protocol bgp-vpn
                    exit
                    action accept
                        community add "VPN-GBIU"
                    exit
                exit
                entry 15
                    from
                        protocol static
                    exit
                    to
                        protocol bgp-vpn
                    exit
                    action next-entry
                        community add "{bgp["policy"][0]}"
                    exit
                exit
                entry 16
                    from
                        protocol static
                    exit
                    to
                        protocol bgp-vpn
                    exit
                    action next-entry
                        community add "{bgp["policy"][1]}"
                    exit
                exit
                entry 20
                    from
                        protocol static
                    exit
                    to
                        protocol bgp-vpn
                    exit
                    action accept
                        community add "VPN-GBIU"
                    exit
                exit
                entry 25
                    from
                        protocol bgp
                    exit
                    to
                        protocol bgp-vpn
                    exit
                    action next-entry
                        community add "{bgp["policy"][0]}"
                    exit
                exit
                entry 26
                    from
                        protocol bgp
                    exit
                    to
                        protocol bgp-vpn
                    exit
                    action next-entry
                        community add "{bgp["policy"][1]}"
                    exit
                exit
                entry 30
                    from
                        protocol bgp
                    exit
                    to
                        protocol bgp-vpn
                    exit
                    action accept
                        community add "VPN-GBIU"
                    exit
                exit
                default-action drop
                exit
            exit
            policy-statement "VPN_IMPORT_VPN-GBIU"
                entry 10
                    from
                        protocol bgp-vpn
                        community "VPN-GBIU"
                    exit
                    action accept
                    exit
                exit
                default-action drop
                exit
            exit
            policy-statement "VPN_EXPORT_VPN-DADOS"
                entry 5
                    from
                        protocol direct
                    exit
                    to
                        protocol bgp-vpn
                    exit
                    action next-entry
                        community add "{bgp["policy"][0]}"
                    exit
                exit
                entry 6
                    from
                        protocol direct
                    exit
                    to
                        protocol bgp-vpn
                    exit
                    action next-entry
                        community add "{bgp["policy"][1]}"
                    exit
                exit
                entry 10
                    from
                        protocol direct
                    exit
                    to
                        protocol bgp-vpn
                    exit
                    action accept
                        community add "VPN-DADOS"
                    exit
                exit
                entry 15
                    from
                        protocol static
                    exit
                    to
                        protocol bgp-vpn
                    exit
                    action next-entry
                        community add "{bgp["policy"][0]}"
                    exit
                exit
                entry 16
                    from
                        protocol static
                    exit
                    to
                        protocol bgp-vpn
                    exit
                    action next-entry
                        community add "{bgp["policy"][1]}"
                    exit
                exit
                entry 20
                    from
                        protocol static
                    exit
                    to
                        protocol bgp-vpn
                    exit
                    action accept
                        community add "VPN-DADOS"
                    exit
                exit
                entry 25
                    from
                        protocol bgp
                    exit
                    to
                        protocol bgp-vpn
                    exit
                    action next-entry
                        community add "{bgp["policy"][0]}"
                    exit
                exit
                entry 26
                    from
                        protocol bgp
                    exit
                    to
                        protocol bgp-vpn
                    exit
                    action next-entry
                        community add "{bgp["policy"][1]}"
                    exit
                exit
                entry 30
                    from
                        protocol bgp
                    exit
                    to
                        protocol bgp-vpn
                    exit
                    action accept
                        community add "VPN-DADOS"
                    exit
                exit
                default-action drop
                exit
            exit
            policy-statement "VPN_IMPORT_VPN-DADOS"
                exit
                entry 10
                    from
                        protocol bgp-vpn
                        community "VPN-DADOS"
                    exit
                    action accept
                    exit
                exit
                default-action drop
                exit
            exit
            policy-statement "VPN_EXPORT_VPN-GERENCIA"
                entry 5
                    from
                        protocol direct
                    exit
                    to
                        protocol bgp-vpn
                    exit
                    action next-entry
                        community add "{bgp["policy"][0]}"
                    exit
                exit
                entry 6
                    from
                        protocol direct
                    exit
                    to
                        protocol bgp-vpn
                    exit
                    action next-entry
                        community add "{bgp["policy"][1]}"
                    exit
                exit
                entry 10
                    from
                        protocol direct
                    exit
                    to
                        protocol bgp-vpn
                    exit
                    action accept
                        community add "VPN-GERENCIA"
                    exit
                exit
                entry 15
                    from
                        protocol static
                    exit
                    to
                        protocol bgp-vpn
                    exit
                    action next-entry
                        community add "{bgp["policy"][0]}"
                    exit
                exit
                entry 16
                    from
                        protocol static
                    exit
                    to
                        protocol bgp-vpn
                    exit
                    action next-entry
                        community add "{bgp["policy"][1]}"
                    exit
                exit
                entry 20
                    from
                        protocol static
                    exit
                    to
                        protocol bgp-vpn
                    exit
                    action accept
                        community add "VPN-GERENCIA"
                    exit
                exit
                entry 25
                    from
                        protocol bgp
                    exit
                    to
                        protocol bgp-vpn
                    exit
                    action next-entry
                        community add "{bgp["policy"][0]}"
                    exit
                exit
                entry 26
                    from
                        protocol bgp
                    exit
                    to
                        protocol bgp-vpn
                    exit
                    action next-entry
                        community add "{bgp["policy"][1]}"
                    exit
                exit
                entry 30
                    from
                        protocol bgp
                    exit
                    to
                        protocol bgp-vpn
                    exit
                    action accept
                        community add "VPN-GERENCIA"
                    exit
                exit
                default-action drop
                exit
            exit
            policy-statement "VPN_IMPORT_VPN-GERENCIA"
                entry 10
                    from
                        protocol bgp-vpn
                        community "VPN-GERENCIA"
                    exit
                    action accept
                    exit
                exit
                default-action drop
                exit
            exit
            policy-statement "VPN_EXPORT_VPN-VIDEOSURV"
                entry 5
                    from
                        protocol direct
                    exit
                    to
                        protocol bgp-vpn
                    exit
                    action next-entry
                        community add "{bgp["policy"][0]}"
                    exit
                exit
                entry 6
                    from
                        protocol direct
                    exit
                    to
                        protocol bgp-vpn
                    exit
                    action next-entry
                        community add "{bgp["policy"][1]}"
                    exit
                exit
                entry 10
                    from
                        protocol direct
                    exit
                    to
                        protocol bgp-vpn
                    exit
                    action accept
                        community add "VPN-VIDEOSURV"
                    exit
                exit
                entry 15
                    from
                        protocol static
                    exit
                    to
                        protocol bgp-vpn
                    exit
                    action next-entry
                        community add "{bgp["policy"][0]}"
                    exit
                exit
                entry 16
                    from
                        protocol static
                    exit
                    to
                        protocol bgp-vpn
                    exit
                    action next-entry
                        community add "{bgp["policy"][1]}"
                    exit
                exit
                entry 20
                    from
                        protocol static
                    exit
                    to
                        protocol bgp-vpn
                    exit
                    action accept
                        community add "VPN-VIDEOSURV"
                    exit
                exit
                entry 25
                    from
                        protocol bgp
                    exit
                    to
                        protocol bgp-vpn
                    exit
                    action next-entry
                        community add "{bgp["policy"][0]}"
                    exit
                exit
                entry 26
                    from
                        protocol bgp
                    exit
                    to
                        protocol bgp-vpn
                    exit
                    action next-entry
                        community add "{bgp["policy"][1]}"
                    exit
                exit
                entry 30
                    from
                        protocol bgp
                    exit
                    to
                        protocol bgp-vpn
                    exit
                    action accept
                        community add "VPN-VIDEOSURV"
                    exit
                exit
                default-action drop
                exit
            exit
            policy-statement "VPN_IMPORT_VPN-VIDEOSURV"
                entry 10
                    from
                        protocol bgp-vpn
                        community "VPN-VIDEOSURV"
                    exit
                    action accept
                    exit
                exit
                default-action drop
                exit
            exit
            commit
exit all
#
#
#--------------------------------------------------
# Router BGP Configuration
#--------------------------------------------------
#
# NA CONFIGURACAO DO BGP A SEGUIR, AS VIZINHANCAS COM OS
# ROUTE-REFLECTORS DEVEM SER ASSOCIADAS AO GROUP <CLIENT>.
#
configure router bgp
    router-id {ip_loopback}
    multi-path
        ipv4 8
        label-ipv4 8
    exit
    ibgp-multipath
    min-route-advertisement 5
    enable-peer-tracking
    group "Client"
        family ipv4 vpn-ipv4 l2-vpn mvpn-ipv4 label-ipv4 vpn-ipv6
        authentication-key {os.getenv("BGP")}
        outbound-route-filtering
            extended-community
                send-orf
                accept-orf
            exit
        exit
        export "EXPORT_BGP_GLOBAL"
        peer-as {bgp["processo"]}
        local-address {ip_loopback}
        advertise-inactive
        enable-peer-tracking"""
    for ip, neighbor in bgp["neighbors"]:
                script += f"""
        neighbor {ip}
            description "TO_{neighbor}"
            next-hop-self
        exit"""
    script += f"""
    exit
    no shutdown
exit all
#
# 
#--------------------------------------------------
# Service Configuration VPRN GERENCIA, 2G, 3G, 4G e 5G
#--------------------------------------------------
#
configure service
        customer 21 create
            description "CLARO"
        exit
exit all
#
#
configure service vprn {bgp["ddd"]}61 name "GERENCIA" customer 21 create
    autonomous-system {bgp["processo"]}
    bgp-ipvpn
        mpls
            vrf-import "VPN_IMPORT_VPN-GERENCIA"
            vrf-export "VPN_EXPORT_VPN-GERENCIA"
            route-distinguisher {bgp["processo"]}:61
            auto-bind-tunnel
                resolution any
            exit
            no shutdown
        exit
    exit
    no shutdown
exit
#
configure service vprn {bgp["ddd"]}1 name "IUB" customer 21 create
    autonomous-system {bgp["processo"]}
    bgp-ipvpn
       mpls
          vrf-import "VPN_IMPORT_VPN-DADOS"
          vrf-export "VPN_EXPORT_VPN-DADOS"
          route-distinguisher {bgp["processo"]}:1
          auto-bind-tunnel
             resolution any
          exit
          no shutdown
       exit
    exit
    no shutdown
exit
#
configure service vprn {bgp["ddd"]}103 name "ABIS" customer 21 create
    autonomous-system {bgp["processo"]}
    bgp-ipvpn
        mpls
           vrf-import "VPN_IMPORT_VPN-ABIS"
           vrf-export "VPN_EXPORT_VPN-ABIS"
           route-distinguisher {bgp["processo"]}:103
           auto-bind-tunnel
              resolution any
           exit
           no shutdown
        exit
    exit
    no shutdown
exit
#
configure service vprn {bgp["ddd"]}95 name "S1" customer 21 create
    autonomous-system {bgp["processo"]}
    bgp-ipvpn
       mpls
          vrf-import "VPN_IMPORT_VPN-LTE"
          vrf-export "VPN_EXPORT_VPN-LTE"
          route-distinguisher {bgp["processo"]}:95
          auto-bind-tunnel
             resolution any
          exit
          no shutdown
       exit
    exit
    no shutdown
exit
#
configure service vprn {bgp["ddd"]}7281 name "{bgp["ddd"]}7281" customer 21 create
    bgp-ipvpn
        mpls
            vrf-import "GERL3_EBT_CLARO_VPN_IMPORT"
            vrf-export "GERL3_EBT_CLARO_VPN_EXPORT"
            route-distinguisher {bgp["processo"]}:7282
            auto-bind-tunnel
                resolution-filter
                    ldp
                exit
                resolution-filter
            exit
            no shutdown
       exit
    exit
    no shutdown
exit
"""
    if rotas_estaticas:
        script+= """
#--------------------------------------------------
# ROTAS Estáticas nas VPRN 61 1 95 103
#--------------------------------------------------
#"""
        for rota in rotas_estaticas:
            script += f"""
configure service vprn {bgp["ddd"]}{rota["vrf_numero"]}
    static-route-entry {rota["ip_origem"]}/{rota["mask"]}
        next-hop {rota["ip_destino"]}
            no shutdown
        exit
    exit
exit all"""

    script += """
#--------------------------------------------------
# System Sync-If-Timing Configuration
#--------------------------------------------------
#
#
configure system sync-if-timing
    begin
    ql-selection"""

    port_new_old = [(nova, fibra[i]["porta"]) for i, nova in enumerate(portas_fo)]
    port_new_old += [(nova, mwrot[i]["porta"]) for i, nova in enumerate(portas_mwrot)]
    print (port_new_old)
    if ptp:  # só entra se houver referências
        script += "\n    ref-order ref1 ref2 ptp gnss"
        for i, porta_antiga in enumerate(ptp):
            porta_nova = next(nova for nova, antiga in port_new_old if antiga == porta_antiga)
            script+=f"""
    ref{i+1}
        source-port {porta_nova}/1
        no shutdown
    exit"""

    script += """
    revert
    commit
exit all
#
#"""
    script+= """
#--------------------------------------------------
# Redundancy Configuration
#--------------------------------------------------
#
admin redundancy
    synchronize boot-env
    rollback-sync
exit all
#
#
admin save
#"""

    script+= """
#--------------------------------------------------
# SERVICE ASSURANCE AGENT (SAA) 
#--------------------------------------------------"""

    for rmc, ip in saa:
        script+=f"""
    configure saa
        test "T1_{rmc}-BE"
        description "-->{rmc}-BE"
        type
            icmp-ping {ip} ttl 20 size 1500 count 100 timeout 1 fc "be" router-instance "Base"
        exit
        no shutdown
    exit
    test "T2_{rmc}-L2"
        description "-->{rmc}-L2"
        type
            icmp-ping {ip} ttl 20 size 768 count 100 timeout 1 fc "l2" router-instance "Base"
        exit
        no shutdown
    exit
    test "T3_{rmc}-EF"
        description "-->{rmc}-EF"
        type
            icmp-ping {ip} ttl 20 size 128 count 100 timeout 1 fc "ef" router-instance "Base"
        exit
        no shutdown
    exit
    exit all"""
    script+=r'''
#
#
file md cf3:\claro-ipran-SAA-result
/file vi cf3:\claro-ipran-SAA-result\claro-ipran-SAA-script.txt
#
<i> (TECLA)
#'''
    for rmc, ip in saa:
        script+=f"""
oam saa "T1_{rmc}-BE" start
oam saa "T2_{rmc}-L2" start
oam saa "T3_{rmc}-EF" start"""
    script+= r'''
#
<ESC> (TECLA)
#
:wq (TECLA)
#
#
configure system script-control
            script "claro-ipran-SAA-script"
                location "cf3:\claro-ipran-SAA-result\claro-ipran-SAA-script.txt"
                no shutdown
            exit
            script-policy "claro-ipran-SAA-script"
                results "ftp://router:router@10.129.87.98/opt/nsp/nfmp/nebackup/saa/<HOSTNAME>"
                script "claro-ipran-SAA-script"
                no shutdown
            exit
exit all
#
#
configure system cron
        schedule "claro-ipran-SAA-schedule"
            description "Executa os testes SAA a cada 300s"
            interval 300
            script-policy "claro-ipran-SAA-script"
            no shutdown
        exit
exit all
#
#
#
admin save
#
#'''
    if movel:
        script+= f"""
#====================================================================
#QoS 2G ABIS 103
#====================================================================
#
configure qos dscp-fc-map "2" create
            default-action fc "h2" profile in
            dscp "ef" fc "ef"
            dscp "cs5" fc "ef"
            dscp "nc1" fc "h1"
            dscp "cp62" fc "h1"
exit all
#
configure qos ingress-classification-policy "2" allow-attachment any create
            description "TC20_QOS_2G_IN"
            dscp-fc-map "2"
exit all
#
#
configure qos sap-ingress 2 name "TC20_QOS_2G_IN" policer-allocation per-fc create
            description "TC20_QOS_2G_IN"
            ingress-classification-policy "2"
            policer 5 create
                stat-mode offered-profile-with-discards
            exit
            policer 6 create
                stat-mode offered-profile-with-discards
            exit
            policer 7 create
                stat-mode offered-profile-with-discards
            exit
exit all
#
#
configure qos queue-mgmt-policy "QOS_EGRESS_MOVEL" create
            description "QOS_EGRESS_MOVEL"
            mbs 41000
            high-slope
                shutdown
            exit
            low-slope
                shutdown
            exit
            scope template
exit all
#
#
configure qos vlan-qos-policy "2" create
            description "QoS_2G_OUT"
            stat-mode enqueued-with-discards
            queue "5" create
                queue-mgmt "QOS_EGRESS_MOVEL"
                percent-rate 100.00 cir 0.00
                scheduling-priority 3
            exit
            queue "6" create
                percent-rate 100.00 cir 0.00
                scheduling-priority 3
            exit
            queue "7" create
                percent-rate 100.00 cir 0.00
                scheduling-priority 6
            exit
exit all
#
#
#====================================================================
#QoS 3G IUB-DADOS 1
#====================================================================
#
configure qos dscp-fc-map "10" create
            default-action fc "h2" profile in
            dscp "ef" fc "ef"
            dscp "cs5" fc "ef"
            dscp "nc1" fc "h1"
            dscp "cp62" fc "h1"
exit all
#
configure qos ingress-classification-policy "10" allow-attachment any create
            description "TC20_QOS_3G_IN"
            dscp-fc-map "10"
exit all
#
#
configure qos sap-ingress 10 name "TC20_QOS_3G_IN" policer-allocation per-fc create
            description "TC20_QOS_3G_IN"
            ingress-classification-policy "10"
            policer 5 create
                stat-mode offered-profile-with-discards
            exit
            policer 6 create
                stat-mode offered-profile-with-discards
            exit
            policer 7 create
                stat-mode offered-profile-with-discards
            exit
exit all
#
#
configure qos queue-mgmt-policy "QOS_EGRESS_MOVEL" create
            description "QOS_EGRESS_MOVEL"
            mbs 41000
            high-slope
                shutdown
            exit
            low-slope
                shutdown
            exit
            scope template
exit all
#
#
configure qos vlan-qos-policy "10" create
            description "QoS_3G_OUT"
            stat-mode enqueued-with-discards
            queue "5" create
                queue-mgmt "QOS_EGRESS_MOVEL"
                percent-rate 100.00 cir 0.00
                scheduling-priority 3
            exit
            queue "6" create
                percent-rate 100.00 cir 0.00
                scheduling-priority 3
            exit
            queue "7" create
                percent-rate 100.00 cir 0.00
                scheduling-priority 6
            exit
exit all
#
#
#====================================================================
#QoS 4G S1 95
#====================================================================
#
configure qos dscp-fc-map "95" create
            default-action fc "l2"
            dscp "cs4" fc "l1"
            dscp "af41" fc "l1"
            dscp "af42" fc "l1"
            dscp "af43" fc "l1"
            dscp "ef" fc "ef"
            dscp "cs5" fc "ef"
            dscp "nc1" fc "h1"
            dscp "cp62" fc "h1"
exit all
#
configure qos ingress-classification-policy "95" allow-attachment any create
            description "TC20_QOS_4G_IN"
            dscp-fc-map "95"
exit all
#
#
configure qos sap-ingress 95 name "TC20_QOS_4G_IN" policer-allocation per-fc create
            description "TC20_QOS_4G_IN"
            ingress-classification-policy "95"
            policer 2 create
                stat-mode offered-profile-with-discards
            exit
            policer 4 create
                stat-mode offered-profile-with-discards
            exit
            policer 6 create
                stat-mode offered-profile-with-discards
            exit
            policer 7 create
                stat-mode offered-profile-with-discards
            exit
exit all
#
#
configure qos queue-mgmt-policy "QOS_EGRESS_MOVEL" create
     description "QOS_EGRESS_MOVEL"
     mbs 41000
     high-slope
      shutdown
     exit
     low-slope
       shutdown
     exit
     scope template
exit all
#
#
configure qos vlan-qos-policy "95" create
            description "QoS_4G_OUT"
            stat-mode enqueued-with-discards
            queue "1" create
                queue-mgmt "QOS_EGRESS_MOVEL"
                percent-rate 100.00 cir 0.00
                scheduling-priority 1
            exit
            queue "2" create
                queue-mgmt "QOS_EGRESS_MOVEL"
                percent-rate 100.00 cir 0.00
                scheduling-priority 1
            exit
            queue "4" create
                percent-rate 100.00 cir 0.00
                scheduling-priority 1
            exit
            queue "6" create
                percent-rate 100.00 cir 0.00
                scheduling-priority 3
            exit
            queue "7" create
                percent-rate 100.00 cir 0.00
                scheduling-priority 6
            exit
exit all
#
#
#====================================================================
#QoS 5G S1 95
#====================================================================
#
configure qos dscp-fc-map "97" create
            default-action fc "l2"
            dscp "cs4" fc "l1"
            dscp "af41" fc "l1"
            dscp "af42" fc "l1"
            dscp "af43" fc "l1"
            dscp "ef" fc "ef"
            dscp "cs5" fc "ef"
            dscp "nc1" fc "h1"
            dscp "cp62" fc "h1"
exit all
#
configure qos ingress-classification-policy "97" allow-attachment any create
            description "TC20_QOS_5G_IN"
            dscp-fc-map "97"
exit all
#
#
configure qos sap-ingress 97 name "TC20_QOS_5G_IN" policer-allocation per-fc create
            description "TC20_QOS_5G_IN"
            ingress-classification-policy "97"
            policer 2 create
                stat-mode offered-profile-with-discards
            exit
            policer 4 create
                stat-mode offered-profile-with-discards
            exit
            policer 6 create
                stat-mode offered-profile-with-discards
            exit
            policer 7 create
                stat-mode offered-profile-with-discards
            exit
exit all
#
#
configure qos queue-mgmt-policy "QOS_EGRESS_MOVEL" create
     description "QOS_EGRESS_MOVEL"
     mbs 41000
     high-slope
      shutdown
     exit
     low-slope
       shutdown
     exit
     scope template
exit all
#
#
configure qos vlan-qos-policy "97" create
            description "QoS_5G_OUT"
            stat-mode enqueued-with-discards
            queue "1" create
                queue-mgmt "QOS_EGRESS_MOVEL"
                percent-rate 100.00 cir 0.00
                scheduling-priority 1
            exit
            queue "2" create
                queue-mgmt "QOS_EGRESS_MOVEL"
                percent-rate 100.00 cir 0.00
                scheduling-priority 1
            exit
            queue "4" create
                percent-rate 100.00 cir 0.00
                scheduling-priority 1
            exit
            queue "6" create
                percent-rate 100.00 cir 0.00
                scheduling-priority 3
            exit
            queue "7" create
                percent-rate 100.00 cir 0.00
                scheduling-priority 6
            exit
exit all
#
#
#====================================================================
#QoS GERENCIA 61
#====================================================================
#
configure qos dscp-fc-map "132" create
            default-action fc "af"
            dscp "ef" fc "nc"
            dscp "nc2" fc "nc"
exit all
#
configure qos ingress-classification-policy "132" allow-attachment any create
            description "TC20_QOS_GERENCIA_MOVEL_IN"
            dscp-fc-map "132"
exit all
#
#
configure qos sap-ingress 132 name "TC20_QOS_GERENCIA_MOVEL_IN" policer-allocation per-fc create
     description "TC20_QOS_GERENCIA_MOVEL_IN"
     ingress-classification-policy "132"
     policer 3 create
        stat-mode offered-profile-with-discards
     exit
     policer 8 create
        stat-mode offered-profile-with-discards
     exit
exit all
#
#
configure qos vlan-qos-policy "132" create
            description "QOS_GERENCIA_MOVEL_OUT"
            stat-mode enqueued-with-discards
            queue "3" create
                percent-rate 100.00 cir 0.00
                scheduling-priority 3
            exit
            queue "8" create
                percent-rate 100.00 cir 0.00
                scheduling-priority 6
            exit
exit all
"""

    for porta in movel:
        porta_movel = portas10.pop(0)
        portas_movel.append(porta_movel)
        script+= f"""
#====================================================================
# SERVIÇOS MOVEIS INTERFACE FISICA
#====================================================================
    
configure port {porta_movel}
    connector
        breakout c1-{int(porta["speed"])//1000}g
    exit
    no shutdown
exit all
#
configure port {porta_movel}/1
    description "{porta["description"]}"
    ethernet
        mode access
        encap-type dot1q
        speed {porta["speed"]}
        duplex full
        autonegotiate limited
    exit
    no shutdown
exit all
#
#"""
        for interface in porta["interfaces_movel"]:
            if int(interface["vprn"]) == 103: 
                script += f"""
#====================================================================
# CONFIGURAÇÃO 2G ABIS 103
#====================================================================
#
configure service vprn {bgp["ddd"]}{interface["vprn"]} name "ABIS" customer 21 create
    interface "{interface["interface"]}" create
        description "{interface["description"]}"
        address {interface["ip"]}
        sap {porta_movel}/1:{interface["dot1q"]} create
            shutdown
            ingress
                qos 2
            exit
            egress
                vlan-qos-policy "2"
            exit
            collect-stats
            accounting-policy 12
            no shutdown
        exit
        no shutdown
    exit
    no shutdown
exit all
#"""
            elif int(interface["vprn"]) == 1: 
                script += f"""
#====================================================================
# CONFIGURAÇÃO 3G IUB-DADOS 1
#====================================================================
#
configure service vprn {bgp["ddd"]}{interface["vprn"]} name "IUB" customer 21 create
    interface "{interface["interface"]}" create
        description "{interface["description"]}"
        address {interface["ip"]}
        sap {porta_movel}/1:{interface["dot1q"]} create
            shutdown
            ingress
                qos 10
            exit
            egress
                vlan-qos-policy "10"
            exit
            collect-stats
            accounting-policy 12
            no shutdown
        exit
        no shutdown
    exit
    no shutdown
exit all
#
#"""
            elif int(interface["vprn"]) == 95 and not "5G" in interface["description"]: 
                script += f"""
#====================================================================
# CONFIGURAÇÃO 4G S1 95
#====================================================================

configure service vprn {bgp["ddd"]}{interface["vprn"]} name "S1" customer 21 create
    interface "{interface["interface"]}" create
        description "{interface["description"]}"
        address {interface["ip"]}
        sap {porta_movel}/1:{interface["dot1q"]} create
            shutdown
            ingress
                qos 95
            exit
            egress
                vlan-qos-policy "95"
            exit
            collect-stats
            accounting-policy 12
            no shutdown
        exit
        no shutdown
    exit
    no shutdown
exit all
#
#"""
            elif int(interface["vprn"]) == 95 and "5G" in interface["description"]:  
                script += f"""
#====================================================================
# CONFIGURAÇÃO 5G S1 95
#====================================================================
#
configure service vprn {bgp["ddd"]}{interface["vprn"]} name "S1" customer 21 create
    interface "{interface["interface"]}" create
        description "{interface["description"]}"
        address {interface["ip"]}
        sap {porta_movel}/1:{interface["dot1q"]} create
            shutdown
            ingress
                qos 97
            exit
            egress
                vlan-qos-policy "97"
            exit
            collect-stats
            accounting-policy 12
            no shutdown
        exit
        no shutdown
    exit
    no shutdown
exit all
#
#"""
            else:
                script += f"""
#====================================================================
# CONFIGURAÇÃO GERENCIA 61
#====================================================================
configure service vprn {bgp["ddd"]}{interface["vprn"]} name "GERENCIA" customer 21 create
    interface "{interface["interface"]}" create
        description "{interface["description"]}"
        address {interface["ip"]}"""
                if interface["dhcp"]:
                    script += f"""
        dhcp
            no option
            server {interface['dhcp']}
            gi-address {interface["ip"].split("/")[0].strip()}
            no shutdown
        exit"""
                script += f"""
        sap {porta_movel}/1:{interface["dot1q"]} create
            shutdown
            ingress
                qos 132
            exit
            egress
                vlan-qos-policy "132"
            exit
            collect-stats
            accounting-policy 12
            no shutdown
        exit
        no shutdown
    exit
    no shutdown
exit all
#
#
admin save
#"""
    if bateria:
        script += f"""
#====================================================================
# QOS BATERIA
#==================================================================== 
configure qos dscp-fc-map "32" create
            default-action fc "af"
            exit all
#
#
configure qos ingress-classification-policy "32" allow-attachment any create
            description "TC20_QOS_GERENCIA_IN"
            dscp-fc-map "32"
        exit all
#
#
configure qos sap-ingress 32 name "TC20_QOS_GERENCIA_IN" policer-allocation per-fc create
            description "TC20_QOS_GERENCIA_IN"
            ingress-classification-policy "32"
            policer 3 create
                stat-mode offered-profile-with-discards
            exit
exit all
#
#
#====================================================================
# BATERIA LITIO
#===================================================================="""
        for porta in bateria: 
            porta_bateria = portas10.pop(0)
            portas_bateria.append(porta_bateria)
            script += f"""
configure port {porta_bateria}
        connector
            breakout c1-1g
        exit
        no shutdown
    exit all
#
#
configure port {porta_bateria}/1
        description "{porta["description"]}"
        ethernet
            mode access
            speed 1000
            duplex full
            encap-type dot1q
            autonegotiate
        back
        no shutdown
    exit all
#
#
configure service vprn {bgp["ddd"]}61
            interface "{porta["gerencia"]["interface"]}" create
                description "{porta["gerencia"]["description"]}"
                address {porta["gerencia"]["ip"]}
                sap {porta_bateria}/1:0 create
                    ingress
                        qos 32
                    exit
                    collect-stats
                    accounting-policy 12
                exit
            exit
            no shutdown
        exit all
#
#
admin save
#"""
    if empresarial:
        script += f"""
#====================================================================
# QOS e ROUTE POLICY - EMPRESARIAL
#====================================================================
#
configure qos dot1p-fc-map "499" create
            default-action fc "af" profile out
            dot1p 2 fc "af"
        exit all
#
#
configure qos dscp-fc-map "499" create
            default-action fc "af"
            dscp "be" fc "be"
            dscp "ef" fc "ef"
            dscp "cs4" fc "l1"
            dscp "nc1" fc "h1"
            dscp "af41" fc "l1"
            dscp "af42" fc "l1"
            dscp "af43" fc "l1"
        exit all
#
#
configure qos ingress-classification-policy "499" allow-attachment any create
            description "TC20_EoMPLS_CIRCUITO_QOS_DEFAULT_IN"
            dscp-fc-map "499"
        exit all
#
#
configure qos sap-ingress 499 name "TC20_EoMPLS_CIRCUITO_QOS_DEFAULT_IN" policer-allocation per-fc create
            description "TC-EoMPLS-CIRCUITO-7250-IXR"
            ingress-classification-policy "499"
        exit 
exit all
#
#
configure router
        policy-options
          begin
            community "GERL3_EBT_CLARO_7281"
                members "target:65092:7281"
            community "GERL3_EBT_CLARO_7282"
                members "target:65092:7282"
#
            policy-statement "GERL3_EBT_CLARO_VPN_IMPORT"
                entry 10
                    from
                        protocol bgp-vpn
                        community "GERL3_EBT_CLARO_7281"
                    exit
                    to
                    exit
                    action accept
                    exit
                exit
                default-action drop
                exit
            policy-statement "GERL3_EBT_CLARO_VPN_EXPORT"
                entry 10
                    from
                        protocol direct
                    exit
                    to
                        protocol bgp-vpn
                    exit
                    action accept
                        community add "GERL3_EBT_CLARO_7282"
                    exit
                exit
                default-action drop
                exit
           exit
        commit
exit all
#
#
#
#====================================================================
# EMPRESARIAL
#===================================================================="""

    for porta in empresarial:
        porta_edd = portas10.pop(0)
        portas_edd.append(porta_edd)
        script+= f"""
configure port {porta_edd}
        connector
            breakout c1-{int(porta['speed'])//1000}g
        exit
        no shutdown
exit all
#
#
configure port {porta_edd}/1
        description "{porta['description']}"
        ethernet
            speed {porta['speed']}
            no autonegotiate
            mode access
            encap-type {"qinq" if any(ep.get("vlan2") for ep in porta["epipe"]) else "dot1q"}
            mtu {porta['mtu']}
        exit
        no shutdown
exit all
#
#"""
        if porta["gerencia"]:
           script+= f"""
configure service vprn {bgp["ddd"]}7281 name "{bgp["ddd"]}7281" customer 21 create
   interface "{porta_edd}/1.{porta['gerencia']['dot1q']}" create
            description "{porta['gerencia']['description']}"
            address {porta['gerencia']['ip']}
            sap {porta_edd}/1:{porta['gerencia']['dot1q']} create
                ingress
                    qos 499
                    aggregate-policer-rate 517 burst default
                exit
            exit
        exit
    exit
exit all
#
#"""
        if porta["epipe"]:
            for ep in porta["epipe"]:
                script+= f"""
configure service
    sdp {ep['sdp']} mpls create
        description "{ep['description_sdp']}"
        far-end {ep['ip_sdp']}
        ldp
        keep-alive
            shutdown
        exit
        no shutdown
    exit
    epipe {ep['epipe']} name "{ep['description_sdp']}" customer 21 create
        description "{ep['description']}"
        service-mtu {ep['mtu']}
        sap {porta_edd}/1:{ep['vlan']}{'.'+ep['vlan2'] if ep.get('vlan2') else ''} create
            description "{ep['description']}"
            ingress
                qos 499
                aggregate-policer-rate {ep['velocidade']} burst default
            exit
            no shutdown
        exit
        spoke-sdp {ep['ip_sdp']}:{ep['epipe']} create
            no shutdown
        exit
        no shutdown
    exit """

# DE PARA

    de_para_fo = []
    de_para_mwrot = []
    de_para_movel = []
    de_para_bateria = []
    de_para_empresarial = []

    de_para_texto = "\n### DE PARA ###\n"

# NNI FO
    for i in range(len(fibra or [])):
        porta_antiga = fibra[i]['porta']
        porta_nova = f"{portas_fo[i]}"
        de_para_texto += f"De {porta_antiga} → Para {porta_nova} - NNI FIBRA\n"

# NNI MW-ROT
    for i in range(len(mwrot or [])):
        porta_antiga = mwrot[i]['porta']
        porta_nova = f"{portas_mwrot[i]}"
        de_para_texto += f"De {porta_antiga} → Para {porta_nova} - NNI RADIO\n"

# UNI MOVEL
    for i in range(len(movel or [])):
        porta_antiga = movel[i]['porta']
        porta_nova = f"{portas_movel[i]}"
        de_para_texto += f"De {porta_antiga} → Para {porta_nova} - UNI MOVEL\n"

# UNI BATERIA
    for i in range(len(bateria or [])):
        porta_antiga = bateria[i]['porta']
        porta_nova = f"{portas_bateria[i]}"
        de_para_texto += f"De {porta_antiga} → Para {porta_nova} - BATERIA\n"
        
# EMPRESARIAL
    for i in range(len(empresarial or [])):
        porta_antiga = empresarial[i]['porta']
        porta_nova = f"{portas_edd[i]}"
        de_para_texto += f"De {porta_antiga} → Para {porta_nova} - EMPRESARIAL\n"

# Insere o DE PARA no topo do script
    script = de_para_texto + script

## Salva em arquivo
#    with open(f"scripts/{hostname}_NOKIA_IXRe2.txt", 'w', encoding='utf-8') as arquivo:
#       arquivo.write(script)
#    print(f"✅ Script gerado com sucesso para {hostname} NOKIA IXRe2.")

    return script