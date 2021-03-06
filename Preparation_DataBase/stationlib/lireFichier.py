# -*-coding:Latin-1 -*
###############################################################################################################################################################
# Nom : lireFichier()
# Auteurs : Frederick Toupin et Georges Huard pour la version perl. François-Xavier Dueymes pour la traduction en python l'adaptation en library
# Dernière modification le: 25 juillet 2017
# Description : Lit le fichier pointé par filename, extrait les données dans un tuple, regarde selon la date si le dossier  
# où stocker ces données existe, les crée au besoin, puis appelle ecrireFichier() en passant la liste de données à écrire et le path
# Arguments entrée : filename qui est le path du fichier à lire
# Arguments sortie : usefulData qui est une liste contenant toutes les données et informations (path) pour stocker les données convenablement
###############################################################################################################################################################
import datetime, os
import csv 
import codecs
from .ecrireFichier import ecrireFichier
def lireFichier(filename):
	#Ouverture du fichier csv précédemment créé et extraction des données dans un tuple
	try:
		data = codecs.open('stationData.csv')
		reader=csv.reader(data)
		dataTuple=tuple(next(reader))
		data.close()
		
	except Exception as e:
		raise
		print("Impossible d'ouvrir le fichier demande")
		
	"""
	Contenu de dataTuple[]
	----------------------
		[0]		ident_mess
		[1]		annee
		[2]		jour_jul
		[3]		heure_minutes
		[4]		ident_station
		[5]		temp_interne
		[6]		int_donnees
		[7]		volt_bat
		[8]		pression_atm
		[9] 	temp_air
		[10] 	hum_air
		[11]	vit_vent
		[12]	dir_vent
		[13]	vit_max_vent
		[14]	dir_max_vent
		[15]	heure_max_vent
		[16]	vit_vent_2
		[17]	vit_dir_vent_2
		[18]	vit_vent_10
		[19]	dir_vent_10
		[20]	vit_max_vent_10
		[21]	heure_max_vent_10
		[22]	dir_max_vent_10
		[23]	rad_CM3_w
		[24]	rad_CM3_kj
		[25]	rad_cnr1_cm3_haut
		[26]	rad_cnr1_cg3_haut
		[27]	rad_cnr1_cm3_bas
		[28]	rad_cnr1_cg3_bas
		[29]	version
		[30]	mod_bal
		[31]	signature
		[32]	preci1mm
		[33]	preci2mm
		[34]	preci3mm
		[35]	preci1tot
		[36]	preci2tot
		[37]	preci3tot

	
	#"Explicit is better than Implicit" The Zen of Python 2nd aphorism
	"""
	#conversion de la date en jours julien->date standard
	julianDate = str(dataTuple[1])+str(dataTuple[2])+str(dataTuple[3]).zfill(4)
	date = datetime.datetime.strptime(julianDate,'%Y%j%H%M')


	dirPath="/NFS2_RESCUE2/stationuqam/programmes/recup_donnees_station/data_brute/"+date.strftime('%Y%m')

	#sélection des données à stocker dans la base de données
	usefulData=(date, dirPath, dataTuple[10], dataTuple[8], dataTuple[9], dataTuple[12], dataTuple[11], dataTuple[23], dataTuple[25]
		, dataTuple[27], dataTuple[26], dataTuple[28], dataTuple[32], dataTuple[33], dataTuple[34], dataTuple[35], dataTuple[36]
		, dataTuple[37])
	"""
	Contenu de usefulData[]
		-----------------------
		[0]		date (timestamp)
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
	
	print("---- date -"+date.strftime('%Y-%m-%d %Hh %Mmin')+" - dir - /home/stationuqam/tmp")
	try:
		os.mkdir(dirPath)
	#	print("Nouveau répertoire créé: "+dirPath)
		ecrireFichier(usefulData)
	except OSError:
		if os.path.isdir(dirPath):
		#	print("Répertoire "+dirPath+" existe déjà.")
			ecrireFichier(usefulData)
		else:
			raise
	
