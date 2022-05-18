import pandas as pd 
import psycopg2 as psy
import getpass
import matplotlib.pyplot as plt

data = pd.read_csv(r'amazon.csv',usecols=["uniq_id","product_name","manufacturer","price","number_available_in_stock","number_of_reviews","number_of_answered_questions","average_review_rating","amazon_category_and_sub_category","description","product_information","product_description","items_customers_buy_after_viewing_this_item","customer_questions_and_answers"] ,low_memory=False)
df = pd.DataFrame(data)
df2 = df.drop_duplicates().copy()

print(df2)

co=None
try:
    # Connexion à la base
    co=psy.connect(host='berlin',
        database ='dbsaeabblr',
        user='rearnal',
        password ='haha')



# Modif table :
varible=df["number_available_in_stock"].str.split(' ')
df['number_available_in_stock']=variable.str.get(0)

    curs=co.cursor()
    curs.execute('''DROP TABLE IF EXISTS amazon ;''')
    curs.execute('''DROP TABLE IF EXISTS detail ;''')
    curs.execute('''CREATE TABLE amazon (
                uniq_id char(32),
                product_name varchar(5000) ,
                manufacturer varchar(100),
                -- price numeric(5,2),  ENELVER LE SIGNE £
                number_available_in_stock numeric, -- ENLEVER LE "new" dans chacunes des lignes
                number_of_reviews varchar(100),
                number_of_answered_questions varchar(100),
                -- average_review_rating numeric(2,1) ENLEVER LES CARACTERES,
                amazon_category_and_sub_category varchar(500)
                -- ENELEVER COLONNE 10 DESCRIPTION
                -- product_information A FAIRE UNE TABLE AVEC
                -- product_description
                );''')
    curs.execute('''CREATE TABLE detail (
                    -- id char(), A CREER
                    weight numeric(5,2),
                    height numeric(5,2),
                    depth numeric(5,2),
                    assembly bool,
                    battery_included bool,
                    battery_needed bool,
                    recommended_age numeric(3),
                    langage varchar(30)
                );''')                

    for row in df2.itertuples():
        curs. execute ('''INSERT INTO amazon VALUES (%s ,%s ,%s ,%s,%s,%s ,%s );''',
            (row.uniq_id , row.product_name , row.manufacturer , row.number_of_reviews,row.number_available_in_stock , row.number_of_answered_questions ,row.amazon_category_and_sub_category))


#Fermeture    
    co.commit()
    curs.close()
except (Exception , psy.DatabaseError) as error:
    print(error)

finally:
    if co is not None:
        co.close()

