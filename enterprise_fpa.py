"""Advanced FP&A analytics for FIN-W5-ENTERPRISE-05."""
from pathlib import Path
import pandas as pd
import numpy as np

def load_tx(path, date_col, amount_col):
    df=pd.read_csv(path)
    df[date_col]=pd.to_datetime(df[date_col],errors="coerce")
    df[amount_col]=pd.to_numeric(df[amount_col],errors="coerce").fillna(0)
    df=df.dropna(subset=[date_col]).copy()
    df["Month"]=df[date_col].dt.to_period("M")
    df["Quarter"]="Q"+df[date_col].dt.quarter.astype(str)
    return df

def pnl(revenue, expenses, rev_col="Net Sales", exp_col="Amount"):
    r=revenue.groupby("Month")[rev_col].sum().rename("Revenue")
    e=expenses.groupby("Month")[exp_col].sum().rename("Operating_Expenses")
    x=pd.concat([r,e],axis=1).fillna(0)
    x["Gross_Profit"]=x["Revenue"]*0.65
    x["EBITDA"]=x["Gross_Profit"]-x["Operating_Expenses"]
    x["D&A"]=x["Revenue"]*0.025
    x["EBIT"]=x["EBITDA"]-x["D&A"]
    x["Tax"]=np.maximum(x["EBIT"]*0.25,0)
    x["Net_Profit"]=x["EBIT"]-x["Tax"]
    x["Gross_Margin"]=x["Gross_Profit"].div(x["Revenue"].replace(0,np.nan)).fillna(0)
    x["Net_Margin"]=x["Net_Profit"].div(x["Revenue"].replace(0,np.nan)).fillna(0)
    x["MoM_Growth"]=x["Revenue"].pct_change()
    return x.reset_index()

def aging(df,due_col,amount_col,paid_col):
    x=df.copy(); today=pd.Timestamp.today().normalize()
    x[due_col]=pd.to_datetime(x[due_col],errors="coerce")
    x[amount_col]=pd.to_numeric(x[amount_col],errors="coerce").fillna(0)
    x[paid_col]=pd.to_numeric(x[paid_col],errors="coerce").fillna(0)
    x["Outstanding"]=(x[amount_col]-x[paid_col]).clip(lower=0)
    x["Days_Overdue"]=np.where(x["Outstanding"]>0,(today-x[due_col]).dt.days.clip(lower=0),0)
    x["Aging_Bucket"]=pd.cut(x["Days_Overdue"],[-1,30,60,90,np.inf],labels=["0-30","31-60","61-90","90+"])
    x["Status"]=np.select([x["Outstanding"].eq(0),x["Days_Overdue"]>90,x["Days_Overdue"]>60],["Paid","Critical","Overdue"],default="Open")
    return x

def zscore_flags(series, threshold=2.0):
    s=pd.to_numeric(series,errors="coerce")
    z=(s-s.mean())/s.std(ddof=0)
    return z.abs().ge(threshold).fillna(False)
