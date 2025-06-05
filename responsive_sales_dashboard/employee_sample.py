import pandas as pd
from dash import Dash, html, dcc, Input, Output, State
import plotly.express as px

# Simulated data (replace with your fetch_data function in a real application)
def fetch_data(search_text, start_date, end_date):
    data = {
        'employee_id': range(359),
        'quarter': ['Q1']*90 + ['Q2']*80 + ['Q3']*90 + ['Q4']*99,
        'tenure_years': [0.5]*50 + [1.5]*60 + [2.5]*70 + [3.5]*80 + [5]*99,
        'department': ['Legal']*80 + ['Development']*75 + ['Finance']*60 + ['Marketing']*50 + ['HR']*44 + ['Resources']*30 + ['Sales']*20,
        'position': ['Senior Director']*70 + ['Vice President']*60 + ['Director']*55 + ['Mid-Level']*50 + ['Manager']*44 + ['Individual Contributor']*40 + ['Entry-Level']*40,
        'turnover_type': ['Voluntary']*251 + ['Involuntary']*108,
        'turnover_reason': ['Higher Pay']*90 + ['Better Opportunity']*80 + ['Relocation']*70 + ['Work-Life Balance']*60 + ['Career Change']*59
    }
    df = pd.DataFrame(data)
    return df

# Initialize the Dash app
app = Dash(__name__)

# App layout
app.layout = html.Div([
    html.H1("Employee Turnover Dashboard", style={'textAlign': 'center', 'color': '#003087'}),
    
    # KPI Section
    html.Div([
        html.Div([
            html.H3("Employees Turnover"),
            html.H2(id='kpi-total', style={'color': '#003087'})
        ], style={'width': '30%', 'display': 'inline-block', 'textAlign': 'center'}),
        html.Div([
            html.H3("Turnover Rate"),
            html.H2(id='kpi-rate', style={'color': '#003087'})
        ], style={'width': '30%', 'display': 'inline-block', 'textAlign': 'center'}),
        html.Div([
            html.H3("Avg. Years Tenure"),
            html.H2(id='kpi-tenure', style={'color': '#003087'})
        ], style={'width': '30%', 'display': 'inline-block', 'textAlign': 'center'}),
    ], style={'marginBottom': '20px'}),
    
    # Filter Section
    html.Div([
        dcc.Input(id='search-input', placeholder='Search...', type='text', style={'marginRight': '10px'}),
        dcc.DatePickerSingle(id='start-date', date='2024-01-01', style={'marginRight': '10px'}),
        dcc.DatePickerSingle(id='end-date', date='2024-12-31', style={'marginRight': '10px'}),
        html.Button('Filter', id='filter-btn', n_clicks=0)
    ], style={'marginBottom': '20px', 'textAlign': 'center'}),
    
    # Charts Section
    html.Div([
        # Turnover per Quarter and Tenure
        html.Div([
            dcc.Graph(id='quarter-bar-chart'),
            dcc.Graph(id='tenure-bar-chart')
        ], style={'width': '48%', 'display': 'inline-block'}),
        
        # Turnover by Department, Position, and Type
        html.Div([
            dcc.Graph(id='dept-bar-chart'),
            dcc.Graph(id='position-bar-chart'),
            dcc.Graph(id='type-donut-chart')
        ], style={'width': '48%', 'display': 'inline-block', 'verticalAlign': 'top'}),
    ], style={'display': 'flex', 'justifyContent': 'space-between'}),
    
    # Turnover Reasons
    dcc.Graph(id='reason-bar-chart')
])

