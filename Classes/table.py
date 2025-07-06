import tkinter as tk
from tkinter import ttk
from collections import defaultdict, Counter
import statistics
import time

class PacketTable:
    def __init__(self, parent_frame):
        self.tree = ttk.Treeview(
            parent_frame,
            columns=(
                "second", "count", "tcp_udp", "protocols",
                "bitrate"
            ),
            show="headings",
            height=7
        )

        self.tree.heading("second", text="Second")
        self.tree.heading("count", text="Frames")
        self.tree.heading("tcp_udp", text="TCP/UDP (%)")
        self.tree.heading("protocols", text="Protocols")
        self.tree.heading("bitrate", text="Bit Rate (bps)")

        self.tree.column("second", width=70,stretch=False)
        self.tree.column("count", width=70,stretch=False)
        self.tree.column("tcp_udp", width=20)
        self.tree.column("protocols", width=20)
        self.tree.column("bitrate", width=95,stretch=False)

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

    def update_table(self,data):
        try:
            if not self.tree.winfo_exists():
                return
        except tk.TclError:
            return
        '''print('vecchi dati')
        print(len(self.data))
        for i in self.data:
            print(i)
        print("--------")'''
        self.data.extend(data)
        '''print('nuovi dati')
        print(len(self.data))
        for i in self.data:
            print(i)
        print("---------")'''
        protocol_list = []
        tcp_count = 0
        udp_count = 0
        total_bytes = 0
        count = 0
        j = 0

        self.last_ts_rcv = data[0]['timestamp']
        '''print(len(data))
        for i in data:
            print(data)
        print("")'''
        for i, pkt in enumerate(self.data):
            if pkt['timestamp'] - self.last_ts_rcv < 1:
                if pkt['protocol'] == 'TCP':
                    tcp_count += 1
                if pkt['protocol'] == 'UDP':
                    udp_count += 1
                if pkt['protocol'] not in protocol_list:
                    protocol_list.append(pkt['protocol'])
                count = count + 1
                total_bytes += pkt['size']
                j = i
            elif pkt['timestamp'] - self.last_ts_rcv >= 1:
                break


        self.last_ts_rcv = self.data[j]['timestamp']


        self.second = self.second + 1
        total = tcp_count + udp_count
        tcp_udp_str = f"{round(((tcp_count / total) * 100),2)}% / {round(100 - (tcp_count / total * 100),2)}%" if total > 0 else "0% / 0%"

        # Verifica se l'ultima riga è visibile PRIMA di inserire una nuova riga
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

        # Inserisce la nuova riga
        item_id = self.tree.insert("", "end", values=(
            self.second, count, tcp_udp_str, protocol_list,
            total_bytes * 8

        ))

        if last_visible:
            self.tree.see(item_id)

        if j == 0:
            del self.data[j]
        else:
            del self.data[:j+1]

        '''# Limita a 100 secondi per evitare accumulo infinito
        if len(self.displayed_seconds) > 100:
            oldest = sorted(self.displayed_seconds)[:-100]
            for old_sec in oldest:
                self.displayed_seconds.remove(old_sec)
                self.aggregated.pop(old_sec, None)

        self.last_index += len(new_packets)'''

        #print(f"[DEBUG] Update duration: {time.time() - t0:.2f} s")
