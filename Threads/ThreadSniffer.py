import threading
import subprocess
import datetime


class ThreadSniffer(threading.Thread):

    def __init__(self,queue):
        super().__init__()
        self.queue = queue

    def run(self):
        i = 0
        while True:
            with subprocess.Popen("D:\\WiresharkAnalyzer\\scansione.bat", stdout=subprocess.PIPE,
                                  stderr=subprocess.DEVNULL, text=True) as proc:

                for line in proc.stdout:

                    fields = line.strip().split(',')
                    epoch_time = float(fields[2])
                    #dt = datetime.datetime.fromtimestamp(epoch_time)

                    pk = {
                    "ip src": fields[0],
                    "ip dst": fields[1],
                    "timestamp": epoch_time,
                    "protocol": fields[3],
                    "MAC src": fields[4],
                    "size": int(fields[5])
                        }


                    if len(fields) >= 4:

                        self.queue.produce(pk)
