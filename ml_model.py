import datetime
from pathlib import Path

import joblib
import pandas as pd
import yfinance as yf
from prophet import Prophet

BASE_DIR = Path(__file__).resolve(strict=True).parent
TODAY = datetime.date.today()

def train(ticker="MSFT"):
    data = yf.download(ticker, "2020-01-01", TODAY.strftime("%Y-%m-%d"))
    data["Adj Close"].plot(title=f"{ticker} Stock Adjusted Closing Price")

    df_forecast = data.copy()
    df_forecast.reset_index(inplace=True)
    df_forecast["ds"] = df_forecast["Date"]
    df_forecast["y"] = df_forecast["Adj Close"]
    df_forecast = df_forecast[["ds", "y"]]

    model = Prophet()
    model.fit(df_forecast)

    joblib.dump(model, Path(BASE_DIR).joinpath(f"{ticker}.joblib"))

def predict(ticker="MSFT", days=7):
    model_file = Path(BASE_DIR).joinpath(f"{ticker}.joblib")
    if not model_file.exists():
        return False

    model = joblib.load(model_file)
    future = TODAY + datetime.timedelta(days=days)

    dates = pd.date_range(start="2020-01-01", end=future.strftime("%Y-%m-%d"))
    df = pd.DataFrame({"ds": dates})

    forecast = model.predict(df)
    
    plot_filename = Path(BASE_DIR).joinpath(f"{ticker}_plot.png")
    plot_components_filename = Path(BASE_DIR).joinpath(f"{ticker}_plot_components.png")
    
    model.plot(forecast).savefig(plot_filename)
    model.plot_components(forecast).savefig(plot_components_filename)

    return forecast.tail(days).to_dict("records")

def convert(prediction_list):
    output = {}
    for data in prediction_list:
        date = data["ds"].strftime("%m/%d/%Y")
        output[date] = data["trend"]
    return output
