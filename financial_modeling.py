import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Function to gather and process financial data
def financial_modeling():
    st.markdown("## Financial Modeling Framework")
    st.markdown("### Input Financial Data")

    # Sidebar for scenario selection
    st.sidebar.subheader("Scenario Selection")
    scenario = st.sidebar.selectbox("Choose Scenario", ["Base Case", "Best Case", "Worst Case"])

    st.markdown(f"### Financial Data - {scenario}")
    
    # Input forms for financial data with detailed descriptions and validation
    revenue = st.number_input("Revenue", min_value=0.0, step=1000.0, format="%.2f", help="Enter the total revenue generated.")
    expenses = st.number_input("Expenses", min_value=0.0, step=1000.0, format="%.2f", help="Enter the total expenses incurred.")
    assets = st.number_input("Assets", min_value=0.0, step=1000.0, format="%.2f", help="Enter the total value of assets.")
    liabilities = st.number_input("Liabilities", min_value=0.0, step=1000.0, format="%.2f", help="Enter the total value of liabilities.")
    equity = st.number_input("Equity", min_value=0.0, step=1000.0, format="%.2f", help="Enter the total equity.")

    # Perform calculations
    profit = revenue - expenses
    net_assets = assets - liabilities

    # Display calculated financial statements in a visually appealing manner
    st.markdown("### Calculated Financial Statements")
    st.write(f"**Profit:** ${profit:,.2f}")
    st.write(f"**Net Assets:** ${net_assets:,.2f}")
    st.write(f"**Equity:** ${equity:,.2f}")

    # Store financial data for further processing
    return {
        "Scenario": scenario,
        "Revenue": revenue,
        "Expenses": expenses,
        "Assets": assets,
        "Liabilities": liabilities,
        "Equity": equity,
        "Profit": profit,
        "Net Assets": net_assets
    }

# Function to calculate and analyze financial ratios with more advanced metrics
def calculate_ratios(financial_data):
    ratios = {}

    # Calculate common financial ratios with conditional formatting and validation
    ratios["Current Ratio"] = financial_data["Assets"] / financial_data["Liabilities"] if financial_data["Liabilities"] > 0 else float('inf')
    ratios["Debt-to-Equity Ratio"] = financial_data["Liabilities"] / financial_data["Equity"] if financial_data["Equity"] > 0 else float('inf')
    ratios["Profit Margin"] = financial_data["Profit"] / financial_data["Revenue"] if financial_data["Revenue"] > 0 else 0.0
    ratios["Return on Assets (ROA)"] = financial_data["Profit"] / financial_data["Assets"] if financial_data["Assets"] > 0 else 0.0
    ratios["Return on Equity (ROE)"] = financial_data["Profit"] / financial_data["Equity"] if financial_data["Equity"] > 0 else 0.0

    # Add more advanced financial metrics
    ratios["Gross Profit Margin"] = (financial_data["Revenue"] - financial_data["Expenses"]) / financial_data["Revenue"] if financial_data["Revenue"] > 0 else 0.0
    ratios["Operating Margin"] = (financial_data["Profit"]) / financial_data["Revenue"] if financial_data["Revenue"] > 0 else 0.0
    ratios["Net Profit Margin"] = (financial_data["Profit"]) / financial_data["Revenue"] if financial_data["Revenue"] > 0 else 0.0

    return ratios

# Function to display and interpret financial ratios
def ratio_analysis(financial_data):
    st.markdown("### Ratio Analysis")
    ratios = calculate_ratios(financial_data)
    
    # Display ratios in columns for better readability
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(label="Current Ratio", value=f"{ratios['Current Ratio']:.2f}", delta=None)
        st.metric(label="Debt-to-Equity Ratio", value=f"{ratios['Debt-to-Equity Ratio']:.2f}", delta=None)

    with col2:
        st.metric(label="Profit Margin", value=f"{ratios['Profit Margin']:.2%}", delta=None)
        st.metric(label="Gross Profit Margin", value=f"{ratios['Gross Profit Margin']:.2%}", delta=None)

    with col3:
        st.metric(label="Operating Margin", value=f"{ratios['Operating Margin']:.2%}", delta=None)
        st.metric(label="Net Profit Margin", value=f"{ratios['Net Profit Margin']:.2%}", delta=None)

    with col4:
        st.metric(label="ROA", value=f"{ratios['Return on Assets (ROA)']:.2%}", delta=None)
        st.metric(label="ROE", value=f"{ratios['Return on Equity (ROE)']:.2%}", delta=None)

    # Provide interpretation of ratios
    st.markdown("#### Interpretation")
    if ratios["Current Ratio"] < 1:
        st.write("The current ratio is below 1, indicating potential liquidity issues.")
    else:
        st.write("The current ratio is healthy, indicating good liquidity.")

    if ratios["Debt-to-Equity Ratio"] > 2:
        st.write("The debt-to-equity ratio is high, indicating potential leverage risk.")
    else:
        st.write("The debt-to-equity ratio is within a healthy range.")

    if ratios["Gross Profit Margin"] < 0.5:
        st.write("The Gross Profit Margin is below 50%, indicating potential efficiency issues.")
    else:
        st.write("The Gross Profit Margin is healthy, indicating good efficiency.")

    if ratios["Operating Margin"] < 0.2:
        st.write("The Operating Margin is below 20%, indicating potential operational inefficiency.")
    else:
        st.write("The Operating Margin is healthy, indicating good operational efficiency.")

