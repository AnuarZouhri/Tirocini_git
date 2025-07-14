import threading
import time
import datetime
import subprocess
import sys

class ThreadSniffer(threading.Thread):

    def __init__(self, queue,file_path,ip_to_monitor,interface="5"):
        super().__init__()
        self.queue = queue
        self.file_path = file_path
        self.running = True
        self.command = [
            "tshark",
            "-i", interface,
            "-l",  # Flush output line-by-line
            "-T", "fields",
            "-e", "ip.src",
            "-e", "ip.dst",
            "-e", "frame.time_epoch",
            "-e", "_ws.col.Protocol",
            "-e", "eth.src",
            "-e", "frame.len",
            "-e", "eth.dst",
            "-e", "tcp.dstport",
            "-e", "udp.dstport",
            "-e", "data.data",

            "-E", "separator=,"
        ]
        self.ip_to_monitor = ip_to_monitor
        self.id = 0

    def stop(self):
        self.running = False

    def write_pkt(self,protocollo, dimensione):
        with open(self.file_path, 'a') as file:
            #print('ThreadS: write_pkt')
            file.write(f"{protocollo},{dimensione}\n")

    def run(self):
        CREATE_NO_WINDOW = 0x08000000 if sys.platform == "win32" else 0

        with subprocess.Popen(self.command, stdout=subprocess.PIPE,
                              stderr=subprocess.DEVNULL, text=True,
                              creationflags=CREATE_NO_WINDOW) as proc:

        #with subprocess.Popen(self.command, stdout=subprocess.PIPE,
                              #stderr=subprocess.DEVNULL, text=True) as proc:

            packet_buffer = []
            reference_ts = None

            for line in proc.stdout:
                if not self.running:
                    proc.terminate()
                    break

                if not line.strip():
                    continue

                fields = line.strip().split(',')
                if len(fields) < 4 or fields[3] == "Realtek":
                    continue

                try:
                    epoch_time = float(fields[2])
                    pk = {
                        "ip src": fields[0],
                        "ip dst": fields[1],
                        "timestamp": epoch_time,
                        "protocol": fields[3],
                        "MAC src": fields[4],
                        "size": int(fields[5]),
                        "MAC dst": fields[6],
                        "TCP portdst": fields[7],
                        "UDP portdst": fields[8],
                    }

                    if pk["ip src"] in self.ip_to_monitor:
                        pk["data"] = fields[9]
                    print(pk)
                    print("\n")

                    # Primo pacchetto ricevuto → imposta il riferimento
                    if reference_ts is None:
                        reference_ts = epoch_time

                    # Se entro 1 secondo → accumula
                    if epoch_time - reference_ts < 1:
                        packet_buffer.append(pk)
                        self.write_pkt(pk['protocol'], pk['size'])
                    else:
                        # Superato 1 secondo → invia buffer e riparti
                        self.queue.produce(packet_buffer)
                        packet_buffer = [pk]  # questo pacchetto diventa il primo del nuovo blocco
                        reference_ts = epoch_time
                        self.write_pkt(pk['protocol'], pk['size'])
                        print(self.id)
                        self.id += 1
                except Exception:
                    continue
