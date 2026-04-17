import matplotlib.pyplot as plt
import streamlit as st
import pandas as pd
import os

st.title(" 💰 Expense Analyser Based On Python ")
st.markdown("Track expenses, analyze spending habits, and visualize trends.")
st.divider()


file_name = "expenses.csv"

if not os.path.exists(file_name):
    df = pd.DataFrame(columns=["Date", "Amount", "Category", "Description"])
    df.to_csv(file_name, index=False)

date = st.date_input("Select Date")
amount = st.number_input("Enter Amount", min_value=1)
category = st.selectbox(
    "Choose Category", ["Food", "Travel", "Shopping", "Bills", "Other"])
description = st.text_input("Description")

if st.button("Add Expense"):
    new_data = pd.DataFrame([[date, amount, category, description]],
                            columns=["Date", "Amount", "Category", "Description"])

    old_data = pd.read_csv(file_name)
    updated = pd.concat([old_data, new_data], ignore_index=True)
    updated.to_csv(file_name, index=False)

    st.success("Expense Added Successfully!")

# Analyses Part


df = pd.read_csv(file_name)

st.subheader("📋 Expense Records")
st.dataframe(df)

if not df.empty:
    total = df["Amount"].sum()
    highest = df["Amount"].max()
    average = df["Amount"].mean()

    st.subheader("📊 Insights")

    col1, col2, col3 = st.columns(3)

    col1.metric("Total Spent", f"₹{total}")
    col2.metric("Highest Expense", f"₹{highest}")
    col3.metric("Average Spend", f"₹{round(average, 2)}")

    # Category Summary
    st.subheader("📈 Category Wise Spending")

    category_data = df.groupby("Category")["Amount"].sum()

    st.bar_chart(category_data)
# Convert Date column
df["Date"] = pd.to_datetime(df["Date"])

# Sidebar Filter
st.sidebar.header("🔍 Filters")

selected_category = st.sidebar.selectbox(
    "Select Category",
    ["All"] + list(df["Category"].unique())
)

if selected_category != "All":
    filtered_df = df[df["Category"] == selected_category]
else:
    filtered_df = df

# Show filtered data
st.subheader("📋 Filtered Records")
st.dataframe(filtered_df)

# Pie Chart
st.subheader("🥧 Spending Distribution")
pie_data = filtered_df.groupby("Category")["Amount"].sum()

fig, ax = plt.subplots(figsize=(5, 5))

ax.pie(
    pie_data.values,
    labels=pie_data.index.tolist(),
    autopct="%1.1f%%",
    startangle=90
)

ax.axis("equal")
ax.set_title("Category Spending")

st.pyplot(fig)

# Monthly Trend
st.subheader("📈 Monthly Spending Trend")

filtered_df["Month"] = filtered_df["Date"].dt.strftime("%Y-%m")

monthly_data = filtered_df.groupby("Month")["Amount"].sum()

st.line_chart(monthly_data)

st.divider()

# Download CSV
with open(file_name, "rb") as file:
    st.download_button(
        label="📥 Download Expense Data",
        data=file,
        file_name="expenses.csv",
        mime="text/csv"
    )

# Danger zone
st.subheader("⚠️ Manage Data")

if st.button("Delete All Records"):
    empty_df = pd.DataFrame(
        columns=["Date", "Amount", "Category", "Description"])
    empty_df.to_csv(file_name, index=False)
    st.success("All records deleted. Refresh page.")
