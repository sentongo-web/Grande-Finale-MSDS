import streamlit as st
from PIL import Image

# Page configuration
st.set_page_config(
    page_title="Uganda Import Analytics",
    page_icon="🇺🇬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
with open('app/assets/style.css') as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

# Main navigation
st.sidebar.title("Navigation")
page = st.sidebar.radio("Choose a page:", 
    ["📊 Dashboard", "📈 Analytical Reports", "🔮 Price Predictions"])

# Page routing
if page == "📊 Dashboard":
    import app.pages.dashboard as dashboard
    dashboard.render()
elif page == "📈 Analytical Reports":
    import app.pages.reports as reports
    reports.render()
else:
    import app.pages.predictions as predictions
    predictions.render()