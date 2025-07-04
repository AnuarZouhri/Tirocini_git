import tkinter as tk
from tkinter import ttk

# Creazione finestra principale
root = tk.Tk()
root.title("Esempio Interfaccia Grafica Tkinter")
root.geometry("500x400")

# === FRAME SUPERIORE ===
frame_top = tk.Frame(root, bg="lightblue", padx=10, pady=10)
frame_top.pack(fill='x')

tk.Label(frame_top, text="Nome:", bg="lightblue").grid(row=0, column=0, sticky="w")
entry_nome = tk.Entry(frame_top)
entry_nome.grid(row=0, column=1, padx=5)

tk.Label(frame_top, text="Cognome:", bg="lightblue").grid(row=1, column=0, sticky="w")
entry_cognome = tk.Entry(frame_top)
entry_cognome.grid(row=1, column=1, padx=5)

# === FRAME CENTRALE ===
frame_middle = tk.Frame(root, bg="lightgrey", padx=10, pady=10)
frame_middle.pack(fill='x')

tk.Label(frame_middle, text="Genere:", bg="lightgrey").grid(row=0, column=0, sticky="w")
genere_var = tk.StringVar()
tk.Radiobutton(frame_middle, text="Maschio", variable=genere_var, value="M", bg="lightgrey").grid(row=0, column=1)
tk.Radiobutton(frame_middle, text="Femmina", variable=genere_var, value="F", bg="lightgrey").grid(row=0, column=2)

# === FRAME INFERIORE SINISTRO ===
frame_left = tk.Frame(root, bg="white", padx=10, pady=10)
frame_left.pack(side='left', fill='both', expand=True)

tk.Label(frame_left, text="Interessi:", bg="white").pack(anchor='w')
var_sport = tk.BooleanVar()
var_musica = tk.BooleanVar()
var_viaggi = tk.BooleanVar()

tk.Checkbutton(frame_left, text="Sport", variable=var_sport, bg="white").pack(anchor='w')
tk.Checkbutton(frame_left, text="Musica", variable=var_musica, bg="white").pack(anchor='w')
tk.Checkbutton(frame_left, text="Viaggi", variable=var_viaggi, bg="white").pack(anchor='w')

# === FRAME INFERIORE DESTRO ===
frame_right = tk.Frame(root, bg="white", padx=10, pady=10)
frame_right.pack(side='right', fill='both', expand=True)

tk.Label(frame_right, text="Città preferite:", bg="white").pack(anchor='w')
listbox = tk.Listbox(frame_right)
for citta in ["Roma", "Milano", "Firenze", "Napoli", "Torino"]:
    listbox.insert(tk.END, citta)
listbox.pack(fill='both', expand=True)

# === FRAME PULSANTI IN FONDO ===
frame_bottom = tk.Frame(root, pady=10)
frame_bottom.pack(fill='x')

tk.Button(frame_bottom, text="Invia").pack(side='left', padx=10)
tk.Button(frame_bottom, text="Annulla", command=root.quit).pack(side='right', padx=10)

# Avvio dell'interfaccia
root.mainloop()
