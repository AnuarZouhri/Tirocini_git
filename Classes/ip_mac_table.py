import tkinter as tk
from tkinter import ttk
from collections import defaultdict
import csv


class IpMacTable:
    def __init__(self, parent_frame):

        self.packet_counts = defaultdict(int)
        self.user_scrolling = False
        self.after_id = None
        self.group_by_ip_src = False

        self.tree = ttk.Treeview(
            parent_frame,
            columns=("ip_src", "mac_src", "ip_dst", "mac_dst", "count"),
            show="headings",
            height=7
        )
        self._setup_tree_columns()

        self.v_scroll = ttk.Scrollbar(parent_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=self.v_scroll.set)

        self.tree.pack(side="left", fill="both", expand=True)
        self.v_scroll.pack(side="right", fill="y")

        self.tree.bind("<Button-1>", self.on_click)


    def _setup_tree_columns(self):
        self.tree.heading("ip_src", text="IP Source", command=self._toggle_group_by_ip)
        self.tree.heading("mac_src", text="MAC Source")
        self.tree.heading("ip_dst", text="IP Destination")
        self.tree.heading("mac_dst", text="MAC Destination")
        self.tree.heading("count", text="Packets", command=self._reset_group_by_ip)

        self.tree.column("ip_src", width=20)
        self.tree.column("mac_src", width=20)
        self.tree.column("ip_dst", width=20)
        self.tree.column("mac_dst", width=20)
        self.tree.column("count", width=9, anchor='center')

    def _toggle_group_by_ip(self):
        self.group_by_ip_src = True

    def _reset_group_by_ip(self):
        self.group_by_ip_src = False

    def on_click(self, event):
        region = self.tree.identify("region", event.x, event.y)
        if region != "cell":
            return

        item = self.tree.identify_row(event.y)
        if not item:
            return

        selected = self.tree.selection()
        if selected and selected[0] == item:
            self.tree.selection_remove(item)
            return "break"

    def update_table(self, data):
        '''print(len(data))
        for i in data:
            print(data)
        print("")'''
        try:
            if not self.tree.winfo_exists():
                return
        except tk.TclError:
            return

        for pkt in data:

            try:
                ip_src = pkt.get("ip src", "N/A")
                ip_dst = pkt.get("ip dst", "N/A")
                mac_src = pkt.get("MAC src", "N/A")
                mac_dst = pkt.get("MAC dst", "N/A")

                key = (ip_src, mac_src, ip_dst, mac_dst)
                self.packet_counts[key] += 1
                #print(self.packet_counts[key])
            except Exception:
                continue

        selected_items = self.tree.selection()
        selected_values = self.tree.item(selected_items[0], "values") if selected_items else None

        children = self.tree.get_children()
        last_visible = False
        if children:
            last_item = children[-1]
            bbox = self.tree.bbox(last_item)
            if bbox:
                y = bbox[1]
                height = self.tree.winfo_height()
                if y + bbox[3] <= height:
                    last_visible = True

        # Cancella righe precedenti
        self.tree.delete(*children)

        # Costruzione nuova tabella
        if self.group_by_ip_src:
            grouped_by_ip = defaultdict(list)
            for (ip_src, mac_src, ip_dst, mac_dst), count in self.packet_counts.items():
                grouped_by_ip[ip_src].append(((ip_src, mac_src, ip_dst, mac_dst), count))

            def ip_to_int(ip):
                try:
                    return int.from_bytes(map(int, ip.split('.')), byteorder='big')
                except Exception:
                    return -1

            grouped_list = sorted(
                grouped_by_ip.items(),
                key=lambda item: (len(item[1]), ip_to_int(item[0])),
                reverse=True
            )

            sorted_items = []
            for _, group in grouped_list:
                sorted_items.extend(group)
        else:
            sorted_items = sorted(self.packet_counts.items(), key=lambda x: x[1], reverse=True)

        new_items = []
        for (ip_src, mac_src, ip_dst, mac_dst), count in sorted_items:
            item_id = self.tree.insert("", "end", values=(ip_src, mac_src, ip_dst, mac_dst, count))
            new_items.append((item_id, (ip_src, mac_src, ip_dst, mac_dst, str(count))))

        if selected_values:
            for item_id, values in new_items:
                if values[:-1] == selected_values[:-1]:
                    self.tree.selection_set(item_id)
                    self.tree.see(item_id)
                    break

        # ✅ Scorri in fondo solo se l’ultima riga era visibile prima
        if last_visible:
            self.tree.update_idletasks()
            self.tree.yview_moveto(1.0)

    def export_to_csv(self, filename="Threads/Log/tabella_pacchetti.csv"):
        try:
            with open(filename, mode="w", newline="") as file:
                writer = csv.writer(file, delimiter=';')
                # Intestazioni colonna
                writer.writerow(["IP Source", "MAC Source", "IP Destination", "MAC Destination", "Packets"])
                # Scrive tutte le righe visibili nella tabella
                for item_id in self.tree.get_children():
                    values = self.tree.item(item_id, "values")
                    writer.writerow(values)
            print(f"Esportazione completata: {filename}")
        except Exception as e:
            print(f"Errore durante l'esportazione: {e}")

