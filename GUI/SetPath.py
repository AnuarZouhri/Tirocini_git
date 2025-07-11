import tkinter as tk
from tkinter import filedialog

class SetPath(tk.Toplevel):
    def __init__(self, parent, on_confirm_callback):
        super().__init__(parent)
        self.title("Select save folder")
        self.geometry("400x150")
        self.resizable(False, False)

        self.transient(parent)      # Lega visivamente al parent
        self.grab_set()             # Rende modale
        self.focus_force()          # Porta in primo piano

        self.on_confirm_callback = on_confirm_callback
        self.selected_directory = None

        self.label = tk.Label(self, text="Choose the folder to export the PDF")
        self.label.pack(pady=5)

        self.choose_button = tk.Button(self, text="Choose", command=self.choose_directory)
        self.choose_button.pack()

        self.path_label = tk.Label(self, text="No folder selected", fg="gray")
        self.path_label.pack(pady=5)

        button_frame = tk.Frame(self)
        button_frame.pack(pady=10)

        self.confirm_button = tk.Button(button_frame, text="Confirm", command=self.confirm, state=tk.DISABLED)
        self.confirm_button.pack(side=tk.LEFT, padx=10)

        self.cancel_button = tk.Button(button_frame, text="Cancel", command=self.destroy)
        self.cancel_button.pack(side=tk.LEFT, padx=10)

    def choose_directory(self):
        directory = filedialog.askdirectory()  # non usare parent=self
        if directory:
            self.selected_directory = directory
            self.path_label.config(text=directory, fg="black")
            self.confirm_button.config(state=tk.NORMAL)

    def confirm(self):
        if self.selected_directory:
            self.on_confirm_callback(self.selected_directory)
            self.destroy()
