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


    #Number of different products by a manufacturer

    nbP= pd.read_sql('''
    SELECT count(uniq_id) as p, avg(average_review_rating) rat, manufacturer
    FROM amazon
    WHERE average_review_rating !='NaN'
    GROUP BY manufacturer
    ORDER BY count(uniq_id) desc, avg(average_review_rating) desc;
    ''',con=co)
    # 
    print(nbP)
    dataSet=nbP
    fig0, f1= plt.subplots() #Generation du graphique
    x=nbP.manufacturer
    y=nbP.p
    f1.bar(x,y,label='Nb produits')
    f1.set_xlim(0,10)
    f1.set_ylabel('Number of products')
    f1.set_xlabel('Manufacturer')
    f=f1.twinx()
    x=nbP.manufacturer
    y=nbP.rat
    f.plot(x,y, color='red')
    f.set_ylabel('Rating /5')
    f.set_title('TOP 10 - Number of different products by manufacter with the average rating for each manufacturer')
    plt.show() #Affichage

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

    #Number of review by category 
    reviewCategori= pd.read_sql('''
    SELECT count(number_of_reviews) as reviews , amazon_category_and_sub_category
    FROM amazon
    WHERE amazon_category_and_sub_category !='NaN'
    GROUP BY amazon_category_and_sub_category
    ORDER BY count(number_of_reviews) desc;
    ''',con=co)

    print(reviewCategori)
    fig2 = reviewCategori.plot(x='amazon_category_and_sub_category', y='reviews', kind='bar') #Generation du graphique
    fig2.set_xlim(0,10)
    fig2.set_ylabel('Number of review')
    fig2.set_xlabel('Category')
    fig2.set_title('TOP 10 - Number of review by category ')
    plt.show () #Affichage

    #Avg Price by category sort by rates
    priceCat=pd.read_sql('''
    SELECT avg(price) avrg, amazon_category_and_sub_category, avg(average_review_rating) avg
    FROM amazon
    WHERE price !='NaN'
    GROUP BY amazon_category_and_sub_category
        HAVING avg(average_review_rating) !='NaN'

    ORDER BY avg(average_review_rating) desc;
    ''',con=co)

    print(priceCat)
    fig3 = priceCat.plot(x='amazon_category_and_sub_category', y='avrg', kind='bar') #Generation du graphique
    fig3.set_xlim(142,160)
    fig3.set_xlabel('Category')
    fig3.set_ylabel('Average price')
    fig3.set_title('TOP 10 - Price by category order by the best average rates')
    plt.show () #Affichage

    #Bof
    #Average review rating by category order by the most  
    ratCat=pd.read_sql('''
    SELECT avg(average_review_rating) rat, amazon_category_and_sub_category, avg(number_of_reviews)
    FROM amazon
    GROUP BY amazon_category_and_sub_category
    HAVING avg(average_review_rating)!='NaN'
    ORDER BY avg(number_of_reviews) desc
    ''',con=co)

    print(ratCat)
    fig4 = ratCat.plot(x='amazon_category_and_sub_category', y='rat', kind='bar') #Generation du graphique
    fig4.set_xlim(0,30)
    fig4.set_title('Average review rating by category order by the most reviewed categories')
    fig4.set_ylabel('Average review rating')
    fig4.set_xlabel('Category')
    plt.show () #Affichage

    releaseDate=pd.read_sql('''
    SELECT EXTRACT(YEAR FROM launch_date) dy, EXTRACT(MONTH FROM launch_date) dm, count(launch_date) count
    from detail
    where launch_date is not null
    group by EXTRACT(YEAR FROM launch_date), EXTRACT(MONTH FROM launch_date)
    having EXTRACT(YEAR from launch_date) = '2015'
    order by EXTRACT(YEAR FROM launch_date) asc,  EXTRACT(MONTH FROM launch_date) asc;
    ''',con=co)

    dateCurve2015 = releaseDate.plot(x='dm', y='count')
    plt.title("Product release evolution in 2015")
    plt.show()

    productInfo=pd.read_sql('''
    SELECT ROUND(avg(a.average_review_rating),2) as "note where info BAD", (SELECT ROUND(avg(a.average_review_rating),2) as "note where info GOOD"
    FROM detail d, amazon a
    WHERE d.weight!='NaN' and d.dimension!='NaN' and d.recommended_age!='NaN' and d.uniq_id=a.uniq_id and a.average_review_rating!='NaN')
    FROM detail d, amazon a
    WHERE d.weight='NaN' and d.dimension='NaN' and d.assembly='NaN' and d.recommended_age='NaN' and d.uniq_id=a.uniq_id;
    ''',con=co)

    x=["info non renseigné","info renseigné"]
    y=[productInfo['note where info BAD'][0],productInfo['note where info GOOD'][0]]
    plt.title("Moyenne des note en fonction des informations renseignée")
    plt.bar(x, y)
    plt.show()

    batteryRequired=pd.read_sql('''
    SELECT ROUND(AVG(a.average_review_rating),2) as "avg product note noyes", (SELECT ROUND(AVG(a.average_review_rating),2) as "avg product note nono"
    FROM detail d, amazon a
    WHERE d.battery_included = 'No' and d.battery_required = 'Yes' and a.uniq_id = d.uniq_id and a.average_review_rating!='Nan')
    FROM detail d, amazon a
    WHERE d.battery_included = 'Yes' and d.battery_required = 'Yes' and a.uniq_id = d.uniq_id and a.average_review_rating!='Nan';
    ''',con=co)

    print(batteryRequired)

    x=["battery included","battery not included"]
    y=[batteryRequired['avg product note noyes'][0],batteryRequired['avg product note nono'][0]]
    plt.title("Moyenne des note en fonction de si les batterie sont incluse")
    plt.bar(x, y)
    plt.show()

    #Most reviewed products by recommanded age
    ageB=pd.read_sql('''
    SELECT avg(a.number_of_reviews) avg, d.recommended_age age
    FROM amazon a, detail d 
    WHERE d.uniq_id=a.uniq_id
    GROUP BY d.recommended_age
    HAVING avg(number_of_reviews)!='NaN'
    ORDER BY d.recommended_age asc;
    ''',con=co)
    print(ageB)
    fig5 = ageB.plot(x='age', y='avg', kind='bar') #Generation du graphique
    fig5.set_title('Most reviewed products by recommanded age')
    fig5.set_xlabel('Age')
    fig5.set_ylabel('Review')
    plt.show () #Affichage

    #Moyenne des notes par catégorie qd produits monté ou non 
    notAss=pd.read_sql('''
    SELECT avg(a.average_review_rating) assembled, avg(a1.average_review_rating) not_assembled, a.amazon_category_and_sub_category cat
    FROM amazon a, detail d, amazon a1, detail d1
    WHERE d.uniq_id=a.uniq_id and d.assembly='Yes' and d1.assembly='No' and d1.uniq_id=a1.uniq_id and a.amazon_category_and_sub_category=a1.amazon_category_and_sub_category 
    GROUP BY a.amazon_category_and_sub_category
    HAVING avg(a.average_review_rating)!='NaN' and avg(a1.average_review_rating)!='NaN'
    FETCH FIRST 10 ROWS ONLY
    ''',con=co)
    print(notAss)
    fig6 = notAss.plot(x='cat', y=['assembled','not_assembled'], kind='bar') #Generation du graphique
    fig6.set_title('Average rates by category for essembly products or not')
    fig6.set_xlabel('Category')
    fig6.set_ylabel('Average review rate')
    plt.show () #Affichage

    datafr210 = pd.read_sql ('''select a.amazon_category_and_sub_category, d.recommended_age
    from amazon a, detail d
    where a.uniq_id=d.uniq_id and recommended_age<=10; ''', con=co)
    
    datafr211 = pd.read_sql ('''select avg(average_review_rating)
    FRom amazon 
    group by amazon_category_and_sub_category like 'Hobbies > Model Trains & Railway Sets > Rail Vehicles > Trains'; ''', con=co)
    
    datafr212 = pd.read_sql ('''select avg(recommended_age) as Moyenne ,max(recommended_age) as Max ,min(recommended_age) as Min
    from detail where recommended_age !='NaN' and assembly = 'Yes'; ''', con=co)

    datafr213 = pd.read_sql ('''select avg(a.average_review_rating) battery_required, avg(b.average_review_rating) battery_not_required, b.amazon_category_and_sub_category cat
    from amazon a ,detail d, amazon b, detail e
    where a.uniq_id=d.uniq_id and d.battery_required like 'Yes' and b.uniq_id=e.uniq_id and e.battery_required like 'No' and a.average_review_rating!='NaN'
    and b.average_review_rating!='NaN' and b.amazon_category_and_sub_category like 'Hobbies > Model Trains & Railway Sets > Rail Vehicles > Trains' 
    and a.amazon_category_and_sub_category like 'Hobbies > Model Trains & Railway Sets > Rail Vehicles > Trains'
    GROUP BY b.amazon_category_and_sub_category; ''', con=co)
    
    print(datafr210)
    print(datafr211)
    print(datafr212)
    
    print(datafr213)
    
    fig213=datafr213.plot(x='cat' , y=['battery_required','battery_not_required'] ,legend =False,kind='bar')
    fig213.set_title("Average of products'rates")
    fig213.set_xlabel('batterie and not')
    fig213.set_ylabel('Average')
    fig213.set_ylim(4,5)
    plt.show()

    # Calcul médian
    
    curs.execute('''
    Create OR REPLACE function listeprix(manu amazon.manufacturer%TYPE)
    returns table(price Amazon.price%TYPE) as $$
    begin
        RETURN QUERY SELECT a.price
        FROM amazon a
        WHERE a.manufacturer=manu;
    END;
$$ language plpgsql;

Create OR REPLACE function listemanu()
    returns  table(manufacturer Amazon.manufacturer%TYPE) as $$
    begin
        return query SELECT DISTINCT a.manufacturer
        FROM amazon a
        WHERE a.price!='NaN';
    END;
$$ language plpgsql;
    ''',)
    man=pd.read_sql('''
    SELECT listemanu();
    ''',con=co)
    compteur=0
    final=[]
    nom=[]
    for i in man["listemanu"]:
        liste=[]
        compteur+=1
        if compteur==11:
            break
        nom.append(i)
        string="SELECT listeprix(\'"+i+"\');"
        string=string.replace("[a-z]\'","\'\'")
        res=pd.read_sql(string,con=co)
        liste=res["listeprix"].values.tolist()
        liste.sort()
        mediane=liste[len(liste)//2]
        final.append(mediane)
    
    coucou=plt.bar(nom,final)
    plt.title("Price manufacturers' median")
    plt.xlabel("Manufacturer")
    plt.ylabel("Price median")
    plt.show()

#Fermeture    
    #co.commit()
    curs.close()
except (Exception , psy.DatabaseError) as error:
    print(error)
finally:
    if co is not None:
        co.close()
