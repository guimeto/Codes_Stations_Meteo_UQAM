# -*-coding:Latin-1 -*
import mysql.connector
def bd(releveMeteoQuery):
        cnx = mysql.connector.connect(host = 'XXX.XXX.XXX.XX', 
                                      database = 'database_name', 
                                      user = 'name', 
                                      password = 'password') 

#Création d'un curseur et exécution de la requête SQL passée en paramètre
	cursor = cnx.cursor ()
	cursor.execute(releveMeteoQuery)
        cnx.commit()
	cursor.close ()
        
    
