import random
from datetime import date, timedelta

random.seed(42)

categories = {
    "Food": (150, 350),
    "Transport": (50, 150),
    "Rent": (3000, 3000),
    "Utilities": (200, 400),
    "Entertainment": (50, 250),
    "Shopping": (100, 500),
    "Health": (50, 300),
    "Education": (100, 600),
}

start = date(2025, 9, 1)
end = date(2026, 8, 21)

rows = []
d = start
while d <= end:
    # Rent charged once per month, on the 1st
    if d.day == 1:
        rows.append((d.isoformat(), "Rent", "Housing", round(random.uniform(*categories["Rent"]), 2)))
    # Random daily transactions for other categories (not every day, not every category)
    for cat in ["Food", "Transport", "Entertainment", "Shopping", "Health", "Education", "Utilities"]:
        if cat == "Utilities" and d.day != 5:
            continue  # utilities billed once a month on the 5th
        if cat == "Education" and random.random() > 0.15:
            continue  # occasional
        if cat in ("Food", "Transport") and random.random() > 0.55:
            continue
        if cat in ("Entertainment", "Shopping", "Health") and random.random() > 0.25:
            continue
        low, high = categories[cat]
        amt = round(random.uniform(low, high) / (3 if cat in ("Food","Transport") else 1), 2)
        rows.append((d.isoformat(), cat, "Needs" if cat in ("Food","Transport","Rent","Utilities","Health") else "Wants", amt))
    d += timedelta(days=1)

import csv
with open("raw_expenses.csv", "w", newline="") as f:
    w = csv.writer(f)
    w.writerow(["Date", "Category", "Type", "Amount"])
    w.writerows(rows)

print(f"Generated {len(rows)} transactions from {start} to {end}")
