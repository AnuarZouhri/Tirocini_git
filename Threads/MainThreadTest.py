from ThreadSniffer import ThreadSniffer
from ThreadAnalyzer import ThreadAnalyzer
from Queue import Queue
from Interfaccia import Interfaccia
import tkinter as tk

from Threads.ThreadInterface import ThreadInterface

if __name__ == "__main__":
    root = tk.Tk()
    shared_queue = Queue()
    interface = Interfaccia(root)
    thread_sniffer = ThreadSniffer(shared_queue)
    thread_sniffer.daemon = True
    thread_analyzer = ThreadAnalyzer(shared_queue,interface)
    thread_analyzer.daemon = True
    thread_interface = ThreadInterface(interface)
    thread_interface.daemon = True
    print(2)
    thread_sniffer.start()
    thread_analyzer.start()
    thread_interface.start()

    root.mainloop()