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



    #nb prod par manufacturer
    okkkk= pd.read_sql('''
    SELECT manufacturer, count(*) as produits
    FROM amazon
    GROUP BY manufacturer;
    ''',con=co)
    #print(okkkk)
    # fig1 = okkkk.plot(x='manufacturer', y='produits', kind='bar') #Generation du graphique
    # plt.show () #Affichage




    #Nb review by category
    reviewCategori= pd.read_sql('''
    SELECT count(number_of_reviews) as rev 
    FROM amazon
    GROUP BY amazon_category_and_sub_category
    ''',con=co)
    #print(reviewCategori)
    # fig2 = reviewCategori.plot(x='amazon_category_and_sub_category', y='produits', kind='bar') #Generation du graphique
    # plt.show () #Affichage




    #Avg Price by category 
    priceCat=curs.execute('''
    SELECT max(price) maxi, avg(price) avrg, min(price) mini
    FROM amazon
    GROUP BY amazon_category_and_sub_category
    ''')
    print(priceCat)
    # fig3 = reviewCategori.plot(x='amazon_category_and_sub_category', y=['avrg', 'mini', 'maxi'],style =['o-','x--','s:']) #Generation du graphique
    # plt.show () #Affichage

#Fermeture    
    #co.commit()
    curs.close()
except (Exception , psy.DatabaseError) as error:
    print(error)
finally:
    if co is not None:
        co.close()
