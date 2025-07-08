import tkinter as tk
from tkinter import filedialog

class SetPath(tk.Toplevel):
    def __init__(self, parent, on_confirm_callback):
        super().__init__(parent)
        self.title("Seleziona cartella di salvataggio")
        self.geometry("400x100")
        self.resizable(False, False)

        self.on_confirm_callback = on_confirm_callback

        self.label = tk.Label(self, text="Scegli la cartella in cui esportare il PDF:")
        self.label.pack(pady=10)

        self.choose_button = tk.Button(self, text="Sfoglia", command=self.choose_directory)
        self.choose_button.pack()

    def choose_directory(self):
        directory = filedialog.askdirectory()
        if directory:
            print(f"Percorso selezionato: {directory}")  # stampa su console
            self.on_confirm_callback(directory)
            self.destroy()