import requests
import pandas as pd

codice_segretissimo = ["-6", "1614489243000", "1643664948000"]
years = ["2019-20", "2020-21", "2021-22"]
years_compact = ["19", "20", "21"]
#years = ["2015-16", "2016-17", "2017-18"] Solo per ricordo

open('Quotazioni_Fantacalcio_Ruoli_Fantagazzetta.xlsx', 'wb').write(requests.get("https://www.fantacalcio.it/Servizi/Excel.ashx?type=0&r=1&t=" + codice_segretissimo[-1], allow_redirects=True).content)
for y in years: open('Statistiche_Fantacalcio_' + y + '_Fantagazzetta.xlsx', 'wb').write(requests.get("https://www.fantacalcio.it/Servizi/Excel.ashx?type=2&r=1&t=" + codice_segretissimo[years.index(y)] + "&s=" + y, allow_redirects=True).content)

dataset_quotazioni = pd.read_excel("Quotazioni_Fantacalcio_Ruoli_Fantagazzetta.xlsx",header = 1)

#debug 
#list(dataset_quotazioni.columns.values)
#['Id', 'R', 'Nome', 'Squadra', 'Qt. A', 'Qt. I', 'Diff.']

#droppo le colonne che non voglio utilizzare nel dataset finale

clean_quot = ['Id', 'Squadra', 'Qt. A', 'Diff.']
for e in clean_quot:
    try: dataset_quotazioni = dataset_statistiche1.drop(e, 1)
    except: pass

#debug
#list(dataset_quotazioni.columns.values)
#['Nome', 'Qt. I']

dataset_statistiche1 = pd.read_excel("Statistiche_Fantacalcio_" + years[0] + "_Fantagazzetta.xlsx",header = 1)

#debug 
#list(dataset_statistiche1.columns.values)
#to_be_removed = ['Id', 'R', 'Nome', 'Squadra', 'Pg_' + years_compact[0], 'Mv_' + years_compact[0], 'Mf_' + years_compact[0], 'Gf_' + years_compact[0], 'Gs_' + years_compact[0], 'Rp_' + years_compact[0], 'Rc_' + years_compact[0], 'R+_' + years_compact[0], 'R-_' + years_compact[0], 'Ass_' + years_compact[0], 'Asf_' + years_compact[0], 'Amm_' + years_compact[0], 'Esp_' + years_compact[0], 'Au_' + years_compact[0]]

#droppo le colonne che non voglio utilizzare nel dataset finale
#Cancello la media voto, considero la media voto con bonus/malus
to_be_removed = ['Id', 'R', 'Squadra', 'Mv', 'Gf', 'Gs', 'Rp', 'Rc', 'R+', 'R-', 'Ass', 'Asf', 'Amm', 'Esp', 'Au']

for e in to_be_removed: 
    try: dataset_statistiche1 = dataset_statistiche1.drop(e, 1)
    except: pass

    
#list(dataset_statistiche1.columns.values)

#ruolo, nome, partite_giocate,media_fantacalcio
#['R', 'Nome', 'Pg_' + years_compact[0], 'Mf_' + years_compact[0]]

dataset_statistiche2 = pd.read_excel("Statistiche_Fantacalcio_" + years[1] + "_Fantagazzetta.xlsx",header = 1)
#to_be_removed = ['Id', 'R', 'Nome', 'Squadra', 'Pg_' + years_compact[1], 'Mv_' + years_compact[1], 'Mf_' + years_compact[1], 'Gf_' + years_compact[1], 'Gs_' + years_compact[1], 'Rp_' + years_compact[1], 'Rc_' + years_compact[1], 'R+_' + years_compact[1], 'R-_' + years_compact[1], 'Ass_' + years_compact[1], 'Asf_' + years_compact[1], 'Amm_' + years_compact[1], 'Esp_' + years_compact[1], 'Au_' + years_compact[1]]
for e in to_be_removed: 
    try: dataset_statistiche2 = dataset_statistiche2.drop(e, 1)
    except: pass

dataset_statistiche3 = pd.read_excel("Statistiche_Fantacalcio_" + years[2] + "_Fantagazzetta.xlsx",header = 1)
#to_be_removed = ['Id', 'R', 'Nome', 'Squadra', 'Pg_' + years_compact[2], 'Mv_' + years_compact[2], 'Mf_' + years_compact[2], 'Gf_' + years_compact[2], 'Gs_' + years_compact[2], 'Rp_' + years_compact[2], 'Rc_' + years_compact[2], 'R+_' + years_compact[2], 'R-_' + years_compact[2], 'Ass_' + years_compact[2], 'Asf_' + years_compact[2], 'Amm_' + years_compact[2], 'Esp_' + years_compact[2], 'Au_' + years_compact[2]]
for e in to_be_removed: 
    try: dataset_statistiche3 = dataset_statistiche3.drop(e, 1)
    except: pass

# converti in pd
df1 = pd.DataFrame(dataset_quotazioni)
df2 = pd.DataFrame(dataset_statistiche1)
df3 = pd.DataFrame(dataset_statistiche2)
df4 = pd.DataFrame(dataset_statistiche3)

print(df1)
print(df2)
print(df3)
print(df4)


dataset = df1.merge(df2, on="Nome").merge(df3, on="Nome").merge(df4, on="Nome")
result = dataset.sort_values(by='Qt. I')

print(dataset)

media_giocatori = []
for index, row in dataset.iterrows():
	if  row.Pg_x > 0:	 
		media_pesata_partite_giocate = (row.Pg_x/38 * row.Mf_x)*0.20 + (row.Pg_y/38 * row.Mf_y)*0.80
		media_giocatori.append(media_pesata_partite_giocate)
	else:
		media_giocatori.append(0)

dataset["mediaGiocatori"] = media_giocatori

media = []

for index, row in dataset.iterrows():
	if  row.mediaGiocatori > 0:	 
		media.append(row.mediaGiocatori/row["Qt. I"])
	else:
		media.append(0)
dataset["media"] = media
result = dataset.sort_values(by="media")

total = []
for index, row in dataset.iterrows():
	if  row.mediaGiocatori > 0:	 
		total.append(row.mediaGiocatori*row.media*row['Mf'])
	else:
		total.append(0)

dataset["convenienza"] = total
result = dataset.sort_values(by="convenienza",ascending=False)

print(result)

with open("dataset_att.csv", "w") as f:
	df = result[result["R"] == "A"]
	f.write(df.to_string())

with open("dataset_cen.csv", "w") as f:
	df = result[result["R"] == "C"]
	f.write(df.to_string())

with open("dataset_dif.csv", "w") as f:
	df = result[result["R"] == "D"]
	f.write(df.to_string())

with open("dataset_por.csv", "w") as f:
	df = result[result["R"] == "P"]
	f.write(df.to_string())

with open("dataset.csv","w+") as f:
	f.write(result.to_string() )
'''
#f.write(media_giocatori.to_string())


#Dal dataset chiedo in input il numero di crediti da parte dell'utente e creo una formazione tipo "Ideale" basata su una selezione randomica dei giocatori migliori
Questa parte un giorno  la finirò
'''


