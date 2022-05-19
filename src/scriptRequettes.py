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
    fig = okkkk.plot(x='manufacturer', y='produits') #Generation du graphique
    plt.show () #Affichage

    #Nb review by category
    reviewCategori= pd.read_sql('''
    SELECT count(number_of_reviews) as rev
    FROM amazon
    GROUP BY amazon_category_and_sub_category
    ''',con=co)
    #print(reviewCategori)
    fig = okkkk.plot(x='amazon_category_and_sub_category', y='rev') #Generation du graphique
    plt.show () #Affichage

    
    # fig = reviewCategori.plot(x='amazon_category_and_sub_category', y='produits') #Generation du graphique
    # plt.show () #Affichage

    #print(okkkk)

    #Moyenne de produits par manufacturer
    # moyProdPMan= pd.read_sql('''

    # SELECT count(*) as produits
    # FROM amazon
    # GROUP BY manufacturer;
    # DO $$
    #     DECLARE
    #         sum_prod numeric ;
    #         nb_manu numeric ;
    #         res numeric;
    #     BEGIN
    #         SELECT count(*) INTO nb_manu
    #         FROM (SELECT distinct a.manufacturer
    #             FROM amazon a)p;
    #         SELECT count(*) INTO sum_prod
    #         FROM amazon
    #         GROUP BY manufacturer;
    #         res=sum_prod / nb_manu;
    #         RAISE NOTICE 'La moyenne de produit par manufactureur est %.', res;
    #     END ;
    # $$ ;
    # ''',con=co)
    # print(moyProdPMan)



    #Nb de manufacturer différents
    curs.execute('''
    SELECT count(*)
    FROM (SELECT distinct a.manufacturer
        FROM amazon a)p;
    ''')


#Fermeture    
    #co.commit()
    curs.close()
except (Exception , psy.DatabaseError) as error:
    print(error)
finally:
    if co is not None:
        co.close()
