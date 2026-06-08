import logging
import os
import pandas as pd
from sklearn.datasets import fetch_california_housing
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error
import joblib

# 1. Configure Logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.StreamHandler()
    ]
)

def load_and_preprocess_data():
    """Fetches data and prepares splits."""
    logging.info("Fetching California Housing dataset...")
    housing = fetch_california_housing(as_frame=True)
    df = housing.frame
    
    # Simple feature engineering / definition
    X = df.drop(columns=["MedHouseVal"])
    y = df["MedHouseVal"]
    
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )
    logging.info(f"Data split successful. Training shapes: {X_train.shape}, Test shapes: {X_test.shape}")
    return X_train, X_test, y_train, y_test

def train_model(X_train, y_train):
    """Trains a Random Forest Regressor."""
    logging.info("Initializing Random Forest Regressor...")
    model = RandomForestRegressor(n_estimators=50, max_depth=10, random_state=42, n_jobs=-1)
    
    logging.info("Starting model training (this might take a few seconds)...")
    model.fit(X_train, y_train)
    logging.info("Model training completed successfully.")
    return model

def evaluate_model(model, X_test, y_test):
    """Evaluates the model using Mean Squared Error."""
    logging.info("Evaluating model on test data...")
    predictions = model.predict(X_test)
    mse = mean_squared_error(y_test, predictions)
    logging.info(f"Model Evaluation Metrics -> Mean Squared Error: {mse:.4f}")
    return mse

def save_model(model, filename="model.pkl"):
    """Serializes and saves the trained model artifact."""
    logging.info(f"Saving trained model to local file: {filename}")
    joblib.dump(model, filename)
    logging.info("Model saved successfully.")

# 2. Main Entry Point
if __name__ == "__main__":
    try:
        logging.info("=== Starting MLOps Pipeline Run ===")
        
        # Execute steps sequentially
        X_train, X_test, y_train, y_test = load_and_preprocess_data()
        model = train_model(X_train, y_train)
        evaluate_model(model, X_test, y_test)
        save_model(model, "model.pkl")
        
        logging.info("=== MLOps Pipeline Run Finished Successfully ===")
    except Exception as e:
        logging.critical(f"Pipeline failed! Error details: {str(e)}", exc_info=True)