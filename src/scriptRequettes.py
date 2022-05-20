import pandas as pd 
import psycopg2 as psy
import getpass
import matplotlib.pyplot as plt

co=None
try:
    # Connexion à la base
    co=psy.connect(host='berlin',
        database ='dbsaeabblr',
        user='rearnal',
        password ='haha')

    curs=co.cursor()
    #Cb chaque manufacturer a de produits
    curs.execute('''
    SELECT manufacturer, count(*)
    FROM amazon
    GROUP BY manufacturer
    ''')
    #Nb de manufacturer différents
    curs.execute('''
    SELECT count(*)
    FROM (SELECT distinct a.manufacturer
        FROM amazon a)p;
    ''')
    curs.execute('''
    SELECT count(*)
    FROM (SELECT distinct a.manufacturer
        FROM amazon a)p;
    ''')

    curs.execute('''
    SELECT max(a.prix) max, min(a.prix) min
    FROM amazon a
    GROUP BY a.manufacturer
    ''')
#Fermeture    
    #co.commit()
    curs.close()
except (Exception , psy.DatabaseError) as error:
    print(error)
finally:
    if co is not None:
        co.close()
