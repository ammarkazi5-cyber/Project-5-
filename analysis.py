import pandas as pd
import numpy as np

# ============================================================
# 1. LOAD EXCEL FILE
# ============================================================

FILE = "FIN-W5-ENTERPRISE-05..xlsx"

revenue = pd.read_excel(FILE, sheet_name="Revenue")
expenses = pd.read_excel(FILE, sheet_name="Expenses")

# Convert dates
revenue["Date"] = pd.to_datetime(revenue["Date"])
expenses["Date"] = pd.to_datetime(expenses["Date"])

# ============================================================
# 2. REVENUE ANALYSIS
# ============================================================

print("\n" + "=" * 60)
print("REVENUE ANALYSIS")
print("=" * 60)

total_revenue = revenue["Revenue"].sum()
average_revenue = revenue["Revenue"].mean()
highest_revenue = revenue["Revenue"].max()
lowest_revenue = revenue["Revenue"].min()

print(f"Total Revenue       : ₹{total_revenue:,.2f}")
print(f"Average Revenue     : ₹{average_revenue:,.2f}")
print(f"Highest Invoice     : ₹{highest_revenue:,.2f}")
print(f"Lowest Invoice      : ₹{lowest_revenue:,.2f}")

# ------------------------------------------------------------
# Monthly Revenue
# ------------------------------------------------------------

monthly_revenue = (
    revenue
    .groupby(["Year", "Month"], sort=False)["Revenue"]
    .sum()
    .reset_index()
)

print("\nMONTHLY REVENUE")
print(monthly_revenue.to_string(index=False))

# ------------------------------------------------------------
# Revenue by Business Unit
# ------------------------------------------------------------

business_unit_revenue = (
    revenue
    .groupby("Business_Unit")["Revenue"]
    .agg(["sum", "mean", "count"])
    .reset_index()
    .sort_values("sum", ascending=False)
)

business_unit_revenue.columns = [
    "Business_Unit",
    "Total_Revenue",
    "Average_Revenue",
    "Invoice_Count"
]

print("\nREVENUE BY BUSINESS UNIT")
print(business_unit_revenue.to_string(index=False))

# ------------------------------------------------------------
# Revenue by Region
# ------------------------------------------------------------

region_revenue = (
    revenue
    .groupby("Region")["Revenue"]
    .sum()
    .reset_index()
    .sort_values("Revenue", ascending=False)
)

print("\nREVENUE BY REGION")
print(region_revenue.to_string(index=False))

# ------------------------------------------------------------
# Revenue by Customer
# ------------------------------------------------------------

customer_revenue = (
    revenue
    .groupby("Customer")["Revenue"]
    .sum()
    .reset_index()
    .sort_values("Revenue", ascending=False)
)

print("\nTOP CUSTOMERS")
print(customer_revenue.head(10).to_string(index=False))

# ------------------------------------------------------------
# Quarterly Revenue
# ------------------------------------------------------------

quarterly_revenue = (
    revenue
    .groupby(["Year", "Quarter"])["Revenue"]
    .sum()
    .reset_index()
)

print("\nQUARTERLY REVENUE")
print(quarterly_revenue.to_string(index=False))

# ============================================================
# 3. EXPENSE ANALYSIS
# ============================================================

print("\n" + "=" * 60)
print("EXPENSE ANALYSIS")
print("=" * 60)

total_expense = expenses["Actual_Expense"].sum()
average_expense = expenses["Actual_Expense"].mean()
highest_expense = expenses["Actual_Expense"].max()
lowest_expense = expenses["Actual_Expense"].min()

print(f"Total Expense       : ₹{total_expense:,.2f}")
print(f"Average Expense     : ₹{average_expense:,.2f}")
print(f"Highest Expense     : ₹{highest_expense:,.2f}")
print(f"Lowest Expense      : ₹{lowest_expense:,.2f}")

# ------------------------------------------------------------
# Monthly Expense
# ------------------------------------------------------------

monthly_expense = (
    expenses
    .groupby(["Year", "Month"], sort=False)["Actual_Expense"]
    .sum()
    .reset_index()
)

print("\nMONTHLY EXPENSE")
print(monthly_expense.to_string(index=False))

# ------------------------------------------------------------
# Expense by Department
# ------------------------------------------------------------

department_expense = (
    expenses
    .groupby("Department")["Actual_Expense"]
    .agg(["sum", "mean", "count"])
    .reset_index()
    .sort_values("sum", ascending=False)
)

department_expense.columns = [
    "Department",
    "Total_Expense",
    "Average_Expense",
    "Transaction_Count"
]

print("\nEXPENSE BY DEPARTMENT")
print(department_expense.to_string(index=False))

# ------------------------------------------------------------
# Expense by Category
# ------------------------------------------------------------

