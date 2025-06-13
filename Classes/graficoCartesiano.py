#tkinter usato per costruire la GUI (interfaccia grafica):
import tkinter as tk
#consente di integrare i grafici di matplotlib dentro una finestra Tkinter:
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
#oggetto principale per creare figure e sottotrame (grafici) con matplotlib:
from matplotlib.figure import Figure

#definizione di una classe personalizzata che estende tk.Frame, un contenitore grafico Tkinter:
class CartesianPlotFrame(tk.Frame):
    def __init__(self, parent, title="Grafico", x_data=None, y_data=None): #da vedere
        #inizializza il frame usando il costruttore della classe base tk.Frame:
        super().__init__(parent) #da vedere

        # Dati di default se non forniti:
        if x_data is None:
            x_data = [0, 1, 2, 3, 4]
        if y_data is None:
            y_data = [0, 1, 4, 9, 16]

        #creazione figura Matplotlib con dimensioni 5x4 pollici e risoluzione 100dbi:
        self.figure = Figure(figsize=(5, 4), dpi=100)
        #aggiunge un grafico (sottotrama) alla figura. 111 significa : 1 riga, 1 colonna, primo grafico:
        self.ax = self.figure.add_subplot(111)
        #disegna il grafico cartesiano usando i dati forniti (marker='o' aggiunge un cerchietto su ogni punto):
        self.ax.plot(x_data, y_data, marker='o')
        #imposta il titolo del grafico:
        self.ax.set_title(title)
        #imposta le etichette degli assi:
        self.ax.set_xlabel("X")
        self.ax.set_ylabel("Y")
        #attiva la griglia di sfondo per facilitarne la lettura:
        self.ax.grid(True)

        # Inserimento nella GUI:

        #crea un canvas TKinter per visualizzare la figura matplotlib all'interno del frame:
        self.canvas = FigureCanvasTkAgg(self.figure, self)
        #disegna effettivamente la figura nel canvas:
        self.canvas.draw()
        #posiziona il canvas nel frame usando pack(), facendolo espandere e riempire tutto lo spazio disponibile
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

    # Metodo per aggiornare i dati:

    #metodo pubblico per modificare i dati del grafico dopo la creazione:
    def update_plot(self, x_data, y_data):
        #cancella tutto il contenuto precedente del grafico:
        self.ax.clear()
        #ridisegna il nuovo grafico con i dati aggiornati, riapplicando titolo, etichette e griglia
        self.ax.plot(x_data, y_data, marker='o')
        self.ax.set_title("Grafico aggiornato")
        self.ax.set_xlabel("X")
        self.ax.set_ylabel("Y")
        self.ax.grid(True)
        #aggiorna il disegno nella finestra:
        self.canvas.draw()

