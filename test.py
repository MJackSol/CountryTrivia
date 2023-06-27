import requests
import pandas as pd 
import sqlalchemy as db 

#--ask user to select a country--
name = input("Choose a country to be quizzed on: ")
name.lower()
name.strip()

#--retrieve data for selected country--
response = requests.get(f'https://restcountries.com/v3.1/name/{name}?fields=capital,currencies,region')
response_data = response.json() 
print(response_data)

if 'status' not in response_data:
    country = response_data[0]
    currency = country["currencies"]
    for key in currency:
        if 'name' in currency[key]:
            currency = currency[key]['name']
    capital = country["capital"][0]
    region = country["region"]

    #print(f"Currency: {currency}")
    #print(f"Capital: {capital}")
    #print(f"Region: {region}")

#--put data into a database--
    country_data = pd.DataFrame.from_dict({"currency":[currency],"capital":[capital],"region":[region]})
    engine = db.create_engine('sqlite:///country_db.db')
    country_data.to_sql('country_info', con=engine, if_exists='replace', index=False)

    with engine.connect() as connection:
        query_result = connection.execute(db.text("SELECT * FROM country_info;")).fetchall()
        print(pd.DataFrame(query_result))
   
#note: use the format below to grab data from the database
#with engine.connect() as connection:
#   query_result = connection.execute(db.text("SELECT <data> FROM country_info;")).fetchall()
#   (query_result[0][0] <-- this is the data)