import pandas as pd

data = pd.read_csv('src/amazon.csv', low_memory=False)
df = pd.DataFrame(data)

var = df['price'].str.split('£')
print(var.str[1])

print(df['uniq_id'])

df.head()
