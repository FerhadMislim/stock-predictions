from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from model import StockIn, StockOut
from ml_model import convert, predict, train

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": "Welcome to the Stock Prediction API"}

@app.get("/ping")
def pong():
    return {"ping": "pong!"}

@app.post("/train", status_code=200)
def train_model(payload: StockIn):
    train(payload.ticker)
    return {"status": "Model trained"}

@app.post("/predict", response_model=StockOut, status_code=200)
def get_prediction(payload: StockIn):
    ticker = payload.ticker
    prediction_list = predict(ticker)
    if not prediction_list:
        raise HTTPException(status_code=400, detail="Model not found.")
    response_object = {"ticker": ticker, "forecast": convert(prediction_list)}
    return response_object
