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
    ["📊 Dashboard", 
     "📈 Analytical Reports", 
     "🔮 Price Predictions",
     "🌍 About Project"])

# Page routing
if page == "📊 Dashboard":
    import app.pages.dashboard as dashboard
    dashboard.render()
elif page == "📈 Analytical Reports":
    import app.pages.reports as reports
    reports.render()
elif page == "🔮 Price Predictions":
    import app.pages.predictions as predictions
    predictions.render()
elif page == "🌍 About Project":
    import app.pages.about as about
    about.render()

# Adding footer to all pages
st.markdown("""
<div style="text-align: center; margin-top: 2rem; color: #666;">
    <hr style="border: 0.5px solid #ddd;">
    <div style="display: flex; justify-content: center; gap: 20px; margin: 10px 0;">
        <a href="https://www.linkedin.com/in/paul-sentongo-885041284/" target="_blank" style="text-decoration: none; color: #0A66C2;">
            👔 LinkedIn
        </a>
        <a href="https://github.com/sentongo-web" target="_blank" style="text-decoration: none; color: #333;">
            💻 GitHub
        </a>
        <a href="https://www.kaggle.com/sentongogray" target="_blank" style="text-decoration: none; color: #20BEFF;">
            📊 Kaggle
        </a>
    </div>
    <div style="margin-top: 10px;">
        <p style="margin: 5px 0; font-size: 0.9rem;">© 2025 Customs Valuation Intelligence System</p>
        <p style="margin: 5px 0; font-size: 0.9rem;">🔥 Crafted by Paul Sentongo</p>
    </div>
</div>
""", unsafe_allow_html=True)