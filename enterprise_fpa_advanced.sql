-- Advanced FP&A SQL: CTEs, CASE logic and window functions
WITH revenue AS (
 SELECT DATE_TRUNC('month',transaction_date) month, SUM(net_sales) revenue
 FROM revenue_transactions GROUP BY 1
), expense AS (
 SELECT DATE_TRUNC('month',expense_date) month, SUM(amount) operating_expenses
 FROM expense_transactions GROUP BY 1
), pnl AS (
 SELECT COALESCE(r.month,e.month) month, COALESCE(r.revenue,0) revenue,
        COALESCE(e.operating_expenses,0) operating_expenses
 FROM revenue r FULL OUTER JOIN expense e ON r.month=e.month
)
SELECT month,revenue,operating_expenses,
       revenue*.65 gross_profit,
       revenue*.65-operating_expenses ebitda,
       (revenue*.65-operating_expenses)-revenue*.025 ebit,
       GREATEST(((revenue*.65-operating_expenses)-revenue*.025)*.75,0) net_profit,
       LAG(revenue) OVER(ORDER BY month) prior_revenue,
       CASE WHEN LAG(revenue) OVER(ORDER BY month)=0 THEN NULL
            ELSE revenue/LAG(revenue) OVER(ORDER BY month)-1 END mom_growth
FROM pnl ORDER BY month;

-- AR aging
SELECT invoice_id,customer,due_date,invoice_amount,amount_received,
       GREATEST(invoice_amount-amount_received,0) outstanding,
       GREATEST(CURRENT_DATE-due_date,0) days_overdue,
       CASE WHEN invoice_amount-amount_received<=0 THEN 'Paid'
            WHEN GREATEST(CURRENT_DATE-due_date,0)<=30 THEN '0-30'
            WHEN GREATEST(CURRENT_DATE-due_date,0)<=60 THEN '31-60'
            WHEN GREATEST(CURRENT_DATE-due_date,0)<=90 THEN '61-90'
            ELSE '90+' END aging_bucket
FROM ar_transactions;

-- AP aging
SELECT bill_id,supplier,due_date,bill_amount,amount_paid,
       GREATEST(bill_amount-amount_paid,0) outstanding,
       GREATEST(CURRENT_DATE-due_date,0) days_overdue
FROM ap_transactions;
