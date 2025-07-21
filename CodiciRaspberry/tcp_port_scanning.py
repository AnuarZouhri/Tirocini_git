import argparse
import threading
from scapy.all import IP, TCP, sr1

def scan_port(ip, port, timeout, lock, results):
    pkt = IP(dst=ip)/TCP(dport=port, flags="S")
    response = sr1(pkt, timeout=timeout, verbose=0)

    with lock:
        if response is None:
            print(f"[ ] Porta {port}: Nessuna risposta (filtrata o host irraggiungibile)")
        elif response.haslayer(TCP):
            if response[TCP].flags == 0x12:  # SYN-ACK, porta aperta
                print(f"[+] Porta {port}: Aperta")
                results["open"].append(port)
                # Invio RST per chiudere
                sr1(IP(dst=ip)/TCP(dport=port, flags="R"), timeout=timeout, verbose=0)
            elif response[TCP].flags == 0x14:  # RST-ACK, porta chiusa
                print(f"[-] Porta {port}: Chiusa")
                results["closed"].append(port)
        else:
            print(f"[?] Porta {port}: Risposta inattesa")

def threaded_scan(ip, ports, timeout=1, max_threads=100):
    lock = threading.Lock()
    threads = []
    results = {"open": [], "closed": []}

    for port in ports:
        while threading.active_count() > max_threads:
            pass  # aspetta che si liberi un thread
        t = threading.Thread(target=scan_port, args=(ip, port, timeout, lock, results))
        t.start()
        threads.append(t)

    for t in threads:
        t.join()

    return results

def parse_port_range(range_str):
    try:
        start, end = map(int, range_str.split("-"))
        return range(start, end + 1)
    except:
        raise argparse.ArgumentTypeError("Formato range porte non valido (es: 20-100)")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="TCP Port Scanner con multithreading")
    parser.add_argument("-i", "--ip", required=True, help="IP del target")
    parser.add_argument("-p", "--ports", default="20-140", help="Range di porte (es: 20-100)")
    parser.add_argument("-t", "--timeout", type=int, default=1, help="Timeout per porta (default: 1s)")
    parser.add_argument("-T", "--threads", type=int, default=100, help="Numero massimo di thread (default: 100)")
    args = parser.parse_args()

    ports = parse_port_range(args.ports)
    print(f"[*] Avvio scansione TCP su {args.ip}...")
    result = threaded_scan(args.ip, ports, timeout=args.timeout, max_threads=args.threads)

    print("\n=== Risultato finale ===")
    if result["open"]:
        print(f"Porte aperte trovate: {result['open']}")
    else:
        print("Nessuna porta aperta trovata.")