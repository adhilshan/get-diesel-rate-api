import logging
from flask import Flask, request
import requests
from bs4 import BeautifulSoup

logging.basicConfig(level=logging.INFO)

@app.route('/api/diesel-rate')
def home():
    try:
        return getPrice()
    except Exception as e:
        logging.error(f"An error occurred: {e}")
        return {"error": "An internal error occurred"}, 500

def getPrice():
    try:
        data_array = []
        data_array_2 = []
        for place in places:
            JSON_OBJ_1 = {}
            JSON_OBJ_2 = {}
            url = 'https://www.financialexpress.com/diesel-rate-in-'+ place +'/#main-heading'

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
                    logging.warning(f"₹ symbol not found in the text for {place}.")
            data_array_2.append(JSON_OBJ_2)

        JSON_OBJ_1['timestamp'] = time.time()
        JSON_OBJ_1['data'] = data_array_2
        JSON_OBJ_1['measure'] = 'INR/litre'
        return JSON_OBJ_1

    except requests.RequestException as e:
        logging.error(f"Request failed: {e}")
        return {"error": "Failed to retrieve data"}, 500
    except Exception as e:
        logging.error(f"An error occurred: {e}")
        return {"error": "An internal error occurred"}, 500
