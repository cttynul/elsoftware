import pandas as pd
dataset_quotazioni = pd.read_excel("Quotazioni_Fantacalcio_Ruoli_Fantagazzetta.xlsx",header = 1)

#debug 
list(dataset_quotazioni.columns.values)
#['Id', 'R', 'Nome', 'Squadra', 'Qt. A', 'Qt. I', 'Diff.']

#droppo le colonne che non voglio utilizzare nel dataset finale

dataset_quotazioni = dataset_quotazioni.drop('Id',1)

dataset_quotazioni = dataset_quotazioni.drop('Squadra',1)
dataset_quotazioni = dataset_quotazioni.drop('Qt. A',1)
dataset_quotazioni = dataset_quotazioni.drop('Diff.',1)

#debug
list(dataset_quotazioni.columns.values)
#['Nome', 'Qt. I']

dataset_statistiche1 = pd.read_excel("Statistiche_Fantacalcio_2015-16_Fantagazzetta.xlsx",header = 1)

#debug 
list(dataset_statistiche1.columns.values)
#['Id', 'R', 'Nome', 'Squadra', 'Pg_15', 'Mv_15', 'Mf_15', 'Gf_15', 'Gs_15', 'Rp_15', 'Rc_15', 'R+_15', 'R-_15', 'Ass_15', 'Asf_15', 'Amm_15', 'Esp_15', 'Au_15']

#droppo le colonne che non voglio utilizzare nel dataset finale

dataset_statistiche1 = dataset_statistiche1.drop('Id',1)
dataset_statistiche1 = dataset_statistiche1.drop('Squadra',1)
dataset_statistiche1 = dataset_statistiche1.drop('R',1)
#Cancello la media voto, considero la media voto con bonus/malus
dataset_statistiche1 = dataset_statistiche1.drop('Mv_15',1)
dataset_statistiche1 = dataset_statistiche1.drop('Gf_15',1)
dataset_statistiche1 = dataset_statistiche1.drop('Gs_15',1)
dataset_statistiche1 = dataset_statistiche1.drop('Rp_15',1)
dataset_statistiche1 = dataset_statistiche1.drop('Rc_15',1)
dataset_statistiche1 = dataset_statistiche1.drop('R+_15',1)
dataset_statistiche1 = dataset_statistiche1.drop('R-_15',1)
dataset_statistiche1 = dataset_statistiche1.drop('Ass_15',1)
dataset_statistiche1 = dataset_statistiche1.drop('Asf_15',1)
dataset_statistiche1 = dataset_statistiche1.drop('Amm_15',1)
dataset_statistiche1 = dataset_statistiche1.drop('Esp_15',1)
dataset_statistiche1 = dataset_statistiche1.drop('Au_15',1)

list(dataset_statistiche1.columns.values)
#ruolo, nome, partite_giocate,media_fantacalcio
#['R', 'Nome', 'Pg_15', 'Mf_15']

dataset_statistiche2 = pd.read_excel("Statistiche_Fantacalcio_2016-17_Fantagazzetta.xlsx",header = 1)


dataset_statistiche2 = dataset_statistiche2.drop('Id',1)
dataset_statistiche2 = dataset_statistiche2.drop('Squadra',1)
dataset_statistiche2 = dataset_statistiche2.drop('R',1)
#Cancello la media voto, considero la media voto con bonus/malus
dataset_statistiche2 = dataset_statistiche2.drop('Mv_16',1)
dataset_statistiche2 = dataset_statistiche2.drop('Gf_16',1)
dataset_statistiche2 = dataset_statistiche2.drop('Gs_16',1)
dataset_statistiche2 = dataset_statistiche2.drop('Rp_16',1)
dataset_statistiche2 = dataset_statistiche2.drop('Rc_16',1)
dataset_statistiche2 = dataset_statistiche2.drop('R+_16',1)
dataset_statistiche2 = dataset_statistiche2.drop('R-_16',1)
dataset_statistiche2 = dataset_statistiche2.drop('Ass_16',1)
dataset_statistiche2 = dataset_statistiche2.drop('Asf_16',1)
dataset_statistiche2 = dataset_statistiche2.drop('Amm_16',1)
dataset_statistiche2 = dataset_statistiche2.drop('Esp_16',1)
dataset_statistiche2 = dataset_statistiche2.drop('Au_16',1)


dataset_statistiche3 = pd.read_excel("Statistiche_Fantacalcio_2017-18_Fantagazzetta.xlsx",header = 1)


dataset_statistiche3 = dataset_statistiche3.drop('Id',1)
dataset_statistiche3 = dataset_statistiche3.drop('Squadra',1)
dataset_statistiche3 = dataset_statistiche3.drop('R',1)
#Cancello la media voto, considero la media voto con bonus/malus
dataset_statistiche3 = dataset_statistiche3.drop('Mv_17',1)
dataset_statistiche3 = dataset_statistiche3.drop('Gf_17',1)
dataset_statistiche3 = dataset_statistiche3.drop('Gs_17',1)
dataset_statistiche3 = dataset_statistiche3.drop('Rp_17',1)
dataset_statistiche3 = dataset_statistiche3.drop('Rc_17',1)
dataset_statistiche3 = dataset_statistiche3.drop('R+_17',1)
dataset_statistiche3 = dataset_statistiche3.drop('R-_17',1)
dataset_statistiche3 = dataset_statistiche3.drop('Ass_17',1)
dataset_statistiche3 = dataset_statistiche3.drop('Asf_17',1)
dataset_statistiche3 = dataset_statistiche3.drop('Amm_17',1)
dataset_statistiche3 = dataset_statistiche3.drop('Esp_17',1)
dataset_statistiche3 = dataset_statistiche3.drop('Au_17',1)

df1 = pd.DataFrame(dataset_quotazioni)
df2 = pd.DataFrame(dataset_statistiche1)
df3 = pd.DataFrame(dataset_statistiche2)
df4 = pd.DataFrame(dataset_statistiche3)


dataset = df1.merge(df2,on="Nome").merge(df3,on="Nome").merge(df4,on="Nome")
#result = dataset.sort_values(by='Qt. I')

media_giocatori = []
for index, row in dataset.iterrows():
	if  row.Pg_17 > 0:	 
		media_pesata_partite_giocate = (row.Pg_15/38 * row.Mf_15)*0.20 + (row.Pg_16/38 * row.Mf_16)*0.80 #+ (row.Pg_17/38 * row.Mf_17)*0.20
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
		total.append(row.mediaGiocatori*row.media*row['Mf_17'])
	else:
		total.append(0)

dataset["convenienza"] = total
result = dataset.sort_values(by="convenienza",ascending='false')

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


