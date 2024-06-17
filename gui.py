from taipy.gui import Gui, notify
import requests

# Define the function to fetch the forecast from the FastAPI backend
def fetch_forecast(ticker: str, days: int):
    response = requests.post("http://localhost:8000/predict", json={"ticker": ticker})
    if response.status_code == 200:
        return response.json()["forecast"]
    else:
        notify("error", "Prediction failed. Please check the ticker or train the model first.")
        return {}

# Define the function to train the model
def train_model(ticker: str):
    response = requests.post("http://localhost:8000/train", json={"ticker": ticker})
    if response.status_code == 200:
        notify("success", f"Model for {ticker} trained successfully!")
    else:
        notify("error", f"Failed to train model for {ticker}")

# List of common stock tickers
tickers = ["AAPL", "MSFT", "GOOGL", "AMZN", "FB", "TSLA", "NFLX"]

# Define the GUI layout
layout = """
<|layout|columns=1|
<|{forecast_data}|table|>
<|{image_url}|image|>
|>

<|layout|columns=3|
<|Select Ticker|>
<|{ticker}|selector|lov={tickers}|>

<|Train Model|button|on_action=train_model_action|>

<|Days to Predict|>
<|{days}|slider|min=1|max=30|>
<|Predict|button|on_action=predict_action|>
|>
"""

# Define the variables
forecast_data = {}
ticker = "MSFT"
days = 7
image_url = ""

# Define the action functions
def predict_action(state):
    state.forecast_data = fetch_forecast(state.ticker, state.days)
    state.image_url = f"{state.ticker}_plot.png"

def train_model_action(state):
    train_model(state.ticker)

# Create the GUI object
gui = Gui(page=layout)
gui.run()
