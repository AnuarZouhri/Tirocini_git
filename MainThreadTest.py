from Threads.ThreadSniffer import ThreadSniffer
from Threads.ThreadAnalyzer import ThreadAnalyzer
from Threads.Queue import Queue
from Threads.Interfaccia import Interfaccia
from Threads.Statistics.Statistics import generate_statistics
import tkinter as tk
import os
import csv
from time import sleep


def ultimo_script():
    generate_statistics()

def on_closing():
    #interface.close_all_canvas()
    thread_sniffer.stop()
    thread_analyzer.stop()
    #sleep(3)
    ultimo_script()
    # segnala al thread di fermarsi

    #thread_sniffer.join()
    #thread_analyzer.join()
    root.destroy()


if __name__ == "__main__":
    print(1)
    root = tk.Tk()
    root.title("Sniffer GUI")
    root.geometry("1900x1000")

    file_path = "Threads/Statistics/statistiche.txt"
    #generate_statistics(file_path)

    #os.makedirs(os.path.dirname(file_path), exist_ok=True)  # Crea la cartella se non esiste

    if os.path.exists(file_path):
        os.remove(file_path)

    with open(file_path, 'w') as file:
        file.write("PROTOCOLLO,DIMENSIONE\n")

    # Percorso file CSV
    log_path = "Threads/Log/log_protocollo.csv"

    # Crea il file con intestazioni se non esiste
    if not os.path.exists(log_path):
        with open(log_path, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["Protocollo", "Descrizione", "Inizio", "Fine"])


    shared_queue = Queue()
    interface = Interfaccia(root)
    thread_sniffer = ThreadSniffer(shared_queue,file_path)
    thread_sniffer.daemon = True
    thread_analyzer = ThreadAnalyzer(shared_queue,interface,log_path)
    thread_analyzer.daemon = True
    thread_sniffer.start()
    thread_analyzer.start()
    #atexit.register(ultimo_script)
    root.protocol("WM_DELETE_WINDOW", on_closing)
    root.mainloop()

