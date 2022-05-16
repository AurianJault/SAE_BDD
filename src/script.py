import pandas as pd 
import psycopg2 as psy
import getpass
import matplotlib.pyplot as plt

data = pd.read_csv(r'amazon.csv')
df = pd.DataFrame(data)
print(df)

co=None
try:
    # Connexion à la base
    co=psy.connect(host='berlin',
        database ='dbbajacqueli',
        user='bajacqueli',
        password =getpass.getpass("Enter password"))

    curs=co.cursor()
    curs.execute('''DROP TABLE IF EXISTS amazon ;''')
    curs.execute('''CREATE TABLE amazon (
                uniq_id char(32),
                product_name varchar(300) ,
                manufacturer varchar(100),
                -- price numeric(5,2),  ENELVER LE SIGNE £
                -- number_available_in_stock varchar(100), ENLEVER LE "new" dans chacunes des lignes
                number_of_reviews numeric(3),
                number_of_answered_questions numeric(2),
                -- average_review_rating numeric(2,1) ENLEVER LES CARACTERES,
                amazon_category_and_sub_category varachar(500),
                -- ENELEVER COLONNE 10 DESCRIPTION
                -- product_information A FAIRE UNE TABLE AVEC
                -- product_description A SUPPRIMER ON LA DEUX FOIS
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
                    langage varchar(30),
                );''')                

    for row in df2.itertuples():
        curs. execute ('''INSERT INTO amazon VALUES (%s ,%s ,%s ,%s,%s ,%s );''',
            (row.uniq_id , row.product_name , row.manufacturer , row.number_of_reviews , row.number_of_answered_questions ,row.amazon_category_and_sub_category))


#Fermeture    
    co.commit()
    curs.close()
except (Exception , psy.DatabaseError) as error:
    print(error)

finally:
    if co is not None:
        co.close()

