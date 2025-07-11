import tkinter as tk
class NotificationPopup(tk.Toplevel):
    def __init__(self, parent, message, duration=3000, bg_color="#ffffcc"):
        super().__init__(parent)
        self.withdraw()
        self.overrideredirect(True)
        self.attributes('-topmost', True)
        self.configure(bg=bg_color)

        self.message = message
        label = tk.Label(self, text=message, bg=bg_color, fg="black",
                         font=("Helvetica", 10), padx=10, pady=10)
        label.pack(fill='both', expand=True)

        self.geometry("250x50")
        self.update_idletasks()
        self.deiconify()
        self.after(duration, self.destroy)

    def place_popup(self, parent, y_offset):
        parent.update_idletasks()
        x = parent.winfo_rootx() + parent.winfo_width() - 260
        y = parent.winfo_rooty() + parent.winfo_height() - y_offset
        self.geometry(f"250x50+{x}+{y}")
