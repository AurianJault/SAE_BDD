import pandas as pd 
import psycopg2 as psy
import getpass
import matplotlib.pyplot as plt

data = pd.read_csv(r'src/amazon.csv',usecols=["uniq_id","product_name","manufacturer","price","number_available_in_stock","number_of_reviews","number_of_answered_questions","average_review_rating","amazon_category_and_sub_category","description","product_information"] ,low_memory=False)
df = pd.DataFrame(data)
df1 = df.drop_duplicates().copy()
df2 = df1.mask(df1 == '')

#cut the number_available column to have number and new/used
var=df2['number_available_in_stock'].str.split()
df2['number_available_in_stock']=var.str.get(0)
df2['stock_status']=var.str.get(1)
print(var.str[0])
print(var.str[1])

#cut the £ sign in price column
var1a = df2['price'].str.replace('-','£').replace(' ','£')
var1 = var1a.str.split('£')
df2['price']=var1.str[1]
print(var1.str[1])

#cut tout sauf le nombre
var2 = df2['average_review_rating'].str.split(' ')
df2['average_review_rating'] = var2.str[0]
print(var2.str[0])

print(df2.loc[153,:]) 

co=None
try:
    # Connexion à la base
    co=psy.connect(host='berlin',
        database ='dbsaeabblr',
        user='rearnal',
        password ='haha')

    curs=co.cursor()
    curs.execute('''DROP TABLE IF EXISTS amazon ;''')
    curs.execute('''DROP TABLE IF EXISTS detail ;''')
    curs.execute('''CREATE TABLE amazon (
                uniq_id char(32),
                product_name varchar(5000) ,
                manufacturer varchar(100),
                price numeric(6,2),
                number_available_in_stock numeric,
                stock_status varchar(30),
                number_of_reviews numeric(4),
                number_of_answered_questions numeric(4),
                average_review_rating numeric(2,1),
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
        curs. execute ('''INSERT INTO amazon VALUES (%s ,%s ,%s ,%s ,%s ,%s ,%s ,%s ,%s ,%s);''',
            (row.uniq_id ,row.product_name ,row.manufacturer ,row.price ,row.number_available_in_stock ,row.stock_status, row.number_of_reviews, row.number_of_answered_questions ,row.average_review_rating ,row.amazon_category_and_sub_category))


#Fermeture    
    co.commit()
    curs.close()
except (Exception , psy.DatabaseError) as error:
    print(error)

finally:
    if co is not None:
        co.close()

