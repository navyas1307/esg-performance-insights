#extraction
import yfinance as yf
import pandas as pd
import time

# List of 50 company tickers
tickers = [
    "AAPL", "MSFT", "GOOGL", "AMZN", "TSLA", "META", "NVDA", "INTC", "ORCL", "IBM",
    "JPM", "BAC", "GS", "WFC", "C", "AXP", "BRK-B", "JNJ", "PFE", "MRK",
    "ABBV", "LLY", "PG", "KO", "PEP", "WMT", "HD", "MCD", "NKE", "XOM",
    "CVX", "BP", "SHEL", "GE", "BA", "CAT", "LMT", "RTX", "MMM", "VZ",
    "T", "TMUS", "DIS", "NFLX", "CMCSA", "F", "GM", "TM", "HMC","ADBE", "PYPL", "CSCO", "QCOM", "TXN", "AVGO", "AMD", "SHOP", "CRM", "SAP",
    "BABA", "TSM", "UBER", "LYFT", "SQ", "ZM", "SNOW", "INTU", "DOCU", "TWLO",
    "NFLX", "ROKU", "EA", "TTD", "ATVI", "SBUX", "TGT", "LOW", "COST", "DG",
    "FDX", "UPS", "NSC", "UNP", "LUV", "DAL", "AAL", "UAL", "EXPE", "BKNG",
    "MAR", "HLT", "V", "MA", "AXP", "DFS", "COF", "BLK", "SPGI", "MS"
]

# List to store ESG data
esg_data_list = []

# Function to flatten nested ESG data
def flatten_esg_data(esg_dict, ticker):
    flat_data = {}
    for key, value in esg_dict.items():
        flat_data[key] = value[0] if isinstance(value, (list, tuple)) else value
    flat_data["Ticker"] = ticker
    return flat_data

# Fetch ESG data for each ticker
for ticker in tickers:
    try:
        stock = yf.Ticker(ticker)
        esg_data = stock.sustainability

        if esg_data is not None:
            esg_dict = esg_data.to_dict()
            cleaned_data = flatten_esg_data(esg_dict, ticker)
            esg_data_list.append(cleaned_data)
            print(f"Retrieved ESG data for {ticker}")
        else:
            print(f"No ESG data available for {ticker}")

        # Add delay to avoid rate limits
        time.sleep(1)

    except Exception as e:
        print(f"Error retrieving data for {ticker}: {e}")

# Convert to DataFrame and export to CSV
if esg_data_list:
    df = pd.DataFrame(esg_data_list)

    # Rename columns for better readability
    df.columns = df.columns.str.replace('_score', ' Score').str.title()

    # Save cleaned data to CSV
    df.to_csv("ESG_data_cleaned.csv", index=False)
    print("ESG data successfully saved to ESG_data_cleaned.csv")
else:
    print("No ESG data retrieved.")

# Display the first few rows
print(df.head())



#fixing format
import pandas as pd
import ast

# Load the CSV file

