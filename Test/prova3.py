from Threads.ThreadSniffer import ThreadSniffer
from Threads.ThreadAnalyzer import ThreadAnalyzer
from Threads.Queue import Queue
from Threads.Interfaccia import Interfaccia
from Threads.Statistics.Statistics import generate_statistics
import tkinter as tk
from Classes.PieChart import PieChartFrame
from Classes.ip_mac_table import IpMacTable
from Classes.table import PacketTable
from Classes.alert_table import DoSAlertTable
from Classes.avg_size_plot import LivePlot
import os
import atexit
import csv
from Classes.avg_size_plot import LivePlot


class Interfaccia:

    def __init__(self, parent):
        self.main_frame = parent

     # Suddivido l'interfaccia in due porzioni
        left_frame = tk.Frame(self.main_frame, bg="white", padx=10, pady=10)
        left_frame.pack(side='left', fill='both', expand=True)

        right_frame = tk.Frame(self.main_frame, bg="white", padx=10, pady=10)
        right_frame.pack(side='left', fill='both', expand=True)

        right_frame_packet_table = tk.Frame(right_frame,bg="white", padx=10, pady=10)
        right_frame_packet_table.pack(side='top',fill='both', expand=True)

        right_frame_ip_mac_table = tk.Frame(right_frame, bg="white", padx=10, pady=10)
        right_frame_ip_mac_table.pack(side='top', fill='both', expand=True)

        right_frame_pie = tk.Frame(right_frame, bg="white", padx=10, pady=10)
        right_frame_pie.pack(side='top', fill='both', expand=True)

        right_frame_pie1 = tk.Frame(right_frame_pie, bg="white", padx=2, pady=2)
        right_frame_pie1.pack(side='left', fill='both', expand=True)

        right_frame_pie2 = tk.Frame(right_frame_pie, bg="white", padx=2, pady=2)
        right_frame_pie2.pack(side='left', fill='both', expand=True)

        #right_frame_pie3 = tk.Frame(right_frame_pie, bg="white", padx=2, pady=2)
        #right_frame_pie3.pack(side='left', fill='both', expand=True)

        right_frame_alert_table = tk.Frame(right_frame, bg="white", padx=2, pady=2)
        right_frame_alert_table.pack(side='top', fill='both', expand=True)


        self.avg_size_plot = LivePlot(left_frame)

        self.packet_table = PacketTable(right_frame_packet_table)
        self.ip_mac_table = IpMacTable(right_frame_ip_mac_table)

        self.pie_chart1 = PieChartFrame(right_frame_pie1, 'Packets per Protocol', legend="Protocols")
        self.pie_chart1.grid(row=0, column=0, sticky='nsew', padx=2)

        self.pie_chart2 = PieChartFrame(right_frame_pie2, 'IP Src Distribution', legend="IP Src")
        self.pie_chart2.grid(row=0, column=1, sticky='nsew', padx=2)

        self.pie_chart3 = PieChartFrame(right_frame_pie2, 'IP Dst Distribution', legend="IP Dst")
        self.pie_chart3.grid(row=0, column=2, sticky='nsew', padx=2)

        self.alert_table = DoSAlertTable(right_frame_alert_table)
        self.alert_table.pack(fill="both", expand=True)


        self.collection_graphics = {
            'packet per protocol': self.pie_chart1,
            'IP source distribution': self.pie_chart2,
            'IP dst distribution': self.pie_chart3
        }

        # Combobox
        self.chart_selector = tk.ttk.Combobox(right_frame_pie2, values=["IP Src", "IP Dst"], state="readonly")
        self.chart_selector.grid(row=1, column=0, columnspan=3, sticky="ew", pady=4)
        self.chart_selector.set("IP Src")
        self.chart_selector.bind("<<ComboboxSelected>>", lambda e: self.show_selected_pie(self.chart_selector.get()))

        # Mostra grafico iniziale
        self.show_selected_pie("IP Src")

    def update_pie_chart(self, data, selected):
        self.collection_graphics[selected].updateData(data)

    def update_table_ip_mac(self, data):
        self.ip_mac_table.update_table(data)

    def update_packet_table(self, data):
        self.packet_table.update_table(data)

    def update_alert_table(self, data):
        self.alert_table.clear_all_alerts()
        if data:
            self.alert_table.add_alert(data)

    #def update_live_plot(self, data):
     #   self.avg_size_plot.update(data)

    #per decidere quale grafico a torta mostrare
    def show_selected_pie(self,selection):
        for chart in (self.pie_chart2, self.pie_chart3):
            chart.grid_remove()
        if selection == "IP Src":
            self.pie_chart2.grid()
        elif selection == "IP Dst":
            self.pie_chart3.grid()


def ultimo_script():
    generate_statistics(file_path)


if __name__ == "__main__":

    root = tk.Tk()
    root.title("Sniffer GUI")
    root.geometry("1900x1000")

    file_path = "../Threads/Statistics/statistiche.txt"
    # generate_statistics(file_path)

    # os.makedirs(os.path.dirname(file_path), exist_ok=True)  # Crea la cartella se non esiste

    if os.path.exists(file_path):
        os.remove(file_path)

    with open(file_path, 'w') as file:
        file.write("PROTOCOLLO,DIMENSIONEvghrtdfxc\n")

    # Percorso file CSV
    log_path = "../Threads/Log/log_protocollo.csv"

    # Crea il file con intestazioni se non esiste
    if not os.path.exists(log_path):
        with open(log_path, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["Protocollo", "Descrizione", "Inizio", "Fine"])

    #plotLive = LivePlot(root)
    shared_queue = Queue()
    interface = Interfaccia(root)
    thread_sniffer = ThreadSniffer(shared_queue, file_path)
    thread_sniffer.daemon = True
    thread_analyzer = ThreadAnalyzer(shared_queue, interface, log_path)
    thread_analyzer.daemon = True
    thread_sniffer.start()
    thread_analyzer.start()
    # atexit.register(ultimo_script)
    root.mainloop()

