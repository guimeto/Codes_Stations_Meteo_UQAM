# -*-coding:Latin-1 -*
###############################################################################################################################################################
# Nom : lectureDir()
# Auteurs : Frederick Toupin et Georges Huard pour la version perl. François-Xavier Dueymes pour la traduction en python l'adaptation en library
# Dernière modification le: 25 juillet 2017
# Description : Appelle lireFichier() sur chacun des fichiers temporaires présents dans le répertoire désigné
###############################################################################################################################################################
import os
from .lireFichier import lireFichier
from .variables import path

def lectureDir():
	#Parcours des fichiers tmp existants et appel de lireFichier() sur chacun d'entre eux
	for filename in os.listdir(path):
		filename= path+filename
		lireFichier(filename)
