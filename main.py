import pandas as pd

data = pd.read_csv("data/file.csv")
data = data.dropna()

data["date"] = pd.to_datetime(data["date"])
data = data.sort_values("date")

# Average spend per category
data_aspc = data.groupby("category")["amount"].mean().reset_index()

# Top 3 highest expenses
data_sort_cost = data.sort_values("amount", ascending=False)
data_top3 = data_sort_cost.head(3)

# Flag
data["flag"] = data["amount"].apply(lambda x: "LARGE EXPENSE" if x>5000 else "OK")

print(data)
# Search
def search():
    query = input("Enter merchant name ")
    query_result = data[data["merchant"].str.contains(query)]
    print(query_result)

#search()

# Date range
def date_range():
    start = pd.to_datetime(input("Enter start "))
    end = pd.to_datetime(input("Enter end "))
    date_result = data[(data["date"]>start) & (data["date"]<end)]
    print(date_result)

#date_range()

# Double filter
filtered = data[(data["amount"]>1000) & (data["payment_method"]=="UPI")]
filtered = filtered.rename(columns={"amount":"money","merchant":"shop"})

print(filtered)