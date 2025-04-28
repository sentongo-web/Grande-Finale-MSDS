import pandas as pd
import joblib
import streamlit as st
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import StandardScaler, OneHotEncoder

# ---- DATA LOADING ----
@st.cache_data
def load_data():
    """Load and preprocess data for dashboard visualizations"""
    df = pd.read_csv('data/Uganda_imports_train.csv')
    
    # Create essential features for reports
    df['Value_Density'] = df['CIF_Value_USD'] / (df['Gross_Mass_kg'] + 1e-6)
    df['Tax_Load'] = df['Tax_Rate'] * df['CIF_Value_USD']
    df['Import_Duration'] = df['Year'] + df['Month']/12
    df['FOB_per_kg'] = df['FOB_Value_USD'] / (df['Gross_Mass_kg'] + 1e-6)
    df['Freight_per_kg'] = df['Freight_USD'] / (df['Gross_Mass_kg'] + 1e-6)
    df['Insurance_per_kg'] = df['Insurance_USD'] / (df['Gross_Mass_kg'] + 1e-6)
    
    return df

# ---- MODEL LOADING ----
@st.cache_resource
def load_model():
    """Load trained model and preprocessor"""
    model = joblib.load('best_price_predictor.pkl')
    return model['model'], model['preprocessor']

# ---- MODELING PREPROCESSING ----
TARGET = 'Unit_Price_UGX'

def preprocess_data(data):
    """Feature engineering for model training/prediction"""
    # Start with dashboard features
    processed = load_data()
    
    # Additional modeling-specific processing
    to_drop = ['CIF_Value_UGX', 'Invoice_Amount', 'Value_per_kg', 
              'Value_per_unit', 'Date']
    
    return processed.drop(columns=to_drop, errors='ignore')

# ColumnTransformer setup
numeric_features = [
    'Quantity', 'Net_Mass_kg', 'Gross_Mass_kg',
    'FOB_Value_USD', 'Freight_USD', 'Insurance_USD',
    'CIF_Value_USD', 'Tax_Rate', 'Tax_Load',
    'Import_Duration', 'Value_Density',
    'FOB_per_kg', 'Freight_per_kg', 'Insurance_per_kg'
]

categorical_features = [
    'HS_Code', 'Country_of_Origin', 'Port_of_Shipment',
    'Quantity_Unit', 'Currency_Code', 'Mode_of_Transport',
    'Valuation_Method', 'Item_Description'
]

preprocessor = ColumnTransformer(
    transformers=[
        ('num', StandardScaler(), numeric_features),
        ('cat', OneHotEncoder(handle_unknown='ignore', sparse_output=False), categorical_features)
    ])