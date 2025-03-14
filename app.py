import os
import csv
import requests
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from flask import Flask, jsonify, render_template
from sklearn.linear_model import LinearRegression

# Flask app setup

app = Flask(__name__)

DATA_FILE = "stock_data.csv"  # CSV file to store the fetched stock data

# Created Stock Analysis class for data processing and model training

class StockAnalysis:
    def __init__(self, filename):
        self.filename = filename
        self.df = None
        self.model = None

    def load_and_clean_data(self):
        """Load CSV data into a DataFrame and compute derived columns."""
        try:
            self.df = pd.read_csv(self.filename)
            # Convert 'Date' to datetime
            self.df['Date'] = pd.to_datetime(self.df['Date'], errors='coerce')
            # Sort by Date
            self.df.sort_values('Date', inplace=True)

            # Convert numeric columns to float
            for col in ['Open', 'High', 'Low', 'Close', 'Volume']:
                self.df[col] = pd.to_numeric(self.df[col], errors='coerce')

            # Remove rows where 'Close' is NaN
            self.df.dropna(subset=['Close'], inplace=True)

            # Compute additional metrics
            self.df['Daily Return'] = self.df['Close'].pct_change().fillna(0)
            self.df['5-Day MA'] = self.df['Close'].rolling(window=5).mean().fillna(method='backfill')
            self.df['Volatility'] = self.df['Close'].rolling(window=5).std().fillna(method='backfill')
            print("[INFO] Data loaded and cleaned.")
        except Exception as e:
            print(f"[ERROR] load_and_clean_data: {e}")

    def train_model(self):
        """Train a simple linear regression model based on 'Days' since earliest date."""
        try:
            if self.df is None or self.df.empty:
                print("[WARNING] No data to train the model.")
                return

            # Create 'Days' feature
            self.df['Days'] = (self.df['Date'] - self.df['Date'].min()).dt.days
            X = self.df[['Days']].values
            y = self.df['Close'].values

            self.model = LinearRegression()
            self.model.fit(X, y)
            print("[INFO] Model trained.")
        except Exception as e:
            print(f"[ERROR] train_model: {e}")

    def predict_future_prices(self, days_ahead=7):
        """Predict future closing prices for the next 'days_ahead' days."""
        try:
            if not self.model or self.df is None or self.df.empty:
                return []

            last_date = self.df['Date'].max()
            future_dates = [last_date + timedelta(days=i) for i in range(1, days_ahead + 1)]
            future_days = [(d - self.df['Date'].min()).days for d in future_dates]
            predicted_prices = self.model.predict(np.array(future_days).reshape(-1, 1))

            return [
                {
                    "Date": d.strftime("%Y-%m-%d"),
                    "Predicted Price": float(p)
                }
                for d, p in zip(future_dates, predicted_prices)
            ]
        except Exception as e:
            print(f"[ERROR] predict_future_prices: {e}")
            return []

    def get_historical_data(self):
        """Return the entire historical data needed for charting."""
        if self.df is None or self.df.empty:
            return []
        # Return only the columns needed for the charts
        df_chart = self.df[['Date', 'Close', '5-Day MA']].copy()
        df_chart['Date'] = df_chart['Date'].dt.strftime('%Y-%m-%d')
        return df_chart.to_dict(orient='records')

    def get_previous_7_days(self):
        """Return the last 7 trading days from the DataFrame."""
        if self.df is None or self.df.empty:
            return []
        df_last_7 = self.df.sort_values('Date').tail(7)
        df_last_7 = df_last_7[['Date', 'Close']].copy()
        df_last_7['Date'] = df_last_7['Date'].dt.strftime('%Y-%m-%d')
        return df_last_7.to_dict(orient='records')

# API

def fetch_daily_data(api_key, symbol="SHOP"):
    """Fetch daily stock data from Alpha Vantage for a given symbol."""
    try:
        url = "https://www.alphavantage.co/query"
        params = {
            "function": "TIME_SERIES_DAILY",
            "symbol": symbol,
            "apikey": api_key,
            "outputsize": "compact"
        }
        response = requests.get(url, params=params)
        if response.status_code == 200:
            return response.json()
        else:
            print(f"[ERROR] fetch_daily_data: HTTP {response.status_code}")
            return None
    except Exception as e:
        print(f"[ERROR] fetch_daily_data: {e}")
        return None

def save_daily_to_csv(data, filename):
    """Save the daily time series data to a CSV file."""
    try:
        if "Time Series (Daily)" not in data:
            print("[ERROR] 'Time Series (Daily)' not in data.")
            return
        ts_daily = data["Time Series (Daily)"]

        with open(filename, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            # CSV header
            writer.writerow(["Date", "Open", "High", "Low", "Close", "Volume"])
            # Sort the data by ascending date
            for date_str in sorted(ts_daily.keys()):
                row = ts_daily[date_str]
                writer.writerow([
                    date_str,
                    row["1. open"],
                    row["2. high"],
                    row["3. low"],
                    row["4. close"],
                    row["5. volume"]
                ])
        print("[INFO] Data saved to CSV.")
    except Exception as e:
        print(f"[ERROR] save_daily_to_csv: {e}")

# Stock Analysis

analysis = StockAnalysis(DATA_FILE)

# Create CSV if it doesn't exist
if not os.path.exists(DATA_FILE):
    with open(DATA_FILE, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(["Date", "Open", "High", "Low", "Close", "Volume"])

# Load data if any, then train model
analysis.load_and_clean_data()
if analysis.df is not None and not analysis.df.empty:
    analysis.train_model()

#Routes

@app.route("/")
def index():
    """Render the main dashboard (served from templates/index.html)."""
    return render_template("index.html")

@app.route("/data", methods=["GET"])
def data():
    """Return the entire historical data for charting."""
    return jsonify(analysis.get_historical_data())

@app.route("/previous-7-days", methods=["GET"])
def previous_7_days():
    """Return the last 7 trading days of actual data."""
    return jsonify(analysis.get_previous_7_days())

@app.route("/predict", methods=["GET"])
def predict():
    """Return the next 7 days predicted prices."""
    return jsonify(analysis.predict_future_prices(days_ahead=7))

@app.route("/fetch-data", methods=["GET"])
def fetch_data():
    """Fetch latest stock data from Alpha Vantage, save, reload, and retrain."""
    api_key = "YOUR_API_KEY"  # <-- Replace with your actual Alpha Vantage API key
    symbol = "SHOP"
    new_data = fetch_daily_data(api_key, symbol)
    if new_data:
        save_daily_to_csv(new_data, DATA_FILE)
        analysis.load_and_clean_data()
        analysis.train_model()
        return jsonify({"message": "Data updated successfully!"})
    else:
        return jsonify({"error": "Failed to fetch data from Alpha Vantage"}), 500

#Main

if __name__ == "__main__":
    app.run(debug=True)
