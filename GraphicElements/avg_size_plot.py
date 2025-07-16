import tkinter as tk

class LiveGraph:
    def __init__(self,parent,width=700, height=325, max_points=60):
        self.canvas = tk.Canvas(parent, bg='white')
        self.canvas.pack(fill='both',expand=True)

        self.point_spacing = 15
        self.width, self.height = width, height
        self.max_points = max_points
        self.data = []
        self.margin = 70  # spazio per assi e valori

        self.time_counter = 1  # Numero di secondi trascorsi
        self.time_labels = []  # Etichette da mostrare sotto l'asse X

    def draw_axes(self):

        # Titolo del grafico
        self.canvas.create_text(self.width // 2, self.margin // 2,
                                text="Average Packets Size",
                                font=("Arial", 14, "bold"))

        # Etichetta asse X
        self.canvas.create_text(self.width // 2, self.height - self.margin // 2.5,
                                text="Scan ID", font=("Arial", 10, "bold"))

        # Etichetta asse Y
        self.canvas.create_text(self.margin // 4,self.height // 2,
                                text="Average Byte", font=("Arial", 10, "bold"),
                                angle=90)

        # Linee assi X e Y
        self.canvas.create_line(self.margin, self.margin,
                                self.margin, self.height - self.margin, width=2)
        self.canvas.create_line(self.margin, self.height - self.margin,
                                self.width - self.margin, self.height - self.margin, width=2)
        # Tacche asse X
        num_points = len(self.data)
        start_x = self.margin

        for i in range(num_points):
            x = start_x + i * self.point_spacing
            if x > self.width - self.margin:
                break

            if i % 2 == 0:  # Tacche ogni 5 punti (puoi cambiare)
                second_label = str(self.time_counter - num_points + i + 1)
                self.canvas.create_line(x, self.height - self.margin, x, self.height - self.margin + 5, width=1)
                self.canvas.create_text(x, self.height - self.margin + 15, text=second_label, anchor="n",
                                        font=("Arial", 8))

        # Calcolo sicuro dei valori sulle tacche Y
        num_y_steps = 8
        if self.data:
            max_val = max(self.data)
            min_val = min(self.data)
        else:
            max_val, min_val = 1, 0

        range_val = (max_val - min_val) or 1  # evita divisione per zero
        step_val = range_val / num_y_steps


        for i in range(num_y_steps + 1):
            y = self.height - self.margin - ((self.height - 2 * self.margin) * i / num_y_steps)
            value = min_val + step_val * i
            self.canvas.create_line(self.margin - 5, y, self.margin, y, width=1)
            self.canvas.create_text(self.margin - 8, y, text=f"{value:.1f}", anchor="e", font=("Arial", 8))
            self.canvas.create_line(self.margin, y, self.width - self.margin, y, fill="#e0e0e0", dash=(2, 2))

    def draw_graph(self):
        try:
            if self.canvas.winfo_exists():
                pass
        except Exception as e:
            return
        if len(self.data) < 2:
            return

        raw_max = max(self.data)
        raw_min = min(self.data)
        padding = 0.05 * (raw_max - raw_min or 1)

        max_val = raw_max + padding
        min_val = raw_min - padding
        span = max_val - min_val
        y_scale = (self.height - 2 * self.margin) / span

        start_x = self.margin
        pts = []

        for i, val in enumerate(self.data):
            x = start_x + i * self.point_spacing
            y = self.height - self.margin - (val - min_val) * y_scale
            pts.append((x, y))

        # Disegna linee
        for (x1, y1), (x2, y2) in zip(pts, pts[1:]):
            self.canvas.create_line(x1, y1, x2, y2, fill='blue', width=2)
        for x, y in pts:
            self.canvas.create_oval(x - 3, y - 3, x + 3, y + 3, fill='red')


    def update(self, new_data):
        if new_data:
            avg = sum(pkt['size'] for pkt in new_data) / len(new_data)
        else:
            avg = 0  # Nessun dato ricevuto, valore predefinito

        self.data.append(avg)

        # Calcola quanti punti stanno visivamente nel canvas
        max_visible_points = (self.width - 2 * self.margin) // self.point_spacing
        if len(self.data) > max_visible_points:
            self.data.pop(0)

        self.canvas.delete('all')
        self.draw_axes()
        self.draw_graph()
        self.time_counter += 1
