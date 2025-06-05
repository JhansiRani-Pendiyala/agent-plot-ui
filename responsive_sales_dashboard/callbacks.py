from dash import Input, Output, State
import plotly.express as px
from data import fetch_data

def register_callbacks(app):
    print("Registering callbacks...")  # Debug print

    @app.callback(
        [Output('kpi-total', 'children'),
         Output('kpi-average', 'children'),
         Output('bar-chart', 'figure'),
         Output('donut-chart', 'figure'),
         Output('data-table', 'data'),
         Output('data-table', 'columns')],
        Input('filter-btn', 'n_clicks'),
        [State('search-input', 'value'),
         State('start-date', 'date'),
         State('end-date', 'date')],
        prevent_initial_call=True
    )
    def update_dashboard(n_clicks, search_text, start_date, end_date):
        print("Callback triggered:", search_text, start_date, end_date)
        df = fetch_data(search_text, start_date, end_date)
        total = df['total_products_sold'].sum() if not df.empty else 0
        avg = round(df['total_products_sold'].mean(), 2) if not df.empty else 0

        if not df.empty:
            # Sort df for horizontal bar chart (ascending so biggest bars top)
            df_sorted = df.sort_values(by='total_products_sold', ascending=True)

            bar_fig = px.bar(
                df_sorted,
                x='total_products_sold',
                y='full_name',
                orientation='h',
                title="Products Sold by Employee",
                labels={"full_name": "Employee", "total_products_sold": "Units Sold"},
                text='total_products_sold'
            )

            bar_fig.update_traces(
                textposition='outside',
                marker_line_color="#8fafe7",  # dark blue line
                marker_line_width=1.5,
                hovertemplate='<b>%{y}</b><br>Units Sold: %{x}<extra></extra>'
            )

            bar_fig.update_layout(
                yaxis=dict(autorange="reversed"),
                xaxis_title="Units Sold",
                yaxis_title="Employee",
                plot_bgcolor='white',
                paper_bgcolor='white',
                font=dict(size=14),
                margin=dict(t=60, l=160, r=40, b=50),
                hovermode="y unified",
                uniformtext_minsize=12,
                uniformtext_mode='hide'
            )

            bar_fig.update_xaxes(showgrid=True, gridwidth=1, gridcolor='#4A7592')
            bar_fig.update_yaxes(showgrid=False)

            # Donut chart based on exploded product_list
            if 'product_list' in df.columns:
                # Ensure product_list is a list
                df['product_list'] = df['product_list'].apply(
                    lambda x: x if isinstance(x, list) else [x]
                )
                df_exploded = df.explode('product_list')
                filtered_df = df_exploded[df_exploded['product_list'].notnull()]
                grouped_df = filtered_df.groupby('product_list', as_index=False)['total_products_sold'].sum()

                donut_fig = px.pie(
                    grouped_df,
                    names='product_list',
                    values='total_products_sold',
                    title="Sales Distribution by Product",
                    hole=0.4,
                    color_discrete_sequence=px.colors.sequential.GnBu
                ) if not grouped_df.empty else {}
            else:
                donut_fig = {}
             
            # Convert product_list back to comma string for display
            if 'product_list' in df.columns:
                df['product_list'] = df['product_list'].apply(
                    lambda x: ", ".join(str(i) if i is not None else '' for i in x) if isinstance(x, list) else x
                )
            # Format dates nicely
            if 'created_date' in df.columns:
                df['created_date'] = df['created_date'].dt.strftime('%Y-%m-%d')

        else:
            bar_fig = {}
            donut_fig = {}

        columns = [{"name": col.replace("_", " ").title(), "id": col} for col in df.columns]

        return str(total), str(avg), bar_fig, donut_fig, df.to_dict('records'), columns