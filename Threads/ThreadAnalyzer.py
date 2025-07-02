import threading
from collections import defaultdict, deque


class ThreadAnalyzer(threading.Thread):
    def __init__(self, queue, data):
        super().__init__()
        self.queue = queue
        self.data = data
        self.packet_read = []
        self.mac_packet = defaultdict(deque)
        self.total_byte = 0
        self.last_timestamp = 0
        self.total_package = 0

        self.mac_time_window = 10
        self.prot_time_window = 10

    def add_packet(self):
        for p in self.packet_read:
            self.last_timestamp = p['timestamp']
            self.total_byte += p['size']
            pk = {
                "timestamp": p['timestamp'],
                "size": p['size'],
                "protocol": p['protocol']
            }
            self.mac_packet[p['MAC src']].append(pk)
            self.total_byte += 1

        # Rimozione dei pacchetti troppo vecchi e MAC vuoti
        to_delete = []
        for mac, q in self.mac_packet.items():
            while q and q[0]['timestamp'] < self.last_timestamp - self.mac_time_window:
                old_pkt = q.popleft()
                self.total_byte -= old_pkt['size']
                self.total_byte -= 1
            if not q:
                to_delete.append(mac)

        for mac in to_delete:
            del self.mac_packet[mac]

    def updateAllData(self):
        mac_traffic = {}

        for mac, q in self.mac_packet.items():
            total = sum(pkt['size'] for pkt in q)
            mac_traffic[mac] = total / self.total_byte if self.total_byte else 0.0

        print(mac_traffic)
        self.data.update_data(mac_traffic)

    def run(self):
        while True:
            self.packet_read = self.queue.consume()
            #print(self.packet_read)
            self.add_packet()
            self.updateAllData()
            print(self.total_byte)



