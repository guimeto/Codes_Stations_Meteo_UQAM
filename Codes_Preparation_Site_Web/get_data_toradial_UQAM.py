import numpy as np
import mysql.connector
import datetime
from datetime import date
import pandas as pd
import json
import warnings
warnings.filterwarnings("ignore")

###################
##############
####   Guillaume Dueymes
####   03/10/2018
####   Code qui prepare les donnees pour la visualisation du graphique radial pour le site de la station
####   Besoin d avoir localement les fichiers Clim_max_data_2014_2017.txt Clim_min_data_2014_2017.txt
####         max_max_data_2014_2017.txt et min_min_data_2014_2017.txt et du fichier data.txt
##############
start = datetime.date.today()
start = start.replace(month=1,day=1)

today = datetime.datetime.now()
today = today.replace(minute=0, second=0, microsecond=0).strftime('%Y-%m-%d')

year=date.today().year

# open a database connection
# be sure to change the host IP address, username, password and database name to match your own
cnx = mysql.connector.connect(host = '132.208.132.40', database = 'BD_labostation__enquete', user = 'station', password = 'reli39,cao')
# prepare a cursor object using cursor() method
cursor = cnx.cursor ()
query = ("select temperature from ReleveMeteo where temperature between -50 and 50 and date between %s and %s")

tmin_data=np.zeros(366)
tmax_data=np.zeros(366)
tmean_data=np.zeros(366)
tmin_data[:] = np.NAN
tmax_data[:] = np.NAN
tmean_data[:] = np.NAN

if year % 4 == 0 and (year % 100 != 0 or year % 400 == 0):
  next=start+ datetime.timedelta(days=1)
  i=0
  #print str(year) + " is a leap year"
  while start <= datetime.date.today()-datetime.timedelta(days=1):
 #    print  start
 #    print   next
     cursor.execute (query,(start,next))
     if not cursor.rowcount:
         
          i=i+1       
     else:        
          data = cursor.fetchall()
          mean = np.mean(data, axis=0)
          sd = np.std(data, axis=0)

          final_list = [x for x in data if (x > mean - 2 * sd)]
          final_list = [x for x in final_list if (x < mean + 2 * sd)]
          
          if len(final_list) == 0:
            tmin_data[i]=np.nan
            tmax_data[i]=np.nan
            tmean_data[i]=np.nan
          else:
            tmin_data[i]=round(np.min(final_list),1)
            tmax_data[i]=round(np.max(final_list),1)
            tmean_data[i]=round(np.mean(final_list),1)
     start=start + datetime.timedelta(days=1)
     next=next + datetime.timedelta(days=1)
     i=i+1
else:

#  print str(year) + " is NOT a leap year"
  next=start+ datetime.timedelta(days=1)
  i=0
  while start <= datetime.date.today()-datetime.timedelta(days=1):
 #    print  start
 #    print   next
     cursor.execute (query,(start,next))
     if not cursor.rowcount:
         
          i=i+1      
     else:
         
          data = cursor.fetchall() 
          
          if len(data) == 0:
            tmin_data[i]=np.nan
            tmax_data[i]=np.nan
            tmean_data[i]=np.nan
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

        
          i=i+1
     start=start + datetime.timedelta(days=1)
     next=next + datetime.timedelta(days=1)

cursor.close ()
np.savetxt('/NFS2_RESCUE2/stationuqam/programmes/preparation_donnees_station/tmin_radial_'+str(year)+'.txt', tmin_data)
np.savetxt('/NFS2_RESCUE2/stationuqam/programmes/preparation_donnees_station/tmax_radial_'+str(year)+'.txt', tmax_data)

############################
####  preparation du fichier .json
####


clim_max = pd.read_csv('/NFS2_RESCUE2/stationuqam/programmes/preparation_donnees_station/Clim_max_data_2014_2018.txt', header=None)
clim_min = pd.read_csv('/NFS2_RESCUE2/stationuqam/programmes/preparation_donnees_station/Clim_min_data_2014_2018.txt', header=None)
tmp =np.arange(366)
df = pd.DataFrame(tmp)