category_expense = (
    expenses
    .groupby("Category")["Actual_Expense"]
    .agg(["sum", "mean", "count"])
    .reset_index()
    .sort_values("sum", ascending=False)
)

category_expense.columns = [
    "Category",
    "Total_Expense",
    "Average_Expense",
    "Transaction_Count"
]

print("\nEXPENSE BY CATEGORY")
print(category_expense.to_string(index=False))

# ============================================================
# 4. REVENUE VS EXPENSE
# ============================================================

print("\n" + "=" * 60)
print("REVENUE VS EXPENSE ANALYSIS")
print("=" * 60)

total_profit = total_revenue - total_expense

profit_margin = (
    total_profit / total_revenue * 100
    if total_revenue != 0 else 0
)

expense_ratio = (
    total_expense / total_revenue * 100
    if total_revenue != 0 else 0
)

print(f"Total Revenue       : ₹{total_revenue:,.2f}")
print(f"Total Expense       : ₹{total_expense:,.2f}")
print(f"Operating Profit    : ₹{total_profit:,.2f}")
print(f"Profit Margin       : {profit_margin:.2f}%")
print(f"Expense Ratio       : {expense_ratio:.2f}%")

# ------------------------------------------------------------
# Monthly Profit
# ------------------------------------------------------------

monthly = pd.merge(
    monthly_revenue,
    monthly_expense,
    on=["Year", "Month"],
    how="outer"
)

monthly["Revenue"] = monthly["Revenue"].fillna(0)
monthly["Actual_Expense"] = monthly["Actual_Expense"].fillna(0)

monthly["Profit"] = (
    monthly["Revenue"] - monthly["Actual_Expense"]
)

monthly["Profit_Margin_%"] = np.where(
    monthly["Revenue"] != 0,
    monthly["Profit"] / monthly["Revenue"] * 100,
    0
)

print("\nMONTHLY PROFITABILITY")
print(monthly.to_string(index=False))

# ============================================================
# 5. EXPENSE GROWTH
# ============================================================

monthly["Expense_Growth_%"] = (
    monthly["Actual_Expense"]
    .pct_change() * 100
)

print("\nEXPENSE GROWTH")
print(
    monthly[
        ["Year", "Month", "Actual_Expense", "Expense_Growth_%"]
    ].to_string(index=False)
)

# ============================================================
# 6. TOP SPENDING DEPARTMENT
# ============================================================

top_department = department_expense.iloc[0]

print("\nTOP SPENDING DEPARTMENT")
print(f"Department : {top_department['Department']}")
print(f"Expense    : ₹{top_department['Total_Expense']:,.2f}")

# ============================================================
# 7. TOP EXPENSE CATEGORY
# ============================================================

top_category = category_expense.iloc[0]

print("\nTOP EXPENSE CATEGORY")
print(f"Category   : {top_category['Category']}")
print(f"Expense    : ₹{top_category['Total_Expense']:,.2f}")

# ============================================================
# 8. REVENUE CONCENTRATION
# ============================================================

customer_revenue["Revenue_%"] = (
    customer_revenue["Revenue"] /
    total_revenue * 100
)

print("\nTOP 10 CUSTOMERS BY REVENUE")
print(
    customer_revenue.head(10).to_string(index=False)
)

# ============================================================
# 9. SAVE ALL ANALYSIS TO EXCEL
# ============================================================

with pd.ExcelWriter(
    "Revenue_Expense_Analysis.xlsx",
    engine="openpyxl"
) as writer:

    revenue.to_excel(
        writer,
        sheet_name="Revenue_Data",
        index=False
    )

    expenses.to_excel(
        writer,
        sheet_name="Expense_Data",
        index=False
    )

    monthly_revenue.to_excel(
        writer,
        sheet_name="Monthly_Revenue",
        index=False
    )

    business_unit_revenue.to_excel(
        writer,
        sheet_name="Business_Unit",
        index=False
    )

    region_revenue.to_excel(
        writer,
        sheet_name="Region_Revenue",
        index=False
    )

    customer_revenue.to_excel(
        writer,
        sheet_name="Customer_Revenue",
        index=False
    )

    monthly_expense.to_excel(
        writer,
        sheet_name="Monthly_Expense",
        index=False
    )

    department_expense.to_excel(
        writer,
        sheet_name="Department_Expense",
        index=False
    )

    category_expense.to_excel(
        writer,
        sheet_name="Category_Expense",
        index=False
    )

    monthly.to_excel(
        writer,
        sheet_name="Profitability",
        index=False
    )

print("\n" + "=" * 60)
print("ANALYSIS COMPLETED")
print("=" * 60)
print("Output file: Revenue_Expense_Analysis.xlsx")