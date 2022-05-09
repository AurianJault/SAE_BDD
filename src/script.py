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
                uniq_id varchar(150) ,
                product_name varchar(30) ,
                manufacturer numeric(4) ,
                price varchar(100),
                -- number_available_in_stock varchar(100), A FAIRE DE CHANGEMENTS
                number_of_reviews numeric,
                number_of_answered_questions numeric,
                average_review_rating numeric,
                amazon_category_and_sub_category numeric,
                description numeric,
                -- product_information A FAIRE UNE TABLE AVEC
                -- product_description A SUPPRIMER ON LA DEUX FOIS               
                );''')

    for row in df2.itertuples():
        curs. execute ('''INSERT INTO venteJeux VALUES (%s ,%s ,%s ,%s,%s ,%s ,%s ,%s,%s ,%s);''',
            (row.Name , row.Platform , row.Year , row.Genre, row.Publisher , row.NA_Sales , row.EU_Sales , row.JP_Sales,row.Other_Sales , row.Global_Sales ))
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

