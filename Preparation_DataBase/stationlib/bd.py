# -*-coding:Latin-1 -*
import mysql.connector
def bd(releveMeteoQuery):
        cnx = mysql.connector.connect(host = '132.208.132.40', 
                                      database = 'BD_labostation__enquete', 
                                      user = 'station', 
                                      password = 'reli39,cao') 

#Création d'un curseur et exécution de la requête SQL passée en paramètre
	cursor = cnx.cursor ()
	cursor.execute(releveMeteoQuery)
        cnx.commit()
	cursor.close ()
        
    
