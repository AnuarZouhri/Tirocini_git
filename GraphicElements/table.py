import tkinter as tk
from tkinter import ttk
from collections import defaultdict, Counter
import statistics
import datetime as datetime
import csv

class PacketTable:
    def __init__(self, parent_frame):
        self.tree = ttk.Treeview(
            parent_frame,
            columns=(
                "Id scansione", "count", "tcp_udp", "protocols",
                "bitrate", "Time"
            ),
            show="headings",
            height=7
        )

        self.tree.heading("Id scansione", text="Id scansione")
        self.tree.heading("count", text="Frames")
        self.tree.heading("tcp_udp", text="TCP/UDP (%)")
        self.tree.heading("protocols", text="Protocols")
        self.tree.heading("bitrate", text="Bit Rate (bps)")
        self.tree.heading("Time", text="Time")

        self.tree.column("Id scansione", width=85,stretch=False)
        self.tree.column("count", width=70,stretch=False)
        self.tree.column("tcp_udp", width=20)
        self.tree.column("protocols", width=20)
        self.tree.column("bitrate", width=95,stretch=False)
        self.tree.column("Time", width=150,stretch=False)

        self.tree.pack(fill="both", expand=True)

        self.after_id = None
        self.second = 0
        self.last_ts_rcv = 0
        self.data = []

        self.tree.bind("<Button-1>", self.on_click)


    def on_click(self, event):
        region = self.tree.identify("region", event.x, event.y)
        if region == "heading":
            return

        row_id = self.tree.identify_row(event.y)
        if not row_id:
            self.tree.selection_remove(self.tree.selection())
            return "break"

        selected = self.tree.selection()
        if row_id in selected:
            self.tree.selection_remove(row_id)
            return "break"

    def update_table(self, data):
        try:
            if not self.tree.winfo_exists():
                return
        except tk.TclError:
            return

        if not data:
            self.second += 1
            item_id = self.tree.insert(
                "", "end",
                values=(self.second, 0, "0% / 0%", [], 0, "")
            )
            self.tree.see(item_id)
            return

        self.data.extend(data)

        protocol_list = []
        tcp_count = 0
        udp_count = 0
        total_bytes = 0
        count = 0
        j = 0

        # Timestamp di riferimento per la finestra di 1 secondo
        start_ts = self.data[0]['timestamp']

        for i, pkt in enumerate(self.data):
            if pkt['timestamp'] - start_ts < 1:
                if pkt['protocol'] == 'TCP':
                    tcp_count += 1
                if pkt['protocol'] == 'UDP':
                    udp_count += 1
                if pkt['protocol'] not in protocol_list:
                    protocol_list.append(pkt['protocol'])
                count += 1
                total_bytes += pkt['size']
                j = i
            else:
                break

        self.last_ts_rcv = self.data[j]['timestamp']
        self.second += 1
        total = tcp_count + udp_count
        tcp_udp_str = (
            f"{round((tcp_count / total) * 100, 2)}% / {round(100 - (tcp_count / total * 100), 2)}%"
            if total > 0 else "0% / 0%"
        )

        # Verifica se l'ultima riga è visibile
        children = self.tree.get_children()
        last_visible = False
        if children:
            last_item = children[-1]
            bbox = self.tree.bbox(last_item)
            if bbox:
                y = bbox[1]
                height = self.tree.winfo_height()
                if y < height:
                    last_visible = True

        # Timestamp formattato con millisecondi
        dt = datetime.datetime.fromtimestamp(start_ts)
        formatted = dt.strftime('%d/%m/%Y %H:%M:%S') + f".{int(dt.microsecond / 1000):03d}"

        item_id = self.tree.insert(
            "", "end",
            values=(self.second, count, tcp_udp_str, protocol_list, total_bytes * 8, formatted)
        )

        if last_visible:
            self.tree.see(item_id)

        # Rimuovi i pacchetti già processati
        if j == 0:
            del self.data[0]
        else:
            del self.data[:j + 1]



    def export_to_csv(self, filename):
        try:
            with open(filename, mode="w", newline="") as file:
                writer = csv.writer(file, delimiter=';')
                # Intestazioni colonna
                writer.writerow(["Id scansione", "Frames", "TCP/UDP (%)", "Protocols", "Bit rate (bps)", "Time"])
                # Scrive tutte le righe visibili nella tabella
                for item_id in self.tree.get_children():
                    values = self.tree.item(item_id, "values")
                    writer.writerow(values)
            print(f"Esportazione completata: {filename}")
        except Exception as e:
            print(f"Errore durante l'esportazione: {e}")

        #print(f"[DEBUG] Update duration: {time.time() - t0:.2f} s")
