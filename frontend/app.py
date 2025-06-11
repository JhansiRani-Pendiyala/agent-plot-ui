import dash
import dash_bootstrap_components as dbc
from layout import layout
from callbacks import register_callbacks

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
app.title = "Responsive Sales Dashboard"
app.layout = layout

register_callbacks(app)

if __name__ == "__main__":
    app.run(debug=True, port=8070)