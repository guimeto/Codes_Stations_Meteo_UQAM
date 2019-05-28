import numpy as np
import mysql.connector
import datetime
import itertools
import pandas as pd
import warnings
warnings.filterwarnings("ignore")

#ouverture de la connexion du serveur sql
cnx = mysql.connector.connect(host = '132.208.132.40', database = 'BD_labostation__enquete', user = 'station', password = 'reli39,cao')


############## Partie a modififer 
station='Station_UQAM'
##### tavail en UTC pour la base de donnees
end_UTC=datetime.datetime.utcnow()
end_local=datetime.datetime.now()
##### definition des pas de temps requetes pour chaque variable
query1 = ("select temperature from ReleveMeteo where date between %s and %s")
query2 = ("select humidite from ReleveMeteo where date between %s and %s")
query3 = ("select pression from ReleveMeteo where date between %s and %s")
query4 = ("select date from ReleveMeteo where date between %s and %s")
query5 = ("select directionVent from ReleveMeteo where date between %s and %s")
query6 = ("select vitesseVent from ReleveMeteo where date  between %s and %s")

query7 = ("select prec1mm from ReleveMeteo where prec1mm between 0 and 5 and date between %s and %s")
query8 = ("select prec2mm from ReleveMeteo where prec2mm between 0 and 5 and date between %s and %s")
query9 = ("select prec3mm from ReleveMeteo where prec3mm between 0 and 5 and date between %s and %s")

#####   definition des champs 
temp_data=np.zeros(1,'float')
temp_data[:] = np.NAN
humi_data=np.zeros(1,"float")
humi_data[:] = np.NAN

chill_data=np.zeros(1,"float")
chill_data[:] = np.NAN

td_data=np.zeros(1,"float")
td_data[:] = np.NAN
x_data=np.zeros(1,"float")
x_data[:] = np.NAN

press_sea=np.zeros(1,"float")
press_sea[:] = np.NAN
press_data=np.zeros(1,"float")
press_data[:] = np.NAN
vect_U=np.zeros(10,"float")
vect_U[:] = np.NAN
vect_V=np.zeros(10,"float")
vect_V[:] = np.NAN

mean_dir=np.zeros(1,"float")
mean_dir[:] = np.NAN
mean_mod=np.zeros(1,"float")
mean_mod[:] = np.NAN


prec1_data=np.zeros(3,"float")
prec1_data[:] = np.NAN
prec2_data=np.zeros(3,"float")
prec2_data[:] = np.NAN
prec3_data=np.zeros(3,"float")
prec3_data[:] = np.NAN
prectot=np.zeros(3,"float")
prectot[:] = np.NAN

#####  DEBUT DE LA BOUCLE HORAIRE   
incr=end_UTC
i=0
#### travail sur le vent
# # # # # # # # # on travaille sur les 10 dernieres  minutes pou le vent
last = incr - datetime.timedelta(minutes=10)
cursor = cnx.cursor ()
cursor.execute (query5,(last,incr))
dirwind = cursor.fetchall()    
cursor.close () 

cursor = cnx.cursor ()
cursor.execute (query6,(last,incr))
mod = cursor.fetchall()    
cursor.close ()
ws=list(itertools.chain.from_iterable(mod))
wd=list(itertools.chain.from_iterable(dirwind))
mean_dir[i]=round(np.mean(wd))
mean_mod[i]=round(np.mean(ws)*3.6)

#### travail sur la temperature
last = incr - datetime.timedelta(minutes=5)
cursor = cnx.cursor ()
cursor.execute (query1,(last,incr))
data1 = cursor.fetchall()

if len(data1) == 0: 
    data1 = np.nan
    temp_data[i] = np.nan
else:
    temp_data[i] = round(np.mean(data1[-1]),1)
cursor.close ()


#### The standard Wind Chill formula for ECCC is: 

if temp_data[0]  <=  0 and mean_mod[0] >= 5: 
    chill_data[0] = round(np.mean(13.12 + ( 0.6215 * temp_data[0] ) - (11.37 * (mean_mod[0]**0.16)) + 0.3965 * temp_data[0] * (mean_mod[0]**0.16)   ))
elif temp_data[0]  <=  0 and mean_mod[i] < 5: 
    chill_data[0] = round(np.mean( temp_data[0] +(((-1.59 + 0.1345 * temp_data[0] )/5) * mean_mod[0] )  ))
