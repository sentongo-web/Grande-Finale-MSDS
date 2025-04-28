import streamlit as st
import plotly.express as px
from utils.data_loader import load_data

def render():
    st.title("🌍 About Import Valuation Intelligence")
    
    # Project Overview Section
    with st.container():
        st.header("Project Overview")
        st.markdown("""
        <div style="text-align: justify; line-height: 1.6;">
        **Import Valuation Intelligence** is an innovative solution addressing Uganda's critical challenge 
        of customs valuation discrepancies. Our platform combines advanced machine learning with 
        transparent data visualization to:
        
        - 🔍 Detect anomalous import valuations in real-time
        - 📊 Provide data-driven insights for customs optimization
        - 🤖 Automate price prediction using trade pattern analysis
        - 🌐 Promote fair trade practices through transparency
        
        Developed as part of the MSDS Capstone Project, this system aims to modernize Uganda's customs 
        infrastructure while serving as a model for developing nations.
        </div>
        """, unsafe_allow_html=True)
    
    # Motivation Section
    st.markdown("---")
    col1, col2 = st.columns([1, 2])
    with col1:
        st.image("https://cdn-icons-png.flaticon.com/512/814/814938.png", width=150)
    with col2:
        st.header("Developer's Mission")
        st.markdown("""
        <div style="text-align: justify;">
        *"Witnessing Uganda lose millions annually to trade misinvoicing inspired me to develop 
        this solution. Our goal is to empower customs authorities with AI tools that level the 
        playing field in international trade while maintaining developing countries' competitive 
        edge."*  
        </div>
        """, unsafe_allow_html=True)
    
    # The Problem Section
    st.markdown("---")
    st.header("Uganda's Import Items Valuation Challenge")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Estimated Annual Loss", "$350M", "from trade misinvoicing")
    with col2:
        st.metric("Customs Efficiency", "62%", "of declarations need manual review")
    with col3:
        st.metric("Detection Rate", "<15%", "of undervalued goods identified")
    
    df = load_data().sample(1000)
    fig = px.scatter(
        df, 
        x='CIF_Value_USD', 
        y='Unit_Price_UGX', 
        color='Country_of_Origin',
        title="Discrepancies in Declared Values",
        labels={'CIF_Value_USD': 'Declared Value (USD)', 'Unit_Price_UGX': 'Calculated Unit Price (UGX)'}
    )
    st.plotly_chart(fig, use_container_width=True)
    
    # Technical Architecture
    st.markdown("---")
    st.header("🛠️ Technical Architecture")
    
    with st.expander("See System Design"):
        st.image(
            "https://upload.wikimedia.org/wikipedia/commons/thumb/3/39/ML_Process.png/800px-ML_Process.png",
            caption="Typical ML Pipeline Structure (Source: Wikimedia Commons)",
            use_column_width=True
        )
        st.markdown("""
        **Learn More:**
        - [Machine Learning Pipeline Fundamentals (Quix Blog)](https://quix.io/blog/the-anatomy-of-a-machine-learning-pipeline)
        - [Production ML Systems (Google Cloud)](https://cloud.google.com/architecture/mlops-continuous-delivery-and-automation-pipelines-in-machine-learning)
        """)
        st.markdown("""
        <div style="column-count: 2; text-align: justify;">
        - **Data Integration**: Aggregates 15+ data sources including UN Comtrade and URA records  
        - **Anomaly Detection**: Isolation Forest algorithm identifies suspicious declarations  
        - **Price Prediction**: Gradient Boosting model estimates fair market prices  
        - **Explainable AI**: SHAP values provide transparent decision-making insights  
        - **Real-time Monitoring**: Streamlit-powered dashboard for operational use  
        - **Compliance Tools**: Automated HS Code validation and historical comparisons  
        </div>
        """, unsafe_allow_html=True)

    # 📚 Recommended Reading (another expander — separated now)
    with st.expander("📚 Recommended Reading & References"):
        st.markdown("""
        - [World Bank Trade Misinvoicing Report (2023)](https://www.worldbank.org)
        - [URA Annual Performance Report](https://www.ura.go.ug)
        - [UNCTAD Customs Modernization Guidelines](https://unctad.org)
        - [IMF Revenue Mobilization Strategies](https://www.imf.org)
        """)

    # Footer
    st.markdown("""
    <div style="text-align: center; padding: 20px; background-color: #f0f2f6; border-radius: 10px;">
        <h4>Driving Fair Trade Through Technology</h4>
        <p>An Open Source Initiative · Contribute on <a href="https://github.com">GitHub</a></p>
    </div>
    """, unsafe_allow_html=True)
