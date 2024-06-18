import random
import pandas as pd
import math

# Initialize empty lists for each column
user_ids = []
budgets = []
food_preferences = []
location_preferences = []
destinations = []
restaurants = []

# Generate 5000 random examples
for user_id in range(1, 5001):
    user_ids.append(user_id)
    budgets.append(math.ceil(random.randint(200, 5000)/ 100) * 100)  # Random salary between 40,000 and 90,000
    food_pref = random.choice(['Italian', 'Mexican', 'Japanese', 'Chinese', 'Indian', 'Sri Lankan','Thai','Greek','Spanish','Brazilian','Korean','Turkish','Moroccan','Vietenamese','Ithiopian','Russian','Malaysian','Swedish','Jamaican','Australian','German','Indonesian','Filipino','Bangladesi','Hawaiian','Finnish'])
    food_preferences.append(food_pref)
    location_pref = random.choice(['Beach', 'City', 'Mountains', 'Countryside','Island','Lakeside','Forested','Cultural','Artistic','Industrial','Entertainment','Music','Military','Religious','Sporting Evets','Historical','Desert'])
    location_preferences.append(location_pref)
    destination = f"{location_pref} {random.choice(['Resort', 'Apartment', 'Cabin','Hostel','Hotel','Inn','Guesthouse','Lodge','Cabin','Airbnb','TreeHouse'])}"
    destinations.append(destination)
    restaurant = f'{food_pref} Restaurant'
    restaurants.append(restaurant)

# Create a DataFrame from the generated lists
data = {
    'user_id': user_ids,
    'budget': budgets,
    'food_preferences': food_preferences,
    'location_preferences': location_preferences,
    'destination': destinations,
    'restaurant': restaurants,
}

df = pd.DataFrame(data)

# Print the first few rows of the generated dataset
print(df)

# df.to_csv('output.csv', index=False)

# Creating a dataset with city, accommodation place, accommodation budget, interest place, and interest place budget

dataset = [
    {
        'city': 'New York',
        'accommodation_place': 'Hotel ABC',
        'accommodation_budget': 200,
        'interest_place': 'Central Park',
        'interest_place_budget': 50
    },
    {
        'city': 'Paris',
        'accommodation_place': 'Hotel XYZ',
        'accommodation_budget': 150,
        'interest_place': 'Eiffel Tower',
        'interest_place_budget': 30
    },
    {
        'city': 'Paris',
        'accommodation_place': 'Hotel X',
        'accommodation_budget': 150,
        'interest_place': 'Eiffel Tower',
        'interest_place_budget': 30
    },
    {
        'city': 'Paris',
        'accommodation_place': 'Hotel XY',
        'accommodation_budget': 200,
        'interest_place': 'Eiffel Tower',
        'interest_place_budget': 30
    },
    {
        'city': 'Paris',
        'accommodation_place': 'Hotel XYZ',
        'accommodation_budget': 280,
        'interest_place': 'Eiffel Tower',
        'interest_place_budget': 80
    },
    {
        'city': 'Tokyo',
        'accommodation_place': 'Ryokan 123',
        'accommodation_budget': 180,
        'interest_place': 'Tokyo Tower',
        'interest_place_budget': 40
    },
    # Add more entries as needed
]

# Printing the dataset
for entry in dataset:
    print(entry)


def recommend_place(city, budget, dataset):
    # Filter dataset based on user's city
    city_data = [entry for entry in dataset if entry['city'].lower() == city.lower()]

    if not city_data:
        return "Sorry, we don't have information for that city in our dataset."

    # Find combinations of accommodation and interest places within budget
    valid_combinations = []
    for accommodation in city_data:
        for interest_place in city_data:
            total_budget = accommodation['accommodation_budget'] + interest_place['interest_place_budget']
            if total_budget <= budget:
                valid_combinations.append({
                    'accommodation_place': accommodation['accommodation_place'],
                    'interest_place': interest_place['interest_place'],
                    'total_budget': total_budget
                })

    if not valid_combinations:
        return f"Sorry, we couldn't find any valid combinations within your budget in {city}."

    # Select the combination with the highest total budget within the user's budget
    best_combination = max(valid_combinations, key=lambda x: x['total_budget'])

    return {
        'accommodation_place': best_combination['accommodation_place'],
        'interest_place': best_combination['interest_place']
    }

# Example usage:
user_city = input("Enter the city: ")
user_budget = float(input("Enter your budget: "))

recommendation = recommend_place(user_city, user_budget, dataset)

if isinstance(recommendation, str):
    print(recommendation)
else:
    print(f"Recommended Accommodation: {recommendation['accommodation_place']}")
    print(f"Recommended Interest Place: {recommendation['interest_place']}")


            
