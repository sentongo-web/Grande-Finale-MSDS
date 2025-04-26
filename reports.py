import streamlit as st
import plotly.express as px
from utils.data_loader import load_data

def render():
    st.title("📈 Custom Analytical Reports")
    
    df = load_data()
    
    # Report configuration
    st.sidebar.header("Report Parameters")
    report_type = st.sidebar.selectbox("Choose Report Type", 
        ["Top Import Items", "Country Analysis", "Price Trends"])
    
    # Dynamic report generation
    if report_type == "Top Import Items":
        st.subheader("Top 10 Imported Items")
        top_items = df.groupby('Item_Description')['CIF_Value_USD'].sum().nlargest(10)
        fig = px.bar(top_items, orientation='h', 
                    color=top_items.values,
                    labels={'value': 'Total Value (USD)'})
        st.plotly_chart(fig, use_container_width=True)
    
    elif report_type == "Country Analysis":
        st.subheader("Country-wise Import Statistics")
        selected_country = st.selectbox("Select Country", df['Country_of_Origin'].unique())
        country_data = df[df['Country_of_Origin'] == selected_country]
        
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Total Imports", f"${country_data['CIF_Value_USD'].sum():,.0f}")
        with col2:
            st.metric("Average Unit Price", f"UGX {country_data['Unit_Price_UGX'].mean():,.0f}")
        
        fig = px.pie(country_data, names='Item_Description', 
                    values='CIF_Value_USD',
                    title=f"Item Distribution from {selected_country}")
        st.plotly_chart(fig, use_container_width=True)