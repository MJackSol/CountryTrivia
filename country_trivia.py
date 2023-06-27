import requests
from restcountries import RestCountryApiV2 as rapi

#--game start stuff here--

#--ask user to select a country--
name = input("Choose a country to be quizzed on: ")
name.lower()
name.strip()

#--retrieve data for selected country--
response = requests.get(f'https://restcountries.com/v3.1/name/{name}?fields=capital,currencies,lang,region')
response_data = response.json() 
print(response_data)

#--put data into a database--

