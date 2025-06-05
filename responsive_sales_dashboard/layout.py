from dash import html, dcc, dash_table
import plotly.express as px
import dash_bootstrap_components as dbc

# Shared style for text input
input_style = {
    "height": "38px",
    "width": "100%",
    "fontSize": "1rem",
    "padding": "6px 12px",
    "border": "1px solid #ced4da",
    "borderRadius": "4px",
    "backgroundColor": "white"
}

layout = dbc.Container([
    dbc.Row([
        dbc.Col(
            html.H2(
                "📊 Product & Sales Dashboard",
                className="text-center text-grey fw-bold mb-4"
            ),
            width=12
        )
    ]),

    # Filters
    dbc.Row([
        dbc.Col([
            dbc.Label("Serach Product and Sales information", className="fw-semibold"),
            dcc.Input(
                id="search-input",
                type="text",
                debounce=True,
                placeholder="Type your query...",
                style=input_style
            )
        ], xs=12, md=4),

        dbc.Col([
            dbc.Label("Start Date", className="fw-semibold"),
            dcc.DatePickerSingle(
                id="start-date",
                display_format="YYYY-MM-DD",
            )
        ], xs=6, md=2),

        dbc.Col([
            dbc.Label("End Date", className="fw-semibold"),
            dcc.DatePickerSingle(
                id="end-date",
                display_format="YYYY-MM-DD"
            )
        ], xs=6, md=2),

        dbc.Col([
            dbc.Label(" "),  # space above button
            dbc.Button(
                "Apply Filters",
                id="filter-btn",
                color="primary",
                className="w-100 fw-semibold",
                style={"height": "38px", "fontSize": "1rem"}
            )
        ], xs=12, md=2),
    ], className="mb-4"),

    # KPIs
    dbc.Row([
        dbc.Col(dbc.Card([
            dbc.CardBody([
                html.H6("Total Products Sold", className="card-title text-white"),
                html.H3(id="kpi-total", className="card-text text-white fw-bold")
            ])
        ], className="info"), md=6),

        dbc.Col(dbc.Card([
            dbc.CardBody([
                html.H6("Avg Products per Employee", className="card-title text-white"),
                html.H3(id="kpi-average", className="card-text text-white fw-bold")
            ])
        ], className="title_success", inverse=True), md=6),
    ], className="mb-4"),

    # Charts
    dbc.Row([
        dbc.Col(dcc.Graph(id="bar-chart", config={"displayModeBar": False}), md=6),
        dbc.Col(dcc.Graph(id="donut-chart", config={"displayModeBar": False}), md=6),
    ], className="mb-4"),

    # Data Table
    dbc.Row([
        dbc.Col(dash_table.DataTable(
            id="data-table",
            page_size=8,
            style_table={"overflowX": "auto"},
            style_cell={"textAlign": "left", "fontSize": "14px", "padding": "8px"},
            style_header={
                "backgroundColor": px.colors.sequential.Greys[3],
                "color": "white",
                "fontWeight": "bold"
            },
        ), width=12)
    ])
], fluid=True, className="p-4 bg-light")