# Register callbacks
def register_callbacks(app):
    @app.callback(
        [Output('kpi-total', 'children'),
         Output('kpi-rate', 'children'),
         Output('kpi-tenure', 'children'),
         Output('quarter-bar-chart', 'figure'),
         Output('tenure-bar-chart', 'figure'),
         Output('dept-bar-chart', 'figure'),
         Output('position-bar-chart', 'figure'),
         Output('type-donut-chart', 'figure'),
         Output('reason-bar-chart', 'figure')],
        Input('filter-btn', 'n_clicks'),
        [State('search-input', 'value'),
         State('start-date', 'date'),
         State('end-date', 'date')],
        prevent_initial_call=True
    )
    def update_dashboard(n_clicks, search_text, start_date, end_date):
        df = fetch_data(search_text, start_date, end_date)

        # KPIs
        total_turnover = len(df) if not df.empty else 0
        total_employees = 1994  # Derived from 359 / 0.18
        turnover_rate = round((total_turnover / total_employees) * 100, 1) if total_employees > 0 else 0
        avg_tenure = round(df['tenure_years'].mean(), 1) if not df.empty else 0

        # Turnover per Quarter
        quarter_df = df.groupby('quarter', as_index=False).size()
        quarter_fig = px.bar(
            quarter_df,
            x='quarter',
            y='size',
            title="Turnover per Quarter",
            labels={"quarter": "Quarter", "size": "Turnovers"},
            color_discrete_sequence=['#0074D9']
        ) if not quarter_df.empty else {}
        if quarter_fig:
            quarter_fig.update_layout(plot_bgcolor='white', paper_bgcolor='white', font=dict(size=12))

        # Turnover by Length of Employment
        tenure_bins = [0, 1, 2, 3, 4, float('inf')]
        tenure_labels = ['<1 Year', '1-2 Years', '2-3 Years', '3-4 Years', '>4 Years']
        df['tenure_group'] = pd.cut(df['tenure_years'], bins=tenure_bins, labels=tenure_labels, include_lowest=True)
        tenure_df = df.groupby('tenure_group', as_index=False).size()
        tenure_fig = px.bar(
            tenure_df,
            x='tenure_group',
            y='size',
            title="Turnover by Length of Employment",
            labels={"tenure_group": "Years of Employment", "size": "Turnovers"},
            color_discrete_sequence=['#0074D9']
        ) if not tenure_df.empty else {}
        if tenure_fig:
            tenure_fig.update_layout(plot_bgcolor='white', paper_bgcolor='white', font=dict(size=12))

        # Turnover by Department
        dept_df = df.groupby('department', as_index=False).size()
        dept_df['percentage'] = (dept_df['size'] / total_turnover * 100).round(1)
        dept_fig = px.bar(
            dept_df,
            x='percentage',
            y='department',
            orientation='h',
            title="Turnover % per Department",
            labels={"percentage": "Turnover %", "department": "Department"},
            color_discrete_sequence=['#0074D9']
        ) if not dept_df.empty else {}
        if dept_fig:
            dept_fig.update_layout(plot_bgcolor='white', paper_bgcolor='white', font=dict(size=12))

        # Turnover by Position
        pos_df = df.groupby('position', as_index=False).size()
        pos_df['percentage'] = (pos_df['size'] / total_turnover * 100).round(1)
        pos_fig = px.bar(
            pos_df,
            x='percentage',
            y='position',
            orientation='h',
            title="Turnover % per Position",
            labels={"percentage": "Turnover %", "position": "Position"},
            color_discrete_sequence=['#0074D9']
        ) if not pos_df.empty else {}
        if pos_fig:
            pos_fig.update_layout(plot_bgcolor='white', paper_bgcolor='white', font=dict(size=12))

        # Turnover Type (Donut Chart)
        type_df = df.groupby('turnover_type', as_index=False).size()
        type_fig = px.pie(
            type_df,
            names='turnover_type',
            values='size',
            title="Turnover Type",
            hole=0.4,
            color_discrete_sequence=['#0074D9', '#D3D3D3']
        ) if not type_df.empty else {}
        if type_fig:
            type_fig.update_traces(textinfo='percent+label')

        # Turnover Reasons
        reason_df = df.groupby('turnover_reason', as_index=False).size()
        reason_fig = px.bar(
            reason_df,
            x='size',
            y='turnover_reason',
            orientation='h',
            title="Turnover Reasons",
            labels={"size": "Turnovers", "turnover_reason": "Reason"},
            color_discrete_sequence=['#0074D9']
        ) if not reason_df.empty else {}
        if reason_fig:
            reason_fig.update_layout(plot_bgcolor='white', paper_bgcolor='white', font=dict(size=12))

        return str(total_turnover), f"{turnover_rate}%", str(avg_tenure), quarter_fig, tenure_fig, dept_fig, pos_fig, type_fig, reason_fig

# Register the callbacks
register_callbacks(app)

# Run the app
if __name__ == '__main__':
    app.run(debug=True, port=8050)