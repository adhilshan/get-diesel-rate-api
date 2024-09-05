from flask import Flask, jsonify
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

places = [
    "Agra", "Ahmedabad", "Allahabad", "Aurangabad", "Bangalore", "Bhopal", "Bhubaneswar", "Chandigarh", 
    "Chennai", "Coimbatore", "Dehradun", "Erode", "Faridabad", "Ghaziabad", "Gurgaon", "Guwahati", 
    "Hyderabad", "Indore", "Jaipur", "Jammu", "Jamshedpur", "Kanpur Urban", "Kolhapur", "Kolkata", 
    "Kozhikode", "Lucknow", "Ludhiana", "Madurai", "Mangalore", "Mumbai", "Mysore", "Nagpur", "Nashik", 
    "New Delhi", "Noida", "Patna", "Pune", "Raipur", "Rajkot", "Ranchi", "Salem", "Shimla", "Srinagar", 
    "Surat", "Thane", "Tiruchchirappalli", "Trivandrum", "Vadodara", "Varanasi", "Visakhapatnam"
]

@app.route('/api/diesel-rate')
def home():
    return jsonify(getPrice())

def getPrice():
    data_array_2 = []
    for place in places:
        JSON_OBJ_2 = {}
        url = f'https://www.financialexpress.com/diesel-rate-in-{place}/#main-heading'
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.5615.138 Safari/537.36'
        }
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')
        titles = soup.find_all('span', class_='active summary_')
        for title in titles:
            index = title.get_text().find("₹")
            if index != -1:
                amount = title.get_text()[index+1:].split()[0]
                JSON_OBJ_2['place'] = place
                JSON_OBJ_2['amount'] = amount
            else:
                data_array_2.append(JSON_OBJ_2)
    JSON_OBJ_1 = {
        'data': data_array_2,
        'measure': 'INR/litre'
    }
    return JSON_OBJ_1
