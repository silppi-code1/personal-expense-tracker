"""
Personal Finance Expense Tracker - Analysis & Forecasting
Reads the RAW transaction log from Excel (not the formula-based summary,
which avoids any issue with Excel not having recalculated cached values),
analyzes spending patterns, and forecasts next month's total spending
using linear regression.
"""
import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

# ---------- 1. Load RAW transactions (not the formula summary sheet) ----------
df = pd.read_excel("Expense_Tracker.xlsx", sheet_name="Transactions")
df = df.dropna(subset=["Date", "Category", "Amount"])  # drop the "Total" row at the bottom
df["Date"] = pd.to_datetime(df["Date"])
df["Month"] = df["Date"].dt.to_period("M").astype(str)

# ---------- 2. Compute monthly totals directly in Python ----------
monthly_totals = df.groupby("Month")["Amount"].sum().sort_index()
months = monthly_totals.index.tolist()

print("=== Monthly Totals ===")
print(monthly_totals.round(2))

# ---------- 3. Spending pattern analysis ----------
category_totals = df.groupby("Category")["Amount"].sum().sort_values(ascending=False)
print("\n=== Total Spend by Category ===")
print(category_totals.round(2))

avg_monthly = monthly_totals.mean()
print(f"\nAverage monthly spend: ${avg_monthly:,.2f}")

top_category = category_totals.index[0]
top_pct = 100 * category_totals.iloc[0] / category_totals.sum()
print(f"Biggest expense category: {top_category} ({top_pct:.1f}% of total spend)")

needs = ["Food", "Transport", "Rent", "Utilities", "Health"]
wants = ["Entertainment", "Shopping", "Education"]
needs_total = category_totals.reindex(needs).fillna(0).sum()
wants_total = category_totals.reindex(wants).fillna(0).sum()
needs_pct = 100 * needs_total / (needs_total + wants_total)
wants_pct = 100 * wants_total / (needs_total + wants_total)
print(f"Needs vs Wants: ${needs_total:,.2f} vs ${wants_total:,.2f} "
      f"({needs_pct:.1f}% / {wants_pct:.1f}%)")

# ---------- 4. Forecast next month's total spending ----------
X = np.arange(len(months)).reshape(-1, 1)
y = monthly_totals.values

model = LinearRegression()
model.fit(X, y)

forecast = model.predict(np.array([[len(months)]]))[0]
r2 = model.score(X, y)

print(f"\n=== Forecast ===")
print(f"Trend slope: ${model.coef_[0]:,.2f} change per month")
print(f"Predicted next month's total spending: ${forecast:,.2f}")
print(f"Model fit (R^2): {r2:.3f}")

# ---------- 5. Save chart ----------
plt.figure(figsize=(10, 5))
plt.plot(months, y, marker="o", label="Actual monthly spend", color="#2F5597")
trend_line = model.predict(X)
plt.plot(months, trend_line, linestyle="--", color="gray", label="Trend line")
plt.scatter(["Forecast"], [forecast], color="red", zorder=5, label="Next month forecast")
plt.plot([months[-1], "Forecast"], [y[-1], forecast], linestyle=":", color="red")
plt.xticks(rotation=45)
plt.ylabel("Total Spend ($)")
plt.title("Monthly Spending Trend & Next-Month Forecast")
plt.legend()
plt.tight_layout()
plt.savefig("spending_trend_forecast.png", dpi=150)
print("\nSaved chart: spending_trend_forecast.png")

# ---------- 6. Save text report ----------
with open("insights_report.txt", "w") as f:
    f.write("PERSONAL FINANCE - EXPENSE INSIGHTS REPORT\n")
    f.write("=" * 45 + "\n\n")
    f.write(f"Average monthly spend: ${avg_monthly:,.2f}\n")
    f.write(f"Biggest expense category: {top_category} ({top_pct:.1f}% of total spend)\n")
    f.write(f"Needs vs Wants split: {needs_pct:.1f}% / {wants_pct:.1f}%\n\n")
    f.write("Category totals:\n")
    for cat, val in category_totals.items():
        f.write(f"  {cat:<15} ${val:,.2f}\n")
    f.write(f"\nForecast for next month: ${forecast:,.2f}\n")
    f.write(f"Trend: spending is {'increasing' if model.coef_[0] > 0 else 'decreasing'} "
            f"by ~${abs(model.coef_[0]):,.2f}/month\n")
    f.write(f"Model R^2: {r2:.3f}\n")

print("Saved report: insights_report.txt")