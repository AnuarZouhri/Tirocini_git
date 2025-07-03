import threading
import subprocess
import time
import datetime


class ThreadSniffer(threading.Thread):

    def __init__(self, queue,file_path):
        super().__init__()
        self.queue = queue
        self.file_path = file_path

    def write_pkt(self,protocollo, dimensione):
        with open(self.file_path, 'a') as file:
            file.write(f"{protocollo},{dimensione}\n")

    def run(self):
        while True:
            with subprocess.Popen("D:\\WiresharkAnalyzer\\scansione.bat", stdout=subprocess.PIPE,
                                  stderr=subprocess.DEVNULL, text=True) as proc:

                packet_buffer = []
                start_time = time.time()

                for line in proc.stdout:


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
                            "MAC dst": fields[6]
                        }
                        packet_buffer.append(pk)
                        self.write_pkt(pk['protocol'],pk['size'])
                    except Exception:
                        continue  # ignora righe malformate

                    # Se è passato 1 secondo, invia i pacchetti raccolti
                    if time.time() - start_time >= 1:
                        #packet_buffer.sort(key=lambda pkt: pkt['timestamp'])

                        self.queue.produce(packet_buffer)
                        packet_buffer = []
                        start_time = time.time()
