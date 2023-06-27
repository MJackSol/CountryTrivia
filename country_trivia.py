import requests
import pandas as pd 
import sqlalchemy as db 

#--define functions--
def display_rules():
    print("==COUNTRY TRIVIA==")
    print("Input a country below to be quizzed")
    print("You will be asked a series of questions about your selected country")
    print("Answer all questions correctly to win!")

def select_country():
    #user selects country
    #if country not found ask again
    #else make database and return the country name and database 
    name = input("Choose a country to be quizzed on: ")
    name.lower().strip()

    response = requests.get(f'https://restcountries.com/v3.1/name/{name}?fields=capital,currencies,region')
    response_data = response.json() 

    while 'status' in response_data:
        name = input("Choose a country to be quizzed on: ")
        name.lower().strip()

        response = requests.get(f'https://restcountries.com/v3.1/name/{name}?fields=capital,currencies,region')
        response_data = response.json()

    country = response_data[0]
    currency = country["currencies"]
    for key in currency:
        if 'name' in currency[key]:
            currency = currency[key]['name']
    capital = country["capital"][0]
    region = country["region"]

    country_data = pd.DataFrame.from_dict({"currency":[currency],"capital":[capital],"region":[region]})
    return [name,country_data]

def quiz(database):
    engine = db.create_engine('sqlite:///country_db.db')
    database.to_sql('country_info', con=engine, if_exists='replace', index=False)

    with engine.connect() as connection:
        query_result = connection.execute(db.text("SELECT * FROM country_info;")).fetchall()
        print(pd.DataFrame(query_result))
    
    #ask three questions and count score

def game():
    #--this is where everything goes-- 
    display_rules()
    
    select_data = select_country()
    
    country_name = select_data[0]
    country_data = select_data[1]

    quiz(country_name, country_data)


#--game start stuff here--
game()

