# 💰 FinTrack AI – Personal Finance Assistant

FinTrack AI is an intelligent personal finance management system that helps users track expenses, analyze spending patterns, and receive AI-powered financial advice.

---

## 🚀 Features

- 💰 Add, Edit, Delete Expenses (CRUD)
- 📅 Date-wise expense tracking
- 📊 Interactive Dashboard (charts & analytics)
- 📷 OCR-based expense extraction from screenshots
- 🤖 AI Financial Advisor (personalized insights)
- 📚 Upload Financial Knowledge (Text + PDF)
- 🔍 Search & Filter expenses
- ⬇ Download expenses as CSV
- 🔐 Login system
- 🗄️ SQLite database storage

---

## 🧠 How It Works

1. User enters income and expenses (manual or OCR)
2. User can upload financial articles or PDFs
3. System analyzes:
   - Spending patterns
   - Highest expense category
   - Saving rate
4. AI generates personalized financial advice

---

## 🛠️ Tech Stack

- Frontend: Streamlit
- Backend: Python
- Database: SQLite
- OCR: Tesseract (pytesseract)
- AI: OpenAI API (with fallback system)
- Visualization: Plotly + Pandas
- PDF Processing: PyPDF2

---

## ⚙️ Installation

```bash
git clone https://github.com/your-username/finance-ai-agent.git
cd finance-ai-agent
pip install -r requirements.txt
streamlit run app.py