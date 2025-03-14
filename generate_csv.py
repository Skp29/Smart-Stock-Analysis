# import the required module
import requests
import csv

# fetching the api 
def fetch_daily_data(api_key, symbol):
    url = "https://www.alphavantage.co/query"
    params = {
        "function": "TIME_SERIES_DAILY",
        "symbol": symbol,
        "apikey": api_key
    }
    response = requests.get(url, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error fetching data: {response.status_code}")
        return None
# saving the data to csv file
def save_daily_to_csv(data, filename):
    if "Time Series (Daily)" in data:
        daily_data = data["Time Series (Daily)"]
        with open(filename, mode="w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(["Date", "Open", "High", "Low", "Close", "Volume"])
            for date, values in daily_data.items():
                writer.writerow([
                    date,
                    values["1. open"],
                    values["2. high"],
                    values["3. low"],
                    values["4. close"],
                    values["5. volume"]
                ])
        print(f"CSV file saved to {filename}")
    else:
        print("No data found!")

if __name__ == "__main__":
    API_KEY = "1O2P4P653ACLEDA1"  # Replace with your API key
    SYMBOL = "SHOP"
    FILENAME = "shopify_daily.csv"

    # Fetch and save data
    data = fetch_daily_data(API_KEY, SYMBOL)
    if data:
        save_daily_to_csv(data, FILENAME)
    else:
        print("Failed to fetch data.")