import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from collections import defaultdict
import time

class NetworkProtocolPlot:
    def __init__(self, parent_frame):

        self.last_index = 0
        self.protocol_counts = defaultdict(lambda: defaultdict(int))
        self.attack_state = {}
        self.last_packet_time = {}
        self.timeout_seconds = 10

        self.selected_protocol = tk.StringVar()
        self.selected_protocol.set("IP")

        self.frame = ttk.Frame(parent_frame)
        self.frame.pack(fill="both", expand=True)

        self.dropdown = ttk.Combobox(self.frame, textvariable=self.selected_protocol, values=[], state="readonly")
        self.dropdown.pack()

        self.fig, self.ax = plt.subplots(figsize=(10, 3))
        self.fig.tight_layout(pad=2.0)
        self.fig.subplots_adjust(left=0.09, bottom=0.15)
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.frame)
        self.canvas.get_tk_widget().pack(fill="both", expand=True)

        self.after_id = None
        self.start_time = time.time()


    def update(self, data):
        widget = self.canvas.get_tk_widget()

        current_real_time = int(time.time() - self.sniffer.start_time)

        new_packets = data

        temp_counts = defaultdict(lambda: defaultdict(int))  # proto -> second -> count

        for pkt in new_packets:
            try:
                if pkt.sniff_timestamp is None or self.sniffer.start_time is None:
                    continue
                try:
                    second = int(float(pkt.sniff_timestamp) - self.sniffer.start_time)
                except Exception:
                    continue
                protocols = [layer.layer_name.upper() for layer in pkt.layers]
                for proto in protocols:
                    temp_counts[proto][second] += 1
                    self.last_packet_time[proto] = second
            except Exception:
                continue

        for proto, seconds_dict in temp_counts.items():
            for second, count in seconds_dict.items():
                self.protocol_counts[proto][second] = count

        self.last_index += len(new_packets)

        available_protocols = sorted(self.protocol_counts.keys())

        if tuple(self.dropdown['values']) != tuple(available_protocols):
            self.dropdown['values'] = available_protocols

        selected = self.selected_protocol.get()
        if selected not in available_protocols:
            if available_protocols:
                selected = available_protocols[0]
                self.selected_protocol.set(selected)
            else:
                selected = "IP"
                self.selected_protocol.set(selected)

        self.ax.clear()
        self.ax.set_title(f"Packets per Protocol: {selected}")
        self.ax.set_xlabel("Seconds")
        self.ax.set_ylabel("Packet Count")
        self.ax.grid(True, linestyle='--', linewidth=0.5, alpha=0.7)

        x_min = max(0, current_real_time - 100 + 1)
        x_max = current_real_time
        seconds = list(range(x_min, x_max + 1))
        counts = [self.protocol_counts[selected].get(s, 0) for s in seconds]

        self.ax.fill_between(seconds, counts, color='skyblue', alpha=0.7)
        self.ax.plot(seconds, counts, color='blue', linewidth=2)

        self.ax.set_xlim(x_min, max(x_min + 1, x_max + 1))
        self.ax.set_ylim(0, max(max(counts, default=0) * 1.3, 20))

        self.ax.set_xticks(range(x_min, x_max + 1, 5))
        self.ax.set_xticklabels([str(t) for t in range(x_min, x_max + 1, 5)], rotation=0, ha='center')

        try:
            self.canvas.draw_idle()
        except Exception:
            return # Se il canvas è stato distrutto, interrompi l'update

