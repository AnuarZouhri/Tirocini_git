import threading
import tkinter as tk

from Classes.PieChart import PieChartFrame
from Classes.ip_mac_table import IpMacTable
from Classes.table import PacketTable
from Classes.alert_table import DoSAlertTable
from Classes.avg_size_plot import LivePlot

class Interfaccia:

    def __init__(self, parent):
        #componenti dell'interfaccia
        self.parent = parent

        main_frame = tk.Frame(self.parent)
        main_frame.pack(fill="both", expand=True)

        frame_width, frame_height = 300, 150


        left_frame = tk.Frame(main_frame)
        left_frame.pack(side="left", fill="both", expand=True)

        alert_table_frame = tk.Frame(left_frame, width=frame_width, height=frame_height)
        alert_table_frame.pack(side="top", fill="both", expand=True, pady=(0, 5))
        alert_table_frame.pack_propagate(False)

        '''cartesian_frame = tk.Frame(left_frame, width=frame_width, height=frame_height)
        cartesian_frame.pack(side="top", fill="both", expand=True, pady=(0, 5))
        cartesian_frame.pack_propagate(False)

        self.live_plot = LivePlot(cartesian_frame)'''

        self.alert_table = DoSAlertTable(alert_table_frame)
        self.alert_table.pack(fill="both", expand=True)



        right_frame = tk.Frame(main_frame)
        right_frame.pack(side="right", fill="both", expand=True)

        tables_container = tk.Frame(right_frame)
        tables_container.pack(side="top", fill="both", expand=True)

        # Inizializza le tabelle
        self.packet_table = PacketTable(tables_container)
        self.ip_mac_table = IpMacTable(tables_container)

        # Pie charts sotto le tabelle
        pie_charts_frame = tk.Frame(right_frame)
        pie_charts_frame.pack(side="top", fill="x", padx=0)
        self.pie_chart1 = PieChartFrame(pie_charts_frame, 'packet per protocol', legend="protocols")
        self.pie_chart1.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.pie_chart2 = PieChartFrame(pie_charts_frame, 'IP source distribution', legend="IP source")
        self.pie_chart2.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.pie_chart3 = PieChartFrame(pie_charts_frame, 'IP dst distribution', legend="IP dst")
        self.pie_chart3.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        '''alert_tabel_frame = tk.Frame(right_frame)
        alert_tabel_frame.pack(side="bottom", fill="both", expand=True, pady=(5, 0))
        self.alert_table = DoSAlertTable(alert_tabel_frame)
        self.alert_table.pack(fill="both", expand=True)'''

        self.collection_graphics = {'packet per protocol' : self.pie_chart1,
                                    'IP source distribution' : self.pie_chart2,
                                    'IP dst distribution' : self.pie_chart3}


    def update_pie_chart(self, data,selected):
        # Qui "data" è un dict con i protocolli e il conteggio pacchetti
        # Aggiorna il grafico a torta nel thread principale
        self.parent.after(0, self.collection_graphics[selected].updateData, data)

    def update_table_ip_mac(self, data):
        self.parent.after(0, self.ip_mac_table.update_table, data)

    def update_packet_table(self, data):
        self.parent.after(0, self.packet_table.update_table, data)

    def update_alert_table(self, data):
        self.alert_table.clear_all_alerts()
        if data:
            self.alert_table.add_alert(data)

    def update_live_plot(self,data):
        self.live_plot.update(data)

