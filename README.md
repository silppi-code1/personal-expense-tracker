# 💰 Personal Finance Expense Tracker with Insights

An end-to-end personal finance analytics project that combines **Excel** (data
cleaning & aggregation), **Python** (analysis & machine learning), and a
**forecasting model** to turn raw expense data into actionable spending insights.

---

## 📑 Table of Contents

- [About This Project](#about-this-project)
- [Problem Statement](#problem-statement)
- [Tech Stack](#tech-stack)
- [Project Structure](#project-structure)
- [Methodology](#methodology)
  - [1. Data Generation / Ingestion](#1-data-generation--ingestion)
  - [2. Data Cleaning in Excel](#2-data-cleaning-in-excel)
  - [3. Analysis in Python](#3-analysis-in-python)
  - [4. Forecasting Model](#4-forecasting-model)
  - [5. Visualization](#5-visualization)
- [Key Findings](#key-findings)
- [How to Reproduce](#how-to-reproduce)
- [Challenges & Fixes](#challenges--fixes)
- [Limitations](#limitations)
- [Next Steps](#next-steps)
- [Author](#author)

---

## About This Project

Most people track expenses in a spreadsheet and stop there. This project goes a
step further — it builds a small but complete data pipeline that:

1. Logs and cleans expense data in **Excel**, using real formulas (not
   hardcoded numbers) so the summary updates automatically if the underlying
   data changes.
2. Analyzes spending patterns in **Python** (pandas) — category breakdowns,
   needs-vs-wants ratio, and monthly trends.
3. Builds a simple **machine learning model** (scikit-learn linear regression)
   to forecast next month's total spending.
4. Outputs a **visual chart** and a **plain-text insights report** summarizing
   the findings.

The goal is to demonstrate a practical, reproducible workflow that mirrors how
personal or small-business finance data might actually be analyzed — moving
smoothly between a spreadsheet layer (familiar, editable, shareable) and a
code layer (repeatable, extensible, and capable of prediction).

---

## Problem Statement

Manually tracking expenses in a spreadsheet answers "what did I spend?" but
rarely answers the more useful questions:

- Which category is quietly eating the largest share of my budget?
- Am I spending more on **needs** or **wants**, and is that ratio healthy?
- Is my monthly spending trending up, down, or staying flat?
- Based on my history, what should I expect to spend **next month** — and can
  I plan around it?

This project answers all four using a combination of spreadsheet aggregation
and a lightweight predictive model.

---

## Tech Stack

| Layer | Tool | Purpose |
|---|---|---|
| Data cleaning & aggregation | **Microsoft Excel** (openpyxl) | Transaction log + formula-driven monthly summary |
| Data analysis | **Python (pandas)** | Category totals, monthly trends, needs
