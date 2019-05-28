import numpy as np
import mysql.connector
import datetime
from datetime import timedelta as td
import itertools
import pandas as pd
import warnings
warnings.filterwarnings("ignore")

###################
# Guillaume Dueymes: version du 30 Mai 2018  
# Le Script extrait a toutes les heures (de l heure ecoule avant son lancement jusqu a 24heures avant)
#          - temperature 
#          - humidite relative
#          - pression: la pression est ramenee au niveau de la mer par l equation hypsometrique
#          - vent: pour le vent, a chaque heure on moyenne les 10 dernieres minutes 
#          - precipitation 
##################

#ouverture de la connexion du serveur sql
cnx = mysql.connector.connect(host = '132.208.132.40', database = 'BD_labostation__enquete', user = 'station', password = 'reli39,cao')

############## Partie a modififer 
station='Station_UQAM'

##### definition des pas de temps heure LOCALE
end_local=datetime.datetime.now()
start_local=datetime.datetime.now()- datetime.timedelta(days=1)
end_local = end_local.replace(minute=0, second=0, microsecond=0)
start_local = start_local.replace(minute=0, second=0, microsecond=0)

##### tavail en UTC pour la base de donnees
end_UTC=datetime.datetime.utcnow()
end_UTC = end_UTC.replace(minute=0, second=0, microsecond=0)                           
start_UTC=end_UTC - datetime.timedelta(days=1)
start_UTC = start_UTC.replace(minute=0, second=0, microsecond=0)

##### definition des pas de temps requetes pour chaque variable
query1 = ("select temperature from ReleveMeteo where date between %s and %s")
query2 = ("select humidite from ReleveMeteo where date between %s and %s")
query3 = ("select pression from ReleveMeteo where date between %s and %s")

query4 = ("select date from ReleveMeteo where date between %s and %s")

query5 = ("select directionVent from ReleveMeteo where date  between %s and %s")
query6 = ("select vitesseVent from ReleveMeteo where date  between %s and %s")

query7 = ("select prec1mm from ReleveMeteo where prec1mm between 0 and 5 and date between %s and %s")
query8 = ("select prec2mm from ReleveMeteo where prec2mm between 0 and 5 and date between %s and %s")
query9 = ("select prec3mm from ReleveMeteo where prec3mm between 0 and 5 and date between %s and %s")

#nombre d heures COMPLETES passees dans la journees (24)
nb_hours=int((((end_local-start_local).total_seconds())/3600)+1)


# Generate a series of corresponding hours labels
def get_delta(start_local , end_local):
    delta = end_local - start_local
    return delta

delta = get_delta(start_local,end_local)


#####   definition des champs 
temp_data=np.zeros(nb_hours,'float')
temp_data[:] = np.NAN
humi_data=np.zeros(nb_hours,"float")
humi_data[:] = np.NAN
press_data=np.zeros(nb_hours,"float")
press_data[:] = np.NAN
vect_U=np.zeros(nb_hours,"float")
vect_U[:] = np.NAN
vect_V=np.zeros(nb_hours,"float")
vect_V[:] = np.NAN
td_data=np.zeros(nb_hours,"float")
td_data[:] = np.NAN
humidex_data=np.zeros(nb_hours,"float")
humidex_data[:] = np.NAN
chill_data=np.zeros(nb_hours,"float")
chill_data[:] = np.NAN
esat_data=np.zeros(nb_hours,"float")
esat_data[:] = np.NAN
x_data=np.zeros(nb_hours,"float")
x_data[:] = np.NAN
h_data=np.zeros(nb_hours,"float")
h_data[:] = np.NAN

prec1_data=np.zeros(nb_hours,"float")
prec1_data[:] = np.NAN
prec2_data=np.zeros(nb_hours,"float")
prec2_data[:] = np.NAN
prec3_data=np.zeros(nb_hours,"float")
prec3_data[:] = np.NAN
prectot=np.zeros(nb_hours,"float")
prectot[:] = np.NAN

mean_dir=np.zeros(nb_hours,"float")
mean_dir[:] = np.NAN
mean_mod=np.zeros(nb_hours,"float")
mean_mod[:] = np.NAN

#####  DEBUT DE LA BOUCLE HORAIRE   
incr=start_UTC
i=0
while incr <= end_UTC :
#### travail sur le vent
 # # # # # # # # # on travaille sur les 10 dernieres  minutes pou le vent
 
 last = incr - datetime.timedelta(minutes=60)
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
 cursor = cnx.cursor ()
 cursor.execute (query1,(last,incr))
 data1 = cursor.fetchall()
 if len(data1) == 0:
    temp_data[i] = np.nan
 else:
    temp_data[i] = round(np.mean(data1[-1]),1)
 cursor.close ()

