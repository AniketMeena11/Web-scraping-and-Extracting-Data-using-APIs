# web Scraping and Extracting Data Using APIs

import requests
import sqlite3
import pandas as pd
from bs4 import BeautifulSoup

url = 'https://www.boxofficemojo.com/chart/top_lifetime_gross/?area=XWW'
db_name = 'Movies.db'
table_name = 'Top_50'
csv_path = 'C:/Users/HP/Desktop/Data Engineering/Webscraping/top_50_films.csv'
df = pd.DataFrame(columns=["Rank","Title","Life time Gross","Year"])
count = 0

html_page = requests.get(url).text
data = BeautifulSoup(html_page, 'html.parser')

table = data.find_all('table')
rows = table[0].find_all('tr')
for row in rows:
    if count<50:
        col = row.find_all('td')
        if len(col)!=0:
            data_dict = {"Rank": col[0].contents[0],
                         "Title": col[1].contents[0],
                         "Life time Gross": col[2].contents[0],
                         "Year":col[3].contents[0]}
            df1 = pd.DataFrame(data_dict, index=[0])
            df = pd.concat([df,df1], ignore_index=True)
            count+=1
    else:
        break

print(df)

df.to_csv(csv_path)

conn = sqlite3.connect(db_name)
df.to_sql(table_name, conn, if_exists='replace', index=False)
conn.close()