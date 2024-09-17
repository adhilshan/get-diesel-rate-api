# Documentation

This project is a Flask-based web scraper that retrieves diesel prices from the NDTV website for various states and cities in India. It exposes a set of API endpoints that fetch diesel price data, change status, and other relevant details.

## Features

- Fetch diesel prices for all states in India.
- Fetch recent diesel prices for a specific state.
- Fetch recent diesel prices for a specific city.
- Retrieve additional places and states with diesel prices.
- Scrapes data from NDTV's diesel price pages and returns it in JSON format.

## Requirements

Before you begin, ensure you have met the following requirements:

- Python 3.x installed on your local machine.
- `pip` installed to manage Python packages.

## Installation

1. **Clone the repository:**

   ```bash
   git clone https://github.com/yourusername/diesel-price-scraper.git
   cd diesel-price-scraper
   ```

2. **Install the required dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

   The main dependencies are:
   - Flask: To handle routing and web requests.
   - Requests: For making HTTP requests to NDTV.
   - BeautifulSoup (from `bs4`): To parse the HTML content.

## Usage

1. **Run the Flask server:**

   ```bash
   flask run
   ```

2. **Access the API endpoints:**

   After starting the Flask server, you can access the API endpoints using the following routes:

   - **Home Page:**

     ```bash
     GET /
     ```

     This serves the homepage of the web application.

   - **Get Diesel Prices for All States:**

     ```bash
     GET /api/diesel-price/all
     ```

     Fetches diesel prices, change status, and other details for all states in India.

   - **Get Diesel Prices by State:**

     ```bash
     GET /api/diesel-price/bystate/recent?state={state}
     ```

     Example:

     ```bash
     GET /api/diesel-price/bystate/recent?state=uttar-pradesh
     ```

     Fetches recent diesel prices for the given state.

   - **Get Diesel Prices by City:**

     ```bash
     GET /api/diesel-price/bycity/recent?city={city}
     ```

     Example:

     ```bash
     GET /api/diesel-price/bycity/recent?city=mumbai
     ```

     Fetches recent diesel prices for the given city.

   - **Get Diesel Prices for Other Places (Additional states):**

     ```bash
     GET /api/diesel-price/other-places?state={state}
     ```

     Example:

     ```bash
     GET /api/diesel-price/other-places?state=maharashtra
     ```

     Fetches diesel prices for states/places other than the main states listed.

## API Response Format

Each API returns the diesel price data in the following format:

```json
{
  "data": [
    {
      "state": "Maharashtra",
      "price": "Rs 90.15",
      "change": "+0.25",
      "change_status": "Increase"
    },
    {
      "state": "Gujarat",
      "price": "Rs 88.50",
      "change": "0",
      "change_status": "No Change"
    }
    ...
  ]
}
```

### Error Handling

In case of an error, the API returns a JSON object with an error message and the HTTP status code.

```json
{
  "error": "Failed to retrieve the webpage. Status code: 404"
}
```

## Development

To contribute to this project:

1. Fork the repository.
2. Create a new feature branch (`git checkout -b feature-name`).
3. Commit your changes (`git commit -m 'Add new feature'`).
4. Push to the branch (`git push origin feature-name`).
5. Create a new Pull Request.


### Key Points Covered in the `README.md`:
1. **Project Description**: Explains what the project does.
2. **Features**: Summarizes key functionality.
3. **Requirements**: Lists the dependencies required.
4. **Installation**: Instructions to clone the repository and install dependencies.
5. **Usage**: Describes how to run the Flask app and use the API routes.
6. **API Response Format**: Shows what the returned data looks like.
7. **Development**: Provides guidelines on how to contribute to the project.


## How it Works

This example uses the Web Server Gateway Interface (WSGI) with Flask to enable handling requests on Vercel with Serverless Functions.

## Running Locally

```bash
npm i -g vercel
vercel dev
```

Your Flask application is now available at `http://localhost:3000`.

## One-Click Deploy

Deploy the example using [Vercel](https://vercel.com?utm_source=github&utm_medium=readme&utm_campaign=vercel-examples):

[![Deploy with Vercel](https://vercel.com/button)](https://vercel.com/new/clone?repository-url=https%3A%2F%2Fgithub.com%2Fvercel%2Fexamples%2Ftree%2Fmain%2Fpython%2Fflask3&demo-title=Flask%203%20%2B%20Vercel&demo-description=Use%20Flask%203%20on%20Vercel%20with%20Serverless%20Functions%20using%20the%20Python%20Runtime.&demo-url=https%3A%2F%2Fflask3-python-template.vercel.app%2F&demo-image=https://assets.vercel.com/image/upload/v1669994156/random/flask.png)
