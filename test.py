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

    releaseDate2015=pd.read_sql('''
    SELECT EXTRACT(YEAR FROM launch_date) dy, EXTRACT(MONTH FROM launch_date) dm, count(launch_date) count
    from detail
    where launch_date is not null
    group by EXTRACT(YEAR FROM launch_date), EXTRACT(MONTH FROM launch_date)
    having EXTRACT(YEAR from launch_date) = '2015'
    order by EXTRACT(YEAR FROM launch_date) asc,  EXTRACT(MONTH FROM launch_date) asc;
    ''',con=co)

    x2015=releaseDate2015['dm']
    y2015=releaseDate2015['count']

    releaseDate2014=pd.read_sql('''
    SELECT EXTRACT(YEAR FROM launch_date) dy, EXTRACT(MONTH FROM launch_date) dm, count(launch_date) count
    from detail
    where launch_date is not null
    group by EXTRACT(YEAR FROM launch_date), EXTRACT(MONTH FROM launch_date)
    having EXTRACT(YEAR from launch_date) = '2014'
    order by EXTRACT(YEAR FROM launch_date) asc,  EXTRACT(MONTH FROM launch_date) asc;
    ''',con=co)

    x2014=releaseDate2014['dm']
    y2014=releaseDate2014['count']

    releaseDate2013=pd.read_sql('''
    SELECT EXTRACT(YEAR FROM launch_date) dy, EXTRACT(MONTH FROM launch_date) dm, count(launch_date) count
    from detail
    where launch_date is not null
    group by EXTRACT(YEAR FROM launch_date), EXTRACT(MONTH FROM launch_date)
    having EXTRACT(YEAR from launch_date) = '2013'
    order by EXTRACT(YEAR FROM launch_date) asc,  EXTRACT(MONTH FROM launch_date) asc;
    ''',con=co)

    x2013=releaseDate2013['dm']
    y2013=releaseDate2013['count']

    releaseDate2012=pd.read_sql('''
    SELECT EXTRACT(YEAR FROM launch_date) dy, EXTRACT(MONTH FROM launch_date) dm, count(launch_date) count
    from detail
    where launch_date is not null
    group by EXTRACT(YEAR FROM launch_date), EXTRACT(MONTH FROM launch_date)
    having EXTRACT(YEAR from launch_date) = '2012'
    order by EXTRACT(YEAR FROM launch_date) asc,  EXTRACT(MONTH FROM launch_date) asc;
    ''',con=co)

    x2012=releaseDate2012['dm']
    y2012=releaseDate2012['count']

    plt.plot(x2015, y2015, 'r', x2014, y2014, 'g', x2013, y2013, 'b', x2012, y2012, 'y')
    plt.title("Evoluion of products releases in 2015")
    plt.xlabel("Months")
    plt.ylabel("Number of products released")
    plt.show()

#Fermeture    
    #co.commit()
    curs.close()
except (Exception , psy.DatabaseError) as error:
    print(error)
finally:
    if co is not None:
        co.close()