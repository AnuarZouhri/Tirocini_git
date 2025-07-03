import threading


class ThreadAnalyzer(threading.Thread):
    def __init__(self, queue, interface):
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
                               'TCP':3}
        self.alarm = False
        self.alarm_list = []

    def get_top_protocols_by_count(self, top_n=4):
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

    def get_top_source_ipd_by_count(self, top_n=4):
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
        self.top_ipd= items

        self.interface.update_pie_chart(items,selected = 'IP dst distribution')

    def get_top_source_ips_by_count(self, top_n=4):
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

    def send_alert(self):
        if self.alarm:
            self.alarm_list = [
                prot for prot in self.alarm_list
                if prot in self.top_protocols
                   and prot in self.prot_threshold
                   and self.top_protocols[prot] >= self.prot_threshold[prot]
            ]

        for key in self.top_protocols:
            if (
                    key in self.prot_threshold and
                    self.top_protocols[key] > self.prot_threshold[key] and
                    key not in self.alarm_list
            ):
                self.alarm_list.append(key)

        self.interface.update_alert_table(self.alarm_list)

        self.alarm = bool(self.alarm_list)

    def run(self):
        while True:
            self.packet_read = self.queue.consume()

            self.get_top_protocols_by_count()
            self.get_top_source_ips_by_count()
            self.get_top_source_ipd_by_count()
            self.send_packets_to_table()
            self.interface.update_table_ip_mac(self.latest_pack_to_send)
            self.interface.update_packet_table(self.latest_pack_to_send)
            self.send_alert()


