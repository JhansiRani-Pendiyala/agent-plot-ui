import dash
from dash import dcc, html, dash_table, Input, Output, State
import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd
import requests

# Backend API Endpoint
API_URL = "http://0.0.0.0:8080/api/query"  # Change as needed

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.SUPERHERO])
app.title = "Executive Sales Dashboard"

# Fetch and filter data from backend
def fetch_data(search_text, start_date, end_date):
    try:
        response = requests.post(API_URL, json={"query": search_text or ""}, headers={"Content-Type": "application/json"})
        response.raise_for_status()
        df = pd.DataFrame(response.json())

        if df.empty:
            return df

        # Parse columns and add full name
        df['created_date'] = pd.to_datetime(df['created_date'])
        df['full_name'] = df['first_name'] + " " + df['last_name']

        # Apply date filters
        if start_date:
            df = df[df['created_date'] >= pd.to_datetime(start_date)]
        if end_date:
            df = df[df['created_date'] <= pd.to_datetime(end_date)]

        return df
    except Exception as e:
        print("Error fetching data:", e)
        return pd.DataFrame()

# App Layout
app.layout = dbc.Container([
    html.H2("Executive Sales Dashboard", className="my-4 text-center"),

    dbc.Row([
        dbc.Col([
            dbc.Label("Search Employee"),
            dcc.Input(id="search-input", type="text", debounce=True, placeholder="Enter name...", style={"width": "100%"})
        ], width=4),

        dbc.Col([
            dbc.Label("Start Date"),
            dcc.DatePickerSingle(id="start-date")
        ], width=2),

        dbc.Col([
            dbc.Label("End Date"),
            dcc.DatePickerSingle(id="end-date")
        ], width=2),

        dbc.Col([
            dbc.Button("Filter", id="filter-btn", color="primary", className="mt-4")
        ], width=2)
    ], className="mb-4"),

    dbc.Row([
        dbc.Col(dbc.Card([
            dbc.CardBody([
                html.H6("Total Products Sold"),
                html.H3(id="kpi-total")
            ])
        ], color="info", inverse=True), width=4),

        dbc.Col(dbc.Card([
            dbc.CardBody([
                html.H6("Average per Employee"),
                html.H3(id="kpi-average")
            ])
        ], color="success", inverse=True), width=4),
    ], className="mb-4"),

    dbc.Row([
        dbc.Col(dcc.Graph(id="bar-chart"), width=6),
        dbc.Col(dcc.Graph(id="donut-chart"), width=6),
    ]),

    dbc.Row([
        dbc.Col([
            dash_table.DataTable(
                id="data-table",
                page_size=10,
                style_table={"overflowX": "auto"},
                style_cell={"textAlign": "left", "fontSize": "12px"},
                style_header={"backgroundColor": "#2c3e50", "color": "white", "fontWeight": "bold"},
            )
        ])
    ])
], fluid=True)


# Callback
@app.callback(
    Output("kpi-total", "children"),
    Output("kpi-average", "children"),
    Output("bar-chart", "figure"),
    Output("donut-chart", "figure"),
    Output("data-table", "data"),
    Output("data-table", "columns"),
    Input("filter-btn", "n_clicks"),
    State("search-input", "value"),
    State("start-date", "date"),
    State("end-date", "date"),
    prevent_initial_call=True
)
def update_dashboard(n_clicks, search_text, start_date, end_date):
    df = fetch_data(search_text, start_date, end_date)

    # KPIs
    total = df['total_products_sold'].sum() if not df.empty else 0
    avg = round(df['total_products_sold'].mean(), 2) if not df.empty else 0

    # Bar chart
    bar_fig = px.bar(
        df, x='full_name', y='total_products_sold',
        title="Products Sold per Employee",
        labels={"total_products_sold": "Products Sold", "full_name": "Employee"},
        color='total_products_sold',
        color_continuous_scale='Blues'
    )

    # Donut chart
    donut_fig = px.pie(
        df, names='full_name', values='total_products_sold',
        hole=0.4, title="Sales Distribution",
        color_discrete_sequence=px.colors.sequential.Viridis
    )

    # Format table
    if 'product_list' in df.columns:
        df['product_list'] = df['product_list'].apply(lambda x: ", ".join(x) if isinstance(x, list) else x)
    df['created_date'] = df['created_date'].dt.strftime('%Y-%m-%d')

    columns = [{"name": col.replace("_", " ").title(), "id": col} for col in df.columns]
    return str(total), str(avg), bar_fig, donut_fig, df.to_dict("records"), columns


if __name__ == "__main__":
    app.run(debug=True, port=8090)