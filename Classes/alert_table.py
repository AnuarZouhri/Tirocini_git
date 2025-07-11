import tkinter as tk
from tkinter import ttk
from datetime import datetime


class DoSAlertTable(ttk.Frame):

    def __init__(self, parent: tk.Widget):
        super().__init__(parent)

        title_label = ttk.Label(self, text="Notification table", font=("Arial", 10, "bold"))
        title_label.pack(anchor="w", pady=(0, 2))

        # Scrollbar
        scrollbar = ttk.Scrollbar(self, orient="vertical")
        scrollbar.pack(side="right", fill="y")

        # Treeview con due colonne: Status e Time
        self.tree = ttk.Treeview(self, columns=("Status", "Time"), show="headings", height=4, yscrollcommand=scrollbar.set)
        self.tree.heading("Status", text="Status")
        self.tree.heading("Time", text="Time")

        self.tree.column("Status", anchor="w", width=300)
        self.tree.column("Time", anchor="center", width=120)

        self.tree.pack(fill="both", expand=True)
        scrollbar.config(command=self.tree.yview)

        # Stile
        style = ttk.Style()
        style.configure("Treeview", font=("Arial", 9), rowheight=25)
        style.configure("Treeview.Heading", font=("Arial", 9, "bold"))

        # Messaggi di default
        self.PROTOCOL_MESSAGES = {
            "TCP": "Possible ongoing attack: DoS (TCP flood)",
            "UDP": "Possible ongoing attack: DoS (UDP flood)",
            "DNS": "Possible ongoing attack: DoS (DNS amplification)",
            "ICMP": "Possible ongoing attack: DoS (ARP flood)",
            "ARP": "Possible ongoing attack: DoS (ICMP flood)",
            "Port": "Unexpected data received on the port",
        }

    def add_alert(self, alert: str, alert_time):
        """Aggiunge una riga alla tabella con protocollo e orario"""
        try:
            if not self.tree.winfo_exists():
                return
        except tk.TclError:
            return


        self.tree.insert("", "end", values=(alert, alert_time))

    def clear_all_alerts(self):
        try:
            if not self.tree.winfo_exists():
                return
        except tk.TclError:
            return

        for item in self.tree.get_children():
            self.tree.delete(item)

'''import tkinter as tk
from tkinter import ttk


class DoSAlertTable(ttk.Frame):

    def __init__(self, parent: tk.Widget):
        super().__init__(parent)
        
        title_label = ttk.Label(self, text="⚠ Attack Alerts", font=("Arial", 10, "bold"))
        title_label.pack(anchor="w", pady=(0, 2))

        # Treeview con una sola colonna: "Status"
        self.tree = ttk.Treeview(self, columns=("Status",), show="headings", height=4)
        self.tree.heading("Status", text="Status")
        self.tree.column("Status", anchor="center", width=270)
        self.tree.pack(fill="both", expand=True)

        self._start_times = {}
        style = ttk.Style()
        style.configure("Treeview", font=("Arial", 9), rowheight=25)
        style.configure("Treeview.Heading", font=("Arial", 9, "bold"))

        self._active_alerts = []

        self.PROTOCOL_MESSAGES = {
            "TCP": "Possible ongoing attack: DoS (TCP flood)",
            "UDP": "Possible ongoing attack: DoS (UDP flood)",
            "DNS": "Possible ongoing attack: DoS (DNS amplification)",
            "ICMP": "Possible ongoing attack: DoS (ping flood)",
            "ARP": "Possible ongoing attack: DoS (ping flood)",
            "Port": "unexpected data received on the port",
        }

    def add_alert(self, data):
        try:
            if not self.tree.winfo_exists():
                return
        except tk.TclError:
            return
        self._active_alerts = data

        for proto in self._active_alerts:
            if not self.tree.exists(proto):
                status = self.PROTOCOL_MESSAGES[proto]
                self.tree.insert("", "end", iid=proto, values=(status,))

    def remove_alert(self, proto: str):
        try:
            if not self.tree.winfo_exists():
                return
        except tk.TclError:
            return
        self.tree.delete(proto)
        self._active_alerts.remove(proto)

    def clear_all_alerts(self):
        try:
            if not self.tree.winfo_exists():
                return
        except tk.TclError:
            return
        for proto in self._active_alerts[:]:  # copia della lista per evitare modifica durante iterazione
            self.remove_alert(proto)'''
