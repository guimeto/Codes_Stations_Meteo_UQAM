# -*-coding:Latin-1 -*
###############################################################################################################################################################
# Nom : recup()
# Auteurs : Frederick Toupin et Georges Huard pour la version perl. François-Xavier Dueymes pour la traduction en python l'adaptation en library
# Dernière modification le: 25 juillet 2017
# Description : Récupère les données du datalogger par FTP et écrit ces données dans un fichier local temporaire. Appelle de lectureDir()
###############################################################################################################################################################
from ftplib import FTP
import fnmatch
from .lireFichier import lireFichier
from .variables import path
def recup():
	#Connexion au dataLogger via FTP et récupération des données à écrire dans un fichier.csv temporaire
	ftp = FTP('XXX.XXX.XXX.XX', 'name', 'passwd')
	ftp.cwd('/USR')
	filename = 'stationData.csv'
	ftp.dir()
	localfile = open(path+filename, 'wb')
	for name in ftp.nlst():
		if fnmatch.fnmatch(name,'UQAM*'):
			ftp.retrbinary('RETR '+name, localfile.write)
	ftp.quit()
	localfile.close()
	lireFichier(filename)
