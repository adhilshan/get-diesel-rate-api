from flask import Flask, request, render_template
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('home.html')
@app.route('/api/diesel-price/all')
def all():
    url = 'https://www.ndtv.com/fuel-prices/diesel-price-in-all-state'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.5615.138 Safari/537.36'
    }

    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        
        rows = soup.find_all('tr')
        
        data = []
        
        for row in rows[1:]:
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
        
        return {"data": data}
    else:
        return {"error": f"Failed to retrieve the webpage. Status code: {response.status_code}"}


@app.route('/api/diesel-price/bystate/recent')
def getStateWise():
    state = request.args.get('state')

    url = f'https://www.ndtv.com/fuel-prices/diesel-price-in-{state}-state'

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.5615.138 Safari/537.36'
    }

    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        
        rows = soup.find_all('tr')
        
        data = []
        
        for row in rows[1:11]:
            cells = row.find_all('td')
            
            if len(cells) == 3:
                date = cells[0].get_text(strip=True)
                price = cells[1].get_text(strip=True)
                change = cells[2].get_text(strip=True)
                
                # Error handling for span and class attributes
                if cells[2].span and 'class' in cells[2].span.attrs:
                    if 'lr' in cells[2].span['class']:
                        change_status = "No Change"
                    elif 'down' in cells[2].span['class']:
                        change_status = "Increase"
                    else:
                        change_status = "Decrease"
                else:
                    change_status = "Unknown"
                
                # Append the scraped data to the list
                data.append({
                    'date': date,
                    'price': price,
                    'change': change,
                    'change_status': change_status
                })
        
        return {"data": data}
    else:
        return {"error": f"Failed to retrieve the webpage. Status code: {response.status_code}"}

@app.route('/api/diesel-price/bycity/recent')
def getCityWise():
    city = request.args.get('city')

    url = f'https://www.ndtv.com/fuel-prices/diesel-price-in-{city}-city'

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.5615.138 Safari/537.36'
    }

    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        
        rows = soup.find_all('tr')
        
        data = []
        
        for row in rows[1:11]:
            cells = row.find_all('td')
            
            if len(cells) == 3:
                date = cells[0].get_text(strip=True)
                price = cells[1].get_text(strip=True)
                change = cells[2].get_text(strip=True)
                
                if cells[2].span and 'class' in cells[2].span.attrs:
                    if 'lr' in cells[2].span['class']:
                        change_status = "No Change"
                    elif 'down' in cells[2].span['class']:
                        change_status = "Increase"
                    else:
                        change_status = "Decrease"
                else:
                    change_status = "Unknown"
                
                data.append({
                    'date': date,
                    'price': price,
                    'change': change,
                    'change_status': change_status
                })
        
        return {"data": data}
    else:
        return {"error": f"Failed to retrieve the webpage. Status code: {response.status_code}"}
    

@app.route('/api/diesel-price/other-places')
def byCity():
    state = request.args.get('state')

    url = f'https://www.ndtv.com/fuel-prices/diesel-price-in-{state}-state'

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.5615.138 Safari/537.36'
    }

    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        
        rows = soup.find_all('tr')
        
        data = []
        
        for row in rows[11:]:
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
                
                # Append the scraped data to the list
                data.append({
                    'state': state,
                    'price': price,
                    'change': change,
                    'change_status': change_status
                })
        
        return {"data": data}
    else:
        return {"error": f"Failed to retrieve the webpage. Status code: {response.status_code}"} , response.status_code