max_max = pd.read_csv('/NFS2_RESCUE2/stationuqam/programmes/preparation_donnees_station/Max_max_data_2014_2018.txt', header=None)
min_min = pd.read_csv('/NFS2_RESCUE2/stationuqam/programmes/preparation_donnees_station/Min_min_data_2014_2018.txt', header=None)

min_data =  pd.read_csv('/NFS2_RESCUE2/stationuqam/programmes/preparation_donnees_station/tmin_radial_'+str(year)+'.txt', header=None)
max_data =  pd.read_csv('/NFS2_RESCUE2/stationuqam/programmes/preparation_donnees_station/tmax_radial_'+str(year)+'.txt', header=None)

min_data2 = np.empty(366)
min_data2[:] = np.nan
max_data2 = np.empty(366)
max_data2[:] = np.nan

if( (year % 4) == 0):
    if ( (year % 100 ) == 0):

        if ( (year % 400) == 0):

 #           print("{0} is a leap year".format(year))
            
            for i in range(0,365):
                min_data2[i]=round(min_data.loc[i],1)
                max_data2[i]=round(max_data.loc[i],1)
        else:

 #           print("{0} is not a leap year".format(year))
            i2=0
            for i in range(0,365):
                if i==58:
                    min_data2[i]=np.nan
                    max_data2[i]=np.nan
                else:
                    min_data2[i]=round(min_data.loc[i2],1)
                    max_data2[i]=round(max_data.loc[i2],1)
                    i2=i2+1
            
    else:

 #       print("{0} is a leap year".format(year))
        for i in range(0,365):
                min_data2[i]=round(min_data.loc[i],1)
                max_data2[i]=round(max_data.loc[i],1)

else:

#    print("{0} is not a leap year".format(year))
    i2=0
    for i in range(0,365):
        if i==59:
            min_data2[i]=np.nan
            max_data2[i]=np.nan
        else:
            min_data2[i]=round(min_data.loc[i2],1)
            max_data2[i]=round(max_data.loc[i2],1)
            i2=i2+1


date = pd.read_csv('/NFS2_RESCUE2/stationuqam/programmes/preparation_donnees_station/date.txt', header=None)

dfmax = pd.DataFrame(max_data2)
dfmin = pd.DataFrame(min_data2)
min_min = min_min[0].apply(lambda x:round(x,2))
max_max = max_max[0].apply(lambda x:round(x,2))
clim_min = clim_min[0].apply(lambda x:round(x,2))
clim_max = clim_max[0].apply(lambda x:round(x,2))

frames = [df,dfmin,dfmax,min_min,max_max,clim_min,date,clim_max]
result = pd.concat(frames, axis=1)
result.columns = ['index','min', 'max','recLow','recHigh','avgLow','date','avgHigh']

result.avgHigh = result.avgHigh.astype(str)
result.avgLow = result.avgLow.astype(str)
result.recHigh = result.recHigh.astype(str)
result.recLow = result.recLow.astype(str)
result=result.fillna(0)
# df2= pd.DataFrame([df_transposed.Sites,df_transposed.lat.astype(float),df_transposed.lon.astype(float)])
# df2_transposed = df2.T 

d= [
    dict([
        (colname, row[i]) 
        for i,colname in enumerate(result.columns)
    ])
    for row in result.values
]

with open('/NFS2_RESCUE2/stationuqam/programmes/preparation_donnees_station/data/UQAM_radial.json', 'w') as outfile:
    json.dump(d, outfile, indent=2)  
    
with open('/NFS2_RESCUE2/stationuqam/programmes/preparation_donnees_station/data/UQAM_radial.json','r') as f:
  data = f.read()

data = '{"values":' + data + ', "name": "Station UQAM 2019"}'
json_data = json.loads(data)

with open('/NFS2_RESCUE2/stationuqam/programmes/preparation_donnees_station/data/UQAM_radial.json', 'w') as outfile:
    json.dump(json_data, outfile, indent=2)  
