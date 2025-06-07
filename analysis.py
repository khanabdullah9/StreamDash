import pandas as pd
from prophet import Prophet
import traceback

def get_month(date: pd._libs.tslibs.timestamps.Timestamp):
    return date.month
def get_year(date: pd._libs.tslibs.timestamps.Timestamp):
    return date.year
def get_day(date: pd._libs.tslibs.timestamps.Timestamp):
    return date.day
def get_month_range(df):
    if df is None:
        return   
    return df["Month"].unique()

def get_year_range(df):
    if df is None:
        return
    return df["Year"].unique()

def feature_engineering(data):
    df = data.copy()

    df = df[["Date","Note","Amount"]]

    df["Month"] = df["Date"].apply(get_month)
    df["Year"] = df["Date"].apply(get_year)
    df["Day"] = df["Date"].apply(get_day)

    return df

def get_month_wise_expense(df, year):
    if df is None:
        return
    
    filtered = df[df["Year"] == year]
    grouped = filtered.groupby(by=["Year", "Month"])[["Amount"]].sum().reset_index()
    return grouped.sort_values(by=["Year", "Month"])

def get_year_expense(df, year):
    if df is None:
        return
    
    return df[df["Year"] == year]

def get_month_insights(df, month_num, year):
    if df is None:
        return
    if month_num is None or year is None:
        return
    
    filtered = df[(df["Month"] == month_num) & (df["Year"] == year)]
    if filtered is None:
        return
    
    return filtered["Amount"].describe()

def get_note_insights(df, note, month_num, year):
    if note is None or len(note) == 0:
        return
    
    filtered = df[(df["Month"] == month_num) & (df["Year"] == year)]
    filtered = filtered[filtered["Note"].str.lower().str.contains(note.lower())]
    return filtered.describe()["Amount"]

def get_percentiles(df, month, year):
    if df is None:
        return
    
    filtered = df[(df["Month"] == month) & (df["Year"] == year)]
    q1, q2, q3, max = filtered["Amount"].quantile(q=0.25),\
                      filtered["Amount"].quantile(q=0.5), \
                      filtered["Amount"].quantile(q=0.75), \
                      filtered["Amount"].quantile(q=1)
    
    return q1, q2, q3, max

def predict_n_months(df, n=12):
    print("Predicting...")
    try:
        # Step 1: Convert date column to datetime if not already
        df['Date'] = pd.to_datetime(df['Date'])

        # Step 2: Group by month-end and sum 'Amount'
        grouped = (
            df.resample('M', on='Date')['Amount']
            .sum()
            .reset_index()
            .rename(columns={'Date': 'ds', 'Amount': 'y'})
        )

        model = Prophet()
        model.fit(grouped)

        future = model.make_future_dataframe(periods=n, freq='M')
        forecast = model.predict(future)

        return forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']].tail(n+1)

    except Exception:
        print(traceback.format_exc())

