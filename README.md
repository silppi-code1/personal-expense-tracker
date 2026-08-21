💰 Personal Finance Expense Tracker with Insights

An end-to-end personal finance analytics project that combines Excel (data cleaning & aggregation), Python (analysis & machine learning), and a forecasting model to turn raw expense data into actionable spending insights.

📑 Table of Contents
About This Project
Problem Statement
Tech Stack
Project Structure
Methodology
1. Data Generation / Ingestion
2. Data Cleaning in Excel
3. Analysis in Python
4. Forecasting Model
5. Visualization
Key Findings
How to Reproduce
Challenges & Fixes
Limitations
Next Steps
Author
About This Project

Most people track expenses in a spreadsheet and stop there. This project goes a step further — it builds a small but complete data pipeline that:

Logs and cleans expense data in Excel, using real formulas (not hardcoded numbers) so the summary updates automatically if the underlying data changes.
Analyzes spending patterns in Python (pandas) — category breakdowns, needs-vs-wants ratio, and monthly trends.
Builds a simple machine learning model (scikit-learn linear regression) to forecast next month's total spending.
Outputs a visual chart and a plain-text insights report summarizing the findings.

The goal is to demonstrate a practical, reproducible workflow that mirrors how personal or small-business finance data might actually be analyzed — moving smoothly between a spreadsheet layer (familiar, editable, shareable) and a code layer (repeatable, extensible, and capable of prediction).

Problem Statement

Manually tracking expenses in a spreadsheet answers "what did I spend?" but rarely answers the more useful questions:

Which category is quietly eating the largest share of my budget?
Am I spending more on needs or wants, and is that ratio healthy?
Is my monthly spending trending up, down, or staying flat?
Based on my history, what should I expect to spend next month — and can I plan around it?

This project answers all four using a combination of spreadsheet aggregation and a lightweight predictive model.

Tech Stack
Layer	Tool	Purpose
Data cleaning & aggregation	Microsoft Excel (openpyxl)	Transaction log + formula-driven monthly summary
Data analysis	Python (pandas)	Category totals, monthly trends, needs vs. wants split
Machine learning	scikit-learn (Linear Regression)	Forecast next month's total spend
Visualization	Matplotlib	Spending trend chart with forecast overlay
(Optional extension)	Power BI	Interactive dashboard on top of the Excel output
Project Structure
expense-tracker-insights/
│
├── generate_data.py            # Creates a 12-month sample expense dataset
├── raw_expenses.csv            # Generated raw transaction data (Date, Category, Type, Amount)
│
├── build_excel.py              # Builds the Excel workbook from raw_expenses.csv
├── Expense_Tracker.xlsx        # Excel deliverable — 2 sheets (see below)
│
├── analyze_forecast.py         # Reads Excel data, analyzes trends, forecasts next month
├── spending_trend_forecast.png # Output chart: actual spend + trend + forecast
├── insights_report.txt         # Output: plain-text summary of key findings
│
└── README.md
Inside Expense_Tracker.xlsx
Sheet	Contents
Transactions	Raw, cleaned transaction log — Date, Category, Type (Needs/Wants), Amount. ~725 rows across 12 months. Includes a SUM() total row.
Monthly Summary	Category × Month matrix built with SUMIFS formulas that reference the Transactions sheet directly — so the summary recalculates automatically if you edit or add transactions.
Methodology
1. Data Generation / Ingestion

generate_data.py produces a realistic 12-month synthetic dataset across 8 spending categories (Food, Transport, Rent, Utilities, Entertainment, Shopping, Health, Education), with randomized but plausible transaction frequency and amounts (e.g., rent charged once a month, groceries several times a week).

In a real-world version of this project, this step would be replaced by importing an actual bank/UPI statement export instead of synthetic data.

2. Data Cleaning in Excel

build_excel.py uses openpyxl to programmatically build a clean, formatted Excel workbook from the raw CSV:

Consistent date formatting, currency formatting, header styling, and frozen header rows for readability.
A Monthly Summary sheet built entirely from SUMIFS formulas — e.g.:
  =SUMIFS(Transactions!$D$2:$D$726,
          Transactions!$B$2:$B$726, $A2,
          Transactions!$A$2:$A$726, ">="&DATE(2025,9,1),
          Transactions!$A$2:$A$726, "<"&EDATE(DATE(2025,9,1),1))

