import streamlit as st
from utils.data_loader import load_data
from utils.visualization import (plot_import_trends, 
                                show_geo_distribution,
                                display_kpi_cards)

def render():
    st.title("🇺🇬 Real-Time Import Dashboard")
    
    # Load data
    df = load_data()
    
    # KPI Cards
    st.subheader("Key Performance Indicators")
    display_kpi_cards(df)
    
    # Main columns
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("Import Value Trends")
        plot_import_trends(df)
        
    with col2:
        st.subheader("Top Import Partners")
        show_geo_distribution(df)