
import threading
import tkinter as tk

from Classes.PieChart import PieChartFrame
from Classes.ip_mac_table import IpMacTable
from Classes.table import PacketTable
from Classes.alert_table import DoSAlertTable
from Classes.avg_size_plot import LivePlot

class Interfaccia:

    def __init__(self, parent):
        self.parent = parent

        main_frame = tk.Frame(self.parent)
        main_frame.pack(fill="both", expand=True)

        # Due metà uguali
        left_frame = tk.Frame(main_frame, width=600, bg='lightgrey')
        left_frame.pack(side="left", fill="y")  # Altezza si adatta, larghezza fissa

        right_frame = tk.Frame(main_frame)
        right_frame.pack(side="left", fill="both", expand=True)  # Occupa tutto il resto

        # Configuro il grid sul right_frame per gestire altezza proporzionale
        right_frame.grid_rowconfigure(0, weight=1)  # tabelle
        right_frame.grid_rowconfigure(1, weight=2)  # grafici
        right_frame.grid_rowconfigure(2, weight=2)  # alert
        right_frame.grid_columnconfigure(0, weight=2)

        # Contenitore tabelle (2 tabelle impilate)
        tables_container = tk.Frame(right_frame)
        tables_container.grid(row=0, column=0, sticky='nsew')
        tables_container.grid_propagate(False)  # Disabilita il ridimensionamento automatico in base ai contenuti
        tables_container.config(height=400)  # Imposta un’altezza fissa (modifica il valore finché ti piace)

        tables_container.grid_rowconfigure(0, weight=1)
        tables_container.grid_rowconfigure(1, weight=1)
        tables_container.grid_columnconfigure(0, weight=1)

        # Frame per PacketTable
        packet_table_frame = tk.Frame(tables_container)
        packet_table_frame.grid(row=0, column=0, sticky='nsew')
        self.packet_table = PacketTable(packet_table_frame)

        # Frame per IpMacTable
        ip_mac_table_frame = tk.Frame(tables_container)
        ip_mac_table_frame.grid(row=1, column=0, sticky='nsew')
        self.ip_mac_table = IpMacTable(ip_mac_table_frame)

        # Contenitore grafici a torta (3 affiancati)
        pie_charts_frame = tk.Frame(right_frame)
        pie_charts_frame.grid(row=1, column=0, sticky='nsew', pady=5)

        pie_charts_frame.grid_columnconfigure(0, weight=1)
        pie_charts_frame.grid_columnconfigure(1, weight=1)
        pie_charts_frame.grid_columnconfigure(2, weight=1)
        pie_charts_frame.grid_rowconfigure(0, weight=1)

        self.pie_chart1 = PieChartFrame(pie_charts_frame, 'packet per protocol', legend="protocols")
        self.pie_chart1.grid(row=0, column=0, sticky='nsew', padx=2)

        self.pie_chart2 = PieChartFrame(pie_charts_frame, 'IP source distribution', legend="IP source")
        self.pie_chart2.grid(row=0, column=1, sticky='nsew', padx=2)

        self.pie_chart3 = PieChartFrame(pie_charts_frame, 'IP dst distribution', legend="IP dst")
        self.pie_chart3.grid(row=0, column=2, sticky='nsew', padx=2)

        # Contenitore tabella alert sotto i grafici
        alert_table_frame = tk.Frame(right_frame)
        alert_table_frame.grid(row=2, column=0, sticky='nsew', pady=(5, 0))

        self.alert_table = DoSAlertTable(alert_table_frame)
        self.alert_table.pack(fill="both", expand=True)

        self.collection_graphics = {
            'packet per protocol': self.pie_chart1,
            'IP source distribution': self.pie_chart2,
            'IP dst distribution': self.pie_chart3
        }

    def update_pie_chart(self, data, selected):
        self.parent.after(0, self.collection_graphics[selected].updateData, data)

    def update_table_ip_mac(self, data):
        self.parent.after(0, self.ip_mac_table.update_table, data)

    def update_packet_table(self, data):
        self.parent.after(0, self.packet_table.update_table, data)

    def update_alert_table(self, data):
        self.alert_table.clear_all_alerts()
        if data:
            self.alert_table.add_alert(data)

    def update_live_plot(self, data):
        self.live_plot.update(data)