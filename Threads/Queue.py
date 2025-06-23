from copy import deepcopy
import threading

from os.path import getsize


class Queue:
    def __init__(self):
        self.queue = []
        self.lock = threading.Lock()
        self.condition = threading.Condition(self.lock)
        self.reading = False


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

    def produce(self, e):
        with self.condition:
            # Aspetta finché il consumatore sta leggendo
            while self.reading:
                self.condition.wait()

            self.insert(e)
            #print(f"[PRODUTTORE] Prodotto: {e} (totale: {self.getsize()})")

            # Notifica il consumatore se ci sono almeno 50 elementi
            if self.getsize() >= 10:
                self.condition.notify_all()

    def consume(self):
        with self.condition:
            # Aspetta che ci siano almeno 50 elementi
            while self.getsize() < 10:
                self.condition.wait()

            # Blocca il produttore
            self.reading = True

            copy = self.deepcopy()
            self.clear()
            #print("[CONSUMATORE] Fine consumo")


            # Sblocca il produttore
            self.reading = False
            self.condition.notify_all()
            return copy