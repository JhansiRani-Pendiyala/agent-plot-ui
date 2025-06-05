import dash
from dash import dcc, html, dash_table
import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd
from datetime import datetime, timedelta

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
app.title = "Ellie Rogers's team"

# Custom CSS for fonts and colors to match the image
app.index_string = '''
<!DOCTYPE html>
<html>
    <head>
        {%metas%}
        <title>{%title%}</title>
        {%favicon%}
        {%css%}
        <link href="https://fonts.googleapis.com/css2?family=Roboto:wght@400;500;700&display=swap" rel="stylesheet">
        <style>
            body, h1, h2, h3, h4, h5, h6, p {
                font-family: 'Roboto', sans-serif !important;
            }
            .card-title {
                font-size: 14px !important;
                font-weight: 500 !important;
                color: #333 !important;
            }
            .card-text {
                font-size: 24px !important;
                font-weight: 700 !important;
            }
            .kpi-card {
                background-color: #4E79A7 !important;
                color: white !important;
                border: none !important;
            }
            .chart-title {
                font-size: 14px !important;
                font-weight: 500 !important;
                color: #333 !important;
            }
            .tableau-header {
                background-color: #2C3E50 !important;
                color: white !important;
                padding: 5px 10px !important;
                font-size: 12px !important;
            }
            .filter-text {
                font-size: 12px !important;
                color: #666 !important;
            }
        </style>
    </head>
    <body>
        {%app_entry%}
        <footer>
            {%config%}
            {%scripts%}
            {%renderer%}
        </footer>
    </body>
</html>
'''

# Data for charts and table
start_date = datetime(2017, 10, 4)
dates = [start_date + timedelta(days=x) for x in range(26)]
closing_opportunities = [5, 7, 10, 12, 15, 18, 20, 22, 20, 18, 15, 12, 10, 8, 7, 6, 5, 4, 3, 2, 1, 1, 0, 0, 0, 0]

df_closing = pd.DataFrame({
    'Date': dates,
    'Opportunities': closing_opportunities
})

stages = ['Qualification', 'Needs Analysis', 'Value Proposition', 'Id. Decision Makers', 'Perception Analysis', 'Negotiation/Review']
breakdown_values = [30, 25, 20, 15, 10, 5]
days_in_stage = [20, 25, 30, 35, 40, 45]

df_breakdown = pd.DataFrame({
    'Stage': stages,
    'Opportunities': breakdown_values
})

df_stage_days = pd.DataFrame({
    'Stage': stages,
    'Opportunities': breakdown_values,
    'Days': days_in_stage
})

top_opportunities = pd.DataFrame({
    'Opportunity': ['10th Open Opportunity', 'Salesforce Einstein PC', 'Salesforce Einstein PC', 'Salesforce Einstein PC', 
                    'Salesforce Einstein PC', 'Salesforce Einstein PC', 'Salesforce Einstein PC', 'Salesforce Einstein PC', 
                    'Salesforce Einstein PC', 'Salesforce Einstein PC'],
    'Expected Amount': ['$75,000', '$72,000', '$68,000', '$65,000', '$60,000', '$55,000', '$50,000', '$45,000', '$40,000', '$35,000']
})

# App layout
app.layout = dbc.Container([
    # Simulated Tableau Header
    html.Div([
        html.Span("Home | Salesforce | Open Pipeline", className="tableau-header")
    ], className="mb-2"),

    dbc.Card([
        dbc.CardBody([
            # Title
            html.H4("Ellie Rogers's team", className="mb-3", style={'fontSize': '20px', 'fontWeight': '700'}),

            # KPIs
            dbc.Row([
                dbc.Col(dbc.Card([
                    dbc.CardBody([
                        html.H6("Total Expected Amount", className="card-title text-center"),
                        html.H3("$3,093,000", className="card-text text-center")
                    ])
                ], className="kpi-card"), xs=12, md=3),
                dbc.Col(dbc.Card([
                    dbc.CardBody([
                        html.H6("Average Deal Size", className="card-title text-center"),
                        html.H3("$19,453", className="card-text text-center")
                    ])
                ], className="kpi-card"), xs=12, md=3),
                dbc.Col(dbc.Card([
                    dbc.CardBody([
                        html.H6("Number of Opportunities", className="card-title text-center"),
                        html.H3("159", className="card-text text-center")
                    ])
                ], className="kpi-card"), xs=12, md=3),
                dbc.Col(dbc.Card([
                    dbc.CardBody([
                        html.H6("Avg Age of Opportunity", className="card-title text-center"),
                        html.H3("75 days", className="card-text text-center")
                    ])
                ], className="kpi-card"), xs=12, md=3),
            ], className="mb-4"),

            # Charts and Table
            dbc.Row([
                # Left Column (Pipeline Overview)
                dbc.Col([
                    html.H5("Open Pipeline", className="chart-title mb-2"),
                    html.P("Use Options Below to Filter", className="filter-text"),
                    dcc.Graph(
                        figure=px.line(df_closing, x='Date', y='Opportunities', title="Overall Opportunities Closing by Day",
                                       color_discrete_sequence=['#4E79A7']).update_layout(
                            showlegend=False,
                            margin=dict(l=20, r=20, t=30, b=20),
                            xaxis_title="",
                            yaxis_title=""
                        ),
                        config={'displayModeBar': False}
                    ),
                    dcc.Graph(
                        figure=px.bar(df_breakdown, x='Opportunities', y='Stage', orientation='h',
                                      title="Breakdown by Stage | by Day",
                                      color_discrete_sequence=['#F7CA18']).update_layout(
                            showlegend=False,
                            margin=dict(l=20, r=20, t=30, b=20),
                            xaxis_title="",
                            yaxis_title=""
                        ),
                        config={'displayModeBar': False}
                    )
                ], xs=12, md=6),

                # Right Column (Opportunities and Days in Stage)
                dbc.Col([
                    html.H5("Number of Open Opportunities", className="chart-title mb-2"),
                    html.P("Click a Filter to Filter", className="filter-text"),
                    dcc.Graph(
                        figure=px.bar(df_stage_days, x='Opportunities', y='Stage', orientation='h',
                                      title="Number of Open Opportunities and Average Days in Stage",
                                      color_discrete_sequence=['#F7CA18']).update_layout(
                            showlegend=False,
                            margin=dict(l=20, r=20, t=30, b=20),
                            xaxis_title="Opportunities",
                            yaxis_title="Days in Stage"
                        ),
                        config={'displayModeBar': False}
                    ),
                    html.H5("Top 10 Opportunities | by Expected Amount", className="chart-title mb-2"),
                    dash_table.DataTable(
                        data=top_opportunities.to_dict('records'),
                        columns=[{'name': i, 'id': i} for i in top_opportunities.columns],
                        style_table={'overflowX': 'auto'},
                        style_header={'backgroundColor': '#F7CA18', 'fontWeight': 'bold', 'color': '#333'},
                        style_data={'backgroundColor': '#FFFFFF', 'color': '#333'},
                        style_cell={'fontSize': 14, 'fontFamily': 'Roboto', 'textAlign': 'left', 'padding': '5px'}
                    )
                ], xs=12, md=6)
            ])
        ])
    ])
], fluid=True)

if __name__ == "__main__":
    app.run(debug=True, port=8090)