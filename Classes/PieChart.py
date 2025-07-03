import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

class PieChartFrame(tk.Frame):

    def __init__(self,master,title,legend,data = None,**kwargs):
        """

        Args:
            master: radice tk a cui appartiene il grafico a torta
            title: titolo del grafico a torta
            data: dati iniziali del grafico a torta
            **kwargs:
        """
        super().__init__(master,**kwargs)
        self.data = []
        self.legend = legend

        if data is None:

            self.labels = []
            self.values = []
        else:

            self.labels = list(data.keys())
            self.values = list(data.values())


        self.fig = Figure(figsize=(2, 2))
        self.ax = self.fig.add_subplot(111)
        self.ax.set_title(title)
        self.pie = None
        self.drawPie()

        self.canvas = FigureCanvasTkAgg(self.fig, master=self)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

    def drawPie(self):
        self.ax.clear()

        wedges, texts, autotexts = self.ax.pie(
            self.values,
            labels=None,
            autopct=self.autopct,
            startangle=90
        )
        self.ax.axis('equal')  # mantiene la torta rotonda

        # Legenda sotto al grafico
        self.ax.legend(
            wedges,
            self.labels,
            title=self.legend,
            loc='upper center',
            bbox_to_anchor=(0.7, 0.6),  # sotto al grafico

        )
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


