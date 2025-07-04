import threading
import time
import csv

class ThreadAnalyzer(threading.Thread):
    def __init__(self, queue, interface, log_path):
        super().__init__()
        self.queue = queue
        self.interface = interface
        self.packet_read = []

        self.last_timestamp_sent = 0
        self.top_protocols = {}
        self.top_source_ips = {}
        self.top_source_ipd = {}
        self.latest_pack_to_send = []
        self.prot_threshold = {'ARP' : 49,
                               'ICMP' : 29,
                               'TCP':2}
        self.alarm = False
        self.alarm_list = []
        self.alarm_log = {} #ad ogni chiave è associato il tempo in cui è finito l'allarme
        self.log_path = log_path
        self.running = True

    def get_top_protocols_by_count(self, top_n=4):
        print('get_top_protocols_by_count')
        protocol_counts = {}

        for pkt in self.packet_read:
            proto = pkt.get('protocol', 'Unknown')
            protocol_counts[proto] = protocol_counts.get(proto, 0) + 1

        sorted_protocols = sorted(protocol_counts.items(), key=lambda x: x[1], reverse=True)
        top_protocols = sorted_protocols[:top_n]
        others_count = sum(count for _, count in sorted_protocols[top_n:])
        if others_count > 0:
            top_protocols.append(('Other', others_count))

        items = dict(top_protocols)
        self.top_protocols = items
        self.interface.update_pie_chart(items,selected = 'packet per protocol')

        self.PROTOCOL_MESSAGES = {
            "TCP": "Possible ongoing attack: DoS (TCP flood)",
            "UDP": "Possible ongoing attack: DoS (UDP flood)",
            "DNS": "Possible ongoing attack: DoS (DNS amplification)",
            "ICMP": "Possible ongoing attack: DoS (ping flood)",
            "ARP": "Possible ongoing attack: DoS (ping flood)"
        }

    def get_top_source_ipd_by_count(self, top_n=4):
        print('get_top_source_ipd_by_count')
        ip_counts = {}

        for pkt in self.packet_read:
            ip_dst = pkt.get('ip dst', 'Unknown')
            ip_counts[ip_dst] = ip_counts.get(ip_dst, 0) + 1

        sorted_ipd = sorted(ip_counts.items(), key=lambda x: x[1], reverse=True)
        top_ipd = sorted_ipd[:top_n]
        others_count = sum(count for _, count in sorted_ipd[top_n:])
        if others_count > 0:
            top_ipd.append(('Other', others_count))

        items = dict(top_ipd)
        self.top_ipd = items

        self.interface.update_pie_chart(items,selected = 'IP dst distribution')

    def get_top_source_ips_by_count(self, top_n=4):
        print('get_top_source_ips_by_count')
        ip_counts = {}

        for pkt in self.packet_read:
            ip_src = pkt.get('ip src', 'Unknown')
            ip_counts[ip_src] = ip_counts.get(ip_src, 0) + 1

        sorted_ips = sorted(ip_counts.items(), key=lambda x: x[1], reverse=True)
        top_ips = sorted_ips[:top_n]
        others_count = sum(count for _, count in sorted_ips[top_n:])
        if others_count > 0:
            top_ips.append(('Other', others_count))

        items = dict(top_ips)
        self.top_ips= items

        self.interface.update_pie_chart(items,selected = 'IP source distribution')

    def send_packets_to_table(self):
        new_packets = [pkt for pkt in self.packet_read if pkt["timestamp"] > self.last_timestamp_sent]

        if new_packets:
            # aggiorna il valore massimo prima di inviare
            self.last_timestamp_sent = new_packets[-1]['timestamp']
            self.latest_pack_to_send = new_packets

    def log_protocol_event(self,protocollo, descrizione, inizio, fine):
        with open(self.log_path, mode='a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([protocollo, descrizione, inizio, fine])

    def send_alert(self):
        print('Send Alert')
        temp_alarm = self.alarm_list[:]
        if self.alarm:
            for prot in self.alarm_list:
                flag = prot in self.top_protocols and prot in self.prot_threshold and self.top_protocols[prot] >= self.prot_threshold[prot]

                if not flag:
                    print('devo scrivere nel file')
                    temp_alarm.remove(prot)
                    self.log_protocol_event(prot,self.PROTOCOL_MESSAGES[prot],self.alarm_log[prot],time.time())
                    self.alarm_log.pop(prot,None)

        for key in self.top_protocols:
            if (
                    key in self.prot_threshold and
                    self.top_protocols[key] > self.prot_threshold[key] and
                    key not in temp_alarm
            ):
                temp_alarm.append(key)
                self.alarm_log[key]=time.time()

        self.interface.update_alert_table(self.alarm_list)
        self.alarm_list = temp_alarm
        self.alarm = bool(self.alarm_list)

    def stop(self):
        self.running = False

    def run(self):
        while self.running:
            self.packet_read = self.queue.consume()

            self.get_top_protocols_by_count()
            self.get_top_source_ips_by_count()
            self.get_top_source_ipd_by_count()
            self.send_packets_to_table()
            self.interface.update_table_ip_mac(self.latest_pack_to_send)
            self.interface.update_packet_table(self.latest_pack_to_send)
            #self.interface.update_live_plot(self.latest_pack_to_send)
            self.send_alert()
            print('dormo per 3 secondi')
            time.sleep(3)


