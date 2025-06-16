import threading


class Data:

    def __init__(self):
        self.mac_traffic_percent = {}
        self.prot_traffic = {}
        self.lock = threading.Lock()
        self.condition = threading.Condition(self.lock)
        self.read = False


    def updateData(self, mac):
        with self.condition:
            self.mac_traffic_percent.update(mac)
            self.read = True
            #print(self.mac_traffic_percent)
            self.condition.notify_all()

