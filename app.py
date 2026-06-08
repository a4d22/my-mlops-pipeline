import logging
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import joblib
import pandas as pd
import os
from contextlib import asynccontextmanager

# Configure Logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")

# 1. Modern Lifespan Setup
@asynccontextmanager
async def lifespan(app: FastAPI):
    """Handles setup (startup) and teardown (shutdown) operations cleanly."""
    global model
    model_path = "model.pkl"
    
    # --- Startup Logic ---
    if not os.path.exists(model_path):
        logging.error(f"Model file {model_path} not found! Run training first.")
        raise FileNotFoundError("Model serialization artifact missing.")
    
    logging.info(f"Loading model from {model_path}...")
    model = joblib.load(model_path)
    logging.info("Model loaded into memory successfully.")
    
    yield  # The application runs while this yield is active
    
    # --- Shutdown Logic (Clean up resources if needed) ---
    logging.info("Shutting down application and clearing model resources.")
    model = None

# 2. Pass the lifespan manager to FastAPI
app = FastAPI(title="California Housing Prediction Service", lifespan=lifespan)

# Global variable to hold our trained model
model = None

class HousingInputData(BaseModel):
    MedInc: float
    HouseAge: float
    AveRooms: float
    AveBedrms: float
    Population: float
    AveOccup: float
    Latitude: float
    Longitude: float

@app.get("/")
def health_check():
    return {"status": "healthy", "service": "housing-predictor"}

@app.post("/predict")
def predict_housing_value(data: HousingInputData):
    if model is None:
        raise HTTPException(status_code=503, detail="Model is initialized but not loaded.")
    try:
        input_dict = data.model_dump()
        input_df = pd.DataFrame([input_dict])
        prediction = model.predict(input_df)[0]
        logging.info(f"Prediction requested. Resulting value: {prediction:.4f}")
        return {"prediction_med_house_val": float(prediction)}
    except Exception as e:
        logging.error(f"Prediction failed! Details: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server inference error.")