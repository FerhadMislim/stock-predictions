import pandas as pd
from taipy.gui import Gui, notify
import requests
import logging

# Set the logging level to INFO
logging.basicConfig(level=logging.DEBUG)

# Function to fetch forecast data from FastAPI backend
def fetch_forecast(ticker: str, days: int):
    try:
        response = requests.post("http://localhost:8000/predict", json={"ticker": ticker})
        response.raise_for_status()  # Raise an exception for HTTP errors (e.g., 404, 500)
        data = response.json()
        if "forecast" in data:
            return data["forecast"]
        else:
            logging.error("Invalid response format. Forecast data not found.")
            return {}
    except requests.exceptions.RequestException as e:
        logging.error(f"Error fetching forecast: {e}")
        return {}

# Function to train the model via FastAPI
def train_model(ticker: str):
    try:
        response = requests.post("http://localhost:8000/train", json={"ticker": ticker})
        response.raise_for_status()  # Raise an exception for HTTP errors (e.g., 404, 500)
        logging.info(f"Model for {ticker} trained successfully!")
    except requests.exceptions.RequestException as e:
        logging.error(f"Failed to train model for {ticker}: {e}")

# List of common stock tickers
tickers = ["AAPL", "MSFT", "GOOGL", "AMZN", "FB", "TSLA", "NFLX"]

# Define the GUI layout
layout = """
<|text-center|
#Stock Forecasting App
|>

<|layout|columns=1 1 1|
<|Select Ticker|>
<|{ticker}|selector|lov={tickers}|>

<|text-center|

<|Train Model|button|on_action=train_model_action|>

<|Days to Predict|>

<|{days}|slider|min=1|max=30|>

<|Predict|button|on_action=predict_action|>
|>

<|{image_url}|image|>
<|{image_component}|image|>
|>

<|{forecast_data}|table|>

"""

# Define the variables
forecast_data = pd.DataFrame(columns=["Date", "Forecast"])
ticker = "MSFT"
days = 7
image_url = ""
image_component = ""

# Define the action functions
def predict_action(state):
    forecast_data = fetch_forecast(state.ticker, state.days)
    # to dataframe
    forecast_data = pd.DataFrame(forecast_data.items(), columns=["Date", "Forecast"])
    state.forecast_data = forecast_data
    state.image_url = f"{state.ticker}_plot.png"
    state.image_component = f"{state.ticker}_plot_components.png"

def train_model_action(state):
    train_model(state.ticker)

# Create the GUI object
gui = Gui(page=layout)
gui.run()
