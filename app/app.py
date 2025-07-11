import sys
import os
import pandas as pd
from dash import Dash, dcc, html, dash_table, Input, Output

# Add 'src' directory to sys.path for local imports
src_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src"))
sys.path.append(src_path)

# Functions for the data loading and processing steps
from core_logic import load_stock_data, compute_daily_returns, get_correlation_matrix

# Load stock data once at startup
zip_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "stock_data.zip"))
stock_data = load_stock_data(zip_path)
daily_returns = compute_daily_returns(stock_data)

# Filter dates that have the 20-day rolling window available
valid_dates = daily_returns.index[20:].strftime("%Y-%m-%d").tolist()
ticker_list = daily_returns.columns.tolist()

# Initializing the Dash app
app = Dash(__name__)
app.title = "Stock Correlation Explorer"  # Title for the browser tab

app.layout = html.Div([
    html.H2("Stock Correlation Explorer"),

    html.Label("Select Date:"),
    dcc.Dropdown(
        id='date-dropdown',
        options=[{"label": d, "value": d} for d in valid_dates],
        value=valid_dates[-1] if valid_dates else None,
    ),

    html.Label("Select at least 2 Tickers:"),
    dcc.Dropdown(
        id='ticker-dropdown',
        options=[{"label": t, "value": t} for t in ticker_list],
        value=ticker_list[:5],
        multi=True,  # Need multi-select
    ),

    dash_table.DataTable(
        id='correlation-table',
        style_cell={'minWidth': 80, 'textAlign': 'center'},
    ),
])

# Callback that updates the correlation table based on the user's selections in the dropdown
@app.callback(
    Output('correlation-table', 'data'),
    Output('correlation-table', 'columns'),
    Input('date-dropdown', 'value'),
    Input('ticker-dropdown', 'value'),
)
def update_correlation(date_selected, tickers_selected):
    if not tickers_selected or len(tickers_selected) < 2:
        return [], []

    corr_matrix = get_correlation_matrix(daily_returns, tickers_selected, date_selected)

    # Correlation table
    corr_data = corr_matrix.round(3).reset_index().to_dict('records')
    columns = [{"name": col, "id": col} for col in corr_matrix.reset_index().columns]
    return corr_data, columns

if __name__ == "__main__":
    app.run(debug=True)
