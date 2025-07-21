from scapy.all import *

iface = "eth0"
broadcast_ip = "192.168.1.255"   # Indirizzo broadcast della reteh LAN
port = 60000                      # Porta UDP da testare

pkt = IP(dst=broadcast_ip)/UDP(dport=port)/Raw(load="ping")

send(pkt, iface=iface)
print(f"Pacchetto UDP broadcast inviato su {broadcast_ip}:{port}")