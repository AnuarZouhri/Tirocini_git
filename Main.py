import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from Classes.PieChart import PieChartFrame

class MainApplication(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent
        self.pieChart1 = PieChartFrame(parent,'Test1')
        self.pieChart2 = PieChartFrame(parent,'Test2')

        self.pieChart1.pack(side=tk.LEFT, expand=True, fill=tk.BOTH)
        self.pieChart2.pack(side=tk.LEFT, expand=True, fill=tk.BOTH)


root = tk.Tk()
MainApplication(root).pack(side="top", fill="both", expand=True)
root.mainloop()