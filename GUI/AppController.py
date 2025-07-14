# app_controller.py

import tkinter as tk
from GUI.Interface import Interface
from GUI.StartPage import StartPage
from Threads.ThreadSniffer import ThreadSniffer
from Threads.ThreadAnalyzer import ThreadAnalyzer
from Threads.Queue import Queue
import time
import os
import csv
import sys

class AppController:
    def __init__(self, root):
        self.root = root

        # Trova il percorso corretto (funziona anche da .exe)
        if getattr(sys, 'frozen', False):  # Se eseguito da exe (PyInstaller)
            base_path = sys._MEIPASS
        else:
            base_path = os.path.abspath(".")

        # Percorso completo all'icona
        icon_path = os.path.join(base_path, "Pictures", "Logo.ico")

        # Imposta l'icona se esiste
        if os.path.exists(icon_path):
            self.root.iconbitmap(icon_path)
        else:
            print(f"⚠️ Icon not found: {icon_path}")

        #self.root.iconbitmap("Pictures/Logo.ico")
        self.root.title("EASY SHARK")

        self.root.geometry("1900x1000")
        self.setted_values = {}

        self.container = tk.Frame(self.root)
        self.container.pack(fill="both", expand=True)
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)

        self.queue = Queue()

        self.file_path = os.path.join(base_path, "Threads", "Statistics", "statistiche.txt")
        self.log_path = os.path.join(base_path, "Threads", "Log", "log_file.csv")

        #self.file_path = "Threads/Statistics/statistiche.txt"
        #self.log_path = "Threads/Log/log_file.csv"

        self._init_files()
        self.start_analyzing = time.time()

        # Crea le schermate
        self.frames = {}
        self.frames["StartPage"] = StartPage(self.container, self)
        self.frames["Interfaccia"] = Interface(self.container, self.start_analyzing)

        # Posiziona entrambi i frame nel container
        for frame in self.frames.values():
            frame.grid(row=0, column=0, sticky="nsew")


        self.show_frame("StartPage")

        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

    def _init_files(self):
        if os.path.exists(self.file_path):
            os.remove(self.file_path)
        with open(self.file_path, 'w') as file:
            file.write("PROTOCOLLO,DIMENSIONE\n")
        if not os.path.exists(self.log_path):
            with open(self.log_path, mode='w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(["Description", "Inizio", "Fine"])

    def show_frame(self, name):
        frame = self.frames[name]
        frame.tkraise()

    def start_analysis(self,setted_values, ports, ips):
        self.setted_values = setted_values
        self.thread_sniffer = ThreadSniffer(self.queue, self.file_path,ips,interface=str(setted_values['interface']))
        self.thread_analyzer = ThreadAnalyzer(self.queue, self.frames["Interfaccia"], self.log_path, dict(list(self.setted_values.items())[1:]),ports)
        self.frames["Interfaccia"].set_threads(self.thread_sniffer, self.thread_analyzer)

        self.thread_sniffer.daemon = True
        self.thread_analyzer.daemon = True
        self.thread_sniffer.start()
        self.thread_analyzer.start()

        self.show_frame("Interfaccia")

    def on_closing(self):
        try:
            self.thread_sniffer.stop()
            self.thread_analyzer.stop()
        except AttributeError:
            pass  # thread not started yet
        self.root.destroy()
