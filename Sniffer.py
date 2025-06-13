import subprocess
import datetime
from time import sleep
from threading import Thread
import tkinter as tk
from queue import Queue


packet_queue = Queue()

def sniffing():
    with subprocess.Popen("C:\\Users\\darka\\scansione.bat",stdout=subprocess.PIPE,
                     stderr=subprocess.DEVNULL, text=True) as proc:
                         print(1)
                         for line in proc.stdout:
                            print(2)
                            fields = line.strip().split(',')
                            epoch_time = float(fields[2])
                            dt = datetime.datetime.fromtimestamp(epoch_time)
                            if len(fields) >= 4:
                                formatted = (f"ip src: {fields[0]}, ip dst: {fields[1]}, timestamp: {dt.strftime('%Y-%m-%d %H:%M:%S.%f')} protocol: {fields[3]}, MAC src: {fields[4]}")
                                print(formatted)
                                packet_queue.put(formatted)




# GUI setup
root = tk.Tk()
root.title("Sniffer Live")
root.geometry("800x400")

text_area = tk.Text(root, wrap="none")
text_area.pack(fill="both", expand=True)

def update_gui():

    while not packet_queue.empty():
        packet = packet_queue.get()
        print(packet)
        text_area.insert("end", packet + "\n")
        text_area.see("end")
    root.after(100, update_gui)


'''root = Tk()
frm = ttk.Frame(root, padding=10)
frm.grid()
ttk.Label(frm, text="Hello World!").grid(column=0, row=0)
ttk.Button(frm, text="Quit", command=root.destroy).grid(column=1, row=0)'''



thread_sniff = Thread(target = sniffing, daemon = True)
thread_sniff.start()
#sniffing()


#while True:
 #   print(2)
  #  sleep(2)

update_gui()
root.mainloop()

