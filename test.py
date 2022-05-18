import pandas as pd

data = pd.read_csv('src/amazon.csv', low_memory=False)
df = pd.DataFrame(data)

#cut the £ sign in price column
var = df['price'].str.split('£')
print(var.str[1])

#cut the number_available column to have number and new/used
var1 = df['average_review_rating'].str.split(' ')
print(var1.str[0])
