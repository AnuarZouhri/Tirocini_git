import os
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
from collections import defaultdict
from datetime import datetime
from matplotlib.ticker import MultipleLocator
from math import sqrt

def dev_std(x):
    var = np.sum((x - np.mean(x)) ** 2) / (len(x) - 1)
    return sqrt(var)

def generate_statistics(start_time,
                        nome_file="Threads/Statistics/statistiche.txt",
                        output_dir="Threads/Statistics",
                        nome_pdf="Analisi-Dati.pdf",
                        ):
    # Dizionario per raccogliere le dimensioni per ogni protocollo
    dati_per_protocollo = defaultdict(list)

    # Apri il file e leggi riga per riga
    with open(nome_file, "r") as file:
        next(file)  # Salta l'intestazione "PROTOCOLLO,DIMENSIONE"
        for linea in file:
            linea = linea.strip()
            if linea:  # Ignora righe vuote
                protocollo, dimensione = linea.split(",")
                dati_per_protocollo[protocollo].append(int(dimensione))

    dati = dict(dati_per_protocollo)

    max_per_pagina = 4
    numero_righe = 2
    numero_colonne = 2
    protocolli = list(dati.items())

    dimensioni_all = []
    for dim_list in dati.values():
        dimensioni_all.extend(dim_list)

    inizio = datetime.fromtimestamp(start_time).strftime("%d/%m/%Y %H:%M:%S")
    fine = datetime.now().strftime("%d/%m/%Y %H:%M:%S")


    # Crea cartella output se non esiste
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    output_pdf = os.path.join(output_dir, nome_pdf)

    # Crea PDF
    with PdfPages(output_pdf) as pdf:

        fig = plt.figure(figsize=(12, 8))
        fig.text(0.5, 0.85, "Analisi descrittiva dei pacchetti monitorati", fontsize=20, ha='center')
        fig.text(0.35, 0.725, f"Inizio scansione: {inizio}", fontsize=15, ha='center')
        fig.text(0.75, 0.725, f"Fine scansione: {fine}", fontsize=15, ha='center')
        fig.text(0.1, 0.60, f"Totale pacchetti analizzati: {len(dimensioni_all)}", fontsize=14, ha='left')
        fig.text(0.1, 0.55, f"Dimensione media dei pacchetti: {round(np.mean(dimensioni_all),2)}", fontsize=14, ha='left')
        fig.text(0.1, 0.50, f"Mediana sulla dimensione dei pacchetti: {np.median(dimensioni_all)}", fontsize=14, ha='left')

        #fig.text(0.1, 0.45, f"Deviazione standard stimata sulla dimensione dei pacchetti: {round(dev_std(dimensioni_all),2)}", fontsize=14, ha='left')

        #fig.text(0.5, 0.4, "Descrizione:", fontsize=14, ha='center')
        #fig.text(0.5, 0.35, "----", ha='center')

        plt.axis('off')
        pdf.savefig(fig)
        plt.close()

        # Inserimento dei boxplot per ogni protocollo
        for i in range(0, len(protocolli), max_per_pagina):

            gruppo = protocolli[i:i + max_per_pagina]

            fig, axs = plt.subplots(numero_righe, numero_colonne, figsize=(12, 8))
            axs = axs.flatten()

            if i == 0:
                fig.suptitle("Boxplot per Protocollo", fontsize=16)

            for j, (protocollo, dimensioni) in enumerate(gruppo):
                axs[j].boxplot(dimensioni)
                axs[j].set_title(protocollo)
                axs[j].set_xlabel("Campioni")
                axs[j].set_ylabel("Dimensione")

            for k in range(len(gruppo), len(axs)):
                fig.delaxes(axs[k])

            plt.tight_layout()
            pdf.savefig(fig)
            plt.close()

        fig, ax = plt.subplots(figsize=(12, 8))
        fig.suptitle("Boxplot sulle dimensioni", fontsize=16)

        ax.yaxis.set_major_locator(MultipleLocator(50))
        median_prop = dict(linewidth=3, color='red')
        ax.boxplot(dimensioni_all, medianprops=median_prop)
        ax.set_xlabel("Campioni")
        ax.set_ylabel("Dimensione")

        x_jitter = np.random.normal(1, 0.04, size=len(dimensioni_all))
        ax.scatter(x_jitter, dimensioni_all, alpha=0.5, color='blue')

        plt.tight_layout()
        pdf.savefig(fig)
        plt.close()

        conteggi = {protocollo: len(dimensioni) for protocollo, dimensioni in dati.items()}

        etichette = list(conteggi.keys())
        valori = list(conteggi.values())

        fig, ax = plt.subplots(figsize=(12, 8))
        ax.bar(etichette, valori, color='skyblue')
        ax.set_title("Numero di elementi per protocollo")
        ax.set_xlabel("Protocollo")
        ax.set_ylabel("Numero di elementi")
        ax.grid(axis='y', linestyle='--', alpha=0.7)
        plt.tight_layout()
        pdf.savefig(fig)
        plt.close()

    print(f"PDF generato in: {output_pdf} con massimo {max_per_pagina} boxplot per pagina!")

