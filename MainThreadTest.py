from Threads.ThreadSniffer import ThreadSniffer
from Threads.ThreadAnalyzer import ThreadAnalyzer
from Threads.Queue import Queue
from Threads.Interfaccia import Interfaccia
import tkinter as tk
import os

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Sniffer GUI")
    root.geometry("1300x750")

    file_path = "Threads/Statistics/statistiche.txt"


    if os.path.exists(file_path):
        os.remove(file_path)

    with open(file_path, 'w') as file:
        file.write("PROTOCOLLO,DIMENSIONE\n")


    shared_queue = Queue()
    interface = Interfaccia(root)
    thread_sniffer = ThreadSniffer(shared_queue,file_path)
    thread_sniffer.daemon = True
    thread_analyzer = ThreadAnalyzer(shared_queue,interface)
    thread_analyzer.daemon = True
    thread_sniffer.start()
    thread_analyzer.start()

    root.mainloop()