from copy import deepcopy
import threading

from os.path import getsize


class Queue:
    def __init__(self,max_age=10):
        self.queue = []
        self.lock = threading.Lock()
        self.condition = threading.Condition(self.lock)
        self.writing = True
        self.max_age = max_age
        self.last_ts_read = 0


    def insert(self, e):
        self.queue.append(e)

    def pop(self):
        self.queue.pop(0)

    def clear(self):
        self.queue.clear()

    def deepcopy(self):
        return deepcopy(self.queue)

    def getsize(self):
        return len(self.queue)

    def remove_old_packets(self):
        if not self.queue:
            return


        # Mantieni solo i pacchetti con timestamp >= threshold
        self.queue = [pkt for pkt in self.queue if (self.queue[-1]['timestamp'] - pkt['timestamp'] <= self.max_age)]

    def produce(self, e):
        with self.condition:
            while not self.writing:
                self.condition.wait()
            # Inserisce pacchetti multipli o singoli
            if isinstance(e, list):
                for pkt in e:
                    self.insert(pkt)
            else:
                self.insert(e)


            # Rimuove pacchetti troppo vecchi
            self.remove_old_packets()

            if self.getsize() >= 1:
                pass
            self.writing = False
            self.condition.notify_all()


    def consume(self):
        with self.condition:
            # Aspetta che ci siano almeno 50 elementi
            while self.writing:
                self.condition.wait()

            copy = self.deepcopy()
            #print("[CONSUMATORE] Fine consumo")


            # Sblocca il produttore
            self.writing = True
            self.condition.notify_all()
            return copy