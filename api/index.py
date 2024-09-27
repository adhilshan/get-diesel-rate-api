import os
import firebase_admin
from firebase_admin import credentials, db
from dotenv import load_dotenv
from flask import Flask, request, render_template
import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
from flask_cors import CORS

load_dotenv()

firebase_admin_sdk_key = {
    "type": os.getenv('FIREBASE_ADMIN_SDK_KEY_TYPE'),
    "project_id": os.getenv('FIREBASE_ADMIN_SDK_KEY_PROJECT_ID'),
    "private_key_id": os.getenv('FIREBASE_ADMIN_SDK_KEY_PRIVATE_KEY_ID'),
    "private_key": os.getenv('FIREBASE_ADMIN_SDK_KEY_PRIVATE_KEY').replace('\\n', '\n'),
    "client_email": os.getenv('FIREBASE_ADMIN_SDK_KEY_CLIENT_EMAIL'),
    "client_id": os.getenv('FIREBASE_ADMIN_SDK_KEY_CLIENT_ID'),
    "auth_uri": os.getenv('FIREBASE_ADMIN_SDK_KEY_AUTH_URI'),
    "token_uri": os.getenv('FIREBASE_ADMIN_SDK_KEY_TOKEN_URI'),
    "auth_provider_x509_cert_url": os.getenv('FIREBASE_ADMIN_SDK_KEY_AUTH_PROVIDER'),
    "client_x509_cert_url": os.getenv('FIREBASE_ADMIN_SDK_KEY_CLIENT_URL'),
    "universe_domain": os.getenv('UNIVERSE_DOMAIN')
}

if not firebase_admin._apps:
    cred = credentials.Certificate(firebase_admin_sdk_key)
    firebase_admin.initialize_app(cred, {
        'databaseURL': os.getenv('FIREBASE_ADMIN_SDK_KEY_DATABASE_URL')
    })

def get_database_reference(reference_path):
    return db.reference(reference_path)

def push_or_update_data(reference_path, data):
    ref = get_database_reference(reference_path)
    ref.set(data)
    print(f"Data pushed or updated at {reference_path}")

def retrieve_data(reference_path):
    ref = get_database_reference(reference_path)
    data = ref.get()
    return data

def is_data_stale(timestamp):
    data_time = datetime.strptime(timestamp, "%Y-%m-%d %H:%M:%S")
    return datetime.now() - data_time > timedelta(hours=14)

def scrape_data(url, limit=None):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.5615.138 Safari/537.36'
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        rows = soup.find_all('tr')
        data = []
        max_rows = limit if limit is not None else len(rows) - 1
        for row in rows[1:max_rows + 1]:
            cells = row.find_all('td')
            if len(cells) == 3:
                state = cells[0].get_text(strip=True)
                price = cells[1].get_text(strip=True)
                change = cells[2].get_text(strip=True)
                if 'lr' in cells[2].span['class']:
                    change_status = "No Change"
                elif 'down' in cells[2].span['class']:
                    change_status = "Increase"
                else:
                    change_status = "Decrease"
                data.append({
                    'state': state,
                    'price': price,
                    'change': change,
                    'change_status': change_status
                })
        return data
    else:
        raise Exception(f"Failed to retrieve the webpage. Status code: {response.status_code}")

app = Flask(__name__)
CORS(app)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/api/diesel-price/all')
def get_all_data():
    url = 'https://www.ndtv.com/fuel-prices/diesel-price-in-all-state'
    firebase_ref = 'diesel_prices/all'

    firebase_data = retrieve_data(firebase_ref)
    if firebase_data:
        if is_data_stale(firebase_data['timestamp']):
            print("Data is older than 14 hours, refreshing from the web...")
            data = scrape_data(url)
            new_data = {
                'data': data,
                'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
            push_or_update_data(firebase_ref, new_data)
            return {"data": new_data['data']}
        else:
            print("Serving data from Firebase...")
            return {"data": firebase_data['data']}
    else:
        data = scrape_data(url)
        new_data = {
            'data': data,
            'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        push_or_update_data(firebase_ref, new_data)
        return {"data": new_data['data']}

@app.route('/api/diesel-price/bystate/recent')
def get_state_wise():
    state = request.args.get('state')
    url = f'https://www.ndtv.com/fuel-prices/diesel-price-in-{state}-state'
    firebase_ref = f'diesel_prices/{state}'

    firebase_data = retrieve_data(firebase_ref)
    if firebase_data:
        if is_data_stale(firebase_data['timestamp']):
            print("Data is older than 14 hours, refreshing from the web...")
            data = scrape_data(url)
            new_data = {
                'data': data,
                'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
            push_or_update_data(firebase_ref, new_data)
            return {"data": new_data['data']}
        else:
            print("Serving data from Firebase...")
            return {"data": firebase_data['data']}
    else:
        data = scrape_data(url)
        new_data = {
            'data': data,
            'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        push_or_update_data(firebase_ref, new_data)
        return {"data": new_data['data']}

@app.route('/api/diesel-price/bycity/recent')
def get_city_wise():
    city = request.args.get('city')
    city_url_friendly = city.replace(" ", "-").lower()
    url = f'https://www.ndtv.com/fuel-prices/diesel-price-in-{city_url_friendly}-city'
    firebase_ref = f'diesel_prices/cities/{city}'

    firebase_data = retrieve_data(firebase_ref)
    if firebase_data:
        if is_data_stale(firebase_data['timestamp']):
            print("City data is older than 14 hours, refreshing from the web...")
            data = scrape_data(url, limit=10)
            new_data = {
                'data': data,
                'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
            push_or_update_data(firebase_ref, new_data)
            return {"data": new_data['data']}
        else:
            print("Serving city data from Firebase...")
            return {"data": firebase_data['data']}
    else:
        data = scrape_data(url, limit=10)
        new_data = {
            'data': data,
            'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        push_or_update_data(firebase_ref, new_data)
        return {"data": new_data['data']}

if __name__ == '__main__':
    app.run(debug=True)
