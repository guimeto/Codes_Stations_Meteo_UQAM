import pandas as pd
import datetime
import numpy as np
Dbins=[0.062,0.187,0.312,0.437,0.562,0.687,0.812,0.937,1.062,1.187,1.375,1.625,1.875,2.125,2.375,2.750,3.25,3.75,4.25,4.75,5.5,6.5,7.5,8.5,9.5,11,13,15,17,19,21.5,24]     
vTbins=[0.05,0.15,0.25,0.35,0.45,0.55,0.65,0.75,0.85,0.95,1.10,1.30,1.5,1.7,1.9,2.2,2.6,3,3.4,3.8,4.4,5.2,6,6.8,7.6,8.8,10.4,12,13.6,15.2,17.6,20.80]

dgrid=np.zeros(len(Dbins))
vgrid=np.zeros(len(Dbins))

dgrid[0] = 0+ Dbins[0]/2.
vgrid[0] = 0+ vTbins[0]/2.
for i in range(0,len(Dbins)):
    if i<(len(Dbins)-1):
        dgrid[i+1]=Dbins[i]+(Dbins[i+1]-Dbins[i])/2.
        vgrid[i+1]=vTbins[i]+(vTbins[i+1]-vTbins[i])/2.
        
d_line = np.round(dgrid,2)
v_line = np.round(vgrid,2)      
dgrid = np.tile(dgrid, (32, 1))
vgrid = np.tile(vgrid, (32, 1)).transpose()[::-1] 

today=datetime.datetime.now()
appended_data = []
mat = []
print(today)
fichier1 = open("/stationuqam/disdrometre/Parsivel_UQAM_"+str(today.year)+str(today.month)+('%02d' % today.day)+".dat","r") 
fichier2 = open("/stationuqam/disdrometre/Parsivel_UQAM.dat","r") 
 
def read_disdro(fichierIn):    
    i=0
    for ligne in  fichierIn:   
        i+=1 
        if i==1 :
            titleTab = ligne.split(";")               
        elif (i-1)%3==0 :
                continue
        elif i%3==0 :
                continue
            
        else :
            ch = ligne.split("<SPECTRUM>")
            chDesc = ch[0]
            tabDesc = chDesc.split(";") 
            tabDesc[0] = tabDesc[0].replace(".","-")                               # extraction de la date et du temps
            date_time_str = tabDesc[0] + ' ' + tabDesc[1]                          
            #date_time_obj = datetime.strptime(date_time_str, '%d-%m-%Y %H:%M:%S')
            date_time_obj = date_time_str
            nbpart = tabDesc[10]
            intensity = tabDesc[2]
            
            chSpec = ch[1]
            chSpec3 = chSpec.replace("</SPECTRUM>","")    
            if "ZERO" in chSpec3:
                
                noSpectrum = 1024*";"
                chSpec4 = chSpec3.replace("ZERO",noSpectrum)
               
                tabSpec = chSpec4.split(";")
                       
            else:
                tabSpec = chSpec3.split(";")      
            for bin,ch in enumerate(tabSpec):
               
                if ch == '':
                    tabSpec[bin]="0"
            tmp=pd.DataFrame(tabSpec).T
            tmp['Date'] = date_time_obj        
            tmp.set_index('Date', inplace=True)        
            appended_data.append(tmp)
            
            ar = np.array([[int(nbpart), float(intensity)]])
            df = pd.DataFrame(ar, columns=['nb_particules', 'Intensity'], index = [date_time_obj])
            mat.append(df)
            
read_disdro(fichier1)
read_disdro(fichier2)
            
            # fin de la boucle sur les pas de temps de 10 secondes
mat =  pd.concat(mat)         
appended_data = pd.concat(appended_data)   
#appended_data=appended_data.apply(pd.to_numeric, errors='ignore') 
appended_data=appended_data.convert_objects(convert_numeric=True)
appended_data = appended_data.iloc[:, :-1]
appended_data.index = pd.to_datetime(appended_data.index, dayfirst=True)

