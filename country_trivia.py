import requests
import pandas as pd
import sqlalchemy as db

# --define functions--


def display_rules():
    print("")
    print("==COUNTRY TRIVIA==")
    print("")
    print("Input a country below to be quizzed")
    print("You will be asked a series of questions about the selected country")
    print("Answer all questions correctly to win!")


def get_input():
    print("")
    name = input("Choose a country to be quizzed on: ")
    name.lower().strip()
    return name


def select_country():
    # user selects country
    # if country not found ask again
    # else make database and return the country name and database
    name = get_input()

    response = requests.get(
        f'https://restcountries.com/v3.1/name/{name}?fields=capital,currencies,region')
    response_data = response.json()

    while 'status' in response_data:
        name = input("Choose a country to be quizzed on: ")
        name.lower().strip()

        response = requests.get(
            f'https://restcountries.com/v3.1/name/{name}?fields=capital,currencies,region')
        response_data = response.json()

    country = response_data[0]
    currencies = country["currencies"]
    for key in currencies:
        if 'name' in currencies[key]:
            currency = currencies[key]['name']
    capital = country["capital"][0]
    region = country["region"]

    country_data = pd.DataFrame.from_dict(
        {"currency": [currency], "capital": [capital], "region": [region]})
    return [name, country_data]


def quiz(name, database):
    engine = db.create_engine('sqlite:///country_db.db')
    database.to_sql(
        'country_info',
        con=engine,
        if_exists='replace',
        index=False)

    correct = 0
    incorrect = 0
    print("")
    capital_input = input(f"QUESTION 1: What is the capital of {name}? ")

    with engine.connect() as connection:
        query_result = connection.execute(
            db.text("SELECT capital FROM country_info;")).fetchall()
        correct_capital = query_result[0][0]

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
    print("")

    currency_input = input(f"QUESTION 2: What is the currency of {name}? ")
    with engine.connect() as connection:
        query_result = connection.execute(
            db.text("SELECT currency FROM country_info;")).fetchall()
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
    print("")

    region_input = input(f"QUESTION 3: On what continent is {name} located? ")
    with engine.connect() as connection:
        query_result = connection.execute(
            db.text("SELECT region FROM country_info;")).fetchall()
        correct_region = query_result[0][0]

        if region_input.lower().strip() == correct_region.lower():
            print("Correct!")
            correct += 1
        else:
            print("Incorrect! The correct answer was: ")
            print(correct_region)
            incorrect += 1
    print("")
    print(
        f"Answered {correct} questions correctly and {incorrect} questions incorrectly")
    if correct >= 2:
        print("Well done!!!")
    else:
        print("Dont worry, you will do better next time!")
    print("")
    print(f"Here is the information about {name}:")
    with engine.connect() as connection:
        query_result = connection.execute(
            db.text("SELECT * FROM country_info;")).fetchall()
        print(pd.DataFrame(query_result))


def game():
    # --this is where everything goes--
    display_rules()

    select_data = select_country()

    country_name = select_data[0]
    country_data = select_data[1]

    quiz(country_name, country_data)


# --game start stuff here--
play_again = True
while play_again:
    game()
    print("")
    play_again = input("GAME OVER! Would you like to try again?(yes/no) ")
    while play_again.lower() != 'yes' and play_again.lower() != 'no':
        play_again = input("GAME OVER! Would you like to try again?(yes/no) ")
    if play_again == 'yes':
        play_again = True
    else:
        play_again = False
print("")
print("Thanks for playing!")
