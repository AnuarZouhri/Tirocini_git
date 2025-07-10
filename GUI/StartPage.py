import tkinter as tk
from tkinter import ttk, messagebox
import ipaddress  # per validazione IP

class StartPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg="#f2f2f2")
        self.controller = controller
        self.setted_value = {}
        self.ports_to_monitor = {}
        self.ip_to_monitor = []

        ttk.Label(self, text="EASY SHARK", font=("Helvetica", 20)).pack(pady=(20, 10))

        form_frame = tk.Frame(self, bg="#f2f2f2")
        form_frame.pack(pady=10)

        self.entries = []
        self.protocolli = ["interface","TCP", "UDP", "ICMP", "ARP"]

        ttk.Label(form_frame, text=f"N. Interfaccia:").grid(row=0, column=0, padx=10, pady=5, sticky='e')
        entry = ttk.Entry(form_frame, width=20, validate='key')
        entry['validatecommand'] = (entry.register(self.validate_int), '%P')
        entry.grid(row=0, column=1, padx=10, pady=5)
        self.entries.append(entry)

        for i in range(len(self.protocolli)-1):
            ttk.Label(form_frame, text=f"Soglia {self.protocolli[i+1]}:").grid(row=i+1, column=0, padx=10, pady=5, sticky='e')
            entry = ttk.Entry(form_frame, width=20, validate='key')
            entry['validatecommand'] = (entry.register(self.validate_int), '%P')
            entry.grid(row=i+1, column=1, padx=10, pady=5)
            self.entries.append(entry)

        # Campo Porta
        ttk.Label(form_frame, text=f"Inserisci porta dst da monitorare:").grid(row=5, column=0, padx=10, pady=5, sticky='e')
        self.entry_porta = ttk.Entry(form_frame, width=20, validate='key')
        self.entry_porta['validatecommand'] = (entry.register(self.validate_int), '%P')
        self.entry_porta.grid(row=5, column=1, padx=10, pady=5)

        # Campo IP
        ttk.Label(form_frame, text=f"Inserisci indirizzo IP da cui aspetti delle notifiche:").grid(row=6, column=0, padx=10, pady=5, sticky='e')
        self.entry_ip = ttk.Entry(form_frame, width=20)
        self.entry_ip.grid(row=6, column=1, padx=10, pady=5)

        ttk.Button(self, text="Avanti", command=self.start).pack(pady=20)

    def validate_int(self, value):
        return value.isdigit() or value == ""

    def validate_ip(self, ip):
        try:
            ipaddress.IPv4Address(ip)
            return True
        except ipaddress.AddressValueError:
            return False

    def start(self):
        ip = self.entry_ip.get().strip()
        porta_monitorata = self.entry_porta.get()

        # Verifica IP solo se non è vuoto
        if ip:
            if not self.validate_ip(ip):
                messagebox.showerror("Errore", "Indirizzo IP non valido.")
                return
            else:
                self.ip_to_monitor.append(ip)

        if porta_monitorata.isdigit():
            # Se IP è vuoto, imposta 0.0.0.0 di default
            self.ports_to_monitor[porta_monitorata] = "0.0.0.0"

        values = [int(e.get()) if e.get().isdigit() else 0 for e in self.entries]
        self.setted_value = dict(zip(self.protocolli, values))

        self.controller.start_analysis(self.setted_value, self.ports_to_monitor, self.ip_to_monitor)
