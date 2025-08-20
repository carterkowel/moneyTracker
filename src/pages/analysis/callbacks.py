
import pandas as pd
import plotly.express as px
from dash import Input, Output, State, callback
import datetime as dt


from utils import read_root_csv

# Callback to update charts based on date selection ---
@callback(
    Output("monthly-spending-chart", "figure"),
    Output("average-monthly-spending-bar-chart", "figure"),
    Input("analysis-date-method", "value"),
    Input("analysis-date-year", "value"),
    Input("analysis-start-date", "date"),
    Input("analysis-end-date", "date"),
    Input("grouping-dropdown", "value"),
)
def update_spending_charts(method, selected_year, custom_start, custom_end, grouping):
    df = read_root_csv()
    if df is None or df.empty:
        empty_fig = px.line(title="📭 No data found.")
        return empty_fig, empty_fig

    df["Date"] = pd.to_datetime(df["Date"], errors="coerce")
    df = df.dropna(subset=["Date"])
    if df.empty:
        empty_fig = px.line(title="⚠️ No valid dates in data.")
        return empty_fig, empty_fig

    # Apply date filtering based on method
    if method == "all":
        filtered_df = df.copy()
    elif method == "last12":
        cutoff = dt.datetime.today() - pd.DateOffset(months=12)
        filtered_df = df[df["Date"] >= cutoff]
    elif method == "by_year" and selected_year:
        filtered_df = df[df["Date"].dt.year == int(selected_year)]
    elif method == "custom":
        start = pd.to_datetime(custom_start) if custom_start else df["Date"].min()
        end = pd.to_datetime(custom_end) if custom_end else df["Date"].max()
        filtered_df = df[(df["Date"] >= start) & (df["Date"] <= end)]
    else:
        filtered_df = df.copy()

    if filtered_df.empty:
        empty_fig = px.line(title="⚠️ No records match the selected date range.")
        return empty_fig, empty_fig

    # Monthly grouping
    filtered_df["Month"] = filtered_df["Date"].dt.to_period("M").dt.to_timestamp()
    grouped = filtered_df.groupby(["Month", grouping], as_index=False)["Amount"].sum()

    # Line chart
    line_fig = px.line(
        grouped,
        x="Month",
        y="Amount",
        color=grouping,
        markers=True,
        labels={"Amount": "Total Spending", "Month": "Month"},
        title=f"Monthly Spending by {grouping}"
    )
    line_fig.update_traces(hovertemplate='%{fullData.name}<br>Total Spending: %{y}<extra></extra>')
    line_fig.update_layout(xaxis_title="Month", yaxis_title="Amount ($)", legend_title=grouping, hovermode="x unified")

    # Average monthly bar chart
    avg_monthly = grouped.groupby(grouping)["Amount"].mean().reset_index().sort_values("Amount", ascending=False)
    bar_fig = px.bar(
        avg_monthly,
        x=grouping,
        y="Amount",
        labels={grouping: grouping, "Amount": "Average Monthly Spending ($)"},
        title=f"Average Monthly Spending by {grouping}"
    )
    bar_fig.update_layout(xaxis_title=grouping, yaxis_title="Average Monthly Spending ($)", hovermode="closest")
    bar_fig.update_traces(hovertemplate='%{x}<br>Average Monthly Spending: %{y:.2f}<extra></extra>')

    return line_fig, bar_fig


# Callback to toggle year and custom date containers ---
@callback(
    Output("analysis-date-year-container", "style"),
    Output("analysis-custom-dates-container", "style"),
    Input("analysis-date-method", "value")
)
def toggle_year_or_custom(method):
    if method == "by_year":
        return {"display": "block"}, {"display": "none"}
    elif method == "custom":
        return {"display": "none"}, {"display": "block"}
    else:
        return {"display": "none"}, {"display": "none"}


# Callback to populate year dropdown options dynamically ---
@callback(
    Output("analysis-date-year", "options"),
    Output("analysis-date-year", "value"),
    Input("url", "pathname")
)
def populate_year_dropdown(_):
    df = read_root_csv()
    if df is None or df.empty or "Date" not in df.columns:
        return [], None
    df["Date"] = pd.to_datetime(df["Date"], errors="coerce")
    years = sorted(df["Date"].dt.year.dropna().unique(), reverse=True)
    options = [{"label": str(y), "value": y} for y in years]
    value = years[0] if years else None
    return options, value