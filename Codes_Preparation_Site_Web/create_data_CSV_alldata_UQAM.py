import numpy as np
import mysql.connector
import datetime
from datetime import date
from datetime import timedelta as td
import pandas as pd
import warnings
warnings.filterwarnings("ignore")

##############
yeari=2014
monthi=2
now = datetime.datetime.now()
yearf = now.year
monthf = now.month

day_start=1
day_end = pd.date_range('{}-{}'.format(yearf, monthf), periods=1, freq='M').day.tolist()[0]

name = str(yearf)

d0 = date(2014, 2, 1)
d1 = date(yearf, monthf, day_end)
delta = d1 - d0
nb_days = delta.days+1

## calcul du nombre d heures pour passer en UTC 
test_local=datetime.datetime.now()
test_utc=datetime.datetime.utcnow()
test_local=test_local.replace(minute=0, second=0, microsecond=0)
test_utc=test_utc.replace(minute=0, second=0, microsecond=0)
delta_h=(test_utc-test_local).total_seconds()/3600  # 3600 secondes dans 1 heure

start_local=datetime.datetime(yeari,monthi,day_start)
end_local=datetime.datetime(yearf,monthf,day_end)

start_utc=start_local+td(hours=delta_h)
end_utc=end_local+td(hours=delta_h)


# open a database connection
# be sure to change the host IP address, username, password and database name to match your own
cnx = mysql.connector.connect(host = '132.208.132.40', database = 'BD_labostation__enquete', user = 'station', password = 'reli39,cao')

# prepare a cursor object using cursor() method
cursor = cnx.cursor ()
query = ("select temperature from ReleveMeteo where temperature between -50 and 45 and date between %s and %s")
query2 = ("select directionVent from ReleveMeteo where date  between %s and %s")
query3 = ("select vitesseVent from ReleveMeteo where date  between %s and %s")

query7 = ("select prec1mm from ReleveMeteo where prec1mm between 0 and 5 and date between %s and %s")
query8 = ("select prec2mm from ReleveMeteo where prec2mm between 0 and 5 and date between %s and %s")
query9 = ("select prec3mm from ReleveMeteo where prec3mm between 0 and 5 and date between %s and %s")

tmin_data=np.zeros(nb_days)
tmax_data=np.zeros(nb_days)
tmean_data=np.zeros(nb_days)
mean_dir=np.zeros(nb_days)
mean_mod=np.zeros(nb_days)

tmin_data[:] = np.NAN
tmax_data[:] = np.NAN
tmean_data[:] = np.NAN
mean_dir[:] = np.NAN
mean_mod[:] = np.NAN

prec1_data=np.zeros(nb_days,"float")
prec1_data[:] = np.NAN
prec2_data=np.zeros(nb_days,"float")
prec2_data[:] = np.NAN
prec3_data=np.zeros(nb_days,"float")
prec3_data[:] = np.NAN
prectot=np.zeros(nb_days,"float")
prectot[:] = np.NAN


incr=start_utc 
i=0
while incr <= end_utc:
  last = incr -datetime.timedelta(days=1)
#   print  incr
#   print  last
#  print i
  cursor.execute (query,(last,incr))
  if not cursor.rowcount:
#          print "No results found"
          i=i+1       
  else:
#          print "Results found"
          data = cursor.fetchall() 
          
          if len(data) == 0:
            tmin_data[i]=np.NAN
            tmax_data[i]=np.NAN
            tmean_data[i]=np.NAN
          else:
            mean = np.nanmean(data, axis=0)
            sd = np.nanstd(data, axis=0)          
            final_list = [x for x in data if (x > mean - 2 * sd)]
            final_list = [x for x in final_list if (x < mean + 2 * sd)] 
            if len(final_list) == 0:
              tmin_data[i]=np.NAN
              tmax_data[i]=np.NAN
              tmean_data[i]=np.NAN
            else:
              tmin_data[i]=round(np.min(final_list),1)
              tmax_data[i]=round(np.max(final_list),1)
              tmean_data[i]=round(np.mean(final_list),1)
  incr=incr + datetime.timedelta(days=1)
  i=i+1

incr=start_utc 
i=0
while incr <= end_utc:
  last = incr -datetime.timedelta(days=1)
#   print  incr
#   print  last

  cursor.execute (query3,(last,incr))
  data2 = cursor.fetchall()    
  mean_mod[i]=round(np.mean(data2))  

  cursor.execute (query2,(last,incr))
  data1 = cursor.fetchall()    
  mean_dir[i]=round(np.mean(data1)) 

  cursor.execute (query7,(last,incr))
  data1 = cursor.fetchall() 
  seuil = np.nanmean(data1, axis=0)*0 + 1    # on fixe un seuil a 1 mm
  final_list1 = [x for x in data1 if  (x < seuil )]
  prec1_data[i] = np.sum(final_list1[:])
  
  cursor.execute (query8,(last,incr))
  data2 = cursor.fetchall()         
  final_list2 = [x for x in data2 if  (x < seuil )]
  prec2_data[i] = np.sum(final_list2[:]) 

  cursor.execute (query9,(last,incr))
  data3 = cursor.fetchall()         
  final_list3 = [x for x in data3 if (x < seuil )]
  prec3_data[i] = np.sum(final_list3[:])
  
  prectot[i]=round(((prec1_data[i]+prec2_data[i]+prec3_data[i])/3),1)

  incr=incr + datetime.timedelta(days=1)
  i=i+1

cursor.close ()


TIME=[]
for i in range(0,nb_days,1):
    start=(start_local+td(days=i)).strftime("%y-%m-%d_%H")
    TIME.append(start)


df = pd.DataFrame({'Date': TIME, 'Temperature minimale': tmin_data, 'Temperature maximale': tmax_data, 'Temperature moyenne': tmean_data, 'Precipitation totale': prectot, 'Dir_wind':  mean_dir,'Mod_wind':   mean_mod }, columns = ['Date','Temperature minimale','Temperature maximale','Temperature moyenne','Precipitation totale', 'Dir_wind','Mod_wind']) 
df = df.set_index('Date')   
df.to_csv('/NFS2_RESCUE2/stationuqam/programmes/preparation_donnees_station/data/UQAM_DATA_STATION_'+name+'.csv')

