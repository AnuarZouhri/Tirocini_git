
import tkinter as tk
from collections import Counter
import random

class TopDestPortsGraph(tk.Frame):
    def __init__(self, parent, width=600, height=380):
        super().__init__(parent)
        self.width = width
        self.height = height
        self.margin = 80
        self.top_margin = 30  # nuova altezza per il margine superiore (titolo)
        self.bar_height = 25
        self.bar_spacing = 5

        self.canvas = tk.Canvas(self, height=self.height, width=self.width, bg='white')
        self.canvas.pack(fill='both')

        self.port_counts = Counter()
        self.max_ports = 10
        self.max_visible_count = 20



    def update(self, data):
        try:
            if self.canvas.winfo_exists():
                self.canvas.delete("all")
        except Exception as e:
            return
        for pkt in data:
            self.port_counts[pkt['port dst']] += 1

        # Titolo
        self.canvas.create_text(
            self.width // 2, 15, text="Top 10 Destination Ports",
            font=("Arial", 14, "bold"), fill="black"
        )

        # Top 10 ordinati per valore crescente
        top_ports = dict(sorted(self.port_counts.items(), key=lambda x: x[1])[-self.max_ports:])
        top_ports = dict(sorted(top_ports.items(), key=lambda x: x[1]))  # Ordine crescente

        if not top_ports:
            return

        max_count = max(top_ports.values()) or 1
        bar_area_width = self.width - 2 * self.margin

        # Scala i valori se superano la soglia visibile
        scale = 1
        if max_count > self.max_visible_count:
            scale = self.max_visible_count / max_count

        y = self.top_margin + 10  # inizia sotto il titolo
        for port, count in top_ports.items():
            scaled_count = count * scale
            bar_len = (scaled_count / self.max_visible_count) * bar_area_width

            self.canvas.create_rectangle(
                self.margin, y,
                self.margin + bar_len, y + self.bar_height,
                fill='skyblue'
            )

            self.canvas.create_text(
                self.margin - 10, y + self.bar_height / 2,
                text=f"Port {port}", anchor='e', font=('Arial', 10, 'bold')
            )

            self.canvas.create_text(
                self.margin + bar_len + 5, y + self.bar_height / 2,
                text=str(count), anchor='w', font=('Arial', 10)
            )

            y += self.bar_height + self.bar_spacing


