import requests
import datetime
import os
from requests.auth import HTTPBasicAuth

# Extracting exercise information using the Nutritionix API:
API_KEY = os.environ['API_KEY']
API_ID = os.environ['API_ID']

SHEETY_USERNAME = os.environ['SHEETY_USERNAME']
SHEETY_PASSWORD = os.environ['SHEETY_PASSWORD']

DATE_TODAY = datetime.date.today().strftime("%d/%m/%Y")
TIME_NOW = datetime.datetime.now().strftime("%H:%M:%S")


endpoint = "https://trackapi.nutritionix.com/v2/natural/exercise"

exercise = input("Tell me which exercises you did: ")

header = {
    "x-app-id": API_ID,
    "x-app-key": API_KEY,
    "x-remote-user-id": "0",
}

data = {
    "query": exercise,
    "gender": "male",
    "weight_kg": 120,
    "height_cm": 196,
    "age": 24
}

response = requests.post(url=endpoint, headers=header, json=data)
response.raise_for_status()
data = response.json()


if len(data['exercises']) != 0:  # Check if any exercises have been recognized.
    for exercise in data['exercises']:
        name = exercise['name'].title()
        duration = exercise['duration_min']
        calories = exercise['nf_calories']


        # Saving Data into Google Sheets:

        sheety_endpoint = os.environ['SHEETY_ENDPOINT']

        sheety_params = {
            "myWorkout": {
                "date": DATE_TODAY,
                "time": TIME_NOW,
                "exercise": name,
                "duration": duration,
                "calories": calories,
            }
        }

        # Send data to Sheet
        basic = HTTPBasicAuth(SHEETY_USERNAME, SHEETY_PASSWORD) # Adding basic auth
        sheety_response = requests.post(url=sheety_endpoint, json=sheety_params, auth=basic)
else:
    print("No exercises found in the response. Please try again!")

