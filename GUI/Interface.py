
from GraphicElements.pie_chart import PieChartFrame
from GraphicElements.ip_mac_table import IpMacTable
from GraphicElements.table import PacketTable
from GraphicElements.alert_table import DoSAlertTable
from GraphicElements.avg_size_plot import LiveGraph
from GraphicElements.protocol_plot import ProtocolLiveGraph
from GraphicElements.port_plot import TopDestPortsGraph
import os
import tkinter as tk
from tkinter import simpledialog, messagebox
import shutil
import sys

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS  # Se eseguito da .exe PyInstaller
    except AttributeError:
        base_path = os.path.abspath(".")  # Se eseguito da sorgente
    return os.path.join(base_path, relative_path)

class Interface(tk.Frame):

    def __init__(self, parent, start_time):
        super().__init__(parent, bg="white")

        self.main_frame = self
        self.graph_frames = {}
        self.t_sniffer = None
        self.t_analyzer = None
        self.active_notifications = []
        self.start_analyzing = start_time


     # Suddivido l'interfaccia in due porzioni
        # Configura la griglia del frame principale
        self.main_frame.columnconfigure(0, weight=1, uniform="group1")
        self.main_frame.columnconfigure(1, weight=1, uniform="group1")
        self.main_frame.rowconfigure(0, weight=1)

        # Frame sinistro
        left_frame = tk.Frame(self.main_frame, bg="white", padx=10, pady=1)
        left_frame.grid(row=0, column=0, sticky="nsew")

        # Frame destro
        right_frame = tk.Frame(self.main_frame, bg="white", padx=10, pady=10)
        right_frame.grid(row=0, column=1, sticky="nsew")

        #configurazione frame sinistro
        left_frame.rowconfigure(0, weight=1)
        left_frame.rowconfigure(1, weight=1, uniform='group2')
        left_frame.rowconfigure(2, weight=1, uniform='group2')
        left_frame.columnconfigure(0, weight=1)  # per estensione orizzontale

        #configurazioni bottoni per interrompere la scansione e stampa dei dati
        btn_frame = tk.Frame(left_frame)
        btn_frame.grid(row=0, column=0, sticky="ew", columnspan=2)

        btn_stop = tk.Button(btn_frame, text="Stop scanning", command=self.stop_threads)
        btn_stop.pack(side="left", padx=5)

        btn_export = tk.Button(btn_frame, text="Export statistics", command=self.export_stats)
        btn_export.pack(side="left", padx=5)


        # Frame per il plot delle porte in basso nella colonna sinistra
        port_plot_frame = tk.Frame(left_frame, bg='white')
        port_plot_frame.grid(row=2, column=0, sticky="nsew")
        port_plot_frame.rowconfigure(0, weight=1)
        port_plot_frame.columnconfigure(0, weight=1)

        # Frame per grafici selezionabili
        graph_container_frame = tk.Frame(left_frame, bg='white')
        graph_container_frame.grid(row=1, column=0, sticky="nsew")
        graph_container_frame.rowconfigure(0, weight=1)
        graph_container_frame.columnconfigure(0, weight=1)

        # I grafici principali si inseriscono in questo contenitore
        new_avg_size_plot_frame = tk.Frame(graph_container_frame, bg='white')
        new_avg_size_plot_frame.grid(row=1, column=0, sticky='nsew')

        protocol_plot_frame = tk.Frame(graph_container_frame, bg='white')
        protocol_plot_frame.grid(row=1, column=0, sticky='nsew')
        protocol_plot_frame.grid_remove()

        # Disattiva propagazione se vuoi altezza fissa interna
        new_avg_size_plot_frame.pack_propagate(False)
        protocol_plot_frame.pack_propagate(False)


        right_frame_packet_table = tk.Frame(right_frame,bg="white", padx=10, pady=10)
        right_frame_packet_table.pack(side='top',fill='both')

        right_frame_ip_mac_table = tk.Frame(right_frame, bg="white", padx=10, pady=10)
        right_frame_ip_mac_table.pack(side='top', fill='both')

        right_frame_pie = tk.Frame(right_frame, bg="white", padx=10, pady=10)
        right_frame_pie.pack(side='top', fill='both')

        right_frame_pie1 = tk.Frame(right_frame_pie, bg="white", padx=2, pady=2)
        right_frame_pie1.pack(side='left', fill='both',expand=True)

        right_frame_pie2 = tk.Frame(right_frame_pie, bg="white", padx=2, pady=2)
        right_frame_pie2.pack(side='left', fill='both',expand=True)

        right_frame_alert_table = tk.Frame(right_frame, bg="white")
        right_frame_alert_table.pack(side='top', fill='both')

        # Istanzia i grafici
        self.new_avg_size_plot = LiveGraph(new_avg_size_plot_frame)
        self.graph_frames['Avg Size'] = new_avg_size_plot_frame


        self.protocol_plot = ProtocolLiveGraph(protocol_plot_frame)
        self.graph_frames['Protocol'] = protocol_plot_frame

        # Istanzia il port plot
        self.port_plot = TopDestPortsGraph(port_plot_frame)
        self.port_plot.pack(fill='both', expand=True)

        self.packet_table = PacketTable(right_frame_packet_table)
        self.ip_mac_table = IpMacTable(right_frame_ip_mac_table)

        self.pie_chart1 = PieChartFrame(right_frame_pie1, 'Packets per Protocol', legend="Protocols")
        self.pie_chart1.pack(fill='both', expand=True)

        self.pie_chart2 = PieChartFrame(right_frame_pie2, 'IP Src Distribution', legend="IP Src")
        self.pie_chart2.pack(fill='both', expand=True)

        self.pie_chart3 = PieChartFrame(right_frame_pie2, 'IP Dst Distribution', legend="IP Dst")
        self.pie_chart3.pack(fill='both', expand=True)


        self.collection_graphics = {
            'packet per protocol': self.pie_chart1,
            'IP source distribution': self.pie_chart2,
            'IP dst distribution': self.pie_chart3
        }

        combox_frame = tk.Frame(btn_frame)
        combox_frame.pack(side='right',padx=4)

        # ComboBox sotto entrambi
        self.chart_selector = tk.ttk.Combobox(combox_frame, values=["IP Src", "IP Dst"], state="readonly")
        self.chart_selector.pack(side='left')
        self.chart_selector.set("IP Src")
        self.chart_selector.bind("<<ComboboxSelected>>", lambda e: self.show_selected_pie(self.chart_selector.get()))

        # Mostra grafico iniziale
        self.show_selected_pie("IP Src")

        self.alert_table = DoSAlertTable(right_frame_alert_table)
        self.alert_table.pack(fill="both")

        # Combobox per selezione tra i due grafici
        graph_selector = tk.ttk.Combobox(combox_frame, values=["Avg Size", "Protocol"], state="readonly")
        graph_selector.pack(side='left')
        graph_selector.set("Avg Size")

        # Mostra grafico iniziale
        self.show_selected_graph("Avg Size")
        graph_selector.bind("<<ComboboxSelected>>", lambda e: self.show_selected_graph(graph_selector.get()))

    def update_pie_chart(self, data, selected):
        self.main_frame.after(0,self.collection_graphics[selected].updateData,data)
        #self.collection_graphics[selected].updateData(data)

    def update_table_ip_mac(self, data):
        self.main_frame.after(1,self.ip_mac_table.update_table,data)
        #self.ip_mac_table.update_table(data)

    def update_packet_table(self, data):
        self.main_frame.after(2,self.packet_table.update_table,data)
        #self.packet_table.update_table(data)

    def update_alert_table(self, data, time):
        #self.alert_table.clear_all_alerts()
        if data:
            self.main_frame.after(1,self.alert_table.add_alert,data, time)
            #self.alert_table.add_alert(data)

    def update_live_plot(self, data):
        self.main_frame.after(0,self.new_avg_size_plot.update,data)
        #self.new_avg_size_plot.update(data)

    def update_protocol_live_plot(self, data):
        self.main_frame.after(0,self.protocol_plot.update_graph,data)
        #self.protocol_plot.update_graph(data)

    def update_port_plot(self,data):
        self.main_frame.after(2,self.port_plot.update,data)

    #per decidere quale grafico a torta mostrare
    def show_selected_pie(self, selection):
        self.pie_chart2.pack_forget()
        self.pie_chart3.pack_forget()

        if selection == "IP Src":
            self.pie_chart2.pack(fill='both', expand=True)
        elif selection == "IP Dst":
            self.pie_chart3.pack(fill='both', expand=True)

    def show_selected_graph(self, selection):
        for name, frame in self.graph_frames.items():
            frame.grid_remove()  # Nasconde il frame (versione grid di pack_forget)
        self.graph_frames[selection].grid(row=0, column=0, sticky='nsew')  # O la posizione corretta nel contenitore

    def set_threads(self,s,a):
        self.t_sniffer = s
        self.t_analyzer = a

    def stop_threads(self):
        if hasattr(self, 't_sniffer'):
            self.t_sniffer.stop()
        if hasattr(self, 't_analyzer'):
            self.t_analyzer.stop()

    def export_stats(self):
        from GUI.SetPath import SetPath

        def on_directory_chosen(cartella_scelta):

            nome_file = simpledialog.askstring(
                "Filename",
                "Enter the name for the PDF file (without .pdf):",
                parent=self
            )

            if not nome_file:
                print("File name not entered, operation cancelled.")
                return

            nome_pdf = nome_file + ".pdf"
            percorso_completo = os.path.join(cartella_scelta, nome_pdf)

            if os.path.exists(percorso_completo):
                messagebox.showerror("Error",
                                     f"The file '{nome_pdf}' already exists in the selected folder.\nPlease choose a different name.")
                print(f"File '{nome_pdf}' already exists in: {cartella_scelta}. Operation canceled.")
                return

            from Threads.Statistics.Statistics import generate_statistics
            percorso_file_statistiche = resource_path("Threads/Statistics/statistiche.txt")
            #percorso_file_statistiche = "Threads/Statistics/statistiche.txt"

            def safe_path(filepath):
                base, ext = os.path.splitext(filepath)
                counter = 1
                new_path = filepath
                while os.path.exists(new_path):
                    new_path = f"{base}_{counter}{ext}"
                    counter += 1
                return new_path

            path_ip_mac_table = safe_path(os.path.join(cartella_scelta, "ip_mac_table.csv"))
            path_packet_table = safe_path(os.path.join(cartella_scelta, "packet_table.csv"))

            generate_statistics(
                nome_file=percorso_file_statistiche,
                output_dir=cartella_scelta,
                nome_pdf=nome_pdf,
                start_time=self.start_analyzing
            )

            print(f"PDF generated in folder: {cartella_scelta} with name: {nome_pdf}")
            self.ip_mac_table.export_to_csv(path_ip_mac_table)
            self.packet_table.export_to_csv(path_packet_table)

            # 🔁 Rinomina log_protocollo.csv se esiste già
            src_path = resource_path("Threads/Log/log_file.csv")
            dst_path = os.path.join(cartella_scelta, "log_file.csv")

            counter = 1
            base, ext = os.path.splitext(dst_path)
            while os.path.exists(dst_path):
                dst_path = f"{base}_{counter}{ext}"
                counter += 1

            if os.path.exists(src_path):
                shutil.move(src_path, dst_path)
                print(f"Export completed: {dst_path}")
            else:
                messagebox.showwarning("Missing file",
                                       f"⚠️ The file '{src_path}' was not found. Partial export.")
                print(f"Warning: file '{src_path}' not found. Partial export.")

            #shutil.move(src_path, dst_path)

        SetPath(self, on_confirm_callback=on_directory_chosen)

