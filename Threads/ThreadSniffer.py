import threading
import time
import datetime
import subprocess


class ThreadSniffer(threading.Thread):

    def __init__(self, queue,file_path,interface="5"):
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

            "-E", "separator=,"
        ]

    def stop(self):
        self.running = False

    def write_pkt(self,protocollo, dimensione):
        with open(self.file_path, 'a') as file:
            #print('ThreadS: write_pkt')
            file.write(f"{protocollo},{dimensione}\n")

    def run(self):
        while self.running:
            #C://Users//darka//PycharmProjects//Tirocini_git//file batch.bat
            with subprocess.Popen(self.command, stdout=subprocess.PIPE,
                                  stderr=subprocess.DEVNULL, text=True) as proc:

                packet_buffer = []
                start_time = time.time()

                for line in proc.stdout:
                    if not self.running:
                        proc.terminate()  # Termina il processo batch
                        break


                    if not line.strip():
                        continue

                    fields = line.strip().split(',')
                    if len(fields) < 4 or fields[3] == "Realtek":
                        continue  # ignora righe non valide

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
                        packet_buffer.append(pk)
                        #print('TS: scansione')
                        self.write_pkt(pk['protocol'],pk['size'])
                    except Exception:
                        continue  # ignora righe malformate

                    # Se è passato 1 secondo, invia i pacchetti raccolti
                    if time.time() - start_time >= 1:
                        #packet_buffer.sort(key=lambda pkt: pkt['timestamp'])

                        self.queue.produce(packet_buffer)
                        packet_buffer = []
                        start_time = time.time()

