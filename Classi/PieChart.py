import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

class PieChartFrame(tk.Frame):

    def __init__(self,master,title,data = None,**kwargs):
        """

        Args:
            master: radice tk a cui appartiene il grafico a torta
            title: titolo del grafico a torta
            data: dati iniziali del grafico a torta
            **kwargs:
        """
        super().__init__(master,**kwargs)

        if data is None:
            data = {"A": 40, "B": 30, "C": 30}

        self.labels = list(data.keys())
        self.values = list(data.values())

        self.fig = Figure(figsize=(4, 4))
        self.ax = self.fig.add_subplot(111)
        self.ax.set_title(title)
        self.pie = None
        self.drawPie()

        self.canvas = FigureCanvasTkAgg(self.fig, master=self)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

    def drawPie(self):
        """
            La funzioen drawPie sovrascrive il precedente grafico a torta utilizzando i valori
            presenti in self.labels e self.values.
        """
        self.ax.clear()
        self.pie = self.ax.pie(self.values, labels=self.labels, autopct=self.autopct)
        self.ax.axis('equal')

    def autopct(self, pct):
        return f'{pct:.1f}%' if pct >= 1 else ''

    def updateData(self, new_data: dict):
        """

        Args:
            new_data:  nuovi dati da inserire e che verranno successivamente utilizzati
            dalla funzione drawPie
        """
        self.labels = list(new_data.keys())
        self.values = list(new_data.values())
        self.drawPie()
        self.canvas.draw()


