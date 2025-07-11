# Stock Correlation Explorer

This is a simple web app for users to explore how different stocks move together over time. It calculates the 20-day rolling correlation of daily returns between selected stocks. The app is built with Dash, uses pandas for data manipulation, and the correlation window is fixed at 20 days.

## App Logic

- **Data Loading:** Reads daily stock price CSV files inside a ZIP file called stock_data.zip, each with 3 columns: tickers, dates, and prices. The function cleans the data by removing missing prices, converting dates, and dropping duplicates.

- **Return Calculation:** Calculates returns daily for each ticker from the cleaned prices.

- **Correlation Calculation:** Calculates the correlation matrix of their returns over the previous 20 trading days with given tickers and dates.

- **User Interface:** The app has dropdowns to select the date and at least two tickers. After the user selects, it displays a table of the correlation coefficients.


## Running the App

1. Use the code below to clone the repo and go to the `app` folder:

```bash
git clone https://github.com/sverma07/jg_assessment.git
cd jg_assessment/app
```

2. Install the necessary Python packages:
```pip install -r requirements.txt```

3. Make sure the stock_data.zip file is in the project's root directory (root/stock_data.zip).

4. Start the app by running: 
```python app.py```

5. Open browser and go to: http://127.0.0.1:8050

6. Make sure pytest is installed (already in requirements.txt), then run tests from the terminal: ```python -m pytest test_logic.py```