import pandas as pd

def clean_data(data):

    data = data.dropna(subset=["amount","date"])
    data = data.fillna("UNKNOWN")
    data["merchant"] = data["merchant"].str.title().str.strip()
    data["category"] = data["category"].str.title().str.strip()
    data["refund"] = data["amount"].apply(lambda x: "YES" if x<0 else "NO")
    data["amount"] = data["amount"].apply(lambda x: -x if x<0 else x)
    data["date"] = pd.to_datetime(data["date"])
    data = data.sort_values("date")
    data["month"] = data["date"].dt.month_name()
    data["year"] = data["date"].dt.year

    return data

def top_3(data):
    data_sort_cost = data.sort_values("amount", ascending=False)
    data_top3 = data_sort_cost.head(3)

    return data_top3

def month_t(data):
    data_month = data.groupby(["month","year"])["amount"].sum().reset_index()
    return (data_month)

def cc(data):
    data_cc = data.groupby("category")["amount"].count().reset_index()
    return (data_cc)

def aspc(data):
    data_aspc = data.groupby("category")["amount"].mean().reset_index()
    return (data_aspc)

def search(data, merchant):

    query_result = data[data["merchant"].str.contains(merchant, case=False, na=False)]
    return(query_result)

def date_range(data, start, end):
    start_date = pd.to_datetime(start)
    end_date = pd.to_datetime(end)      
    date_result = data[(data["date"]>=start_date) & (data["date"]<=end_date)]
    return(date_result)

def total_spent (data):
    total = data[data["refund"]=="NO"]["amount"].sum()
    refund = data[data["refund"]=="YES"]["amount"].sum()
    return (total-refund)