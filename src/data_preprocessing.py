import pandas as pd
from pathlib import Path
from src.logger import info, error
from src.exception import CustomException
import sys

def preprocess_data(symbol="BTC-USD"):
  try:
    input_path = Path("data") / f"{symbol}.csv"
    if not input_path.exists():
      raise CustomException(f"Input file {input_path} does not exist.", sys)
    
    info("loading data")
    df = pd.read_csv(input_path)

    numeric_cols = ['Open', 'High', 'Low', 'Close', 'Adjusted Close', "Volume"]
    for col in numeric_cols :
      if col in df.columns:
        df[col] = pd.to_numeric(df[col], errors='coerce')

    df.dropna(inplace=True)
    df['Date'] = pd.to_datetime(df['Date'])
    df.sort_values(by='Date', inplace=True)

    df['Daily_Return'] = df['Close'].pct_change()
    df['Volatility'] = df['Daily_Return'].rolling(window=7).std()
    df['MA7'] = df['Close'].rolling(window=7).mean()
    df['MA21'] = df['Close'].rolling(window=21).mean()

    df.dropna(inplace=True)
    output_path = Path("data") / f"{symbol}_processed.csv"
    df.to_csv(output_path, index=False)
    info(f"preprocessed data saved to {output_path}")
    info(f"Dataset shape after preprocessing: {df.shape}")
    info(f"Top 5 rows:\n{df.head()}")

    return df
  except Exception as e:
    error(f"Error in data preprocessing: {e}")
    raise CustomException(e, sys)
  

def main():
  import argparse
  parser = argparse.ArgumentParser(description="Preprocess cryptocurrency data.")
  parser.add_argument("--symbol", default="BTC-USD")
  args = parser.parse_args()

  try:
    df = preprocess_data(args.symbol)
    info("Data preprocessing completed successfully.")
  except Exception as e:
    error(f"Data preprocessing failed: {e}")

if __name__ == "__main__":
  main()      

