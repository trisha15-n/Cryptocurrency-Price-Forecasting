import pandas as pd
import numpy as np
from src.logger import info, error
import os

def add_features(input_file, output_file):
  try:
    info("Reading Input File.")
    df = pd.read_csv(input_file, parse_dates=['Date'])
    df.sort_values("Date", inplace=True)

    info("Started Feature Engineering")

    #Relative STrength Index
    delta = df['Close'].diff()
    gain = np.where(delta > 0, delta, 0)
    loss = np.where(delta < 0, -delta, 0)
    avg_gain = pd.Series(gain).rolling(window=14).mean()
    avg_loss = pd.Series(loss).rolling(window=14).mean()
    rs = avg_gain / avg_loss
    df['RSI'] = 100 - (100 / (1 + rs))

    #Volatility based features
    df['Middle'] = df['Close'].rolling(window=20).mean()
    df['Upper'] = df['Middle'] + 2 * df['Close'].rolling(window=20).std()
    df['Lower'] = df['Middle'] - 2 * df['Close'].rolling(window=20).std()

    #Lag Features (Prev. day Close Price)
    df['Lag1'] = df['Close'].shift(1)
    df['Lag2'] = df['Close'].shift(2)
    df['Lag3'] = df['Close'].shift(3)

    df['volatility_21'] = df['Daily_Return'].rolling(window=21).std()
    df.dropna(inplace=True)

    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    df.to_csv(output_file, index=False)
    info("Feature Engineering Completed and saved to output file.")
  except Exception as e:
    error(f"Error in Feature Engineering: {e}")
    raise e
  
if __name__ == "__main__":
  add_features("data/BTC-USD_processed.csv", "data/BTC-USD_features.csv")