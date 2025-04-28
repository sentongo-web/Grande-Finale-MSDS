import streamlit as st
import pandas as pd
from utils.data_loader import load_model

def render():
    st.title("🔮 Unit Price Predictor")
    model, preprocessor = load_model()
    
    with st.form("prediction_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            hs_code = st.text_input("HS Code (8-digit)")
            country = st.selectbox("Country of Origin", ['China', 'India', 'Germany', 'USA'])
            cif_value = st.number_input("CIF Value (USD)", min_value=0.0)
            tax_rate = st.number_input("Tax Rate (%)", min_value=0.0, max_value=100.0, value=18.0) / 100
            
        with col2:
            quantity = st.number_input("Quantity", min_value=1)
            net_mass = st.number_input("Net Mass (kg)", min_value=0.1)
            gross_mass = st.number_input("Gross Mass (kg)", min_value=0.1)
            year_month = st.number_input("Year-Month (YYYYMM)", min_value=202301, max_value=203012)
            
        submitted = st.form_submit_button("Predict Price")
        
    if submitted:
        # Calculate derived features
        year = year_month // 100
        month = year_month % 100
        value_density = cif_value / (gross_mass + 1e-6)
        tax_load = cif_value * tax_rate
        import_duration = year + month/12
        
        input_data = pd.DataFrame([{
            'HS_Code': hs_code,
            'Country_of_Origin': country,
            'Quantity': quantity,
            'Net_Mass_kg': net_mass,
            'Gross_Mass_kg': gross_mass,
            'CIF_Value_USD': cif_value,
            'Tax_Rate': tax_rate,
            'Value_Density': value_density,
            'Tax_Load': tax_load,
            'Import_Duration': import_duration,
            'Year': year,
            'Month': month,
            # Add dummy values for other required columns
            'Port_of_Shipment': 'ENTEBBE',  # Example default
            'Quantity_Unit': 'KG',
            'Currency_Code': 'USD',
            'Mode_of_Transport': 'AIR',
            'Valuation_Method': 'CIF'
        }])
        
        processed = preprocessor.transform(input_data)
        prediction = model.predict(processed)[0]
        st.success(f"Predicted Unit Price: UGX {prediction:,.0f}")