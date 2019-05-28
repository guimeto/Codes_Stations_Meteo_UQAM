import numpy as np
import mysql.connector
import datetime
from datetime import date
from datetime import timedelta as td
import pandas as pd

##############
now = datetime.datetime.now()
yearf = now.year

day_start=1
day_end = pd.date_range('{}-{}'.format(yearf, 12), periods=1, freq='M').day.tolist()[0]

name = str(yearf)

d0 = date(yearf, 1, 1)
d1 = date(yearf, 12, day_end)
delta = d1 - d0
nb_days = delta.days+1

## calcul du nombre d heures pour passer en UTC 
test_local=datetime.datetime.now()
test_utc=datetime.datetime.utcnow()
test_local=test_local.replace(minute=0, second=0, microsecond=0)
test_utc=test_utc.replace(minute=0, second=0, microsecond=0)
delta_h=(test_utc-test_local).total_seconds()/3600  # 3600 secondes dans 1 heure

start_local=datetime.datetime(yearf,1,1)
end_local=datetime.datetime(yearf,12,day_end)

start_utc=start_local+td(hours=delta_h)
end_utc=end_local+td(hours=delta_h)


# open a database connection
# be sure to change the host IP address, username, password and database name to match your own
cnx = mysql.connector.connect(host = '132.208.132.40', database = 'BD_labostation__enquete', user = 'station', password = 'reli39,cao')

# prepare a cursor object using cursor() method
cursor = cnx.cursor ()
query = ("select temperature from ReleveMeteo where temperature between -50 and 50 and date between %s and %s")
tmean_data=np.zeros(nb_days*24)
tmean_data[:] = np.NAN

incr=start_utc 
i=0
while incr <= end_utc:
  last = incr -datetime.timedelta(hours=1)
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
            tmean_data[i]=np.NAN
          else:
            tmean_data[i]=round(np.mean(data),1)
  incr=incr + datetime.timedelta(hours=1)
  i=i+1
  
jj=[]
hh=[]
for i in range(0,nb_days*24,1):
    jours=(start_local+td(hours=i)).strftime("%Y-%m-%d")
    heures=(start_local+td(hours=i)).strftime("%H")
    jj.append(jours)
    hh.append(heures)


df = pd.DataFrame({'Jour': jj, 'Heure': hh,  'Temperature moyenne': tmean_data}, columns = ['Jour','Heure','Temperature moyenne']) 
df = df.set_index('Jour')   
df.to_csv('/NFS2_RESCUE2/stationuqam/programmes/preparation_donnees_station/data/Heat_temp.csv')


