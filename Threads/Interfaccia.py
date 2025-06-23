import threading
import tkinter as tk

from Classes.PieChart import PieChartFrame
from Classes.graficoCartesiano import CartesianPlotFrame

class Interfaccia:

    def __init__(self, parent):
        #componenti dell'interfaccia
        self.parent = parent

        self.pie_chart1 = PieChartFrame(self.parent,'Traffico per MAC')
        self.pie_chart1.pack(fill=tk.BOTH, expand=True)

        self.cartesian_plot_frame = CartesianPlotFrame(self.parent, "Bit/s in media")
        self.cartesian_plot_frame.pack(fill=tk.BOTH, expand=True)

        #dati usati per aggiornare l'interfaccia
        self.mac_traffic_percent = {}
        self.prot_traffic = {}
        self.lock = threading.Lock()
        self.condition = threading.Condition(self.lock)
        self.read = False


    def update_data(self, mac):
        with self.condition:
            while self.read:
                self.condition.wait()
            self.mac_traffic_percent.update(mac)
            self.read = True
            print(self.mac_traffic_percent)
            self.read = True
            self.condition.notify_all()

    def update_interface(self):
        with self.condition:
            while not self.read:
                self.condition.wait()
            self.pie_chart1.updateData(self.mac_traffic_percent)
            self.read = False
            self.condition.notify_all()


