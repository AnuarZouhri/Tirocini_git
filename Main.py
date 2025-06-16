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

        # === 2. Tabella sopra tutto ===
        self.create_table(self.df)

        # === 3. Grafico cartesiano ===
        self.cartesianChart = CartesianPlotFrame(self, title="Grafico XY",
                                                 x_data=[0, 1, 2, 3, 4],
                                                 y_data=[0, 1, 4, 9, 16])
        self.cartesianChart.pack(side=tk.TOP, fill=tk.BOTH, expand=True, pady=0)

        # === 4. Due grafici a torta ===
        bottom_frame = tk.Frame(self)
        bottom_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        self.pieChart1 = PieChartFrame(bottom_frame, 'Test1')
        self.pieChart2 = PieChartFrame(bottom_frame, 'Test2')

        self.pieChart1.pack(side=tk.LEFT, expand=True, fill=tk.BOTH)
        self.pieChart2.pack(side=tk.LEFT, expand=True, fill=tk.BOTH)

    def create_table(self, df):
        """Crea una tabella con i dati del DataFrame in cima alla finestra, con spaziatura compatta."""
        table_frame = tk.Frame(self)
        table_frame.pack(side=tk.TOP, fill=tk.X, padx=10, pady=0)

        columns = list(df.columns)
        style = ttk.Style()
        style.configure("Treeview", rowheight=18)
        tree = ttk.Treeview(table_frame, columns=columns, show='headings', height=3)

        # Intestazioni
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, anchor=tk.CENTER, width=150)

        # Inserimento righe
        for index, row in df.iterrows():
            tree.insert('', tk.END, values=list(row))

        tree.pack(side=tk.LEFT, fill=tk.X, expand=True)


# Avvio applicazione
if __name__ == "__main__":
    root = tk.Tk()
    root.title("Tabella + Grafici")
    MainApplication(root).pack(side="top", fill="both", expand=True)
    root.mainloop()