# Function to generate advanced financial charts with scenario analysis and interactivity
def financial_charts(financial_data):
    st.markdown("### Financial Charts")

    # Revenue vs Expenses Bar Chart
    df = pd.DataFrame({
        "Category": ["Revenue", "Expenses"],
        "Amount": [financial_data["Revenue"], financial_data["Expenses"]]
    })

    fig = px.bar(df, x="Category", y="Amount", title="Revenue vs Expenses", text_auto=True)
    fig.update_traces(texttemplate='$%{text:.2s}', textposition='outside')
    fig.update_layout(
        title="Revenue vs Expenses",
        xaxis_title="Category",
        yaxis_title="Amount ($)",
        font=dict(
            family="Courier New, monospace",
            size=18,
            color="RebeccaPurple"
        )
    )
    st.plotly_chart(fig, use_container_width=True)

    # Profit and Equity Over Time (Scenario Analysis) Line Chart
    scenario_data = {
        "Scenario": ["Base Case", "Best Case", "Worst Case"],
        "Profit": [financial_data["Profit"] * 1, financial_data["Profit"] * 1.2, financial_data["Profit"] * 0.8],
        "Equity": [financial_data["Equity"] * 1, financial_data["Equity"] * 1.2, financial_data["Equity"] * 0.8]
    }
    df_scenario = pd.DataFrame(scenario_data)

    fig = go.Figure()

    fig.add_trace(go.Scatter(x=df_scenario["Scenario"], y=df_scenario["Profit"],
                             mode='lines+markers', name='Profit',
                             line=dict(color='firebrick', width=4)))
    
    fig.add_trace(go.Scatter(x=df_scenario["Scenario"], y=df_scenario["Equity"],
                             mode='lines+markers', name='Equity',
                             line=dict(color='royalblue', width=4)))

    fig.update_layout(
        title='Scenario Analysis: Profit and Equity',
        xaxis_title='Scenario',
        yaxis_title='Amount ($)',
        font=dict(
            family="Courier New, monospace",
            size=18,
            color="RebeccaPurple"
        ),
        hovermode="x unified"
    )
    
    st.plotly_chart(fig, use_container_width=True)

# Additional in-depth financial metrics analysis
def advanced_metrics_analysis(financial_data):
    st.markdown("### Advanced Metrics Analysis")
    
    # More detailed financial analysis
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("#### Financial Leverage")
        financial_leverage = financial_data["Assets"] / financial_data["Equity"] if financial_data["Equity"] > 0 else float('inf')
        st.write(f"Financial Leverage: {financial_leverage:.2f}")

        st.write("#### Efficiency Ratios")
        asset_turnover = financial_data["Revenue"] / financial_data["Assets"] if financial_data["Assets"] > 0 else 0.0
        st.write(f"Asset Turnover: {asset_turnover:.2f}")
        
        equity_multiplier = financial_data["Assets"] / financial_data["Equity"] if financial_data["Equity"] > 0 else float('inf')
        st.write(f"Equity Multiplier: {equity_multiplier:.2f}")

    with col2:
        st.write("#### Dupont Analysis")
        roe_dupont = financial_data["Profit"] / financial_data["Equity"] if financial_data["Equity"] > 0 else 0.0
        st.write(f"ROE (Dupont Analysis): {roe_dupont:.2%}")
        
        roa_dupont = financial_data["Profit"] / financial_data["Assets"] if financial_data["Assets"] > 0 else 0.0
        st.write(f"ROA (Dupont Analysis): {roa_dupont:.2%}")

    # Interpretations of advanced metrics
    st.markdown("#### Advanced Metrics Interpretation")
    if financial_leverage > 2:
        st.write("High Financial Leverage may indicate excessive debt.")
    else:
        st.write("Financial Leverage is within a healthy range.")

    if asset_turnover < 1:
        st.write("Asset Turnover is low, indicating inefficient use of assets.")
    else:
        st.write("Asset Turnover is good, indicating efficient use of assets.")

    if equity_multiplier > 2:
        st.write("Equity Multiplier is high, indicating that the company is relying heavily on debt.")
    else:
        st.write("Equity Multiplier is within a safe range.")

# Main Financial Modeling Page with enhanced UI and functionality
def financial_modeling_page():
    st.markdown("""
    Welcome to the Financial Modeling Framework. This tool allows you to input detailed financial data,
    perform advanced calculations, analyze key financial ratios, and visualize the results through 
    interactive charts. Ideal for financial analysts, CFOs, and industry professionals seeking
    comprehensive financial insights.
    """)
    
    # Gather financial data from the user
    financial_data = financial_modeling()

    # Perform ratio analysis with advanced interpretation
    ratio_analysis(financial_data)

    # Display advanced metrics analysis
    advanced_metrics_analysis(financial_data)

    # Display graphical representations with scenario analysis
    financial_charts(financial_data)


