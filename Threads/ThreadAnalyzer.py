import threading
import time
import csv
import datetime

from pyexpat.errors import messages


class ThreadAnalyzer(threading.Thread):
    def __init__(self, queue, interface, log_path,threshold, ports):

        super().__init__()
        self.queue = queue
        self.interface = interface
        self.packet_read = []

        #dati da passare ai diversi oggetti grafici
        self.last_timestamp_sent = 0
        self.top_protocols = {}
        self.top_source_ips = {}
        self.top_source_ipd = {}
        self.latest_pack = []


        self.prot_threshold = threshold
        self.ports = ports #porte da monitorare

        self.start_attack_messages = {
            "TCP": "Possible ongoing attack: DoS (TCP flood)",
            "UDP": "Possible ongoing attack: DoS (UDP flood)",
            "DNS": "Possible ongoing attack: DoS (DNS amplification)",
            "ICMP": "Possible ongoing attack: DoS (ARP flood)",
            "ARP": "Possible ongoing attack: DoS (ICMP flood)",
            "Port": "Unexpected data received on the port",
        }

        self.end_attack_message = {
            "TCP": "End of TCP flooding",
            "UDP": "End of UDP flooding",
            "DNS": "End of DNS Amplification",
            "ICMP": "End of ARP flooding",
            "ARP": "End of ICMP flooding",
        }


        #print(self.prot_threshold)

        self.alarm = False
        self.alarm_list = []
        self.alarm_log = {} #ad ogni chiave è associato il tempo in cui è finito l'allarme
        self.log_path = log_path
        self.running = True

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

    def new_packets(self):
        new_packets = [pkt for pkt in self.packet_read if pkt["timestamp"] > self.last_timestamp_sent]

        if new_packets:
            # aggiorna il valore massimo prima di inviare
            self.last_timestamp_sent = new_packets[-1]['timestamp']

        self.latest_pack = new_packets

    def packet_protocol_plot(self):
        filtered_list = [
            {"protocol": pkt["protocol"]}
            for pkt in self.latest_pack
            if "protocol" in pkt
        ]

        return filtered_list

    def packet_avg_size_plot(self):
        filtered_list = [
            {"size": pkt["size"], 'protocol': pkt['protocol']}
            for pkt in self.latest_pack
            if "size" in pkt
        ]

        return filtered_list

    def packet_table(self):
        filtered_list = [
            {"size": pkt["size"], 'protocol': pkt['protocol'], 'timestamp':pkt['timestamp']}
            for pkt in self.latest_pack
            if "size" in pkt and 'protocol' in pkt and 'timestamp' in pkt
        ]

        return filtered_list

    def packet_ip_mac_table(self):
        filtered_list = [
            {"ip src": pkt["ip src"], 'ip dst': pkt['ip dst'], 'MAC dst':pkt['MAC dst'], 'MAC src':pkt['MAC src']}
            for pkt in self.latest_pack
            if "ip src" in pkt and 'ip dst' in pkt and 'MAC dst' in pkt and 'MAC src' in pkt
        ]

        return filtered_list

    def packet_port_plot(self):
        filtered_list = []

        for pkt in self.latest_pack:

            port = None
            if pkt.get("TCP portdst"):
                port = pkt["TCP portdst"]
            elif pkt.get("UDP portdst"):
                port = pkt["UDP portdst"]

            if port:
                filtered_list.append({
                    "port dst": int(port)
                })
        return filtered_list

    def write_log_protocol_event(self, descrizione, inizio, fine):
        # Conversione timestamp → stringa leggibile
        inizio_str = self.get_time(inizio)
        fine_str = self.get_time(fine)

        with open(self.log_path, mode='a', newline='') as file:
            writer = csv.writer(file, delimiter=';')
            writer.writerow([descrizione, inizio_str, fine_str])


    def send_alert(self):
        temp_alarm = self.alarm_list[:]

        # Rimuovi gli allarmi rientrati
        if self.alarm:
            for prot in self.alarm_list:
                flag = (
                        prot in self.top_protocols and
                        prot in self.prot_threshold and
                        self.top_protocols[prot] >= self.prot_threshold[prot]
                )

                if not flag:
                    self.interface.update_alert_table(self.end_attack_message[prot],self.get_time(time.time()))
                    temp_alarm.remove(prot)
                    self.write_log_protocol_event(self.start_attack_messages[prot], self.alarm_log[prot], time.time())
                    self.alarm_log.pop(prot, None)

        # Aggiungi solo nuovi allarmi (quelli non già in temp_alarm)
        for key in self.top_protocols:
            if (
                    key in self.prot_threshold and
                    self.top_protocols[key] > self.prot_threshold[key] and
                    key not in temp_alarm
            ):
                temp_alarm.append(key)
                self.alarm_log[key] = time.time()


                self.interface.update_alert_table(self.start_attack_messages[key], self.get_time(time.time()))

        self.alarm_list = temp_alarm
        self.alarm = bool(self.alarm_list)

    def check_risky_port(self):
        for pkt in self.latest_pack:
            port = pkt.get('TCP portdst') or pkt.get('UDP portdst')
            if not port:
                continue

            if port in self.ports:
                print('SCRIVO NEL FILE')
                message = self.start_attack_messages['Port'] + f" {port}"
                self.interface.update_alert_table(message,self.get_time(time.time()))
                self.write_log_protocol_event(message,time.time(),time.time())

    def check_new_messages(self):
        for pkt in self.latest_pack:
            if pkt.get('data'):
                text = bytes.fromhex(pkt['data']).decode("utf-8", errors="ignore")
                print(text)
                self.interface.update_alert_table(text,self.get_time(time.time()))
                self.write_log_protocol_event(text,time.time(),time.time())

    def stop(self):
        self.running = False

        current_time = time.time()
        for prot in self.alarm_list:
            if prot in self.alarm_log:
                start_time = self.alarm_log[prot]
                self.write_log_protocol_event(
                    self.start_attack_messages.get(prot, f"Alert for {prot}"),
                    start_time,
                    current_time
                )

    def get_time(self, time: float):
        return datetime.datetime.fromtimestamp(time).strftime('%d/%m/%Y %H:%M:%S')

    def run(self):
        while self.running:
            self.packet_read = self.queue.consume() #ottieni i nuovi dati

            self.get_top_protocols_by_count()
            self.get_top_source_ips_by_count()
            self.get_top_source_ipd_by_count()
            self.new_packets()
            self.interface.update_table_ip_mac(self.packet_ip_mac_table())
            self.interface.update_packet_table(self.packet_table())
            self.interface.update_live_plot(self.packet_avg_size_plot())
            self.interface.update_protocol_live_plot(self.packet_protocol_plot())
            self.interface.update_port_plot(self.packet_port_plot())
            self.check_risky_port()
            self.check_new_messages()
            self.send_alert()
            #print('ThreadA: Aggiornamento completato')