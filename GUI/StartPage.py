import tkinter as tk
from tkinter import ttk

class StartPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg="#f2f2f2")
        self.controller = controller
        self.setted_value = {}

        ttk.Label(self, text="Easy Scanner", font=("Helvetica", 20)).pack(pady=(20, 10))

        form_frame = tk.Frame(self, bg="#f2f2f2")
        form_frame.pack(pady=10)

        self.entries = []
        self.protocolli = ["interface","TCP", "UDP", "ICMP", "ARP"]  # Esempio

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

        ttk.Button(self, text="Avanti", command=self.start).pack(pady=20)

    def validate_int(self, value):
        return value.isdigit() or value == ""

    def start(self):
        values = [int(e.get()) if e.get().isdigit() else 0 for e in self.entries]
        self.setted_value = dict(zip(self.protocolli, values))
        print(self.setted_value)
        self.controller.start_analysis(self.setted_value)
