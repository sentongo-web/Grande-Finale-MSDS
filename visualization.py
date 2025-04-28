import plotly.express as px
import streamlit as st

def plot_import_trends(df):
    fig = px.line(df, x='Import_Duration', y='CIF_Value_USD', 
                 title='Import Value Trends Over Time')
    st.plotly_chart(fig)

def show_geo_distribution(df):
    geo_df = df.groupby('Country_of_Origin', as_index=False)['CIF_Value_USD'].sum()
    fig = px.choropleth(geo_df, locations='Country_of_Origin', 
                       locationmode='country names', color='CIF_Value_USD',
                       title='Import Value by Country')
    st.plotly_chart(fig)

def display_kpi_cards(df):
    total_imports = df['CIF_Value_USD'].sum()
    avg_density = df['Value_Density'].mean()
    
    st.markdown(f"""
    <div class="kpi-card">
        <h3>Total CIF Value</h3>
        <p>${total_imports:,.2f}</p>
    </div>
    <div class="kpi-card">
        <h3>Avg. Value Density</h3>
        <p>${avg_density:,.2f}/kg</p>
    </div>
    """, unsafe_allow_html=True)