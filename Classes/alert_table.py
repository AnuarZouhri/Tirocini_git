import tkinter as tk
from tkinter import ttk
import csv
import os
from datetime import datetime

class DoSAlertTable(ttk.Frame):
    """
    Widget per la visualizzazione di allerte DoS basate sul protocollo rilevato.
    """

    def __init__(self, parent: tk.Widget):
        super().__init__(parent)

        title_label = ttk.Label(self, text="⚠ Attack Alerts", font=("Arial", 12, "bold"))
        title_label.pack()

        self.tree = ttk.Treeview(self, columns=("Protocol", "Status", "StartTime"), show="headings", height=4)
        self.tree.heading("Protocol", text="Protocol")
        self.tree.heading("Status", text="Status")
        self.tree.heading("StartTime", text="Start Time")
        self.tree.column("Protocol", anchor="center", width=70)
        self.tree.column("Status", anchor="center", width=280)
        self.tree.column("StartTime", anchor="center", width=150)

        """
        self.tree = ttk.Treeview(self, columns=("Protocol", "Status"), show="headings", height=4)
        self.tree.heading("Protocol", text="Protocol")
        self.tree.heading("Status", text="Status")
        self.tree.column("Protocol", anchor="center", width=70)
        self.tree.column("Status", anchor="center", width=280)
        self.tree.pack(fill="both", expand=True, padx=10)
        """
        self._start_times = {}  # Per memorizzare data/ora inizio alert

        # Crea il file CSV con intestazioni se non esiste ancora
        if not os.path.exists("alert_log.csv"):
            with open("alert_log.csv", mode='w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow(["Protocol", "Status", "StartTime", "EndTime"])

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

    """
    def add_alert(self, data):

        self._active_alerts = data

        for proto in self._active_alerts:
            if not self.tree.exists(proto):  # <-- controlla se l'iid esiste
                status = self.PROTOCOL_MESSAGES[proto]
                self.tree.insert("", "end", iid=proto, values=(proto, status))
    """

    def add_alert(self, data):
        self._active_alerts = data

        for proto in self._active_alerts:
            if not self.tree.exists(proto):
                status = self.PROTOCOL_MESSAGES.get(proto, "Unknown alert")
                start_time = datetime.now()
                self._start_times[proto] = start_time
                start_time_str = start_time.strftime("%Y-%m-%d %H:%M:%S")

                # Inserisci anche la colonna StartTime nella tabella (modifica la definizione Treeview di conseguenza)
                self.tree.insert("", "end", iid=proto, values=(proto, status, start_time_str))

                # Scrivi la riga di inizio alert nel CSV
                with open("alert_log.csv", mode='a', newline='', encoding='utf-8') as f:
                    writer = csv.writer(f)
                    writer.writerow([proto, status, start_time_str, ""])
    """
    def remove_alert(self, proto: str):
        Rimuove un allarme esistente.
        self.tree.delete(proto)
        self._active_alerts.remove(proto)
    """
    def clear_all_alerts(self):
        """Cancella tutte le allerte visibili."""
        for proto in self._active_alerts:
            self.remove_alert(proto)

    def remove_alert(self, proto: str):
        if self.tree.exists(proto):
            self.tree.delete(proto)

        if proto in self._active_alerts:
            self._active_alerts.remove(proto)

        if proto in self._start_times:
            end_time_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            # Aggiorna il file CSV sostituendo l'EndTime vuoto con l'ora corrente
            rows = []
            with open("alert_log.csv", mode='r', newline='', encoding='utf-8') as f:
                rows = list(csv.reader(f))

            # Cerca la riga corrispondente a proto con EndTime vuoto (ultima dall’alto)
            for i in range(len(rows) - 1, 0, -1):
                if rows[i][0] == proto and rows[i][3] == "":
                    rows[i][3] = end_time_str
                    break

            with open("alert_log.csv", mode='w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerows(rows)

            del self._start_times[proto]
