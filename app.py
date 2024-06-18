from flask import Flask, render_template, request, redirect, url_for, flash
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = 'secret_key_for_flash_messages'


# Dummy user data (replace with a database)
users = [{'username': 'user1', 'password': generate_password_hash('password1')},
         {'username': 'user2', 'password': generate_password_hash('password2')}]

# @app.route('/')
def index():
    return render_template('index.html')


# API for login
# @app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user = next((user for user in users if user['username'] == username), None)

        if user and check_password_hash(user['password'], password):
            flash('Login successful', 'success')
            # Implement your session management or token generation here
            return render_template('user.html', username=username)
        else:
            flash('Invalid username or password', 'error')

    return render_template('login.html')
    

# API for register
# @app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Check if the username is already taken
        if any(user['username'] == username for user in users):
            flash('Username already taken. Please choose another one.', 'error')
        else:
            # Hash the password before storing it
            hashed_password = generate_password_hash(password)
            users.append({'username': username, 'password': hashed_password})
            flash('Registration successful. You can now log in.', 'success')
            return redirect(url_for('login'))

    return render_template('register.html')


# ...
# API for user
@app.route('/user',methods=['GET', 'POST'])
def user(): 
    # if request.method == 'POST':
    username = username
    print(username)
        
    # Get the user details from the session or token (implement your session management or token verification here)
    # For simplicity, we'll use a dummy user
    dummy_user = {'username': username}
    
    return render_template('user.html', user=dummy_user)

# ...

# import subprocess

# def install_package(package_name):
#     subprocess.check_call(['pip', 'install', package_name])

# # Example: Install pandas
# install_package('pandas')

# import pandas as pd
from modal import Image, Stub, wsgi_app
#modal serve test.py
#Created flask_app => https://nethmifonseka97--test-py-flask-app-dev.modal.run

stub = Stub()
image = Image.debian_slim().pip_install("flask","pymongo")


@stub.function(image=image)
@wsgi_app()
def flask_app():
    from flask import Flask, request

    web_app = Flask(__name__)

    @web_app.get("/msg")
    def home():
        return "Recommend"

    # @web_app.post("/echo")
    # def echo():
    #     return request.json

    
    @web_app.post("/ml")
    def ml():

        # file_path = '/ml.csv'

        
        from pymongo import MongoClient
        client = MongoClient("")
        db = client.get_database('ml')
        records = db.budget
        dataset = list(records.find())
        print(dataset)
        
        
        # Read the CSV file into a DataFrame
        # df = pd.read_csv(file_path)

        # Assuming df is your DataFrame
        # Create an empty list to store the converted dataset
        # dataset = []

        # Iterate over rows in the DataFrame
        # for index, row in df.iterrows():
        #     # Create a dictionary for each row and append it to the dataset list
        #     data = {
        #         'city': row['city'],
        #         'accommodation': row['accommodation'],
        #         'accommodation_budget': row['accommodation_budget'],
        #         'restaurant': row['restaurant'],
        #         'food_preference': row['food_preference'],
        #         'food_budget': row['food_budget'],
        #         'interest': row['interest'],
        #         'interest_budget': row['interest_budget']
        #     }
        #     dataset.append(data)

   
        user_city =  request.json["city"]
        user_budget = request.json["budget"]
        food = request.json["food"]
        leisure = request.json["interest"]

        
        city_data = [entry for entry in dataset if entry['city'].lower() == user_city.lower() and entry['food_preference'].lower() == food.lower() and entry['interest'].lower() == leisure.lower()]
        print(city_data)

        if not city_data:
            return "Sorry, we don't have information for that city in our dataset."

        # Find combinations of accommodation and interest places within budget
        valid_combinations = []
        for accommodation in city_data:
            for interest in city_data:
                for restaurant in city_data:
                    total_budget = accommodation['accommodation_budget'] + interest['interest_budget'] + restaurant['food_budget']
                    if total_budget <= user_budget:
                        valid_combinations.append({
                            'accommodation_place': accommodation['accommodation'],
                            'interest_place': interest['interest'],
                            'restaurant': restaurant['restaurant'],
                            'total_budget': total_budget
                        })

        if not valid_combinations:
            return f"Sorry, we couldn't find any valid combinations within your budget in {user_city}."

        # Select the combination with the highest total budget within the user's budget
        best_combination = max(valid_combinations, key=lambda x: x['total_budget'])

        try:
            result = {'accommodation_place': best_combination['accommodation_place'],
                'interest_place': best_combination['interest_place'],
                'restaurant': best_combination['restaurant'],
                'total_budget': best_combination['total_budget']}
        except:
            result = {"accomadation": "HotelB"}
        
        print (result)
        
        return result

    
        # recommendation = recommend_place(user_city, user_budget,food, leisure, dataset)

        # if isinstance(recommendation, str):
        #     print(recommendation)
        # else:
        #     print(f"Recommended Accommodation: {recommendation['accommodation_place']}")
        #     print(f"Recommended Interest Place: {recommendation['interest_place']}")
        #     print(f"Recommended Interest Place: {recommendation['restaurant']}")
        #     print(f"Recommended Interest Place: {recommendation['total_budget']}")


        # try:
        #     salary = request.json["salary"]
        #     if salary > 2000:
        #         result = {"hotel": "HotelA"}
        #     else:
        #         result = {"hotel": "HotelB"}
        # except KeyError:
        #     result = {"error": "Salary not found in the request JSON"}

        # return result


    return web_app


if __name__ == '__main__':
    app.run(debug=True)
