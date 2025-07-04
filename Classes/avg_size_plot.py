import matplotlib
matplotlib.use("TkAgg")
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import time
import tkinter as tk

class LivePlot:
    def __init__(self,parent_frame,interval=1000):

        self.fig, self.ax = plt.subplots(figsize=(10, 3))
        self.fig.tight_layout(pad=2.0)
        self.fig.subplots_adjust(left=0.09, bottom=0.15)
        self.interval = interval

        self.line, = self.ax.plot([], [], '-o', color='orange', markersize=3, linewidth=2)

        self.ax.set_title("Average Frame Size (bytes/s)")
        self.ax.set_xlabel("Seconds")
        self.ax.set_ylabel("Average Size (bytes)", fontsize=10, labelpad=2)
        self.ax.grid(True)

        self.ax.set_xlim(0, 100)
        self.ax.set_ylim(0, 100)

        self.canvas = FigureCanvasTkAgg(self.fig, master=parent_frame)
        self.canvas_widget = self.canvas.get_tk_widget()
        self.canvas_widget.pack(fill="both", expand=True, padx=0, pady=0)

        self.x_data = []
        self.y_data = []
        self.start_time = time.time()
        self.after_id = None



    '''def update(self,data):
        try:
            exists = self.canvas_widget.winfo_exists()
        except tk.TclError:
            exists = False

        if not exists:
            return
        buckets = {}
        for pkt in data:
            sec = int(float(pkt['timestamp']) - self.start_time)
            size = pkt['size']
            if size < 0:
                continue
            else:
                buckets.setdefault(sec, []).append(size)

        current_time = int(time.time() - self.start_time)

        window = 100
        self.x_data = []
        self.y_data = []

        start_sec = max(0, current_time - window + 1)
        for sec in range(start_sec, current_time + 1):
            sizes = buckets.get(sec, [])
            avg_size = sum(sizes) / len(sizes) if sizes else 0
            self.x_data.append(sec)
            self.y_data.append(avg_size)

        self.line.set_data(self.x_data, self.y_data)

        self.ax.set_xlim(start_sec, current_time + 1)
        self.ax.set_xticks(range(start_sec, current_time + 1, 5))

        max_y = max(self.y_data, default=0)
        self.ax.set_ylim(0, max(100, max_y * 1.2))

        if exists:
            self.canvas.draw_idle()
            '''

    def destroy_plot(self):
        if self.canvas:
            self.canvas.get_tk_widget().destroy()
            plt.close(self.fig)
            self.canvas = None
            self.fig = None

