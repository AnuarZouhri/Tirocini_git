import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from Classes.PieChart import PieChartFrame
from Classes.graficoCartesiano import CartesianPlotFrame  # <-- grafico XY


class MainApplication(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.parent = parent

        # 1. --- Grafico cartesiano in alto ---
        self.cartesianChart = CartesianPlotFrame(self, title="Grafico XY",
                                                 x_data=[0, 1, 2, 3, 4],
                                                 y_data=[0, 1, 4, 9, 16])
        self.cartesianChart.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        # 2. --- Frame contenitore per le due torte ---
        bottom_frame = tk.Frame(self)
        bottom_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        # 3. --- Due grafici a torta affiancati ---
        self.pieChart1 = PieChartFrame(bottom_frame, 'Test1')
        self.pieChart2 = PieChartFrame(bottom_frame, 'Test2')

        self.pieChart1.pack(side=tk.LEFT, expand=True, fill=tk.BOTH)
        self.pieChart2.pack(side=tk.LEFT, expand=True, fill=tk.BOTH)


# Avvio applicazione
if __name__ == "__main__":
    root = tk.Tk()
    root.title("Grafico XY sopra le Torte")
    MainApplication(root).pack(side="top", fill="both", expand=True)
    root.mainloop()