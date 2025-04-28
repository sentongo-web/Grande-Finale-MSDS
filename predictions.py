import streamlit as st
import pandas as pd
from utils.data_loader import load_model, load_data

def render():
    st.title("🔮 Unit Price Predictor")
    model, preprocessor = load_model()
    
    # Get dynamic options from actual data
    df = load_data()
    countries = df['Country_of_Origin'].unique().tolist()
    ports = df['Port_of_Shipment'].unique().tolist()
    transport_modes = df['Mode_of_Transport'].unique().tolist()
    quantity_units = df['Quantity_Unit'].unique().tolist()

    with st.form("prediction_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            hs_code = st.text_input("HS Code (8-digit)", "15079090")
            item_desc = st.text_input("Item Description", "Machinery Parts")
            country = st.selectbox("Country of Origin", sorted(countries))
            port = st.selectbox("Port of Shipment", sorted(ports))
            quantity_unit = st.selectbox("Quantity Unit", sorted(quantity_units))
            
        with col2:
            quantity = st.number_input("Quantity", min_value=1, value=1)
            net_mass = st.number_input("Net Mass (kg)", min_value=0.1, value=0.15)
            gross_mass = st.number_input("Gross Mass (kg)", min_value=0.1, value=0.17)
            fob_value = st.number_input("FOB Value (USD)", min_value=0.0, value=1000.0)
            freight = st.number_input("Freight Cost (USD)", min_value=0.0, value=200.0)
            insurance = st.number_input("Insurance Cost (USD)", min_value=0.0, value=100.0)
            tax_rate = st.number_input("Tax Rate (%)", min_value=0.0, max_value=100.0, value=18.0) / 100
            year_month = st.number_input("Year-Month (YYYYMM)", min_value=202301, max_value=203012, value=202401)

        submitted = st.form_submit_button("Predict Price")
        
    if submitted:
        try:
            # Calculate derived features
            year = year_month // 100
            month = year_month % 100
            import_duration = year + month/12
            fob_per_kg = fob_value / (gross_mass + 1e-6)
            freight_per_kg = freight / (gross_mass + 1e-6)
            insurance_per_kg = insurance / (gross_mass + 1e-6)
            value_density = (fob_value + freight + insurance) / (gross_mass + 1e-6)
            tax_load = (fob_value + freight + insurance) * tax_rate

            # Create input dataframe
            input_data = pd.DataFrame([{
                'HS_Code': hs_code,
                'Item_Description': item_desc,
                'Country_of_Origin': country,
                'Port_of_Shipment': port,
                'Quantity_Unit': quantity_unit,
                'Quantity': quantity,
                'Net_Mass_kg': net_mass,
                'Gross_Mass_kg': gross_mass,
                'FOB_Value_USD': fob_value,
                'Freight_USD': freight,
                'Insurance_USD': insurance,
                'CIF_Value_USD': fob_value + freight + insurance,
                'Tax_Rate': tax_rate,
                'Mode_of_Transport': 'AIR',  # Default value
                'Currency_Code': 'USD',      # Default value
                'Valuation_Method': 'CIF',   # Default value
                'Year': year,
                'Month': month,
                'FOB_per_kg': fob_per_kg,
                'Freight_per_kg': freight_per_kg,
                'Insurance_per_kg': insurance_per_kg,
                'Value_Density': value_density,
                'Tax_Load': tax_load,
                'Import_Duration': import_duration
            }])

            # Ensure correct column order
            input_data = input_data[preprocessor.feature_names_in_]
            
            # Transform and predict
            processed = preprocessor.transform(input_data)
            prediction = model.predict(processed)[0]
            
            st.success(f"Predicted Unit Price: UGX {prediction:,.0f}")
            
        except Exception as e:
            st.error(f"Prediction failed: {str(e)}")
            st.write("### Debug Information:")
            st.write("Required columns:", preprocessor.feature_names_in_)
            st.write("Provided columns:", input_data.columns.tolist())