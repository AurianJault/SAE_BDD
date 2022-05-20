import pandas as pd 
import psycopg2 as psy
import getpass
import matplotlib.pyplot as plt
import numpy as np

co=None
try:
    # Connexion à la base
    co=psy.connect(host='berlin',
        database ='dbsaeabblr',
        user='rearnal',
        password ='haha')

    curs=co.cursor()


    #nb de produit différents vendus par manufact

    nbP= pd.read_sql('''
    SELECT count(uniq_id) as p, avg(average_review_rating) rat, manufacturer
    FROM amazon
    WHERE average_review_rating !='NaN'
    GROUP BY manufacturer
    ORDER BY count(uniq_id) desc, avg(average_review_rating) desc;
    ''',con=co)
    
    # print(nbP)
    # dataSet=nbP
    # fig0, f1= plt.subplots() #Generation du graphique
    # x=nbP.manufacturer
    # y=nbP.p
    # f1.bar(x,y,label='Nb produits')
    # f1.set_xlim(0,10)
    # f1.set_ylabel('Number of products')
    # f1.set_xlabel('Manufacturer')
    # f=f1.twinx()
    # x=nbP.manufacturer
    # y=nbP.rat
    # f.plot(x,y, color='red')
    # f.set_ylabel('Rating /5')
    # f.set_title('Number of different products by manufacter with the average rating for each manufacturer')
    # plt.show() #Affichage    



    #NAZE
    #nb prod dispo par manufacturer
    okkkk= pd.read_sql('''
    SELECT sum(number_available_in_stock) as produits, avg(average_review_rating) rat, manufacturer
    FROM amazon
    GROUP BY manufacturer
    ORDER BY avg(average_review_rating) desc;
    ''',con=co)
    # print(okkkk)
    # fig1 = okkkk.plot(x='manufacturer',y=[ 'produits', 'rat'], style =['o-','x--']) #Generation du graphique
    # fig1. set_ylim (0,50)
    # plt.show () #Affichage




    #Nb review by category
    reviewCategori= pd.read_sql('''
    SELECT count(number_of_reviews) as rev , amazon_category_and_sub_category
    FROM amazon
    WHERE amazon_category_and_sub_category !='NaN'
    GROUP BY amazon_category_and_sub_category
    ORDER BY count(number_of_reviews) desc;

    ''',con=co)
    # print(reviewCategori)
    # fig2 = reviewCategori.plot(x='amazon_category_and_sub_category', y='rev', kind='bar') #Generation du graphique
    # fig2.set_xlim(0,10)
    # plt.show () #Affichage




    #Avg Price by category trié par rating
    priceCat=pd.read_sql('''
    SELECT avg(price) avrg, amazon_category_and_sub_category, avg(average_review_rating) avg
    FROM amazon
    WHERE price !='NaN'
    GROUP BY amazon_category_and_sub_category
        HAVING avg(average_review_rating) !='NaN'

    ORDER BY avg(average_review_rating) desc;
    ''',con=co)
    # print(priceCat)
    # fig3 = priceCat.plot(x='amazon_category_and_sub_category', y='avrg', kind='bar') #Generation du graphique
    # fig3.set_xlim(142,160)
    # plt.show () #Affichage


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

    releaseDate=pd.read_sql('''
    SELECT EXTRACT(YEAR FROM launch_date) dy, EXTRACT(MONTH FROM launch_date) dm, count(launch_date) count
    from detail
    where launch_date is not null
    group by EXTRACT(YEAR FROM launch_date), EXTRACT(MONTH FROM launch_date)
    having EXTRACT(YEAR from launch_date) = '2015'
    order by EXTRACT(YEAR FROM launch_date) asc,  EXTRACT(MONTH FROM launch_date) asc;
    ''',con=co)

    # dateCurve2015 = releaseDate.plot(x='dm', y='count')
    # plt.title("Product release evolution in 2015")
    # plt.show()

    productInfo=pd.read_sql('''
    SELECT ROUND(avg(a.average_review_rating),2) as "note where info BAD", (SELECT ROUND(avg(a.average_review_rating),2) as "note where info GOOD"
    FROM detail d, amazon a
    WHERE d.weight!='NaN' and d.dimension!='NaN' and d.recommended_age!='NaN' and d.uniq_id=a.uniq_id and a.average_review_rating!='NaN')
    FROM detail d, amazon a
    WHERE d.weight='NaN' and d.dimension='NaN' and d.assembly='NaN' and d.recommended_age='NaN' and d.uniq_id=a.uniq_id;
    ''',con=co)

    # x=["info non renseigné","info renseigné"]
    # y=[productInfo['note where info BAD'][0],productInfo['note where info GOOD'][0]]
    # plt.title("Moyenne des note en fonction des informations renseignée")
    # plt.bar(x, y)
    # plt.show()



#Fermeture    
    #co.commit()
    curs.close()
except (Exception , psy.DatabaseError) as error:
    print(error)
finally:
    if co is not None:
        co.close()
