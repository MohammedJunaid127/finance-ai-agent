from dotenv import load_dotenv
import os
from openai import OpenAI
load_dotenv()

def extract_pdf_text(file):
    from PyPDF2 import PdfReader

    reader = PdfReader(file)
    text = ""

    for page in reader.pages:
        content = page.extract_text()
        if content:
            text += content

    return text


def summarize_text(text):
    return text[:1500]  # simple and fast summary

def generate_advice(expenses, income, knowledge_text):
    try:
        api_key = os.getenv("OPENAI_API_KEY")

        if not api_key:
            return "API key not found. Please check your .env file."

        client = OpenAI(api_key=api_key)

        # ---------------- BASIC ANALYSIS ----------------
        total_spent = sum([e["Amount"] for e in expenses])

        category_summary = {}
        for e in expenses:
            category_summary[e["Category"]] = category_summary.get(e["Category"], 0) + e["Amount"]

        # Highest category
        highest_category = max(category_summary, key=category_summary.get) if category_summary else "None"

        # Saving rate
        saving_rate = 0
        if income > 0:
            saving_rate = ((income - total_spent) / income) * 100

        # ---------------- FORMAT DATA ----------------
        expense_text = f"Total Spending: ₹{total_spent}\n"
        for cat, amt in category_summary.items():
            expense_text += f"{cat}: ₹{amt}\n"

        # ---------------- SMART PROMPT ----------------
        prompt = f"""
You are an expert financial advisor.

Analyze the user's financial data and provide personalized advice.

User Income: ₹{income}

Spending Breakdown:
{expense_text}

Insights:
- Highest spending category: {highest_category}
- Saving Rate: {saving_rate:.1f}%

Financial Knowledge:
{knowledge_text}

Instructions:
1. Identify 2-3 problem areas
2. Give specific actionable improvements
3. Suggest a savings or budgeting strategy

Return in this format:

1. Problem:
2. Suggestion:
3. Savings Tip:
"""

        # ---------------- API CALL ----------------
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}]
        )

        return response.choices[0].message.content

    except Exception:
        # ---------------- FALLBACK ----------------
        total_spent = sum([e["Amount"] for e in expenses])

        category_summary = {}
        for e in expenses:
            category_summary[e["Category"]] = category_summary.get(e["Category"], 0) + e["Amount"]

        highest_category = max(category_summary, key=category_summary.get) if category_summary else "None"

        return f"""
AI service unavailable.

Smart Analysis:

- Total spent: ₹{total_spent}
- Highest spending: {highest_category}

Advice:
1. Reduce spending in {highest_category}
2. Follow 50/30/20 budgeting rule
3. Track unnecessary expenses
"""
def extract_pdf_text(file):
    from PyPDF2 import PdfReader

    reader = PdfReader(file)
    text = ""

    for page in reader.pages:
        content = page.extract_text()
        if content:
            text += content

    return text