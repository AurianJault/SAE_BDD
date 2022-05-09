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
        curs. execute ('''INSERT INTO amazon VALUES (%s ,%s ,%s ,%s,%s ,%s ,%s ,%s,%s ,%s,%s);''',
            (row.uniq_id , row.product_name , row.manufacturer , row.price, row.number_available_in_stock , row.number_of_reviews , row.number_of_answered_questions , row.average_review_rating ,row.amazon_category_and_sub_category, row.product_information, row.product_description ))
#    curs.execute('''SELECT *
#                    FROM venteJeux ;''')
#    curs.execute('''SELECT avg(Global_Sales) v
#                    FROM venteJeux
#                    WHERE Genre='Adventure'
#                    GROUP BY Year;''')
#
#    val=curs.fetchall()
#    print(val)
#    datafr = pd. read_sql ('''SELECT avg(Global_Sales) v, Year
#                    FROM venteJeux
#                    WHERE Genre='Adventure'
#                    GROUP BY Year;''', con= co )
#    fig=datafr.plot(x='year', y='v')
#    plt.show()
#    dataf = pd. read_sql ('''SELECT sum(Global_Sales) v, Year
#                    FROM venteJeux
#                    WHERE Genre='Adventure'
#                    GROUP BY Year;''', con= co )
#    fig=dataf.plot(x='year', y='v')
#    plt.show()
#    data= pd. read_sql ('''SELECT sum(Global_Sales) v, Year
#                  FROM venteJeux
#                  GROUP BY Year
#                  ORDER BY Year;''', con= co )
#    fig=data.plot(x='year', y='v')
#    plt.show()
#   co.commit()
#   curs.close()
# Partie 3
#1-

    datafr = pd. read_sql ('''SELECT sum(Eu_Sales) v, Platform
                            FROM venteJeux
                            GROUP BY Platform;''', con= co)
    fig = datafr .plot(x='platform', y='v',legend = False )
    fig. set_xlabel ('plateforme')
    fig. set_ylabel ('Vente en millions')
    fig. set_ylim (0 ,300)

    datafr = pd. read_sql ('''SELECT sum(Eu_Sales) v, Platform
                            FROM venteJeux
                            GROUP BY Platform;''', con= co)
    fig = datafr .plot(x='platform', y='v',legend = False, kind='bar')
    fig. set_xlabel ('plateforme')
    fig. set_ylabel ('Vente en millions')
    fig. set_ylim (0 ,300)
    plt.show () 

    datafr1 = pd. read_sql ('''SELECT sum(NA_Sales) n,sum(Eu_Sales) e,sum(JP_Sales) j,sum(Other_Sales) o, Platform
                            FROM venteJeux
                            GROUP BY Platform;''', con= co)
    fig = datafr1.plot(x='platform', y=[ 'n', 'e', 'j','o'],style =['o-','x--','s:','x-'],legend = False)

    datafr1 = pd. read_sql ('''SELECT sum(NA_Sales) n,sum(Eu_Sales) e,sum(JP_Sales) j,sum(Other_Sales) o, Platform
                            FROM venteJeux
                            GROUP BY Platform;''', con= co)
    fig = datafr1.plot(x='platform', y=[ 'n', 'e', 'j','o'],style =['o-','x--','s:','x-'],legend = False, kind='bar')
    plt.show () 


#4-



#Fermeture    
    co.commit()
    curs.close()
except (Exception , psy.DatabaseError) as error:
    print(error)

finally:
    if co is not None:
        co.close()

