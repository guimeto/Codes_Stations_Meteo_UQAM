#!/usr/bin/python
import pandas as pd
import datetime
from datetime import datetime,  timedelta
import matplotlib 
matplotlib.use('Agg')  # necessaire pour generer une image en backend / crontab 

import matplotlib.pyplot as plt
import numpy as np
import os 
import sys


fichierIn = open("/stationuqam/disdrometre/Parsivel_UQAM.dat","r") 
Dbins=[0.062,0.187,0.312,0.437,0.562,0.687,0.812,0.937,1.062,1.187,1.375,1.625,1.875,2.125,2.375,2.750,3.25,3.75,4.25,4.75,5.5,6.5,7.5,8.5,9.5,11,13,15,17,19,21.5,24]     
vTbins=[0.05,0.15,0.25,0.35,0.45,0.55,0.65,0.75,0.85,0.95,1.10,1.30,1.5,1.7,1.9,2.2,2.6,3,3.4,3.8,4.4,5.2,6,6.8,7.6,8.8,10.4,12,13.6,15.2,17.6,20.80]

dgrid=np.zeros(len(Dbins))
vgrid=np.zeros(len(vTbins))

dgrid[0] = 0+ Dbins[0]/2.
vgrid[0] = 0+ vTbins[0]/2.
for i in range(0,len(Dbins)):
    if i<(len(Dbins)-1):
        dgrid[i+1]=Dbins[i]+(Dbins[i+1]-Dbins[i])/2.
        vgrid[i+1]=vTbins[i]+(vTbins[i+1]-vTbins[i])/2.
        
#dgrid = np.tile(dgrid, (32, 1))
#vgrid = np.tile(vgrid, (32, 1))
dgrid,vgrid = np.meshgrid(dgrid,vgrid)
        
appended_data = []
mat = []
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
        date_time_obj = datetime.strptime(date_time_str, '%d-%m-%Y %H:%M:%S')
        
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
        
        # fin de la boucle sur les pas de temps de 10 secondes
mat =  pd.concat(mat) 
appended_data = pd.concat(appended_data)   
appended_data=appended_data.apply(pd.to_numeric, errors='ignore') 
#appended_data=appended_data.convert_objects(convert_numeric=True)
appended_data = appended_data.iloc[:, :-1]
appended_data.index = pd.to_datetime(appended_data.index, dayfirst=True)
mat.index= pd.to_datetime(mat.index, dayfirst=True)


start=datetime.utcnow().replace(second=0, microsecond=0)
end=(start-timedelta(minutes=10)).replace(second=0, microsecond=0)

# filtre des donnees sur une periode specifique
filtred_data = appended_data[(appended_data.index.get_level_values(0) >= str(end)) & (appended_data.index.get_level_values(0) <= str(start))]
filtred_mat = mat[(mat.index.get_level_values(0) >= str(end)) & (mat.index.get_level_values(0) <= str(start))]
# calcul du centre de masse suivant Ishizaka ()
Dmoy = []
Vmoy = []
for i in range(0, len(filtred_data)):
    tt=filtred_data.iloc[i].replace(0, np.nan)
    a =  pd.to_numeric(tt).values.reshape(32,32) 
 #   a = tt.convert_objects(convert_numeric=True).values.reshape(32,32)
 #   a = np.ma.masked_where(np.isnan(a),a)
    if filtred_mat['nb_particules'][i] == 0.0:
        Vmoy.append(np.nan)
        Dmoy.append(np.nan)
    else: 
        D = np.nansum((np.multiply(a, dgrid)))
        V = np.nansum((np.multiply(a, vgrid)))
        Dmoy.append(D/filtred_mat['nb_particules'][i])
        Vmoy.append(V/filtred_mat['nb_particules'][i])
Vmoy = np.nanmean(Vmoy)
Dmoy = np.nanmean(Dmoy)

# 1) water droplet    
def vrain(x):
    return 3.78*(x**0.67)    
def frain(x):
    return (0.52*3.78)*x**(3.0+0.67)
# 2) lump graupel        
def vlumpg(x):
    return 1.3*x**0.66    
def flumpg(x):
    return (0.078*1.3)*x**(2.8+0.66)

dfit = np.arange(0,23,0.1)

resample_data = filtred_data.sum(axis = 0)  #somme des particules au 10 minutes 
resample_data = resample_data.replace(0, np.nan)

b =  pd.to_numeric(resample_data).values.reshape(32,32) 

#b = resample_data.convert_objects(convert_numeric=True).values.reshape(32,32)
#b = np.ma.masked_where(np.isnan(b),b)
b = np.ma.masked_where(pd.isnull(b),b)
#b =  pd.to_numeric(resample_data).values.reshape(32,32)

fig, ax = plt.subplots(1,1)
X,Y = np.meshgrid(Dbins,vTbins)
pc = ax.pcolormesh(X,Y,b, alpha=0.5, cmap="winter")
fig.colorbar(pc, orientation="horizontal", fraction=0.046, pad=0.04)
ax.scatter(x=Dmoy,y=Vmoy, s=200, marker='+', color="red" )
ax.set_xlim(0,10)
ax.set_ylim(0,10)
plt.plot(dfit,vrain(dfit),'g',label=u"pluie")
plt.plot(dfit,vlumpg(dfit),'r',label=u"neige roule irr.")
for vT in vTbins:
    plt.axhline(y=vT, xmin=0., xmax=18, linewidth=0.2, color = 'k')

for D in Dbins:
    plt.axvline(x=D, ymin=0.0, ymax = 10, linewidth=0.2, color='k')
    
plt.axis((0,Dbins[31],0,vTbins[31]))
plt.xlabel('Diametres des particules (mm)')
plt.ylabel('Vitesse de chute des particules (m/s)')
plt.legend(loc= 'upper left')

# save_path = os.path.dirname(os.path.realpath(__file__))+'/data/parsivel2.png'
# plt.savefig(save_path)


fig1 = plt.gcf()
fig1.suptitle('Parsivel observation: ' + datetime.now().replace(second=0,microsecond=0).isoformat(' '), size=20)
fig1.subplots_adjust(top=0.90)   
fig1.set_size_inches(15.5, 8.5)         
fig1.savefig(('/NFS2_RESCUE2/stationuqam/programmes/preparation_donnees_station/data/parsivel.png'), dpi=300, bbox_inches='tight')


