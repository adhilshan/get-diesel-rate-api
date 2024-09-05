from flask import Flask, request
import requests
from bs4 import BeautifulSoup
import time
import json

app = Flask(__name__)

data_array = []

places = [
  "Agra", "Ahmedabad", "Allahabad", "Aurangabad", "Bangalore", "Bhopal", "Bhubaneswar", "Chandigarh", "Chennai", "Coimbatore", "Dehradun", "Erode", "Faridabad", "Ghaziabad", "Gurgaon", "Guwahati", "Hyderabad", "Indore", "Jaipur", "Jammu", "Jamshedpur", "Kanpur Urban", "Kolhapur", "Kolkata", "Kozhikode", "Lucknow", "Ludhiana", "Madurai", "Mangalore", "Mumbai", "Mysore", "Nagpur", "Nashik", "New Delhi", "Noida", "Patna", "Pune", "Raipur", "Rajkot", "Ranchi", "Salem", "Shimla", "Srinagar", "Surat", "Thane", "Tiruchchirappalli", "Trivandrum", "Vadodara", "Varanasi", "Visakhapatnam"
]

@app.route('/api/diesel-rate')
def home():
    getPrice()
    return data_array[len(data_array) - 1]

def getPrice():
    data_array_2 = []
    for place in places:
        JSON_OBJ_1 = {}
        JSON_OBJ_2 = {}
        url = 'https://www.financialexpress.com/diesel-rate-in-'+ place +'/#main-heading'

        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.5615.138 Safari/537.36'
        }

        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            titles = soup.find_all('span', class_='active summary_')
            for title in titles:
                index = title.get_text().find("₹")
                if index != -1:
                    amount = title.get_text()[index+1:].split()[0]
                    JSON_OBJ_2['place'] = place
                    JSON_OBJ_2['amount'] = amount
                else:
                    print("₹ symbol not found in the text.")
            data_array_2.append(JSON_OBJ_2)
        else:
            print(f"Failed to retrieve the webpage. Status code: {response.status_code}")

    JSON_OBJ_1['timestamp'] = time.time()
    JSON_OBJ_1['data'] = data_array_2
    JSON_OBJ_1['meassure'] = 'INR/litre'
    data_array.append(JSON_OBJ_1)
