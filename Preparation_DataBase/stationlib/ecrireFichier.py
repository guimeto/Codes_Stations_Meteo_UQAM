# -*-coding:Latin-1 -*
###############################################################################################################################################################
# Nom : ecrireFichier()
# Auteurs : Frederick Toupin et Georges Huard pour la version perl. François-Xavier Dueymes pour la traduction en python l'adaptation en library
# Dernière modification le: 25 juillet 2017
# Description : Ecrit les données de data dans un fichier html pointé par le path. Si le fichier existe, ne fait qu'ajouter une nouvelle ligne de 
# données, sinon création d'un nouveau fichier (pour un nouveau jour). 
# ATTENTION CECI EST UNE VERSION TEST, CE SCRIPT DOIT ETRE MODIFIE POUR ENVOYER LES REQUETES A LA BASE DE DONNEES
# Arguments entrée : data, liste contenant path et toutes les données à écrire 
# Arguments sortie : //
###############################################################################################################################################################
from .bd import bd
def ecrireFichier(data):
	#Ouverture ou création du fichier html contenant les données météorologiques journalières. On se place à la fin du fichier pour ajouter toutes les minutes une nouvelle entrée de données
	file = open(data[1]+"/"+data[0].strftime('%Y%m%d')+".html", 'a')
	file.write(data[0].strftime('%Y%m%d%H%M'))
	for i in range(2, 18):
		file.write(";"+data[i])
        
	file.write("\n\r")
	file.close()
    # (date, temperature, humidite, pression, directionVent, vitesseVent, pyranometre, pyranometreUP, pyranometreDW, pyregeometreUP, pyregeometreDW, prec1mm, prec2mm, prec3mm, prec1tot, prec2tot, prec3tot, precmoy, precmoytot) 
	#laboStationQuery = "INSERT INTO LaboStation VALUES('"+data[0].strftime('%Y-%m-%d %H:%M:%S')+"','"+data[2]+"','"+data[4]+"','"+data[5]+"','"+data[6]+"','"+data[7]+"','"+data[8]+"','"+data[10]+"','"+data[9]+"','"+data[11]+"','"+data[3]+"','"+data[12]+"','"+data[13]+"','"+data[14]+"','"+data[15]+"','"+data[16]+"','"+data[17]+"')"
	queryReleveMeteo = "INSERT INTO ReleveMeteo (date,temperature, humidite, pression, directionVent, vitesseVent, pyranometre, pyranometreUP, pyranometreDW, pyregeometreUP, pyregeometreDW, prec1mm, prec2mm, prec3mm, prec1tot, prec2tot, prec3tot) VALUES('"+data[0].strftime('%Y-%m-%d %H:%M:%S')+"','"+data[4]+"','"+data[2]+"','"+data[3]+"','"+data[5]+"','"+data[6]+"','"+data[7]+"','"+data[8]+"','"+data[9]+"','"+data[10]+"','"+data[11]+"','"+data[12]+"','"+data[13]+"','"+data[14]+"','"+data[15]+"','"+data[16]+"','"+data[17]+"')"
#   queryReleveMeteo = "INSERT INTO ReleveMeteo (date) VALUES('"+data[0].strftime('%Y-%m-%d %H:%M:%S')+"')"
    #print(laboStationQuery)
	print(queryReleveMeteo)
	bd(queryReleveMeteo)
	
	"""
	Contenu de data[]
	-----------------------
	[0]		date
	[1]		dirPath
	[2] 	hum_air
	[3] 	pression_atm
	[4]		temp_air
	[5]		dir_vent
	[6]		vit_vent
	[7]		rad_CM3_w
	[8]		rad_cnr1_cm3 haut
	[9]		rad_cnr1_cm3_bas
	[10]	rad_cnr1_cg3_haut
	[11]	rad_cnr1_cg3_bas
	[12]	preci1mm
	[13]	preci2mm
	[14]	preci3mm
	[15]	preci1tot
	[16]	preci2tot
	[17]	preci3tot

	"""
