import tkinter as tk
import random
import math
import time

class LiveGraph:
    def __init__(self, parent, width=600, height=300, max_points=100):
        self.canvas = tk.Canvas(parent, width=width, height=height, bg='white')
        self.canvas.pack()

        self.width, self.height = width, height
        self.max_points = max_points
        self.data = []
        self.margin = 50  # spazio per assi e valori

        self.update()

    def draw_axes(self):
        # Linee assi X e Y
        self.canvas.create_line(self.margin, self.margin,
                                self.margin, self.height - self.margin, width=2)
        self.canvas.create_line(self.margin, self.height - self.margin,
                                self.width - self.margin, self.height - self.margin, width=2)

        # Calcolo sicuro dei valori sulle tacche Y
        num_y_steps = 5
        if self.data:
            max_val = max(self.data)
            min_val = min(self.data)
        else:
            max_val, min_val = 1, 0

        range_val = max_val - min_val or 1  # evita divisione per zero
        step_val = range_val / num_y_steps

        for i in range(num_y_steps + 1):
            y = self.height - self.margin - ((self.height - 2 * self.margin) * i / num_y_steps)
            value = min_val + step_val * i
            self.canvas.create_line(self.margin - 5, y, self.margin, y, width=1)
            self.canvas.create_text(self.margin - 8, y, text=f"{value:.1f}", anchor="e", font=("Arial", 8))
            self.canvas.create_line(self.margin, y, self.width - self.margin, y, fill="#e0e0e0", dash=(2, 2))

    def draw_graph(self):
        n = len(self.data)
        if n < 2:
            return

        max_val = max(self.data)
        min_val = min(self.data)
        span = max_val - min_val or 1

        x_scale = (self.width - 2 * self.margin) / (self.max_points - 1)
        y_scale = (self.height - 2 * self.margin) / span

        points = []
        for i, val in enumerate(self.data):
            x = self.margin + i * x_scale
            y = self.height - self.margin - (val - min_val) * y_scale
            points.append((x, y))

        # 🎨 Area sotto la curva
        area_points = [(self.margin, self.height - self.margin)] + points + [(points[-1][0], self.height - self.margin)]
        self.canvas.create_polygon(area_points, fill='lightblue', outline='', smooth=True)

        # 🔵 Linea principale
        for (x1, y1), (x2, y2) in zip(points, points[1:]):
            self.canvas.create_line(x1, y1, x2, y2, fill='blue', width=2)

        # 🔴 Punti
        for x, y in points:
            self.canvas.create_oval(x - 3, y - 3, x + 3, y + 3, fill='red')

    '''def draw_graph(self):
        n = len(self.data)
        if n < 2:
            return

        max_val = max(self.data)
        min_val = min(self.data)
        span = max_val - min_val or 1

        x_scale = (self.width - 2*self.margin) / (self.max_points - 1)
        y_scale = (self.height - 2*self.margin) / span

        pts = []
        for i, val in enumerate(self.data):
            x = self.margin + i * x_scale
            y = self.height - self.margin - (val - min_val) * y_scale
            pts.append((x, y))

        # Disegna linea e cerchietti
        for (x1, y1), (x2, y2) in zip(pts, pts[1:]):
            self.canvas.create_line(x1, y1, x2, y2, fill='blue', width=2)
        for x, y in pts:
            self.canvas.create_oval(x-3, y-3, x+3, y+3, fill='red')'''

    def update(self):
        # Aggiungi dato dummy (pero puoi sostituirlo con dati reali)
        self.data.append(math.sin(time.time()))
        if len(self.data) > self.max_points:
            self.data.pop(0)

        self.canvas.delete('all')
        self.draw_axes()
        self.draw_graph()

        self.canvas.after(500, self.update)

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Grafico dinamico migliorato")
    graph = LiveGraph(root, width=800, height=400, max_points=100)
    root.mainloop()
