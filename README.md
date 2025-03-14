# 📈 Real-Time Stock Analysis Dashboard

This is a Flask-based **Real-Time Stock Analysis Dashboard** that allows users to:

✅ Fetch real-time stock data from [Alpha Vantage](https://www.alphavantage.co/).  
✅ View interactive **closing prices** and **5-day moving averages** on charts.  
✅ Predict the **next 7 days** of stock prices using a **Linear Regression** model.  
✅ Review the **previous 7 days** of actual stock performance.  
✅ Download and work with the data locally via a generated CSV.

> 💡 **Important**: Always use your **latest Alpha Vantage API key** in the `app.py` file for the most up-to-date stock analysis.

---

---

## 🚀 Features

- 📊 **Interactive Charts** using Chart.js
- 📅 View **historical closing prices** and **moving averages**
- 🤖 **Linear Regression model** predicts next 7 days
- 🔄 Fetch fresh data anytime using your API
- 📥 Export and download the dataset (`stock_data.csv`)

---

## ⚙️ Setup Instructions

1. **Clone the repository**  
   ```bash
   git clone https://github.com/Skp29/Smart-Stock-Analysis.git
   cd stock-dashboard
2. **Install dependencies**
   ```bash
   pip install flask requests pandas scikit-learn
   
3. **Install dependencies** ***Insert your Alpha Vantage API key***
  Open app.py and replace:
  api_key = "YOUR_API_KEY" #with your own api
  with your actual Alpha Vantage API key from https://www.alphavantage.co/support/#api-key.
4. **Run the application**
   ```bash
   python app.py

**How It Works**

Backend:
Fetches data from Alpha Vantage (/fetch-data)
Saves data to stock_data.csv
Trains a simple regression model
Serves predictions (/predict)
Exposes last 7 days data (/previous-7-days)
Serves historical chart data (/data)

**Frontend**
Uses Chart.js to display line graphs for closing prices and 5-day MA
Fetches predictions and recent data via AJAX
Interactive buttons for:
Updating data
Getting predictions
Viewing last 7 actual days

**Screenshots**

**Predictions & Actuals Display**
![Screenshot 2025-03-13 200442](https://github.com/user-attachments/assets/c94eac3c-dd0e-456f-930e-4c5d0fdb3136)

Lists the next 7 days of predicted prices using linear regression and previous 7 days of real market data.


The rest of the Screenshots are in the static folder, kindly check

🙋‍♂️ **Author**
Sumit Pandey

📍 Ottawa, Canada

📧 Email: pand0106@algonquinlive.com

🔗 https://www.linkedin.com/in/skp0209/

 **License**
This project is licensed for personal, academic, and educational use. You're free to fork, modify, and distribute it with credit.

