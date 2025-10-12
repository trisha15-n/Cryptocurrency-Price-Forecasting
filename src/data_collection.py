import argparse
import yfinance as yf
import pandas as pd
from pathlib import Path
from datetime import datetime
from src.logger import info, error
from src.exception import CustomException
import sys

def fetch_crypto_data(symbol="BTC-USD", start="2020-01-01", end=None):
  try:
    if end is None:
      end = datetime.now().strftime("%Y-%m-%d")
    
    info(f"Fetching data for {symbol} from {start} to {end}")
    Path("data").mkdir(parents=True, exist_ok=True)
    df = yf.download(symbol, start=start, end=end, progress=False)
    
    if df.empty:
      raise CustomException(f"No data found for {symbol} between {start} and {end}")
    
    df.reset_index(inplace=True)
    out_path = Path("data") / f"{symbol}.csv"
    df.to_csv(out_path, index=False)
    info(f"Data saved to {out_path}")
    info(f"Dataframe shape: {df.shape}")
    return df
  

  except Exception as e:
      error(f"Error fetching data: {e}")
      raise CustomException(e)


def main():
  parser = argparse.ArgumentParser(description="Fetch historical cryptocurrency data")

  parser.add_argument("--symbol", type=str, default="BTC-USD", help="Cryptocurrency symbol (default: BTC-USD)")

  parser.add_argument("--start", type=str, default="2020-01-01", help="Start date in YYYY-MM-DD format (default: 2020-01-01)")

  parser.add_argument("--end", type=str, default=None, help="End date in YYYY-MM-DD format (default: today)")
  
  args = parser.parse_args()
  try: 
    df = fetch_crypto_data(symbol=args.symbol, start=args.start, end=args.end)
    if df is not None:
      info(df.head())
  except Exception as e:
    error(f"Failed to fetch data: {e}")    

if __name__ == "__main__":
  main()