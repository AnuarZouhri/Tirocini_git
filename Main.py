import tkinter as tk
from tkinter import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from Classes.PieChart import PieChartFrame
from Classes.graficoCartesiano import CartesianPlotFrame
import pandas as pd


class MainApplication(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.parent = parent

        # === 1. Simulazione DataFrame ===
        self.df = pd.DataFrame({
            "MAC Address": ["00:1A:2B:3C:4D:5E", "11:22:33:44:55:66", "AA:BB:CC:DD:EE:FF"],
            "Media dimensione pacchetti (byte/s)": [350, 420, 390],
            "Pacchetti corrotti al secondo": [2, 0, 5],
            "Pacchetti totali al secondo": [100, 120, 110]
        })
        self.df["% pacchetti corrotti"] = (
            self.df["Pacchetti corrotti al secondo"] /
            self.df["Pacchetti totali al secondo"]
        ) * 100

        # === 2. Tabella con etichetta centrata ===
        table_frame = tk.Frame(self)
        table_frame.pack(side=tk.TOP, fill=tk.X, padx=10, pady=(10, 0))

        label_tabella = tk.Label(table_frame, text="Tabella Statistiche Pacchetti", font=("Helvetica", 12, "bold"))
        label_tabella.pack(side=tk.TOP, anchor="center", pady=(0, 5))

        self.create_table(table_frame, self.df)

        # === 3. Grafico cartesiano con etichetta centrata ===
        label_cartesiano = tk.Label(self, text="Grafico Cartesiano", font=("Helvetica", 12, "bold"))
        label_cartesiano.pack(side=tk.TOP, anchor="center", pady=(15, 5))

        self.cartesianChart = CartesianPlotFrame(self, title="Grafico XY",
                                                 x_data=[0, 1, 2, 3, 4],
                                                 y_data=[0, 1, 4, 9, 16])
        self.cartesianChart.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        # === 4. Due grafici a torta con etichette ===
        bottom_frame = tk.Frame(self)
        bottom_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True, pady=(15, 0))

        # Frame sinistro (Torta 1)
        left_frame = tk.Frame(bottom_frame)
        left_frame.pack(side=tk.LEFT, expand=True, fill=tk.BOTH, padx=10)

        label_torta1 = tk.Label(left_frame, text="Distribuzione Torta 1", font=("Helvetica", 12, "bold"))
        label_torta1.pack(side=tk.TOP, anchor="center", pady=(0, 5))

        self.pieChart1 = PieChartFrame(left_frame, 'Test1')
        self.pieChart1.pack(side=tk.TOP, expand=True, fill=tk.BOTH)

        # Frame destro (Torta 2)
        right_frame = tk.Frame(bottom_frame)
        right_frame.pack(side=tk.LEFT, expand=True, fill=tk.BOTH, padx=10)

        label_torta2 = tk.Label(right_frame, text="Distribuzione Torta 2", font=("Helvetica", 12, "bold"))
        label_torta2.pack(side=tk.TOP, anchor="center", pady=(0, 5))

        self.pieChart2 = PieChartFrame(right_frame, 'Test2')
        self.pieChart2.pack(side=tk.TOP, expand=True, fill=tk.BOTH)

    def create_table(self, parent, df):
        """Crea una tabella all'interno del frame specificato (con spaziatura compatta)."""
        columns = list(df.columns)
        style = ttk.Style()
        style.configure("Treeview", rowheight=18)
        tree = ttk.Treeview(parent, columns=columns, show='headings', height=3)

        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, anchor=tk.CENTER, width=150)

        for index, row in df.iterrows():
            tree.insert('', tk.END, values=list(row))

        tree.pack(side=tk.LEFT, fill=tk.X, expand=True)


# Avvio applicazione
if __name__ == "__main__":
    root = tk.Tk()
    root.title("Tabella + Grafici")
    MainApplication(root).pack(side="top", fill="both", expand=True)
    root.mainloop()