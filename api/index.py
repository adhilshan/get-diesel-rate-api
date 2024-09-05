from flask import Flask, request
import requests
from bs4 import BeautifulSoup
import time

app = Flask(__name__)

JSON_OBJ_1 = {}
places = [
    "Ahmedabad", "Bangalore", "Bhopal", "Chandigarh", 
    "Chennai", "Hyderabad", "Jaipur", "Jamshedpur", "Kolkata", 
    "Kozhikode", "Lucknow", "Madurai", "Mumbai", "Nashik",
    "New Delhi", "Pune", "Raipur", "Ranchi", "Salem", "Srinagar", 
    "Trivandrum", "Varanasi", "Visakhapatnam"]

@app.route('/api/diesel-rate')
def home():
    getPrice()
    return JSON_OBJ_1

def getPrice():
    data_array = []
    for place in places:
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
            data_array.append(JSON_OBJ_2)
        else:
            print(f"Failed to retrieve the webpage. Status code: {response.status_code}")

    JSON_OBJ_1['timestamp'] = time.time()
    JSON_OBJ_1['data'] = data_array
    JSON_OBJ_1['meassure'] = 'INR/litre'
