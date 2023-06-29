import requests
import pandas as pd 
import sqlalchemy as db 
import time

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
    currencies = country["currencies"]
    for key in currencies:
        if 'name' in currencies[key]:
            currency = currencies[key]['name']
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
        #print(pd.DataFrame(query_result))
   
#note: use the format below to grab data from the database
#with engine.connect() as connection:
#   query_result = connection.execute(db.text("SELECT <data> FROM country_info;")).fetchall()
#   (query_result[0][0] <-- this is the data)

    #--quiz--
    #ask the user three questions about the selected country
    #take an input of the user's answer 
    #take the user's answer and the correct answer from the database and compare them
    #if they match, increment the number of correct answers, and print a "correct!" message
    #else, increment the number of incorrect answers, and print an "incorrect!" message and tell them the correct answer. We can also add a motivational message
    #once the user answers all the questions, print their final score and all the correct answers

    time_limit = 5  # Set the time limit to 20 seconds
     

    correct = 0
    incorrect = 0
    print("")
    capital_input=input(f"QUESTION 1: What is the capital of {name}?")
    start_time = time.time()
    
    with engine.connect() as connection:
        query_result = connection.execute(db.text("SELECT capital FROM country_info;")).fetchall()
        correct_capital = query_result[0][0]
        elapsed_time = time.time() - start_time
    # Check if the time limit has been reached
        if elapsed_time>= time_limit:
            print("Time's up!")
            print("The answer is ", correct_capital)
            
        else:
            if capital_input.lower().strip() == correct_capital.lower():
                print("Correct!")
                correct += 1
            elif capital_input.lower().strip() in correct_capital.lower():
                print("Close! The full answer was: ")
                print(correct_capital) 
                correct += 1
            else:
                print("Incorrect! The correct answer was: ")
                print(correct_capital)
                incorrect += 1
        
    currency_input=input(f"QUESTION 2: What is the currency of {name}?")
    with engine.connect() as connection:
        query_result = connection.execute(db.text("SELECT currency FROM country_info;")).fetchall()
        correct_currency = query_result[0][0]
        if currency_input.lower().strip() == correct_currency.lower():
            print("Correct!")
            correct += 1
        elif currency_input.lower().strip() in correct_currency.lower():
            print("Close! The full answer was: ")
            print(correct_currency) 
            correct += 1
        else:
            print("Incorrect! The correct answer was: ")
            print(correct_currency)
            incorrect += 1
        
    region_input=input(f"QUESTION 3: In what region is {name} located at?")
    with engine.connect() as connection:
        query_result = connection.execute(db.text("SELECT region FROM country_info;")).fetchall()
        correct_region = query_result[0][0]
        if region_input.lower().strip() == correct_region.lower():
            print("Correct!")
            correct += 1
        else:
            print("Incorrect! The correct answer was: ")
            print(correct_region)
            incorrect += 1
        
    print(f"Answered {correct} questions correctly and {incorrect} questions incorrectly")
