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
    SELECT sum(number_available_in_stock) as produits, manufacturer
    FROM amazon
    GROUP BY manufacturer
    ''',con=co)
#   print(okkkk)
    # fig1 = okkkk.plot(x='manufacturer', y='produits',kind='bar', legend=False) #Generation du graphique
    # plt.show () #Affichage




    #Nb review by category
    reviewCategori= pd.read_sql('''
    SELECT count(number_of_reviews) as rev , amazon_category_and_sub_category
    FROM amazon
    GROUP BY amazon_category_and_sub_category
    ORDER BY count(number_of_reviews) desc;

    ''',con=co)
    # print(reviewCategori)
    # fig2 = reviewCategori.plot(x='amazon_category_and_sub_category', y='rev', kind='bar') #Generation du graphique
    # fig2.set_xlim(0,10)
    # plt.show () #Affichage




    #Avg Price by category 
    priceCat=pd.read_sql('''
    SELECT avg(price) avrg, amazon_category_and_sub_category
    FROM amazon
    GROUP BY amazon_category_and_sub_category
    ORDER BY max(price) desc;
    ''',con=co)
    print(priceCat)
    fig3 = priceCat.plot(x='amazon_category_and_sub_category', y='avrg', kind='bar') #Generation du graphique
    plt.show () #Affichage


    #Avg Price by category 
    ratCat=pd.read_sql('''
    SELECT avg(average_review_rating) rat, amazon_category_and_sub_category
    FROM amazon
    GROUP BY amazon_category_and_sub_category
    --WHERE amazon_category_and_sub_category in ()
    ''',con=co)
    # print(ratCat)
    # fig3 = ratCat.plot(x='amazon_category_and_sub_category', y='rat', kind='bar') #Generation du graphique
    # fig3.set_xlim(0,10)
    # plt.show () #Affichage




#Fermeture    
    #co.commit()
    curs.close()
except (Exception , psy.DatabaseError) as error:
    print(error)
finally:
    if co is not None:
        co.close()
