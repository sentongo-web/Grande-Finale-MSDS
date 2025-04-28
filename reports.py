import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from utils.data_loader import load_data
from datetime import datetime
import pandas as pd  # Needed for Categorical ordering

def render():
    st.title("📈 Advanced Analytical Reports")
    
    df = load_data()
    
    # Report configuration sidebar
    st.sidebar.header("Report Parameters")
    report_type = st.sidebar.selectbox("Choose Report Type", [
        "Top Import Items", 
        "Country Analysis", 
        "Price & Value Trends",
        "Transport Mode Analysis",
        "Tax Burden Analysis",
        "Monthly/Yearly Trends"
    ])
    
    # Date range selector
    min_year = int(df['Year'].min())
    max_year = int(df['Year'].max())
    selected_years = st.sidebar.slider(
        "Select Year Range",
        min_value=min_year,
        max_value=max_year,
        value=(min_year, max_year)
    )
    
    # Filter data based on year selection
    df = df[(df['Year'] >= selected_years[0]) & (df['Year'] <= selected_years[1])]

    # Dynamic report generation
    if report_type == "Top Import Items":
        st.subheader("Top 10 Imported Items by Value")
        top_items = df.groupby('Item_Description')['CIF_Value_USD'].sum().nlargest(10)
        fig = px.bar(
            top_items,
            orientation='h',
            color=top_items.values,
            labels={'value': 'Total Value (USD)', 'index': 'Item'},
            color_continuous_scale='Bluered'
        )
        fig.update_layout(
            xaxis_title="Total Import Value (USD)",
            yaxis_title="Product Description"
        )
        st.plotly_chart(fig, use_container_width=True)
        
        with st.expander("Data Summary"):
            st.write("Top Items Statistical Summary:")

            summary_df = df[df['Item_Description'].isin(top_items.index)].describe(include='all').T

            # Only format numeric columns
            numeric_cols = summary_df.select_dtypes(include=['float64', 'int64']).columns

            st.dataframe(
                summary_df.style.format({col: "{:.2f}" for col in numeric_cols})
            )

    elif report_type == "Country Analysis":
        st.subheader("Country-wise Import Analysis")
        col1, col2 = st.columns([1, 2])
        
        with col1:
            selected_country = st.selectbox("Select Country", df['Country_of_Origin'].unique())
            country_data = df[df['Country_of_Origin'] == selected_country]
            
            st.metric("Total Imports Value", f"${country_data['CIF_Value_USD'].sum():,.0f}")
            st.metric("Average Tax Load", f"${country_data['Tax_Load'].mean():,.0f}")
            st.metric("Most Common Transport", country_data['Mode_of_Transport'].mode()[0])
        
        with col2:
            fig = px.treemap(
                country_data,
                path=['Item_Description'],
                values='CIF_Value_USD',
                color='Value_Density',
                color_continuous_scale='RdBu',
                title=f"Import Composition from {selected_country}"
            )
            st.plotly_chart(fig, use_container_width=True)

    elif report_type == "Price & Value Trends":
        st.subheader("Price and Value Trend Analysis")
        
        # Create period column
        df['Period'] = df['Year'].astype(str) + '-' + df['Month'].astype(str).str.zfill(2)
        
        tab1, tab2 = st.tabs(["Value Trends", "Price Density Analysis"])
        
        with tab1:
            trend_data = df.groupby('Period')['CIF_Value_USD'].sum().reset_index()
            fig = px.line(
                trend_data,
                x='Period', y='CIF_Value_USD',
                title="Monthly Import Value Trends",
                markers=True
            )
            fig.update_xaxes(title="Month-Year", tickangle=45)
            fig.update_yaxes(title="Total Import Value (USD)")
            st.plotly_chart(fig, use_container_width=True)
        
        with tab2:
            fig = px.scatter(
                df,
                x='Value_Density', y='Unit_Price_UGX',
                color='Country_of_Origin',
                trendline="lowess",
                title="Value Density vs Unit Price",
                labels={'Value_Density': 'Value per kg (USD/kg)'}
            )
            st.plotly_chart(fig, use_container_width=True)

    elif report_type == "Transport Mode Analysis":
        st.subheader("Transportation Mode Impact Analysis")
        
        col1, col2 = st.columns(2)
        
        with col1:
            transport_summary = df.groupby('Mode_of_Transport').agg({
                'CIF_Value_USD': 'sum',
                'Freight_USD': 'mean',
                'Import_Duration': 'mean'
            }).reset_index()
            
            st.write("**Transport Mode Statistics:**")
            st.dataframe(
                transport_summary.style.format({
                    'CIF_Value_USD': "${:,.0f}",
                    'Freight_USD': "${:.2f}",
                    'Import_Duration': "{:.1f} months"
                })
            )
        
        with col2:
            fig = px.sunburst(
                df,
                path=['Mode_of_Transport', 'Country_of_Origin'],
                values='CIF_Value_USD',
                color='Freight_USD',
                color_continuous_scale='Viridis'
            )
            st.plotly_chart(fig, use_container_width=True)

    elif report_type == "Tax Burden Analysis":
        st.subheader("Tax Burden Analysis")
        
        tab1, tab2 = st.tabs(["Tax Distribution", "Tax Impact"])
        
        with tab1:
            fig = px.histogram(
                df,
                x='Tax_Load',
                nbins=50,
                title="Distribution of Tax Burden",
                labels={'Tax_Load': 'Tax Amount (USD)'}
            )
            st.plotly_chart(fig, use_container_width=True)
        
        with tab2:
            tax_impact = df.groupby('Country_of_Origin').agg({
                'Tax_Load': 'sum',
                'CIF_Value_USD': 'sum'
            }).reset_index()
            
            tax_impact['Tax_Percentage'] = (tax_impact['Tax_Load'] / tax_impact['CIF_Value_USD']) * 100
            
            fig = px.bar(
                tax_impact.sort_values('Tax_Percentage', ascending=False),
                x='Country_of_Origin', y='Tax_Percentage',
                title="Tax as Percentage of Import Value by Country"
            )
            st.plotly_chart(fig, use_container_width=True)

    elif report_type == "Monthly/Yearly Trends":
        st.subheader("Temporal Import Patterns")
        
        view_type = st.radio("Select View:", ["Monthly Trends", "Yearly Patterns"])
        
        if view_type == "Monthly Trends":
            df['Month_Name'] = df['Month'].apply(lambda x: datetime(2000, x, 1).strftime('%B'))

            # Correct month order
            month_order = [
                "January", "February", "March", "April", "May", "June",
                "July", "August", "September", "October", "November", "December"
            ]
            df['Month_Name'] = pd.Categorical(df['Month_Name'], categories=month_order, ordered=True)

            monthly_data = df.groupby(['Year', 'Month_Name'])['CIF_Value_USD'].sum().reset_index()

            fig = px.line(
                monthly_data,
                x='Month_Name', y='CIF_Value_USD',
                color='Year',
                markers=True,
                title="Seasonal Import Patterns"
            )
            st.plotly_chart(fig, use_container_width=True)
        
        else:
            yearly_data = df.groupby('Year').agg({
                'CIF_Value_USD': 'sum',
                'Unit_Price_UGX': 'mean',
                'Tax_Load': 'sum'
            }).reset_index()
            
            fig = go.Figure()
            fig.add_trace(go.Bar(
                x=yearly_data['Year'],
                y=yearly_data['CIF_Value_USD'],
                name='Total Value'
            ))
            fig.add_trace(go.Scatter(
                x=yearly_data['Year'],
                y=yearly_data['Unit_Price_UGX'],
                name='Average Price',
                yaxis='y2'
            ))
            
            fig.update_layout(
                title="Yearly Import Trends",
                yaxis=dict(title="Total Import Value (USD)"),
                yaxis2=dict(
                    title="Average Unit Price (UGX)",
                    overlaying='y',
                    side='right'
                )
            )
            st.plotly_chart(fig, use_container_width=True)

    # Add explanatory text
    st.markdown("---")
    with st.expander("How to interpret these reports"):
        st.write("""
        - **Value Density**: USD value per kilogram of imported goods
        - **Tax Load**: Total tax amount calculated as CIF Value × Tax Rate
        - **Import Duration**: Temporal reference combining Year and Month
        - Hover over charts for detailed values
        - Use sidebar filters to focus on specific time periods
        """)

