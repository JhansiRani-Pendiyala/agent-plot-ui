import requests
import dash
from dash import dcc, html
import plotly.graph_objs as go
from dash.dependencies import Input, Output, State

API_URL = "http://localhost:8080/api/query"

def fetch_data(user_input=None):
    try:
        headers = {'Content-Type': 'application/json', 'Accept': 'application/json'}
        payload = {"query": user_input} if user_input else {}
        response = requests.post(API_URL, json=payload, headers=headers)
        response.raise_for_status()
        data = response.json()
        print("API response:", data)
        return data
    except requests.RequestException as e:
        print(f"Error fetching data: {e}")
        return []

# Utility: Get first non-empty field from options
def get_first_available(item, keys, default=None):
    for key in keys:
        val = item.get(key)
        if val is not None and val != '':
            return val
    return default

def extract_columns_flexible(data, key1_options, key2_options, default=None):
    col1 = []
    col2 = []
    for item in data:
        col1.append(get_first_available(item, key1_options, default))
        col2.append(get_first_available(item, key2_options, default))
    return col1, col2

app = dash.Dash(__name__)
app.title = "Employee Sales Dashboard"

app.layout = html.Div(
    style={
        'display': 'flex',
        'flexDirection': 'column',
        'justifyContent': 'center',
        'alignItems': 'center',
        'height': '100vh',
        'fontFamily': 'Arial',
        'padding': '40px',
        'maxWidth': '1000px',
        'margin': '0 auto',
        'textAlign': 'center',
    },
    children=[
        html.H2("📊 Employee Sales Dashboard"),

        html.Div(style={'display': 'flex', 'justifyContent': 'center', 'marginBottom': '30px'}, children=[
            dcc.Input(
                id='text-input',
                type='text',
                placeholder='Enter filter text...',
                style={'width': '300px', 'padding': '8px'}
            ),
            html.Button('Submit', id='submit-button', n_clicks=0, style={'marginLeft': '10px', 'padding': '8px 16px'})
        ]),

        html.Div(id='total-employees', style={'fontSize': '20px', 'marginBottom': '20px', 'fontWeight': 'bold'}),

        html.Div(style={'display': 'flex', 'justifyContent': 'center', 'gap': '40px', 'width': '100%'}, children=[
            dcc.Graph(id='sales-chart', style={'flex': '1'}),
            dcc.Graph(id='sales-chart-2', style={'flex': '1'})
        ]),
    ]
)

@app.callback(
    [Output('sales-chart', 'figure'), Output('total-employees', 'children'), Output('sales-chart-2', 'figure')],
    Input('submit-button', 'n_clicks'),
    State('text-input', 'value')
)
def update_dashboard(n_clicks, user_input):
    employees = fetch_data(user_input)
    total_employees = len(employees)

    if total_employees == 0:
        empty_fig = go.Figure()
        return empty_fig, "No data available", empty_fig

    # Sort using the best available employee ID key
    employees_sorted = sorted(
        employees,
        key=lambda e: get_first_available(e, ['employee_id', 'emp_id', 'id'], default=0)
    )

    # Dynamically extract employee IDs and sales values
    labels, sales = extract_columns_flexible(
        employees_sorted,
        key1_options=[
            'employee_id', 'emp_id', 'id', 'employeeId', 
            'first_name', 'last_name'
        ],
        key2_options=[
            'total_sales_amount', 'total_sales', 
            'sales', 'total_products_sold', 'sold_products'
        ],
        default=0
    )

    fig1 = go.Figure(data=[
        go.Bar(
            x=labels,
            y=sales,
            marker=dict(color='royalblue'),
            width=0.5
        ),
    ])
    fig1.update_layout(
        xaxis_title='Employee ID',
        yaxis_title='Total Sales',
        bargap=0.3,
        template='plotly_white'
    )

    fig2 = go.Figure(data=[
        go.Scatter(
            x=labels,
            y=sales,
            mode='lines+markers',
            line=dict(color='green'),
            name='Sales Trend',
            customdata=[
                (
                    emp.get('first_name', ''),
                    emp.get('last_name', ''),
                    ', '.join(emp['sold_products']) if emp.get('sold_products') else '',
                    get_first_available(emp, ['total_sales_amount', 'total_sales', 'sales'], 0)
                )
                for emp in employees_sorted
            ],
            hovertemplate=(
                "Employee ID: %{x}<br>"
                "First Name: %{customdata[0]}<br>"
                "Last Name: %{customdata[1]}<br>"
                "Total Sales: $%{customdata[3]:,.2f}<extra></extra><br>"
                "%{customdata[2]}"
            )
        )
    ])
    fig2.update_layout(
        xaxis_title='Employee ID',
        yaxis_title='Total Sales',
        template='plotly_white'
    )

    total_text = f"Total Employees: {total_employees}"
    return fig1, total_text, fig2

if __name__ == '__main__':
    app.run(debug=True)