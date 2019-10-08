# -*- coding: utf-8 -*-
"""
Created on Thu Apr 11 13:06:25 2019

@author: guillaume
"""

import pandas as pd
from datetime import datetime


########################  OUVERTURE DU CHAMPS A LIRE  ########

rep1='D:/Utilisateurs/guillaume/Documents/GitHub/Codes_Stations_Meteo_UQAM/Preparation_DataBase/data_brute/201910/'
columns=["date","temperature", "humidite", "pression", "directionVent", "vitesseVent","pyranometre", "pyranometreUP", "pyranometreDW", "pyregeometreUP", "pyregeometreDW", "prec1mm", "prec2mm", "prec3mm", "prec1tot", "prec2tot", "prec3tot"]

dfstat = pd.read_csv(rep1+'20191004.html', sep=';',names=columns )

dfstat['date'] = pd.to_datetime(dfstat['date'], format='%Y%m%d%H%M')
dfstat['month'] = dfstat['date'].dt.month
dfstat['day'] = dfstat['date'].dt.day
dfstat['hour'] = dfstat['date'].dt.hour
dfstat['minute'] = dfstat['date'].dt.minute


 

