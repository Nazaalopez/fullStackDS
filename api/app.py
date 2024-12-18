from fastapi import FastAPI, HTTPException, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
import joblib
import numpy as np
import pandas as pd
from io import BytesIO, StringIO
import uvicorn
import csv

app = FastAPI()

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load the model
model = joblib.load('../models/saved_models/random_forest_model.joblib')

@app.get("/")
def read_root():
    return {"message": "Welcome to the Fullstack Data Science End to End Exercise!"}

# Health Check
@app.get("/health/")
async def health_check():
    return {"status": "ok"}

@app.post("/predict/")
async def predict(file: UploadFile = File(...)):
    try:
        # Log 
        print(f'Received file: {file.filename}')

        # Read the uploaded file
        contents = file.file.read()
        input_data = pd.read_csv(BytesIO(contents), encoding='utf-8')

        # Validate the input data
        if len(input_data) != 1:
            raise HTTPException(status_code=400, detail="Please provide only one record for prediction")

        # Define the correct datatypes for pandas
        dtype_dict = {
            'HCP_ID': 'str',
            'PATIENT_AGE': 'Int64',
            'PATIENT_GENDER': 'category',
            'PATIENT_ID': 'str',
            'STATE': 'category',
            'HCP_SPECIALTY': 'category',
            'HCP_AGE': 'Int64',
            'HCP_GENDER': 'category',
            'STATE_NAME': 'category',
            'TXN_LOCATION_TYPE': 'category',
            'INSURANCE_TYPE': 'category',
            'TXN_TYPE': 'category',
            'TXN_DESC': 'category',
            'LOWCONT_COUNT': 'Int64',
            'MEDCONT_COUNT': 'Int64',
            'HIGHCONT_COUNT': 'Int64',
            'NUM_CONDITIONS': 'Int64',
            'NUM_CONTRAINDICATIONS': 'Int64',
            'NUM_SYMPTOMS': 'Int64',
        }

        # Convert columns to the specified data types
        for col, dtype in dtype_dict.items():
            if col in input_data.columns:
                if dtype == 'category':
                    input_data[col] = input_data[col].astype('category')
                elif dtype == 'Int64':
                    input_data[col] = pd.to_numeric(input_data[col], errors='coerce').astype('Int64')
                else:
                    input_data[col] = input_data[col].astype(dtype)

        # Preprocess categorical features
        categorical_columns = input_data.select_dtypes(include=['category']).columns
        input_data = pd.get_dummies(input_data, columns=categorical_columns, drop_first=True)

        # Drop unnecessary columns
        input_data = input_data.drop(columns=['PATIENT_ID', 'TXN_DT', 'HCP_ID'])

        # Ensure all expected columns are present
        expected_columns = model.feature_names_in_
        for col in expected_columns:
            if col not in input_data.columns:
                input_data[col] = False

        # Reorder columns to match the training data
        input_data = input_data[expected_columns]

        # Make prediction
        prediction = model.predict(input_data)

        # Model probabilities
        prediction_probabilities = model.predict_proba(input_data)
        prediction_probabilities = {model.classes_[i]: prob for i, prob in enumerate(prediction_probabilities[0])}

        return {"prediction": prediction[0], "prediction_probabilities": prediction_probabilities}
        #return {"prediction": prediction[0]}

    except Exception as e:
        raise HTTPException(status_code=422, detail=f"Unprocessable Entity: {str(e)}")

if __name__ == "__app__":
    uvicorn.run(app, host="0.0.0.0", port=8000)