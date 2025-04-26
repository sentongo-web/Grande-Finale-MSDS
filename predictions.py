import streamlit as st
import joblib
import pandas as pd
from utils.data_loader import load_model

def render():
    st.title("🔮 Unit Price Predictor")
    
    # Load model
    model, preprocessor = load_model()
    
    # Prediction form
    with st.form("prediction_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            hs_code = st.text_input("HS Code (8-digit)")
            country = st.selectbox("Country of Origin", ['China', 'India', 'Germany', 'USA'])
        
        with col2:
            quantity = st.number_input("Quantity", min_value=1)
            weight = st.number_input("Gross Weight (kg)", min_value=0.1)
        
        submitted = st.form_submit_button("Predict Price")
        
    if submitted:
        # Create input DataFrame
        input_data = pd.DataFrame([{
            'HS_Code': hs_code,
            'Country_of_Origin': country,
            'Quantity': quantity,
            'Gross_Mass_kg': weight
        }])
        
        # Preprocess and predict
        processed = preprocessor.transform(input_data)
        prediction = model.predict(processed)[0]
        
        st.success(f"Predicted Unit Price: UGX {prediction:,.0f}")