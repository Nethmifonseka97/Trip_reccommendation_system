# import subprocess

# def install_package(package_name):
#     subprocess.check_call(['pip', 'install', package_name])

# # Example: Install pandas
# install_package('pandas')

# import pandas as pd
from modal import Image, Stub, wsgi_app
#modal serve test.py
#Created flask_app => https://nethmifonseka97--test-py-flask-app-dev.modal.run

stub = Stub("bmt")
image = Image.debian_slim().pip_install("flask","pymongo","datetime")
import modal

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
    @web_app.post("/echo")
    def echo():
        from sklearn.feature_extraction.text import TfidfVectorizer
        from sklearn.metrics.pairwise import linear_kernel
        from pymongo import MongoClient

        client = MongoClient("")
        db = client.get_database('ml')
        records = db.budget
        df = list(records.find()) 

        # Vectorize the text attributes (food preferences, location preferences, destination)
        tfidf_vectorizer = TfidfVectorizer()
        tfidf_matrix = tfidf_vectorizer.fit_transform(df['food_preferences'] + " " + df['location_preferences'] + " " + df['destination'])

        # Calculate cosine similarity
        cosine_sim = linear_kernel(tfidf_matrix, tfidf_matrix)

        # Function to recommend destinations and restaurants
        def recommend_destinations(user_data):
            user_profile = user_data['food_preferences'] + " " + user_data['location_preferences'] + " " + user_data['destination']

            # Get the index of the user's row in the dataset
            user_idx = df[df['user_id'] == user_data['user_id']].index[0]

            # Calculate the cosine similarities for the user's profile
            sim_scores = list(enumerate(cosine_sim[user_idx]))

            # Sort the destinations and restaurants by similarity scores
            sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)

            # Get the top 5 recommendations
            sim_scores = sim_scores[1:6]  # Exclude the user's own row
            recommendations = df.iloc[[x[0] for x in sim_scores]]

            return recommendations[['destination', 'restaurant']]

    


    # @stub.function(secret=modal.Secret.from_name("MONGODB_URL"))
    @web_app.post("/ml")
    def ml():
        
        # file_path = '/ml.csv'
        from pymongo import MongoClient
        from datetime import datetime
        import secrets

        client = MongoClient("mongodb+srv://test:test@cluster0.47ozeut.mongodb.net/test?retryWrites=true")
        db = client.get_database('ml2')
        records = db.budget
        dataset = list(records.find())
        # print(dataset)
        
        
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
        start_date = request.json["start_date"]
        end_date = request.json["end_date"]
        food = request.json["food"]
        leisure = request.json["interest"]
        # print(food)

        # Convert the string dates to datetime.date objects
        start_date = datetime.strptime(start_date, '%Y/%m/%d').date()
        end_date = datetime.strptime(end_date, '%Y/%m/%d').date()


        difference = end_date - start_date
        days = difference.days
        days = days + 1

        print(days)

        day_budget = (user_budget/days)

        print(day_budget)
        # print(leisure)

        msg = ''
        
        city_data = [entry for entry in dataset if (entry['city'].lower() == user_city.lower())]
        city_data2 = [entry for entry in dataset if ((entry['interest'].lower() == leisure[0].lower()) or (entry['interest'].lower() == leisure[1].lower()) or (entry['interest'].lower() == leisure[2].lower())) and (entry['city'].lower() == user_city.lower())]
        city_data3 = [entry for entry in dataset if ((entry['food_preference'].lower()==food[0].lower()) or (entry['food_preference'].lower()==food[1].lower()) or (entry['food_preference'].lower()==food[2].lower())) and (entry['city'].lower() == user_city.lower())]
        # print(city_data3)

        if not city_data:
            return "Sorry, we don't have information for that city in our dataset."

        # Find combinations of accommodation and interest places within budget
        valid_combinations = []
        for accommodation in city_data:
            for interest in city_data2:
                for restaurant in city_data3:
                    if (restaurant['food_preference'].lower() == food[0].lower() or restaurant['food_preference'].lower() == food[1].lower() or restaurant['food_preference'].lower() == food[2].lower()) and (interest['interest'].lower() == leisure[0].lower() or interest['interest'].lower() == leisure[1].lower() or interest['interest'].lower() == leisure[2].lower()):
                        total_budget = accommodation['accommodation_budget'] + interest['interest_budget'] + restaurant['food_budget']
                        if total_budget <= day_budget:
                            valid_combinations.append({
                                'accommodation':{
                                    'name': accommodation['accommodation'],
                                    'price':{
                                        'standard':accommodation['accommodation_budget'],
                                        'deluxe':accommodation['accommodation_budget']+30,
                                        'suite':accommodation['accommodation_budget']+70,
                                    },
                                },
                                'interest': {
                                    'name' : interest['interest'],
                                    'type' : interest['interest_name'],
                                    'price' : interest['interest_budget'],
                                },
                                'restaurant': {
                                    'name' : restaurant['restaurant'],
                                    'type' : restaurant['food_preference'],
                                    'price' : restaurant['food_budget'],
                                },
                                'total_budget': total_budget
                            })

        # print(valid_combinations)
        
        count = 100
        while valid_combinations == []:
            msg = "Sorry, we couldn't find any valid combinations within your budget but we like to suggest these options."
            print(count)
            for accommodation in city_data:
                for interest in city_data2:
                    for restaurant in city_data3:
                        if(restaurant['food_preference'].lower() == food[0].lower() or restaurant['food_preference'].lower() == food[1].lower()) and (interest['interest'].lower() == leisure[0].lower() or interest['interest'].lower() == leisure[1].lower() ):
                            total_budget = accommodation['accommodation_budget'] + interest['interest_budget'] + restaurant['food_budget']
                            if total_budget <= day_budget + count:
                                valid_combinations.append({
                                    'accommodation':{
                                        'name': accommodation['accommodation'],
                                        'price':{
                                            'standard':accommodation['accommodation_budget'],
                                            'deluxe':accommodation['accommodation_budget']+30,
                                            'suite':accommodation['accommodation_budget']+70,
                                        },
                                    },
                                    'interest': {
                                        'name' : interest['interest'],
                                        'price' : interest['interest_budget'],
                                    },
                                    'restaurant': {
                                        'name' : restaurant['restaurant'],
                                        'price' : restaurant['food_budget'],
                                    },
                                    'total_budget': total_budget
                                })
            count = count + 50

        # except:
        #         return f"Sorry, we couldn't find any valid combinations within your budget in {user_city}."

        # Select the combination with the highest total budget within the user's budget
        best_combination = max(valid_combinations, key=lambda x: x['total_budget'])
        # print(best_combination)
        # print("***")

        # Sort the valid_combinations based on the 'total_budget' key in descending order
        sorted_combinations = sorted(valid_combinations, key=lambda x: x['total_budget'], reverse=True)
        # print(sorted_combinations)

        sorted_restaurant_data = sorted(city_data3, key=lambda x: x['food_budget'], reverse=False)
        sorted_interest_data = sorted(city_data2, key=lambda x: x['interest_budget'], reverse=False)
        # print(sorted_restaurant_data)

        def custom_shuffle(lst):
            # Create a new list to hold the shuffled items
            shuffled = []
            while lst:
                # Select a random index from the list
                index = secrets.randbelow(len(lst))
                # Pop the item at the selected index and append it to the shuffled list
                shuffled.append(lst.pop(index))
            return shuffled

        # Example list
        # my_list = [1, 2, 3, 4, 5]

        # Randomize the list
        restaurant_data = custom_shuffle(sorted_restaurant_data.copy())  # Use .copy() to avoid modifying the original list
        interest_data = custom_shuffle(sorted_interest_data.copy())  # Use .copy() to avoid modifying the original list
        
        for r2 in sorted_combinations:
            if (r2['accommodation']['name'] != best_combination['accommodation']['name']) and ((r2['accommodation']['price']['standard'] < best_combination['accommodation']['price']['standard']) or (r2['accommodation']['price']['standard'] > best_combination['accommodation']['price']['standard'])):
                second_best_combination = r2
                break
            # elif (r2['total_budget'] > best_combination['total_budget']) and  (r2['accommodation']['price']['standard'] > best_combination['accommodation']['price']['standard']):
            #     second_best_combination = r2
            #     break
            else:
                second_best_combination = ''

        print(second_best_combination)

        if second_best_combination != '':
            for r3 in sorted_combinations:
                if (r3['accommodation']['name'] != best_combination['accommodation']['name']) and (r3['accommodation']['price']['standard'] < second_best_combination['accommodation']['price']['standard']) or (r3['accommodation']['price']['standard'] > second_best_combination['accommodation']['price']['standard']):
                    third_best_combination = r3
                    break
                # if (r3['total_budget'] > second_best_combination['total_budget']) and (r3['accommodation']['price']['standard'] > second_best_combination['accommodation']['price']['standard']):
                #     third_best_combination = r3
                #     break
                else:
                    third_best_combination = ''
        
        
        interest_for_days = []
        restaurant_for_days = []


        restaurant_budget = (day_budget - best_combination['accommodation']['price']['standard'])
        # interest_budget = (day_budget - best_combination['accommodation']['price']['standard'])* 0.3

        d = 1.5

        for di in interest_data:
            if (di['interest_budget'] < restaurant_budget) :
                interest_for_days.append( {'interest': {
                                                'name' : di['interest_name'],
                                                'type' : di['interest'],
                                                'price' : di['interest_budget']}})
                d = d + 0.5

            if msg != "":
                interest_for_days.append( {'interest': {
                                                'name' : di['interest_name'],
                                                'type' : di['interest'],
                                                'price' : di['interest_budget']}})
                d = d + 0.5

            if d > days :
                break

        

        d = 1.5

        for dr in restaurant_data:
            if (dr['food_budget'] < restaurant_budget) and (dr['food_preference'].lower() == food[0].lower() or dr['food_preference'].lower() == food[1].lower() or dr['food_preference'].lower() == food[2].lower()):
                restaurant_for_days.append( {'restaurant': {
                                                'name' : dr['restaurant'],
                                                'type' : dr['food_preference'],
                                                'price' : dr['food_budget']}})
                d = d + 0.5

            if msg != "":
                restaurant_for_days.append( {'restaurant': {
                                                'name' : dr['restaurant'],
                                                'type' : dr['food_preference'],
                                                'price' : dr['food_budget']}})
                d = d + 0.5

            if d > days :
                break

        #         if di['restaurant_budget'] < best_combination['restaurant_budget'] :
        #             restaurant_for_days.append()


        result = {  "msg" : msg,
                    "best_combination": best_combination,
                    "second_best_combination" : second_best_combination,
                    "third_best_combination" : third_best_combination,
                    "interest_for_days" : interest_for_days,
                    "restaurant_for_days" : restaurant_for_days,
                 }
        
        # print (result)
        
        return result



    return web_app