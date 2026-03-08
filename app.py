import streamlit as st
import pandas as pd

from ocr_engine import extract_text, extract_amount

st.title("💰 FinTrack AI - Personal Finance Assistant")
st.header("Monthly income")
income = st.number_input("Enter Monthly Income (₹)", min_value=0)
st.header("Add Expense")

amount = st.number_input("Enter Amount (₹)", min_value=0)

category = st.selectbox(
    "Select Category",
    ["Food", "Travel", "Shopping", "Bills", "Other"]
)

description = st.text_input("Description")

if "expenses" not in st.session_state:
    st.session_state.expenses = []

if st.button("Add Expense"):
    expense = {
        "Amount": amount,
        "Category": category,
        "Description": description
    }
    
    st.session_state.expenses.append(expense)
    st.success("Expense added successfully!")

st.header("Expense History")

if st.session_state.expenses:
    df = pd.DataFrame(st.session_state.expenses)
    st.table(df)



# Spending Summary
st.header("📊 Spending Summary")

if st.session_state.expenses:
    df = pd.DataFrame(st.session_state.expenses)

    total_spent = df["Amount"].sum()
    st.metric("Total Money Spent", f"₹{total_spent}")
    if income > 0:
        remaining = income - total_spent
        st.metric("Remaining Budget", f"₹{remaining}")
        saving_rate = (remaining / income) * 100
        st.metric("Saving Rate", f"{saving_rate:.1f}%")


    category_spending = df.groupby("Category")["Amount"].sum()

    st.subheader("Category-wise Spending")
    st.bar_chart(category_spending)
st.header("💡 Financial Insights")

if st.session_state.expenses:
    df = pd.DataFrame(st.session_state.expenses)

    # Insight 1: Highest spending category
    category_totals = df.groupby("Category")["Amount"].sum()
    highest_category = category_totals.idxmax()
    highest_amount = category_totals.max()

    st.write(f"📌 You spend the most on **{highest_category} (₹{highest_amount})**.")

    # Insight 2: Check if any category exceeds 40%
    total_spent = df["Amount"].sum()

    for category, amount in category_totals.items():
        percentage = (amount / total_spent) * 100

        if percentage > 40:
            st.warning(f"⚠ {category} spending is {percentage:.1f}% of your expenses. Consider reducing it.")

    # Insight 3: Saving suggestion
    if total_spent > 5000:
        st.info("💰 Your spending is quite high. Try saving at least 20% of your income.")
    if income > 0 and total_spent > income:
        st.error("🚨You have exceeded your monthly budget!")
    elif total_spent > income * 0.8:
            st.warning("⚠ You have used more than 80% of your budget")

st.header("📷 Upload Payment Screenshot")

uploaded_image = st.file_uploader(
    "Upload a payment screenshot",
    type=["png", "jpg", "jpeg"]
)

if uploaded_image is not None:
    st.image(uploaded_image, caption="Uploaded Screenshot")

    if st.button("Extract Expense"):
        text = extract_text(uploaded_image)

        st.subheader("Extracted Text")
        st.write(text)

        amount = extract_amount(text)

        if amount:
            st.success(f"Detected Amount: ₹{amount}")