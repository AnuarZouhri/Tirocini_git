import tkinter as tk
from tkinter import ttk, messagebox
import ipaddress
import os, sys

class StartPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg="#f2f2f2")
        self.controller = controller
        self.setted_value = {}
        self.ports_to_monitor = {}
        self.ip_to_monitor = []

        self.protocolli = ["TCP", "UDP", "ICMP", "ARP"]
        self.entries = []

        # Logo

        if getattr(sys, 'frozen', False):
            base_path = sys._MEIPASS
        else:
            base_path = os.path.abspath(".")

        image_path = os.path.join(base_path, "Pictures", "logo_first_page.png")
        self.logo = tk.PhotoImage(file=image_path)

        ttk.Label(self, image=self.logo, background="#f2f2f2").pack(pady=(30, 20))

        container = tk.Frame(self, bg="#f2f2f2")
        container.pack(pady=10, padx=20)

        container.grid_columnconfigure(0, weight=1)
        container.grid_columnconfigure(1, weight=1)

        # Sezione Interfaccia (centrata con 3 colonne)
        interfaccia_frame = ttk.LabelFrame(container, text="Interface", padding=(20, 10))
        interfaccia_frame.grid(row=0, column=0, columnspan=2, sticky="ew", padx=10, pady=10)

        # Configura 3 colonne per centraggio simmetrico
        interfaccia_frame.grid_columnconfigure(0, weight=1)
        interfaccia_frame.grid_columnconfigure(1, weight=0)
        interfaccia_frame.grid_columnconfigure(2, weight=1)

        # Etichetta e campo nella colonna centrale
        ttk.Label(interfaccia_frame, text="Interface number:").grid(row=0, column=1, padx=10, pady=5, sticky='e')
        self.interface_entry = ttk.Entry(interfaccia_frame, width=25, validate='key')
        self.interface_entry['validatecommand'] = (self.interface_entry.register(self.validate_int), '%P')
        self.interface_entry.grid(row=0, column=2, padx=10, pady=5, sticky='w')

        # Sezione soglie protocolli
        soglie_frame = ttk.LabelFrame(container, text="Critical threshold settings", padding=(20, 10))
        soglie_frame.grid(row=1, column=0, sticky="nsew", padx=10, pady=10)

        for i, nome in enumerate(self.protocolli):
            ttk.Label(soglie_frame, text=f"Theshold {nome}:").grid(row=i, column=0, padx=10, pady=5, sticky='e')
            entry = ttk.Entry(soglie_frame, width=25, validate='key')
            entry['validatecommand'] = (entry.register(self.validate_int), '%P')
            entry.grid(row=i, column=1, padx=10, pady=5, sticky='w')
            self.entries.append(entry)

        # Sezione Monitoraggio
        monitor_frame = ttk.LabelFrame(container, text="Monitoring", padding=(20, 10))
        monitor_frame.grid(row=1, column=1, sticky="nsew", padx=10, pady=10)

        ttk.Label(monitor_frame, text="Dst port to monitor:").grid(row=0, column=0, padx=10, pady=5, sticky='e')
        self.entry_porta = ttk.Entry(monitor_frame, width=25, validate='key')
        self.entry_porta['validatecommand'] = (self.entry_porta.register(self.validate_int), '%P')
        self.entry_porta.grid(row=0, column=1, padx=10, pady=5, sticky='w')

        ttk.Label(monitor_frame, text="IP Src to monitor:").grid(row=1, column=0, padx=10, pady=5, sticky='e')
        self.entry_ip = ttk.Entry(monitor_frame, width=25)
        self.entry_ip.grid(row=1, column=1, padx=10, pady=5, sticky='w')

        # Pulsante Avanti
        self.start_button = ttk.Button(self, text="Start scanning", command=self.start)
        self.start_button.pack(pady=(10, 5))
        self.start_button.bind("<Return>", lambda e: self.start())

        # Lista ordinata di tutti i campi input (incluso il bottone finale)
        self.all_entries = [
            self.interface_entry,
            *self.entries,
            self.entry_porta,
            self.entry_ip,
            self.start_button  # ⬅️ Aggiunto il bottone alla navigazione
        ]

        for idx, entry in enumerate(self.all_entries):
            entry.bind("<Down>", lambda e, i=idx: self.focus_next(i))
            entry.bind("<Up>", lambda e, i=idx: self.focus_prev(i))

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

        if ip:
            if not self.validate_ip(ip):
                messagebox.showerror("Error", "Invalid IP address.")
                return
            else:
                self.ip_to_monitor.append(ip)

        if porta_monitorata.isdigit():
            self.ports_to_monitor[porta_monitorata] = "0.0.0.0"

        # Inserisce anche l'interfaccia
        interface_val = self.interface_entry.get()
        interface = int(interface_val) if interface_val.isdigit() else 0

        soglie_values = [int(e.get()) if e.get().isdigit() else 0 for e in self.entries]
        protocolli_full = ["interface"] + self.protocolli
        valori_finali = [interface] + soglie_values

        self.setted_value = dict(zip(protocolli_full, valori_finali))

        self.controller.start_analysis(self.setted_value, self.ports_to_monitor, self.ip_to_monitor)

    def focus_next(self, current_index):
        if current_index < len(self.all_entries) - 1:
            self.all_entries[current_index + 1].focus_set()

    def focus_prev(self, current_index):
        if current_index > 0:
            self.all_entries[current_index - 1].focus_set()