This sums all transactions matching a given category and month directly from the raw log — so if new transactions are added to the Transactions sheet, the summary updates automatically without any manual recalculation.

3. Analysis in Python

analyze_forecast.py loads the cleaned transaction data with pandas and computes:

Monthly totals (grouped by month)
Category totals, ranked to identify the largest spending category
Needs vs. Wants split — categories are tagged as "Needs" (Food, Transport, Rent, Utilities, Health) or "Wants" (Entertainment, Shopping, Education), and the ratio between them is calculated
4. Forecasting Model

A simple Linear Regression model (scikit-learn) is fit on the 12 monthly totals, treating each month as a sequential index (0–11), to predict the 13th month's (next month's) total spend:

python
model = LinearRegression()
model.fit(X, y)              # X = month index, y = monthly total spend
forecast = model.predict([[12]])

The model's R² is also reported to indicate how well a straight-line trend explains the historical spending pattern — a low R² is itself an insight (spending is volatile/flat rather than trending strongly).

5. Visualization

matplotlib is used to plot:

Actual monthly spend (solid line)
The fitted trend line (dashed)
The forecasted next month (highlighted point, connected with a dotted line)

The chart is saved as spending_trend_forecast.png.

Key Findings

(from the sample dataset — replace with your own numbers once you swap in real data)

Metric	Value
Average monthly spend	$11,268.35
Biggest expense category	Rent (26.6% of total spend)
Needs vs. Wants split	56.3% / 43.7%
Forecasted next month's spend	$11,195.72
Trend	Roughly flat (~ –$11/month), model R² ≈ 0.001

Interpretation: spending is fairly stable month to month rather than trending sharply up or down — a straight-line model doesn't explain much of the variation (low R²), which suggests spending is driven more by recurring fixed costs (Rent) and irregular discretionary spikes (Shopping, Education) than by any steady month-over-month growth pattern.

How to Reproduce

Prerequisites:

bash
pip install pandas openpyxl scikit-learn matplotlib

Run in order:

bash
python generate_data.py       # → creates raw_expenses.csv
python build_excel.py         # → creates Expense_Tracker.xlsx
python analyze_forecast.py    # → prints insights, saves chart + report

Optional — build a Power BI dashboard on top:

Open Power BI Desktop
Get Data → Excel → select Expense_Tracker.xlsx
Load the Transactions or Monthly Summary table
Build a bar chart (category totals), a line chart (monthly trend), and a slicer to filter by month or category
Challenges & Fixes

Issue: Initial versions of analyze_forecast.py read the "Monthly Summary" sheet directly. Since Excel formulas written by openpyxl are not calculated until the file is opened (and saved) in Excel or LibreOffice, pandas read every formula cell as empty/zero when the file hadn't gone through that calculation step.

Fix: Rewrote the analysis script to read the raw Transactions sheet instead, and compute all monthly/category aggregations directly in pandas (groupby). This removed the dependency on Excel's calculation cache entirely, making the pipeline more robust and portable across machines.

Limitations
Synthetic data: the dataset used here is randomly generated for demonstration, not real transaction history.
Simple forecasting model: linear regression on 12 data points is a reasonable baseline but doesn't capture seasonality or category-level trends — a more advanced model (e.g., moving average, ARIMA, or a category-wise forecast) would be a natural next step.
Fixed needs/wants categorization: the Needs vs. Wants split is based on a simple hardcoded category mapping, not a smarter, more granular classification.
Next Steps
Replace synthetic data with a real personal expense export (bank/UPI statement).
Build the Power BI dashboard described above for interactive exploration.
Add month-over-month % change and a rolling 3-month average for smoother trend detection.
Add a budget vs. actual view with alerts when a category exceeds a set threshold.
Try a stronger forecasting approach (e.g., per-category forecasting instead of just total spend).
Author

Silppi Sahoo Final-year B.Tech, Electrical Engineering — VSSUT Burla 📧 silppisahoo2005@gmail.com · LinkedIn · GitHub
