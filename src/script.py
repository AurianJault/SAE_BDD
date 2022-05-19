import pandas as pd 
import psycopg2 as psy
import getpass
import matplotlib.pyplot as plt

data = pd.read_csv(r'src/amazon.csv',usecols=["uniq_id","product_name","manufacturer","price","number_available_in_stock","number_of_reviews","number_of_answered_questions","average_review_rating","amazon_category_and_sub_category","product_information"] ,low_memory=False)
df = pd.DataFrame(data)
df1 = df.drop_duplicates().copy()
df2 = df1.mask(df1 == '')


#cut the number_available column to have number and new/used
var=df2['number_available_in_stock'].str.split()
df2['number_available_in_stock']=var.str.get(0)
df2['stock_status']=var.str.get(1)
# print(var.str[0])
# print(var.str[1])

#cut the £ sign in price column
var1a = df2['price'].str.replace('-','£').replace(' ','£')
var1 = var1a.str.split('£')
df2['price']=var1.str[1]
# print(var1.str[1])

#cut tout sauf le nombre
var2 = df2['average_review_rating'].str.split(' ')
df2['average_review_rating'] = var2.str[0]
# print(var2.str[0])

# print(df2.loc[0,:]) 

# print(df2.loc[153,:])

#--------------------------------------------------------------------------------------------------

### WEIGHT 
varPoid=df2['product_information'].str.split('Weight')
varPoid=varPoid.str.get(1)
varPoid=varPoid.str.split()
varPoid=varPoid.str.get(0)+varPoid.str.get(1)
df2['weight'] = varPoid

### DIMENSIONS
vardim=df2['product_information'].str.split('Product Dimensions')
vardim=vardim.str.get(1)
vardim=vardim.str.split()
vardim=vardim.str.get(0)+vardim.str.get(1)+vardim.str.get(2)+vardim.str.get(3)+vardim.str.get(4)+vardim.str.get(5)
df2['dimensions'] = vardim

### AGE
varage=df2['product_information'].str.split('recommended age:')
varage=varage.str.get(1)
varage=varage.str.split()
varage=varage.str.get(0)
df2['reco_age'] = varage

### BATTERY IN
varbat=df2['product_information'].str.split('Batteries Included\?')
varbat=varbat.str.get(1)
varbat=varbat.str.split()
varbat=varbat.str.get(0)
df2['battery_in'] = varPoid

### BATTERY REQUIRED
var2bat=df2['product_information'].str.split('Batteries Required\?')
var2bat=var2bat.str.get(1)
var2bat=var2bat.str.split()
var2bat=var2bat.str.get(0)
df2['battery_req'] = var2bat

### ASSEMBLY
varass=df2['product_information'].str.split('Assembly Required')
varass=varass.str.get(1)
varass=varass.str.split()
varass=varass.str.get(0)
df2['assembly'] = varass

### REMOTE CONTROL
varrem=df2['product_information'].str.split('Remote Control Included\?')
varrem=varrem.str.get(1)
varrem=varrem.str.split()
varrem=varrem.str.get(0)
df2['battery_in'] = varrem

### FIRST DATE
vardat=df2['product_information'].str.split('Date First Available')
vardat=vardat.str.get(1)
vardat=vardat.str.split()
vardat=vardat.str.get(0)+" "+vardat.str.get(1)+" "+vardat.str.get(2)
df2['available'] = vardat

#save cleaned dataframe into csv file
df2.to_csv("./amazon_clean.csv")

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
                -- product_information A FAIRE UNE TABLE AVEC
                );''')
    curs.execute('''CREATE TABLE detail (
                    -- id char(),
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