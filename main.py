import pandas as pd

data = pd.read_csv("data/file_.csv")
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

# Ranking

data["rank"] = data["amount"].rank(method="dense",ascending=False)
data = data.sort_values(by="amount", ascending=False)

# Monthly total
data_month = data.groupby(["month","year"])["amount"].sum()

# Category count
data_cc = data.groupby("category")["amount"].count().reset_index()

# Average spend per category
data_aspc = data.groupby("category")["amount"].mean().reset_index()

# Merge test
merge_test = pd.merge(data_cc, data_aspc, on="category", how="outer")

# Top 3 highest expenses
data_sort_cost = data.sort_values("amount", ascending=False)
data_top3 = data_sort_cost.head(3)

# Flag
data["flag"] = data["amount"].apply(lambda x: "LARGE EXPENSE" if x>5000 else "OK")

# Search
def search():
    query = input("Enter merchant name ")
    query_result = data[data["merchant"].str.contains(query, case=False, na=False)]
    print(query_result)

#search()

# Date range
def date_range():
    start = pd.to_datetime(input("Enter start "))
    end = pd.to_datetime(input("Enter end "))
    date_result = data[(data["date"]>start) & (data["date"]<end)]
    print(date_result)

#date_range()

# Pivot and melt test

pivoted_data = data.pivot_table(index="month", columns="category", values="amount", aggfunc="sum")
pivoted_data = pivoted_data.reset_index()

pivoted_data = pd.melt(
    pivoted_data,
    id_vars="month",
    value_vars=pivoted_data.columns.drop("month")
)

# Total spend and total refund
total = data[data["refund"]=="NO"]["amount"].sum()
print(f"Total transaction = {total:.2f}")
refund = data[data["refund"]=="YES"]["amount"].sum()
print(f"Refund = {refund:.2f}")
spent = total - refund
print(f"Spent = {spent:.2f}")

# Double filter and rename concept
filtered = data[(data["amount"]>1000) & (data["payment_method"]=="UPI")]
filtered = filtered.rename(columns={"amount":"money","merchant":"shop"})