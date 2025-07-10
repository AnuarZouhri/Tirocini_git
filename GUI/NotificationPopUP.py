import tkinter as tk

class NotificationPopup(tk.Toplevel):
    def __init__(self, parent, message, y_offset, duration=3000, bg_color="#ffffcc"):
        super().__init__(parent)
        self.configure(bg=bg_color)
        self.overrideredirect(True)
        self.attributes('-topmost', True)  # Sempre in primo piano

        label = tk.Label(self, text=message, bg=bg_color, fg="black",
                         font=("Helvetica", 10), padx=10, pady=10)
        label.pack(fill='both', expand=True)

        # Aspetta che la finestra principale sia pronta per calcolare le dimensioni e posizionarsi
        self.after(10, lambda: self.place_popup(parent, y_offset))
        self.after(duration, self.destroy)

    def place_popup(self, parent, y_offset):
        parent.update_idletasks()
        x = parent.winfo_rootx() + parent.winfo_width() - 260
        y = parent.winfo_rooty() + parent.winfo_height() - y_offset
        self.geometry(f"250x50+{x}+{y}")