# filtre des donnees sur une periode specifique (ATTENTION ON TRAVAILLE EN UTC)
start=datetime.datetime.now().replace(hour=5, minute=0, second=0, microsecond=0)
end=(datetime.datetime.now()+datetime.timedelta(days=1)).replace(hour=5, minute=0, second=0, microsecond=0)

filtred_data = appended_data[(appended_data.index.get_level_values(0) >= str(start) ) & (appended_data.index.get_level_values(0) <= str(end) )]
filtred_data.index = pd.to_datetime(filtred_data.index)


agg_10m = filtred_data.groupby(pd.TimeGrouper(freq='10Min')).aggregate(np.sum)


mat = mat[(mat.index.get_level_values(0) >= str(start) ) & (mat.index.get_level_values(0) <= str(end) )]

# calcul du centre de masse suivant Ishizaka ()
sum_D = []
sum_V = []
for i in range(0, len(agg_10m)):
    tt=agg_10m.iloc[i].replace(0, np.nan)
    a = tt.astype(float).values.reshape(32,32)
    sum_V.append([np.nansum(x) for x in a])
    sum_D.append([np.nansum(x) for x in zip(*a)])

df_D = pd.DataFrame(sum_D)
df_V = pd.DataFrame(sum_V)
df_D = df_D.T
df_V = df_V.T

df_D = df_D.set_index(d_line).replace(0, np.nan)
df_V = df_V.set_index(v_line).replace(0, np.nan)
df_D = df_D.reindex(d_line[::-1])
df_V = df_V.reindex(v_line[::-1])

tempo=pd.DataFrame(pd.np.empty((32, 145 - df_D.shape[1])))
tempo.iloc[:] = np.nan
df_D = pd.concat([df_D, tempo], axis=1, join_axes=[df_D.index])
df_V = pd.concat([df_V, tempo], axis=1, join_axes=[df_V.index])

df_D.columns =  pd.date_range(start, periods=145, freq='10min')
df_V.columns = pd.date_range(start, periods=145, freq='10min')



# preparation du csv pour highchat
Vect=np.arange(32, 0, -1)
Col1 = []
Col2 = []
Col3 = []
colnum = df_D.shape[1]
print(colnum)
for k in range(colnum):
    Col1.append(df_D.iloc[:,k])
    Col2.append(Vect)
    Col3.append(np.ones(32)*k)

flattened_list1 = [y for x in Col1 for y in x]
flattened_list2 = [y for x in Col2 for y in x]
flattened_list3 = [y for x in Col3 for y in x]

jj=[]
start=datetime.datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
end=(datetime.datetime.now()+datetime.timedelta(days=1))
for i in range(0,144,1):
    incr=10*i
    jours=(start+datetime.timedelta(minutes=incr)).strftime("%Y-%m-%d %H:%M")
    for i in range(0,33,1):
        jj.append(jours)

resultD = pd.DataFrame([jj, flattened_list2, flattened_list1]).replace(np.nan,0).T
resultD.to_csv('/NFS2_RESCUE2/stationuqam/programmes/preparation_donnees/data/Timeserie_Diametre2.csv')





Col1 = []
Col2 = []
Col3 = []
colnum = df_V.shape[1]
for k in range(colnum):
    Col1.append(df_V.iloc[:,k])
    Col2.append(Vect)
    Col3.append(np.ones(32)*k)

flattened_list1 = [y for x in Col1 for y in x]
flattened_list2 = [y for x in Col2 for y in x]
flattened_list3 = [y for x in Col3 for y in x]
jj=[]
start=datetime.datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
end=(datetime.datetime.now()+datetime.timedelta(days=1))
for i in range(0,144,1):
    incr=10*i
    jours=(start+datetime.timedelta(minutes=incr)).strftime("%Y-%m-%d %H:%M")
    for i in range(0,33,1):
        jj.append(jours)
    
    
resultV = pd.DataFrame([jj, flattened_list2, flattened_list1]).replace(np.nan,0).T
resultV.to_csv('/NFS2_RESCUE2/stationuqam/programmes/preparation_donnees/data/Timeserie_Vitesse2.csv')

