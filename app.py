import streamlit as st
import pandas as pd
import os
from datetime import date
import plotly.express as px

from ocr_engine import extract_text, extract_amount, extract_merchant
from database import add_expense_db, get_expenses_db
from advisor import generate_advice
from dotenv import load_dotenv
from advisor import generate_advice, extract_pdf_text, summarize_text   

# ---------------- LOAD API KEY ----------------
load_dotenv(dotenv_path="advisorapi.env")
api_key = os.getenv("OPENAI_API_KEY")

if api_key:
    os.environ["OPENAI_API_KEY"] = api_key

# ---------------- LOGIN SYSTEM ----------------
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

def login():
    st.title("🔐 FinTrack AI Login")
    col1, col2, col3 = st.columns([1, 2, 1])

    with col2:
        username = st.text_input("Username", key="login_user")
        password = st.text_input("Password", type="password", key="login_pass")

        if st.button("Login"):
            if username.strip() == "admin" and password.strip() == "1234":
                st.session_state.logged_in = True
                st.rerun()
            else:
                st.error("Invalid username or password")

def logout():
    st.session_state.logged_in = False
    st.rerun()

if not st.session_state.logged_in:
    login()
    st.stop()

# ---------------- HEADER ----------------
h1, h2 = st.columns([6,1])
h1.title("💰 FinTrack AI")
if h2.button("🚪 Logout"):
    logout()

# ---------------- SESSION ----------------
if "expenses" not in st.session_state:
    try:
        data = get_expenses_db()
        st.session_state.expenses = [
            {"Amount": r[0], "Category": r[1], "Description": r[2], "Date": str(date.today())}
            for r in data
        ] if data else []
    except:
        st.session_state.expenses = []

if "knowledge" not in st.session_state:
    st.session_state.knowledge = ""

# ---------------- INPUT ----------------
income = st.number_input("Monthly Income (₹)", min_value=0)

# ---------------- TABS ----------------
tab1, tab2, tab3, tab4 = st.tabs(["💰 Expenses", "📊 Dashboard", "📷 OCR", "🤖 Advisor"])

# ================= TAB 1 =================
with tab1:
    st.header("Add Expense")

    amount = st.number_input("Amount", min_value=0, key="amt")
    category = st.selectbox("Category", ["Food","Travel","Shopping","Bills","Other"], key="cat")
    description = st.text_input("Description", key="desc")

    if st.button("Add Expense"):
        if amount > 0:
            exp = {
                "Amount": amount,
                "Category": category,
                "Description": description,
                "Date": str(date.today())
            }
            st.session_state.expenses.append(exp)

            try:
                add_expense_db(amount, category, description)
            except:
                pass

            st.success("Added!")

    # 🔍 SEARCH
    search = st.text_input("Search")

    data = st.session_state.expenses
    if search:
        data = [e for e in data if search.lower() in e["Description"].lower()]

    # LIST
    for i, exp in enumerate(data):
        c1, c2, c3, c4, c5 = st.columns([2,2,3,1,1])
        c1.write(f"₹{exp['Amount']}")
        c2.write(exp["Category"])
        c3.write(exp["Description"])

        if c4.button("✏️", key=f"edit_{i}"):
            st.session_state.edit_index = i

        if c5.button("🗑️", key=f"del_{i}"):
            st.session_state.expenses.pop(i)
            st.rerun()

    # EDIT
    if "edit_index" in st.session_state:
        i = st.session_state.edit_index
        exp = st.session_state.expenses[i]

        st.subheader("Edit Expense")

        new_amt = st.number_input("Amount", value=exp["Amount"])
        new_cat = st.selectbox("Category", ["Food","Travel","Shopping","Bills","Other"],
                               index=["Food","Travel","Shopping","Bills","Other"].index(exp["Category"]))
        new_desc = st.text_input("Description", value=exp["Description"])

        if st.button("Save"):
            st.session_state.expenses[i] = {
                "Amount": new_amt,
                "Category": new_cat,
                "Description": new_desc,
                "Date": exp["Date"]
            }
            del st.session_state.edit_index
            st.rerun()

# ================= TAB 2 =================
with tab2:
    st.header("Dashboard")

    if st.session_state.expenses:
        df = pd.DataFrame(st.session_state.expenses)

        total = df["Amount"].sum()

        c1, c2 = st.columns(2)
        c1.metric("Total", f"₹{total}")

        if income > 0:
            c2.metric("Remaining", f"₹{income-total}")

        # BAR
        st.bar_chart(df.groupby("Category")["Amount"].sum())

        # PIE
        fig = px.pie(df, names="Category", values="Amount")
        st.plotly_chart(fig)

        # CSV
        st.download_button("Download CSV", df.to_csv(index=False), "expenses.csv")

# ================= TAB 3 =================
with tab3:
    st.header("OCR")

    img = st.file_uploader("Upload", type=["png","jpg","jpeg"])

    if img:
        st.image(img)

        if st.button("Extract"):
            text = extract_text(img)
            st.text_area("OCR", text)

            amt = extract_amount(text)
            merchant = extract_merchant(text)

            if amt:
                st.session_state.expenses.append({
                    "Amount": amt,
                    "Category": "Other",
                    "Description": merchant,
                    "Date": str(date.today())
                })
                st.success("Added!")

# ================= TAB 4 =================
with tab4:
    st.header("🤖 AI Financial Advisor")

    # Manual knowledge input
    knowledge_input = st.text_area("Enter financial knowledge")

    if knowledge_input:
        st.session_state.knowledge = knowledge_input

    # PDF Upload
    st.subheader("📚 Upload Financial PDF")

    uploaded_pdf = st.file_uploader("Upload PDF", type=["pdf"])

    pdf_text = ""

    if uploaded_pdf:
        try:
            raw_text = extract_pdf_text(uploaded_pdf)

            # Apply summarization (OPTION C)
            pdf_text = summarize_text(raw_text)

            st.success("PDF processed successfully!")

            # Optional preview
            with st.expander("Preview PDF Content"):
                st.write(pdf_text[:500])

        except:
            st.error("Error reading PDF")

    # Combine knowledge
    final_knowledge = st.session_state.knowledge + "\n" + pdf_text

    # Generate Advice
    if st.button("Generate Advice"):
        if st.session_state.expenses and income > 0:

            advice = generate_advice(
                st.session_state.expenses,
                income,
                final_knowledge
            )

            st.subheader("📊 Personalized Advice")
            st.write(advice)

        else:
            st.warning("Add expenses and income first.")