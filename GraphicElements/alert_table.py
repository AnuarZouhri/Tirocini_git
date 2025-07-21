import tkinter as tk
from tkinter import ttk
from datetime import datetime


class DoSAlertTable(ttk.Frame):

    def __init__(self, parent: tk.Widget):
        super().__init__(parent)

        title_label = ttk.Label(self, text="Notification Table", font=("Arial", 10, "bold"))
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

    def add_alert(self, alert: str, alert_time):
        try:
            if not self.tree.winfo_exists():
                return
        except tk.TclError:
            return


        self.tree.insert("", "end", values=(alert, alert_time))

    #Non usato ma può essere utile:
    def clear_all_alerts(self):
        try:
            if not self.tree.winfo_exists():
                return
        except tk.TclError:
            return

        for item in self.tree.get_children():
            self.tree.delete(item)

