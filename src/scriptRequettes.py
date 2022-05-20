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
    fig213.set_title('Moyennes des note du produit')
    fig213.set_xlabel('batterie and not')
    fig213.set_ylabel('Moyenne ')
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
    plt.xlabel("Nom des manufacturer")
    plt.ylabel("Médiane des prix")
    plt.show()



#Fermeture    
    #co.commit()
    curs.close()
except (Exception , psy.DatabaseError) as error:
    print(error)
finally:
    if co is not None:
        co.close()