else:
    chill_data[0] = temp_data[0] 
    
#### travail sur l humidite
last = incr - datetime.timedelta(minutes=5)
cursor = cnx.cursor ()
cursor.execute (query2,(last,incr))
data2 = cursor.fetchall() 

if len(data2) == 0: 
    data2 = np.nan
    humi_data[i] = np.nan
else:
    humi_data[i] = round(np.mean(data2[-1]))  
    
cursor.close ()

#### calcul du point de Rosee
a=610.78
b=17.27
c=237.3
x_data[i]=(np.log(humi_data[i]/100))+((b*temp_data[i])/(c+temp_data[i]))
td_data[i]=round((c*x_data[i])/(b-x_data[i]),1)
 
#### travail sur la pression
last = incr - datetime.timedelta(minutes=5)
cursor = cnx.cursor ()
cursor.execute (query3,(last,incr))
data3 = cursor.fetchall()
if len(data3) == 0: 
    data3 = np.nan
    press_data[i] = np.nan
    corr_data3 = np.nan
    press_sea[i] =  np.nan 
else:
    press_data[i] = round(np.mean(data3[-1])) 
    corr_data3=np.mean(data3[-1])*np.exp((0.08/(29.3*np.mean(data1[-1]))))    #### correction de la pression par l equation hypsometrique: station a 80m 
    press_sea[i] = round(corr_data3)   
cursor.close ()

#### travail sur la precipitation sur les dernieres 24h
last = incr - datetime.timedelta(days=1)
cursor = cnx.cursor ()
cursor.execute (query7,(last,incr))
data1 = cursor.fetchall()
prec1_data[0] = np.sum(data1[:])
cursor.close ()
cursor = cnx.cursor ()
cursor.execute (query8,(last,incr))
data2 = cursor.fetchall()
prec2_data[0] = np.sum(data2[:])
cursor.close ()
cursor = cnx.cursor ()
cursor.execute (query9,(last,incr))
data3 = cursor.fetchall()
prec3_data[0] = np.sum(data3[:])
cursor.close ()  
prectot[0]=round(((prec1_data[0]+prec2_data[0]+prec3_data[0])/3),2)

#### travail sur la precipitation sur 3 jours
last = incr - datetime.timedelta(days=3)
cursor = cnx.cursor ()
cursor.execute (query7,(last,incr))
data1 = cursor.fetchall()
prec1_data[1] = np.sum(data1[:])
cursor.close ()
cursor = cnx.cursor ()
cursor.execute (query8,(last,incr))
data2 = cursor.fetchall()
prec2_data[1] = np.sum(data2[:])
cursor.close ()
cursor = cnx.cursor ()
cursor.execute (query9,(last,incr))
data3 = cursor.fetchall()
prec3_data[1] = np.sum(data3[:])
cursor.close ()  
prectot[1]=round(((prec1_data[1]+prec2_data[1]+prec3_data[1])/3),2)

#### travail sur la precipitation sur 7 jours
last = incr - datetime.timedelta(days=7)
cursor = cnx.cursor ()
cursor.execute (query7,(last,incr))
data1 = cursor.fetchall()
prec1_data[2] = np.sum(data1[:])
cursor.close ()
cursor = cnx.cursor ()
cursor.execute (query8,(last,incr))
data2 = cursor.fetchall()
prec2_data[2] = np.sum(data2[:])
cursor.close ()
cursor = cnx.cursor ()
cursor.execute (query9,(last,incr))
data3 = cursor.fetchall()
prec3_data[2] = np.sum(data3[:])
cursor.close ()  
prectot[2]=round(((prec1_data[2]+prec2_data[2]+prec3_data[2])/3),2)







Time=  end_local.strftime("%H-%M")

df = pd.DataFrame({'Temps': Time, 'pressure station': press_data,'slp': press_sea,'temperature':temp_data, 'dew point':td_data ,'chill': chill_data, 
                   'precip1':prectot[0], 'precip2':prectot[1],'precip3': prectot[2],
                   'humidite': humi_data,'dir_wind':  mean_dir,'mod_wind':  mean_mod}, columns = ['Temps','pressure station', 'slp', 'temperature',
                                                                                                  'dew point','chill','precip1','precip2','precip3','humidite','dir_wind','mod_wind'])   
df.to_csv('/NFS2_RESCUE2/stationuqam/programmes/preparation_donnees_station/data/UQAM_DATA_STATION_last.csv')

