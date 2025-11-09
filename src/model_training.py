import pandas as pd
import numpy as np
import joblib
from pathlib import Path
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score
from src.logger import info, error
from src.exception import CustomException
import os
import sys

def train_models(input_file):
  try:
    info("Reading data")
    df = pd.read_csv(input_file, parse_dates=['Date'])
    df.sort_values('Date', inplace=True)

    df["Next_Close"] = df["Close"].shift(-1)
    df.dropna(inplace=True)

    features = ['Close', 'Daily_Return', "Volatility", "MA7", 'MA21', 'Upper', 'Lower', "Lag1", "Lag2", "Lag3", "volatility_21"]

    X = df[features]
    y = df["Next_Close"]

    info("Splitting data")
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, shuffle=False
    )

    info("Training Linear Regression model")
    lr = LinearRegression()
    lr.fit(X_train, y_train)

    info("Training Random Forest Regressor model")
    rf = RandomForestRegressor(n_estimators=100, random_state=42)
    rf.fit(X_train, y_train)

    def evaluate_model(model, name):
      y_pred = model.predict(X_test)
      rmse = np.sqrt(mean_squared_error(y_test, y_pred))
      r2 = r2_score(y_test, y_pred)
      info(f"{name} - MSE: {rmse}, R2: {r2}")
      return rmse, r2
    
    lr_rmse, lr_r2 = evaluate_model(lr, "Linear Regression")
    rf_rmse, rf_r2 = evaluate_model(rf, "Random Forest Regressor")

    best_model = rf if rf_r2 > lr_r2 else lr
    best_model_name = "Random Forest Regressor" if rf_r2 > lr_r2 else "Linear Regression"

    os.makedirs('models', exist_ok=True)
    model_path = Path("models") / f"{best_model}_model.pkl"
    joblib.dump(best_model, model_path)
    info(f"Best model: {best_model_name} saved at {model_path}")

  except Exception as e:
    error("Error occurred during model training")
    raise CustomException(e, sys)

if __name__ == "__main__":
  input_file = "data/BTC-USD_features.csv"
  train_models(input_file)    
