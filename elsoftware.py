import requests, re, json
import pandas as pd

CONFIG_FILE = "config.json"

with open(CONFIG_FILE) as f:
	data = json.load(f)
	try: codice_segretissimo = data["codice_segretissimo"]
	except: codice_segretissimo = ["-6", "1614489243000", "1643664948000"]
	try: years = data["years"]
	except: years = ["2019-20", "2020-21", "2021-22"]
	try: position = data["position"]
	except: position = ["Portieri", "Difensori", "Centrocampisti", "Attaccanti"]

position_compact = [p[:1] for p in position]

logo = '''

      _   _____        __ _                          
     | | /  ___|      / _| |                         
  ___| | \ `--.  ___ | |_| |___      ____ _ _ __ ___ 
 / _ \ |  `--. \/ _ \|  _| __\ \ /\ / / _` | '__/ _ \\
|  __/ | /\__/ / (_) | | | |_ \ V  V / (_| | | |  __/
 \___|_| \____/ \___/|_|  \__| \_/\_/ \__,_|_|  \___|
                                                     
    FantaHack                                - cttynul          
'''

print(logo + "\nSettings:\n\tConfig File: " + CONFIG_FILE + "\n\tAnni: " + str(years) + "\n\tPosition Compact:" + str(position_compact) + "\n")

#years = ["2015-16", "2016-17", "2017-18"] Solo per ricordo

try: partite_giocate = int(re.findall('<td>([0-9]+)<\/td>', requests.get("https://sport.virgilio.it/calcio/serie-a/classifica/").text)[0])
except: partite_giocate = 38

open('Quotazioni_Fantacalcio_Ruoli_Fantagazzetta.xlsx', 'wb').write(requests.get("https://www.fantacalcio.it/Servizi/Excel.ashx?type=0&r=1&t=" + codice_segretissimo[-1], allow_redirects=True).content)
for y in years: open('Statistiche_Fantacalcio_' + y + '_Fantagazzetta.xlsx', 'wb').write(requests.get("https://www.fantacalcio.it/Servizi/Excel.ashx?type=2&r=1&t=" + codice_segretissimo[years.index(y)] + "&s=" + y, allow_redirects=True).content)

dataset_quotazioni = pd.read_excel("Quotazioni_Fantacalcio_Ruoli_Fantagazzetta.xlsx",header = 1)

#droppo le colonne che non voglio utilizzare nel dataset finale
clean_quot = ['Id', 'Qt. A', 'Diff.']
for e in clean_quot:
    try: dataset_quotazioni = dataset_quotazioni.drop(labels=e, axis=1)
    except: pass

dataset_statistiche1 = pd.read_excel("Statistiche_Fantacalcio_" + years[0] + "_Fantagazzetta.xlsx",header = 1)

#droppo le colonne che non voglio utilizzare nel dataset finale
#cancello la media voto, considero la media voto con bonus/malus
to_be_removed = ['Id', 'R', 'Squadra', 'Mv', 'Gf', 'Gs', 'Rp', 'Rc', 'R+', 'R-', 'Ass', 'Asf', 'Amm', 'Esp', 'Au']

for e in to_be_removed: 
    try: dataset_statistiche1 = dataset_statistiche1.drop(labels=e, axis=1)
    except: pass

dataset_statistiche2 = pd.read_excel("Statistiche_Fantacalcio_" + years[1] + "_Fantagazzetta.xlsx",header = 1)
for e in to_be_removed: 
    try: dataset_statistiche2 = dataset_statistiche2.drop(labels=e, axis=1)
    except: pass

dataset_statistiche3 = pd.read_excel("Statistiche_Fantacalcio_" + years[2] + "_Fantagazzetta.xlsx",header = 1)
for e in to_be_removed: 
    try: dataset_statistiche3 = dataset_statistiche3.drop(labels=e, axis=1)
    except: pass

# converti in pd
df1 = pd.DataFrame(dataset_quotazioni)
df2 = (pd.DataFrame(dataset_statistiche1).rename(columns = {'Pg': 'Partite Giocate ' + years[0], 'Pg': 'Partite Giocate ' + years[0]}, inplace = False)).rename(columns = {'Mf': 'Fantamedia ' + years[0], 'Mf': 'Fantamedia ' + years[0]}, inplace = False)
df3 = (pd.DataFrame(dataset_statistiche2).rename(columns = {'Pg': 'Partite Giocate ' + years[1], 'Pg': 'Partite Giocate ' + years[1]}, inplace = False)).rename(columns = {'Mf': 'Fantamedia ' + years[1], 'Mf': 'Fantamedia ' + years[1]}, inplace = False)
df4 = (pd.DataFrame(dataset_statistiche3).rename(columns = {'Pg': 'Partite Giocate ' + years[2], 'Pg': 'Partite Giocate ' + years[2]}, inplace = False)).rename(columns = {'Mf': 'Fantamedia ' + years[2], 'Mf': 'Fantamedia ' + years[2]}, inplace = False)
dataset = df1.merge(df2, on="Nome").merge(df3, on="Nome").merge(df4, on="Nome")
result = dataset.sort_values(by='Qt. I')

#print(dataset)

media_giocatori = []
for index, row in dataset.iterrows():
	if  row['Partite Giocate ' + years[0]] > 0:	 
		media_pesata_partite_giocate = (row['Partite Giocate ' + years[0]]/38 * row['Fantamedia ' + years[0]])*0.20 + (row['Partite Giocate ' + years[1]]/38 * row['Fantamedia ' + years[1]])*0.60 + (row['Partite Giocate ' + years[2]]/partite_giocate * row['Fantamedia ' + years[2]])*1.20
		media_giocatori.append(media_pesata_partite_giocate)
	else:
		media_giocatori.append(0)

dataset["Fattore Fantahack"] = media_giocatori

media = []

for index, row in dataset.iterrows():
	if  row["Fattore Fantahack"] > 0:	 
		media.append(row["Fattore Fantahack"]/row["Qt. I"])
	else:
		media.append(0)
dataset["Rapporto Fattore Quota"] = media
result = dataset.sort_values(by="Rapporto Fattore Quota")

total = []
for index, row in dataset.iterrows():
	if  row["Fattore Fantahack"] > 0:	 
		total.append((row["Fattore Fantahack"]*row["Rapporto Fattore Quota"]*row['Fantamedia ' + years[2]]) / 10)
	else:
		total.append(0)

dataset["Convenienza"] = total
result = dataset.sort_values(by="Convenienza",ascending=False)
print(result)

with pd.ExcelWriter("Fantahack.xlsx") as writer:
	for p in position_compact: result[result["R"] == p].to_excel(writer, sheet_name=position[position_compact.index(p)], index=False)

'''
#f.write(media_giocatori.to_string())


#Dal dataset chiedo in input il numero di crediti da parte dell'utente e creo una formazione tipo "Ideale" basata su una selezione randomica dei giocatori migliori
Questa parte un giorno  la finirò
'''


