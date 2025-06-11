from dash import html, dcc, dash_table
import plotly.express as px
import dash_bootstrap_components as dbc

input_style = {
    "height": "38px",  # Same as DateInput_input height in CSS
    "width": "100%",
    "fontSize": "1rem",
    "padding": "6px 12px",
    "border": "1px solid #ced4da",
    "borderRadius": "4px",
    "backgroundColor": "white",
    "color": "#495057",
    "boxSizing": "border-box"
}

button_style = {
    "height": "38px",
    "fontSize": "1rem",
    "width": "100%",
    "borderRadius": "4px"
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

    # Filters row aligned
    dbc.Row([
        dbc.Col([
            dbc.Label("Search Product and Sales information", className="fw-semibold mb-1"),
            dcc.Input(
                id="search-input",
                type="text",
                debounce=True,
                placeholder="Type your query...",
                style=input_style
            )
        ], xs=12, md=4, className="d-flex flex-column justify-content-start"),

        dbc.Col([
            dbc.Label("Start Date", className="fw-semibold mb-1"),
            dcc.DatePickerSingle(
                id="start-date",
                display_format="YYYY-MM-DD",
                style={"width": "100%"}  # input style overridden by CSS now
            )
        ], xs=6, md=2, className="d-flex flex-column justify-content-start"),

        dbc.Col([
            dbc.Label("End Date", className="fw-semibold mb-1"),
            dcc.DatePickerSingle(
                id="end-date",
                display_format="YYYY-MM-DD",
                style={"width": "100%"}
            )
        ], xs=6, md=2, className="d-flex flex-column justify-content-start"),

        dbc.Col([
            dbc.Label("\u00A0", className="mb-1"),  # non-breaking space for alignment
            dbc.Button(
                "Apply Filters",
                id="filter-btn",
                color="primary",
                className="fw-semibold",
                style=button_style
            )
        ], xs=12, md=2, className="d-flex flex-column justify-content-start"),

        dbc.Col([
            dbc.Label("\u00A0", className="mb-1"),
            dbc.Button(
                "Download CSV",
                id="download-btn",
                color="secondary",
                className="fw-semibold",
                style=button_style
            ),
            dcc.Download(id="download-data")
        ], xs=12, md=2, className="d-flex flex-column justify-content-start"),
    ], className="mb-4 align-items-center"),

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