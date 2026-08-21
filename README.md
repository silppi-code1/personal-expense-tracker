
  This sums all transactions matching a given category and month directly
  from the raw log — so if new transactions are added to the Transactions
  sheet, the summary updates automatically without any manual recalculation.

### 3. Analysis in Python

`analyze_forecast.py` loads the cleaned transaction data with `pandas` and
computes:

- **Monthly totals** (grouped by month)
- **Category totals**, ranked to identify the largest spending category
- **Needs vs. Wants split** — categories are tagged as "Needs" (Food,
  Transport, Rent, Utilities, Health) or "Wants" (Entertainment, Shopping,
  Education), and the ratio between them is calculated

### 4. Forecasting Model

A simple **Linear Regression** model (`scikit-learn`) is fit on the 12 monthly
totals, treating each month as a sequential index (0–11), to predict the
13th month's (next month's) total spend:

```python
model = LinearRegression()
model.fit(X, y)              # X = month index, y = monthly total spend
forecast = model.predict([[12]])
```

The model's **R²** is also reported to indicate how well a straight-line
trend explains the historical spending pattern — a low R² is itself an
insight (spending is volatile/flat rather than trending strongly).

### 5. Visualization

`matplotlib` is used to plot:

- Actual monthly spend (solid line)
- The fitted trend line (dashed)
- The forecasted next month (highlighted point, connected with a dotted line)

The chart is saved as `spending_trend_forecast.png`.

---

## Key Findings

*(from the sample dataset — replace with your own numbers once you swap in
real data)*

| Metric | Value |
|---|---|
| Average monthly spend | **$11,268.35** |
| Biggest expense category | **Rent** (26.6% of total spend) |
| Needs vs. Wants split | **56.3% / 43.7%** |
| Forecasted next month's spend | **$11,195.72** |
| Trend | Roughly flat (~ –$11/month), model R² ≈ 0.001 |

**Interpretation:** spending is fairly stable month to month rather than
trending sharply up or down — a straight-line model doesn't explain much of
the variation (low R²), which suggests spending is driven more by recurring
fixed costs (Rent) and irregular discretionary spikes (Shopping, Education)
than by any steady month-over-month growth pattern.

---

## How to Reproduce

**Prerequisites:**
```bash
pip install pandas openpyxl scikit-learn matplotlib
```

**Run in order:**
```bash
python generate_data.py       # → creates raw_expenses.csv
python build_excel.py         # → creates Expense_Tracker.xlsx
python analyze_forecast.py    # → prints insights, saves chart + report
```

**Optional — build a Power BI dashboard on top:**
1. Open Power BI Desktop
2. **Get Data → Excel** → select `Expense_Tracker.xlsx`
3. Load the **Transactions** or **Monthly Summary** table
4. Build a bar chart (category totals), a line chart (monthly trend), and a
   slicer to filter by month or category

---

## Challenges & Fixes

**Issue:** Initial versions of `analyze_forecast.py` read the "Monthly
Summary" sheet directly. Since Excel formulas written by `openpyxl` are not
calculated until the file is opened (and saved) in Excel or LibreOffice,
pandas read every formula cell as empty/zero when the file hadn't gone
through that calculation step.

**Fix:** Rewrote the analysis script to read the **raw Transactions** sheet
instead, and compute all monthly/category aggregations directly in pandas
(`groupby`). This removed the dependency on Excel's calculation cache
entirely, making the pipeline more robust and portable across machines.

---

## Limitations

- **Synthetic data**: the dataset used here is randomly generated for
  demonstration, not real transaction history.
- **Simple forecasting model**: linear regression on 12 data points is a
  reasonable baseline but doesn't capture seasonality or category-level
  trends — a more advanced model (e.g., moving average, ARIMA, or a
  category-wise forecast) would be a natural next step.
- **Fixed needs/wants categorization**: the Needs vs. Wants split is based on
  a simple hardcoded category mapping, not a smarter, more granular
  classification.

---

## Next Steps

- Replace synthetic data with a real personal expense export (bank/UPI
  statement).
- Build the Power BI dashboard described above for interactive exploration.
- Add month-over-month % change and a rolling 3-month average for smoother
  trend detection.
- Add a **budget vs. actual** view with alerts when a category exceeds a
  set threshold.
- Try a stronger forecasting approach (e.g., per-category forecasting
  instead of just total spend).

---

## Author

**Silppi Sahoo**
Final-year B.Tech, Electrical Engineering — VSSUT Burla
📧 silppisahoo2005@gmail.com · [LinkedIn](https://linkedin.com/in/silppi-sahoo) · [GitHub](https://github.com/silppi-code1)
