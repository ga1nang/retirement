import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import make_interp_spline

# Streamlit app
st.title("Retirement Savings Planner")

# Create two columns with a wider ratio
col1, col2 = st.columns([3, 8])

# Left column for user inputs
with col1:
    st.header("Input")
    # Main parameters
    current_spending = st.number_input("Current Annual Spending (USD)", value=20000, step=1000)
    inflation_rate = st.number_input("Inflation Rate (%)", value=3.0, step=0.1) / 100
    interest_rate = st.number_input("Interest Rate (%)", value=8.0, step=0.1) / 100
    years_to_retirement = st.number_input("Years Until Retirement", value=30, step=1)
    retirement_duration = st.number_input("Retirement Duration (Years)", value=20, step=1)

    # Choose parameter to adjust
    parameter = st.selectbox("Select parameter to adjust", 
                             ["Annual Spending Requirement", "Inflation Rate", "Interest Rate", "Years Until Retirement"])
    
    # Adjustment buttons
    if st.button("Up"):
        if parameter == "Annual Spending Requirement":
            current_spending += 1000  # Increase by 1,000,000 USD
        elif parameter == "Inflation Rate":
            inflation_rate += 0.001  # Increase by 0.1%
        elif parameter == "Interest Rate":
            interest_rate += 0.001  # Increase by 0.1%
        elif parameter == "Years Until Retirement":
            years_to_retirement += 1  # Increase by 1 year

    if st.button("Down"):
        if parameter == "Annual Spending Requirement" and current_spending > 0:
            current_spending -1000  # Decrease by 1,000,000 USD
        elif parameter == "Inflation Rate" and inflation_rate > 0:
            inflation_rate -= 0.001  # Decrease by 0.1%
        elif parameter == "Interest Rate" and interest_rate > 0:
            interest_rate -= 0.001  # Decrease by 0.1%
        elif parameter == "Years Until Retirement" and years_to_retirement > 1:
            years_to_retirement -= 1  # Decrease by 1 year

# Calculations
future_spending = current_spending * (1 + inflation_rate) ** years_to_retirement
adjusted_rate = (1 + interest_rate) / (1 + inflation_rate) - 1
total_needed_at_retirement = future_spending * ((1 - (1 + adjusted_rate) ** -retirement_duration) / adjusted_rate)
annual_deposit = total_needed_at_retirement / (((1 + interest_rate) ** years_to_retirement - 1) / interest_rate)

years = np.arange(1, years_to_retirement + 1)
accumulated_savings = []
current_balance = 0

for year in years:
    current_balance = current_balance * (1 + interest_rate) + annual_deposit
    accumulated_savings.append(current_balance)

x_smooth = np.linspace(years.min(), years.max(), 300)
spl = make_interp_spline(years, accumulated_savings, k=3)
y_smooth = spl(x_smooth)

# Right column for outputs
with col2:
    st.header("Output")
    st.write(f"##### Future Annual Spending Requirement: {future_spending:,.2f} USD")
    st.write(f"##### Total Amount Needed at Retirement: {total_needed_at_retirement:,.2f} USD")
    st.write(f"##### Annual Deposit Required: {annual_deposit:,.2f} USD")

    # Plotting the larger line graph
    fig, ax = plt.subplots(figsize=(9, 5))  # Increase figure size for larger graph
    ax.plot(x_smooth, y_smooth, label='Accumulated Savings', color='b')
    ax.set_title('Accumulated Savings Over Time')
    ax.set_xlabel('Years Until Retirement')
    ax.set_ylabel('Accumulated Savings (USD)')
    ax.grid()
    ax.legend()

    # Display the plot
    st.pyplot(fig)
