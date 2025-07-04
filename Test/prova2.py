import tkinter as tk
import matplotlib
matplotlib.use("TkAgg")
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import time
import random

class LivePlot:
    def __init__(self, parent_frame, interval=1000):
        self.fig, self.ax = plt.subplots(figsize=(5, 3))
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
        self.after_id = None
        self.start_time = time.time()

    def update(self, data):
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

        if self.canvas_widget.winfo_exists():
            self.canvas.draw_idle()


# ==== GUI PRINCIPALE ====
root = tk.Tk()
root.title("Interfaccia Grafica con Grafico Live")
root.geometry("900x500")

# Frame superiore
frame_top = tk.Frame(root, bg="lightblue", padx=10, pady=10)
frame_top.pack(fill='x')

tk.Label(frame_top, text="Nome:", bg="lightblue").grid(row=0, column=0, sticky="w")
entry_nome = tk.Entry(frame_top)
entry_nome.grid(row=0, column=1, padx=5)

tk.Label(frame_top, text="Cognome:", bg="lightblue").grid(row=1, column=0, sticky="w")
entry_cognome = tk.Entry(frame_top)
entry_cognome.grid(row=1, column=1, padx=5)

# Frame centrale
frame_middle = tk.Frame(root, bg="lightgrey", padx=10, pady=10)
frame_middle.pack(fill='x')

tk.Label(frame_middle, text="Genere:", bg="lightgrey").grid(row=0, column=0, sticky="w")
genere_var = tk.StringVar()
tk.Radiobutton(frame_middle, text="Maschio", variable=genere_var, value="M", bg="lightgrey").grid(row=0, column=1)
tk.Radiobutton(frame_middle, text="Femmina", variable=genere_var, value="F", bg="lightgrey").grid(row=0, column=2)

# Frame inferiore diviso in due
frame_bottom = tk.Frame(root)
frame_bottom.pack(fill='both', expand=True)

frame_left = tk.Frame(frame_bottom, bg="white", padx=10, pady=10)
frame_left.pack(side='left', fill='both', expand=True)

frame_right = tk.Frame(frame_bottom, bg="white", padx=10, pady=10)
frame_right.pack(side='right', fill='both', expand=True)

tk.Label(frame_left, text="Interessi:", bg="white").pack(anchor='w')
var_sport = tk.BooleanVar()
var_musica = tk.BooleanVar()
var_viaggi = tk.BooleanVar()

tk.Checkbutton(frame_left, text="Sport", variable=var_sport, bg="white").pack(anchor='w')
tk.Checkbutton(frame_left, text="Musica", variable=var_musica, bg="white").pack(anchor='w')
tk.Checkbutton(frame_left, text="Viaggi", variable=var_viaggi, bg="white").pack(anchor='w')

# Inizializzazione del grafico live nel frame destro
plot = LivePlot(frame_right)

def on_closing():
    if plot.after_id:
        root.after_cancel(plot.after_id)
    plt.close('all')  # chiude le figure matplotlib
    root.destroy()

# Simulazione di pacchetti fittizi
def genera_dati_fittizi():
    now = time.time()
    return [
        {"timestamp": now - random.randint(0, 10), "size": random.randint(20, 1500)}
        for _ in range(30)
    ]

# Pulsante per aggiornare manualmente il grafico
tk.Button(frame_left, text="Aggiorna Grafico", command=lambda: plot.update(genera_dati_fittizi())).pack(pady=20)

# Avvio
root.protocol("WM_DELETE_WINDOW", on_closing)
root.mainloop()
