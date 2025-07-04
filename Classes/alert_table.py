import tkinter as tk
from tkinter import ttk
import csv
import os
from datetime import datetime

class DoSAlertTable(ttk.Frame):
    
    #Widget per la visualizzazione di allerte DoS basate sul protocollo rilevato.
    

    def __init__(self, parent: tk.Widget):
        super().__init__(parent)

        title_label = ttk.Label(self, text="⚠ Attack Alerts", font=("Arial", 10, "bold"))
        title_label.pack()

        self.tree = ttk.Treeview(self, columns=("Protocol", "Status"), show="headings", height=4)
        self.tree.heading("Protocol", text="Protocol")
        self.tree.heading("Status", text="Status")
        self.tree.column("Protocol", anchor="center", width=70)
        self.tree.column("Status", anchor="center", width=280)
        self.tree.pack(fill="both", expand=True, padx=10)

        self._start_times = {}  # Per memorizzare data/ora inizio alert
        
        style = ttk.Style()
        style.configure("Treeview", font=("Arial", 9), rowheight=25)
        style.configure("Treeview.Heading", font=("Arial", 9, "bold"))

        self._active_alerts = []

        self.PROTOCOL_MESSAGES = {
            "TCP": "Possible ongoing attack: DoS (TCP flood)",
            "UDP": "Possible ongoing attack: DoS (UDP flood)",
            "DNS": "Possible ongoing attack: DoS (DNS amplification)",
            "ICMP": "Possible ongoing attack: DoS (ping flood)",
            "ARP": "Possible ongoing attack: DoS (ping flood)"
        }


    def add_alert(self, data):
        try:
            if not self.tree.winfo_exists():
                return
        except tk.TclError:
            return
        self._active_alerts = data

        for proto in self._active_alerts:
            if not self.tree.exists(proto):  # <-- controlla se l'iid esiste
                status = self.PROTOCOL_MESSAGES[proto]
                self.tree.insert("", "end", iid=proto, values=(proto, status))


    def remove_alert(self, proto: str):
        #Rimuove un allarme esistente.
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
        #Cancella tutte le allerte visibili.
        for proto in self._active_alerts:
            self.remove_alert(proto)
