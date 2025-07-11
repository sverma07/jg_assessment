import pandas as pd
import zipfile
from io import TextIOWrapper

def load_stock_data(path="../stock_data.zip"):
    """
    Loads stock price data from a ZIP file containing daily CSV files. Assumes each CSV contains Ticker, Date, Price.
    Cleans the data by dropping rows with missing prices, converting the Date column to datetime, removing duplicate dates and tickers, then
    returns a cleaned df with Ticker, Date, Price.
    """
    with zipfile.ZipFile(path) as z:  # Open the zip file
        dfs = [  # List to hold DataFrames for each CSV
            pd.read_csv(TextIOWrapper(z.open(f)))  # Read each CSV inside the zip file
            for f in sorted(z.namelist())  # Sort file names to maintain date order
            if f.endswith(".csv")  # Only process files ending with .csv
        ]
    df = pd.concat(dfs, ignore_index=True)  # Combine all CSVs into one DataFrame and reset the index
    df = df.dropna(subset=["Price", "Ticker"])  # Drop rows where price or ticker is missing
    df["Date"] = pd.to_datetime(df["Date"], errors="coerce")  # Convert Date column to datetime, invalid dates become NaT
    df = df.drop_duplicates(subset=["Date", "Ticker"])  # Remove duplicate (Date, Ticker) combinations
    return df  # Return the cleaned data



def compute_daily_returns(df):
    """
    Calculates a daily percent returns for each ticker where the parameter is the cleaned df from above, then 
    returns a pivoted DataFrame with dates as index, tickers as columns, and daily returns as values.
    """
    pivot = df.pivot(index="Date", columns="Ticker", values="Price")   # Pivot to Date by Ticker matrix to compute correlations later
    returns_df = pivot.pct_change().dropna(how="all")  # Compute daily percent change for each ticker and drop first row with nulls for all tickers
    return returns_df    


def get_correlation_matrix(returns_df, tickers, date):
    """
    Calculates on-the-fly a 20-day rolling correlation matrix for tickers selected by the user ending on the selected date.
    The inputs for this function are the returns_df from above, a list of tickers, and the date. 
    """
    try:
        if len(tickers) < 2: return pd.DataFrame()  # Need at least 2 tickers, otherweise return empty DataFrame
        selected_date = pd.to_datetime(date)  # Convert string to datetime
        if selected_date not in returns_df.index: return pd.DataFrame()  # Date must exist in returns_df
        selected_position = returns_df.index.get_loc(selected_date)  # Find row position of selected date
        if selected_position < 20: return pd.DataFrame()  # Not enough data for 20-day window, then return empty DataFrame
        start = selected_position - 20  # Start of the 20-day window
        end = selected_position         # End 
        window = returns_df.iloc[start:end]  # Slice the 20 rows from the DataFrame
        recent_returns = window[tickers]  # Select only the chosen tickers
        return recent_returns.corr().fillna(0)  # Compute correlation matrix and fill nulls with 0
    except Exception:
        return pd.DataFrame()  # Return empty DataFrame if any error occurs
