# 💳 moneyTracker

**moneyTracker** is a multipage interactive dashboard built with [Dash](https://dash.plotly.com/) that makes tracking your expenses and analyzing spending habits effortless.  

It allows you to upload your credit card statements, categorize transactions, explore spending patterns, and use financial tools like cashback calculators and budgeting helpers — all in one place.

---

## 🌐 Live Demo  

👉 [Try the live demo here](https://ckowel01.pythonanywhere.com)  

> The demo version includes **fake credit card data** for you to explore all the app’s features.  
> (Uploading your own statements is disabled in demo mode.)

---

## 🚀 Features

### 📂 Edit & Upload
- Drag-and-drop or upload **PDF credit card statements** or **CSV/Excel transaction exports**.
- Automatically extracts useful transaction data.
- **Auto-categorizes** transactions using keyword detection.
- Prompts the user to manually edit any transactions it cannot confidently classify.
- Displays reminders for how recently data was updated for each credit card.

---

### 📊 Analysis
- Explore your stored spending data interactively.
- Adjust the timeline (all data, last 12 months, custom year).
- Filter transactions by **category**, **necessity (needs vs wants)**, or **credit card**.
- Visualize:
  - **Monthly spending trends** (line and bar plots).
  - **Average monthly spending** by category.

---

### 💵 Tools / Credit Card Cashback Calculator
- Quickly estimate how much cashback you’d earn with various credit cards.
- Compare against your actual spending data.
- Helps decide whether to:
  - Stick with your current cards,
  - Switch to a new one, or
  - Justify annual-fee cards.

---

### 📈 Tools / 50-30-20 Budgeting
- Simple tool that compares your spending habits against the **50/30/20 rule**:
  - **50% Needs**
  - **30% Wants**
  - **20% Savings**
- Provides real-time feedback on whether you’re meeting the targets.

---

## 🛠️ Tech Stack
- **[Dash](https://dash.plotly.com/)** — multipage dashboard framework.
- **[Plotly](https://plotly.com/python/)** — interactive data visualization.
- **Pandas** — transaction parsing and data wrangling.
- **PDF/CSV/Excel parsing** utilities for transaction ingestion.
- **Bootstrap (via dash-bootstrap-components)** — responsive layout and styling.

---
## 📦 Installation

> **Note**: Currently, moneyTracker is only compatible with **Scotiabank** and **BMO** credit card statements and CSV/Excel exports.

---

### 1. Clone the repository
```bash
git clone https://github.com/your-username/moneyTracker.git
cd moneyTracker
```

### 2. Create and activate a virtual environment
On **macOS/Linux**:  
```bash
python -m venv .venv
source .venv/bin/activate
```

On **Windows**:  
```bash
python -m venv .venv
.venv\Scripts\activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Run the app
```bash
python app.py
```

### 5. Open in browser
Once running, open your browser and go to:  
```
http://127.0.0.1:8050/
```
_(or use the link provided in your terminal after running the app)_
