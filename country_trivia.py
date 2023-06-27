import requests
from restcountries import RestCountryApiV2 as rapi

#--game start stuff here--

#--ask user to select a country--
name = input("Choose a country to be quizzed on: ")
name.lower()
name.strip()

#--retrieve data for selected country--
response = requests.get(f'https://restcountries.com/v3.1/name/{name}?fields=capital,currencies,region')
response_data = response.json() 
#print(response_data)

if response.status_code==200:
    country=response_data[0]
    currency_=country["currencies"]
    for key in currency_:
        if 'name' in currency_[key]:
            currency_=currency_[key]['name']
    capital_=country["capital"][0]
    region_=country["region"]

    print(f"Currency: {currency_}")
    print(f"Capital: {capital_}")
    print(f"Region: {region_}")

#--put data into a database--

