import tkinter as tk
from tkinter import ttk
from collections import defaultdict


class ProtocolLiveGraph:
    def __init__(self, root):
        self.root = root
        self.canvas_width = 700
        self.canvas_height = 250
        self.margin = 40

        # Canvas grafico
        self.canvas = tk.Canvas(self.root, width=self.canvas_width, height=self.canvas_height, bg="white")
        self.canvas.pack(side = 'top',fill='both',expand=True)

        self.x_spacing = 50  # Spazio tra i punti

        # Dati per protocollo
        self.protocol_data = defaultdict(list)
        self.current_protocol = tk.StringVar()
        self.protocols = ['IP']
        self.current_protocol.set(self.protocols[0])
        self.offset = 0  # Posizione di scroll
        self.protocol_timestamps = defaultdict(list)
        self.time_counter = 0


        # Dropdown scelta protocollo
        self.dropdown = ttk.OptionMenu(
            root, self.current_protocol, self.protocols[0],
            *self.protocols, command=self.on_protocol_change
        )
        self.dropdown.pack(pady=1)

        # Pulsanti di navigazione
        btn_frame = tk.Frame(self.root)
        btn_frame.pack(side='top',pady=1)
        self.btn_back = ttk.Button(btn_frame, text="← Indietro", command=self.scroll_left)
        self.btn_back.grid(row=0, column=0, padx=1)
        self.btn_forward = ttk.Button(btn_frame, text="Avanti →", command=self.scroll_right)
        self.btn_forward.grid(row=0, column=1, padx=1)

    def refresh_dropdown(self):
        menu = self.dropdown["menu"]
        menu.delete(0, "end")

        for proto in self.protocols:
            menu.add_command(label=proto, command=lambda p=proto: self.set_protocol(p))

    def set_protocol(self, proto):
        self.current_protocol.set(proto)
        self.offset = 0
        self.draw_graph()

    def on_protocol_change(self, _):
        self.offset = 0
        self.draw_graph()

    def scroll_left(self):
        proto = self.current_protocol.get()
        visible_points = (self.canvas_width - 2 * self.margin) // self.x_spacing
        total_points = len(self.protocol_data[proto])
        max_offset = max(0, total_points - visible_points)
        if self.offset < max_offset:
            self.offset += 1
            self.draw_graph()

    def scroll_right(self):
        if self.offset > 0:
            self.offset -= 1
            self.draw_graph()

    def update_graph(self, data):
        try:
            if self.canvas.winfo_exists():
                pass
        except Exception as e:
            return
        counter = defaultdict(int)
        new_protocols = []


        for pkt in data:
            proto = pkt['protocol']
            counter[proto] += 1
            if proto not in self.protocols:
                self.protocols.append(proto)
                new_protocols.append(proto)

        # Aggiorna struttura dati
        for proto in self.protocols:
            self.protocol_data[proto].append(counter[proto])
            self.protocol_timestamps[proto].append(self.time_counter)

        self.time_counter += 1

        # Se sono arrivati nuovi protocolli, aggiorna il dropdown
        if new_protocols:
            self.refresh_dropdown()

        # Mostra nuovo grafico se siamo in fondo
        proto = self.current_protocol.get()
        visible_points = (self.canvas_width - 2 * self.margin) // self.x_spacing
        total_points = len(self.protocol_data[proto])
        if self.offset == 0 or total_points <= visible_points:
            self.draw_graph()

    def draw_graph(self):
        self.canvas.delete("all")
        proto = self.current_protocol.get()

        # Assi
        cw, ch, m = self.canvas_width, self.canvas_height, self.margin
        self.canvas.create_line(m, m, m, ch - m, width=2)
        self.canvas.create_line(m, ch - m, cw - m, ch - m, width=2)

        # Titolo del grafico
        self.canvas.create_text(cw // 2, m // 2, text=f"Packets per protocol: {proto}", font=("Arial", 14, "bold"))
        # Etichetta asse Y
        self.canvas.create_text(m // 2, ch // 2, text="Count Packets", angle=90, font=("Arial", 10, "bold"))
        # Etichetta asse X
        self.canvas.create_text(cw // 2, ch - m // 2 + 10, text="Seconds", font=("Arial", 10, "bold"))

        data = self.protocol_data[proto]

        vis_pts = (self.canvas_width - 2 * self.margin) // self.x_spacing
        start = max(0, len(data) - vis_pts - self.offset)
        end = len(data) - self.offset
        visible_data = data[start:end]

        if not visible_data:
            return

        max_val = max(visible_data) or 1
        max_val = int(max_val) + 1
        for i in range(6):
            y_val = i * max_val / 5
            y = ch - m - y_val * ((ch - 2 * m) / max_val)
            self.canvas.create_line(m - 5, y, m + 5, y, fill="gray")
            self.canvas.create_text(m - 10, y, text=str(int(y_val)), anchor="e", font=("Arial", 8))

        for i, _ in enumerate(visible_data):
            x = m + i * self.x_spacing
            if i % 5 == 0:
                self.canvas.create_line(x, ch - m, x, ch - m + 5)
                timestamp = self.protocol_timestamps[proto][start + i]
                label = str(timestamp)
                self.canvas.create_text(x, ch - m + 15, text=label, font=("Arial", 8))

        points = []
        for i, val in enumerate(visible_data):
            x = m + i * self.x_spacing
            y = ch - m - val * ((ch - 2 * m) / max_val)
            points.append((x, y))

        if points:
            area = [(points[0][0], ch - m)] + points + [(points[-1][0], ch - m)]
            self.canvas.create_polygon(area, fill="lightblue", outline="")

        for i in range(1, len(points)):
            self.canvas.create_line(points[i-1], points[i], fill="blue", width=2)
        for x, y in points:
            self.canvas.create_oval(x-3, y-3, x+3, y+3, fill="red", outline="")

