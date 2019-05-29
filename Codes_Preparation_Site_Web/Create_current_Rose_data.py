import numpy as np
import mysql.connector
import datetime
import itertools
import pandas as pd
import warnings
warnings.filterwarnings("ignore")

###################
# Guillaume Dueymes: version du 31  Octobre  2018  
# 
##################

#ouverture de la connexion du serveur sql
cnx = mysql.connector.connect(host = 'XXX.XXX.XXX.XX', database = 'BD_labostation__enquete', user = 'station', password = 'passwd')

now = datetime.datetime.now()
year = now.year
month = now.month

station='Station_UQAM'

query5 = ("select directionVent from ReleveMeteo where date  between %s and %s")
query6 = ("select vitesseVent from ReleveMeteo where date  between %s and %s")

def map_bin(x, bins):
    kwargs = {}
    if x == max(bins):
        kwargs['right'] = True
    bin = bins[np.digitize([x], bins, **kwargs)[0]]
    bin_lower = bins[np.digitize([x], bins, **kwargs)[0]-1]
    return '[{0}-{1}]'.format(bin_lower, bin)

        
start_local=datetime.datetime(year,month,1)
day_end = pd.date_range('{}-{}'.format(year, month), periods=1, freq='M').day.tolist()[0]
end_local = datetime.datetime(year,month,day_end,23,50,00)

#nombre d heures COMPLETES passees depuis le debut du mois * nombre d intervalles de 10 minutes dans 1 heure
nb_hours=int(((((end_local-start_local).total_seconds())/3600)+1)*6)  
mean_dir=np.zeros(nb_hours,"float")
mean_dir[:] = np.NAN
mean_mod=np.zeros(nb_hours,"float")
mean_mod[:] = np.NAN

#####  DEBUT DE LA BOUCLE aux 10 minutes  
start=start_local
i=0
while start <= end_local :
    next_step = start + datetime.timedelta(minutes=10)
#    print(start,' to ',next_step,' step:', i)
    
    cursor = cnx.cursor ()
    cursor.execute (query5,(start,next_step))
    dirwind = cursor.fetchall()    
    cursor.close () 
    cursor = cnx.cursor ()
    cursor.execute (query6,(start,next_step))
    mod = cursor.fetchall()    
    cursor.close ()
    ws=list(itertools.chain.from_iterable(mod))
    wd=list(itertools.chain.from_iterable(dirwind))
    mean_dir[i]=np.mean(wd)
    mean_mod[i]=np.mean(ws)*3.6
    start = next_step
    i=i+1

df = [mean_mod,mean_dir]
spd_bins = [-1, 0, 2, 4, 6, 8, 10, 15, np.inf]
list_spd = ['[0-2]','[2-4]','[4-6]','[6-8]','[8-10]','[10-inf]']


freq_bins = np.arange(0, 382.5, 22.5)
list_dir=['[0.0-22.5]','[22.5-45.0]','[45.0-67.5]','[67.5-90.0]','[90.0-112.5]','[112.5-135.0]','[135.0-157.5]','[157.5-180.0]',
  '[180.0-202.5]','[202.5-225.0]','[225.0-247.5]','[247.5-270.0]','[270.0-292.5]','[292.5-315.0]','[315.0-337.5]','[337.5-360.0]']


data = pd.DataFrame({'Wind Speed 1': df[0],
             'Wind Dir 1': df[1]   } )
data = data.dropna()


data['Binned'] = data['Wind Dir 1'].apply(map_bin, bins=freq_bins)
grouped = data.groupby('Binned')

MAT=[]

for wdir in list_dir:
    col = []
    if wdir in set(data['Binned']): 
       tmp = grouped.get_group(wdir) 
       tmp['Binned2'] = tmp['Wind Speed 1'].apply(map_bin, bins=spd_bins)
       for spd in list_spd: 
           if spd in set( tmp['Binned2']):
               a=((tmp.groupby('Binned2').get_group(spd).count()[0])/float(nb_hours))*100
               col.append(round(a,2))

           else: 
               col.append(0)
    else:
        col = np.zeros(5)
    MAT.append(list(col))

index=['N','NNE','NE','ENE','E','ESE','SE','SSE','S','SSW','SW','WSW','W','WNW','NW','NNW']
dfin = pd.DataFrame(MAT, index=index, columns=list_spd)
dfin.to_csv('/NFS2_RESCUE2/stationuqam/programmes/preparation_donnees_station/data/wind_rose_data'+str(year)+'-'+"{:02d}".format(month)+'.csv', sep=',')