#### The standard Wind Chill formula for ECCC is: 

 if temp_data[i]  <=  0 and mean_mod[i] >= 5: 
    chill_data[i] = round(np.mean(13.12 + ( 0.6215 * temp_data[i] ) - (11.37 * (mean_mod[i]**0.16)) + 0.3965 * temp_data[i] * (mean_mod[i]**0.16)   ))
 elif temp_data[i]  <=  0 and mean_mod[i] < 5: 
    chill_data[i] = round(np.mean( temp_data[i] +(((-1.59 + 0.1345 * temp_data[i] )/5) * mean_mod[i] )  ))
 else:
    chill_data[i] = temp_data[i] 
    
#### travail sur l humidite
 cursor = cnx.cursor ()
 cursor.execute (query2,(last,incr))
 data2 = cursor.fetchall() 
 if len(data2) ==0 :
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
#### calcul de la pression saturante
 a=610.78
 b=17.27
 c=237.3
 esat_data[i]=(a*np.exp(b*temp_data[i]/(temp_data[i]+c)))*0.01
 h_data[i] = 0.5555*(esat_data[i]-10)
 humidex_data[i] = round(temp_data[i] + h_data[i]) 

#### travail sur la pression
 cursor = cnx.cursor ()
 cursor.execute (query3,(last,incr))
 data3 = cursor.fetchall() 
 if len(data3) == 0:
     corr_data3 = np.nan
 else:
     corr_data3=np.mean(data3[-1])*np.exp((0.08/(29.3*np.mean(data1[-1]))))    #### correction de la pression par l equation hypsometrique: station a 80m 
 press_data[i] = round(corr_data3)   
 cursor.close ()

#### #### #### #### #### #### #### #### #### 
 incr=incr + datetime.timedelta(hours=1)
 i=i+1

#####  DEBUT DE LA BOUCLE HORAIRE   
incr=start_UTC
i=0
while incr <= end_UTC :
#### travail sur la precipitation
    last = incr - datetime.timedelta(hours=1)
    cursor = cnx.cursor ()
    cursor.execute (query7,(last,incr))
    data1 = cursor.fetchall()
    prec1_data[i] = np.sum(data1[:])
    cursor.close ()

    cursor = cnx.cursor ()
    cursor.execute (query8,(last,incr))
    data2 = cursor.fetchall()
    prec2_data[i] = np.sum(data2[:])
    cursor.close ()

    cursor = cnx.cursor ()
    cursor.execute (query9,(last,incr))
    data3 = cursor.fetchall()
    prec3_data[i] = np.sum(data3[:])
    cursor.close ()  
    prectot[i]=round(((prec1_data[i]+prec2_data[i]+prec3_data[i])/3),2)
   
#### #### #### #### #### #### #### #### #### 
    incr=incr + datetime.timedelta(hours=1)
    i=i+1
#### #### #### #### #### #### #### #### #### #### #### #### #### #### #### #### #### #### #### #### #### #### #### #### #### #### #### #### #### #### #### #### #### #### #### #### 
#####  FIN DE LA BOUCLE HORAIRE #### #### #### #### #### #### #### #### #### #### #### #### #### #### #### #### #### #### #### #### #### #### #### #### #### #### #### #### ####
#### #### #### #### #### #### #### #### #### #### #### #### #### #### #### #### #### #### #### #### #### #### #### #### #### #### #### #### #### #### #### #### #### #### #### #### 

TIME=[]
for i in range(0,25,1):
    start=(start_local+td(hours=i)).strftime("%y-%m-%d_%H")
    end=(start_local+td(hours=i+1)).strftime("%y-%m-%d_%H")
    TIME.append(start)


df = pd.DataFrame({'Time': TIME, 'Precipitation': prectot,'pressure': press_data,'humidex': humidex_data, 'Rosee': td_data,'Temperature': temp_data, 'Chill': chill_data, 'Humidite': humi_data,'Dir_wind':  mean_dir,'Mod_wind':   mean_mod}, columns = ['Time','Precipitation', 'pressure', 'humidex', 'Rosee','Temperature', 'Chill', 'Humidite','Dir_wind','Mod_wind']) 
df = df.set_index('Time')   
df.to_csv('/NFS2_RESCUE2/stationuqam/programmes/preparation_donnees_station/data/UQAM_DATA_STATION.csv')

