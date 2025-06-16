"""Importa la libreria pandas e la rinomina come `pd`.
pandas è una libreria Python usata per manipolare dati in formato tabellare (come fogli Excel o tabelle SQL):"""
import pandas as pd

#MAC address (sostituirlo con MAC address degli arduino):
mac_addresses = ["00:1A:2B:3C:4D:5E", "11:22:33:44:55:66", "AA:BB:CC:DD:EE:FF"]

#Simulazione dei dati (valori per secondo):

"""Crea un dizionario di dati simulati. Ogni chiave (es. MAC Address) rappresenta una colonna della tabella, 
e il valore associato (una lista) rappresenta i dati delle righe. Ogni quartetta sotto riportata è comunque rappresentata come una colonna:"""
data = {
    "MAC Address": mac_addresses,
    "Media dimensione pacchetti (byte/s)": [350, 420, 390],
    "Pacchetti corrotti al secondo": [2, 0, 5],
    "Pacchetti totali al secondo": [100, 120, 110]
}

#Creazione della tabella:

#Crea un DataFrame (tabella) da data. df è un oggetto tabellare simile a un foglio di calcolo, facile da manipolare e analizzare:
df = pd.DataFrame(data)

#Calcolo della % di pacchetti corrotti, in formula:
df["% pacchetti corrotti"] = (df["Pacchetti corrotti al secondo"] / df["Pacchetti totali al secondo"]) * 100
"""Questa riga crea una nuova colonna nel DataFrame chiamata "% pacchetti corrotti" e ci inserisce la percentuale di pacchetti corrotti rispetto al 
totale, per ogni riga della tabella."""

#Visualizza la tabella:

#Stampa a video della tabella:
print(df)