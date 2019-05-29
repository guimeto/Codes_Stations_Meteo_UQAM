# Codes_Stations_Meteo_UQAM
Ensemble de codes travaillant sur la station météorologique de l'UQAM

<b>Preparation_DataBase :</b> Ensemble des scripts python utilisés pour préparer la base de données de la station météorologique de l’UQAM. 



<b>Codes_Preparation_Site_Web:</b> Ensemble des scripts python utilisés pour préparer les données qui seront visualisées par le site de la station


<table border="1" class="docutils">
<colgroup>
<col width="27%">
<col width="57%">
</colgroup>
<tbody valign="top">
<tr>
    <th>Script</th>
    <th>Description</th> 
    <th>Input</th>
    <th>Output</th>
 </tr>
	
<tr><td><tt class="docutils literal"><span class="pre">Create_CSV_today.py</span></tt></td>
<td> Script pour extraire les données toutes les heures de la station et alimenter le <a href="http://station.escer.uqam.ca/visualisation/meteogramme/">meteogram</a> </td>
<td> Database </td> 
<td> UQAM_DATA_STATION.csv </td> 
</tr>

<tr><td><tt class="docutils literal"><span class="pre">Create_current_Rose_data.py</span></tt></td>
<td> Script qui extrait les données de vent du mois courant pour créer la  <a href="http://station.escer.uqam.ca/visualisation/rose_des_vents/">rose des vents</a> </td>
<td> Database </td> 
<td> wind_rose_data'+str(year)+'-'+"{:02d}".format(month)+'.csv' </td> 
</tr>

<tr><td><tt class="docutils literal"><span class="pre">Create_heatmap.py</span></tt></td>
<td> Script qui extrait les données toutes les heures pour préparer le graphique <a href="http://station.escer.uqam.ca/visualisation/meteogramme2/">Heatmap</a> (évolution horaire de la température)</td>
<td> Database </td> 
<td> Heat_temp.csv </td> 
</tr>

<tr><td><tt class="docutils literal"><span class="pre">create_data_CSV_alldata_UQAM.py</span></tt></td>
<td> Script qui extrait toutes les données de température et de précipitation de la station puis en déduit les moyenne et accumulation journalières pour préparer <a href="http://station.escer.uqam.ca/visualisation/meteogramme2/">graphique</a></td>
<td> Database </td> 
<td> UQAM_DATA_STATION_'+name+'.csv' </td> 
</tr>

<tr><td><tt class="docutils literal"><span class="pre">disdro_picture.py</span></tt></td>
<td> Script pour calculer et tracer le <a href="http://station.escer.uqam.ca/visualisation/disdrometre/">diagramme de dispersion</a> des particules du parsivel OTT2.</td>
<td> OTT2 raw dataset </td> 
<td> Parsivel.png</td> 
</tr>

<tr><td><tt class="docutils literal"><span class="pre">disdro_time_serie.py</span></tt></td>
<td> Script qui calcule l’  <a href="http://station.escer.uqam.ca/visualisation/disdrometre/">évolution</a> aux 10 minutes de la vitesse de chute et de la taille des particules mesurées par le parsivel OTT2.</td>
<td> OTT2 raw dataset</td> 
<td> Timeserie_Diametre.csv et Timeserie_Vitesse.csv </td> 
</tr>

<tr><td><tt class="docutils literal"><span class="pre">disdro_time_serie.py</span></tt></td>
<td> Script qui prépare les données pour la visualisation du graphique <a href="http://station.escer.uqam.ca/visualisation/graphique_radial/">radial</a>.</td>
<td> Database, Clim_max_data_2014_2017.txt, Clim_min_data_2014_2017.txt, max_max_data_2014_2017.txt, min_min_data_2014_2017.txt.</td>  
<td> UQAM_radial.json  </td> 
</tr>

<tr><td><tt class="docutils literal"><span class="pre">last_value.py</span></tt></td>
<td> script qui extrait les dernières observations de la station pour alimenter la page d’<a href="http://station.escer.uqam.ca/">accueil</a>  du site.</td>
<td> Database</td>  
<td> UQAM_DATA_STATION_last.csv  </td> 
</tr>

</tbody>
</table>

	
	




