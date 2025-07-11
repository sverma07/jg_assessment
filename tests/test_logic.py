# Imports
import pandas as pd
import pytest
import os
import sys

# Add 'src' directory to sys.path for local imports so that we can import the functions from the core logic module
src_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src"))
sys.path.append(src_path)

# Import your actual functions (adjust the function names exactly as defined in core_logic.py)
from core_logic import load_stock_data, compute_daily_returns, get_correlation_matrix

# Sample data fixture with aligned dates and prices for 2 tickers
@pytest.fixture     # Using fixture here to keep the sample data consistent across tests and not be repetitive
def sample_data():
    return pd.DataFrame({
        "Date": pd.to_datetime([     # Need data for 22 days to compute 20-day rolling correlation 
            "2025-07-01", "2025-07-02", "2025-07-03", "2025-07-04", "2025-07-07", "2025-07-08", "2025-07-09", "2025-07-10", "2025-07-11", "2025-07-14",
            "2025-07-15", "2025-07-16", "2025-07-17", "2025-07-18", "2025-07-21", "2025-07-22", "2025-07-23", "2025-07-24", "2025-07-25", "2025-07-28",
            "2025-07-29", "2025-07-30"
        ] * 2),
        "Ticker": ["MSFT"] * 22 + ["TSLA"] * 22,
        "Price": [
            410.0, 412.5, 415.0, 413.0, 416.0, 418.0, 420.0, 422.5, 421.0, 423.0, 425.0, 427.5, 429.0, 431.0, 433.0,
            435.0, 437.5, 439.0, 440.0, 442.0, 444.0, 445.0,  # MSFT prices

            680.0, 685.0, 690.0, 688.0, 692.0, 695.0, 698.0, 700.0, 702.5, 705.0, 707.0, 710.0, 712.0, 715.0, 718.0,
            720.0, 723.0, 725.0, 728.0, 730.0, 732.0, 733.0 # TSLA prices
        ]
    })

def test_returns_shape(sample_data):
    returns = compute_daily_returns(sample_data)
    # We expect number of rows to be 21 since we have 22 dates and the first row is null after pct_change since the first row has no previous price to compare
    assert returns.shape[0] == 21


def test_correlation_matrix_empty(sample_data):
    # Take only first 2 days, which is less than the 20-day window, so corr should be empty
    short_data = sample_data[sample_data["Date"] < "2025-07-03"]
    returns = compute_daily_returns(short_data)
    last_date = returns.index[-1]
    corr = get_correlation_matrix(returns, ["MSFT", "TSLA"], last_date)
    assert corr.empty


def test_correlation_matrix_shape(sample_data):
    returns = compute_daily_returns(sample_data)
    # pick the 21st date (index 20) since rolling window needs 20 prior days
    valid_date = returns.index[-1]
    corr = get_correlation_matrix(returns, ["MSFT", "TSLA"], valid_date)
    assert corr.shape == (2, 2)