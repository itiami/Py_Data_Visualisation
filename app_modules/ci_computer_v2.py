import pandas as pd
import plotly.express as px
import os
import dash
from dash import Dash, html, dcc, dash_table, Input, Output
import dash_bootstrap_components as dbc

BASE_DIR = os.path.dirname(os.path.dirname(__file__))

def init_dataTbl(server):
    csv_path = os.path.join(BASE_DIR, 'app_modules', 'assets', 'data', 'cmdb_ci_computer.csv')

    tbl_app = dash.Dash(
        __name__,
        server=server,
        url_base_pathname='/v2/',
        external_stylesheets=[dbc.themes.BOOTSTRAP]
    )

    df = pd.read_csv(csv_path, encoding='ISO-8859-1')

    # Pie Chart for asset_tag count
    asset_counts = df['asset_tag'].value_counts().reset_index()
    asset_counts.columns = ['asset_tag', 'count']

    pie_fig = px.pie(asset_counts, names='asset_tag', values='count', title='Asset Distribution by Asset Tag')

    pie_chart = dbc.Card(
        [
            dbc.CardHeader("Asset Tag Distribution"),
            dbc.CardBody(dcc.Graph(figure=pie_fig))
        ],
        className="mb-4"
    )

    # Categorize devices as Laptop/Desktop based on name prefix
    df['Device_Type'] = df['name'].astype(str).apply(
        lambda x: 'Desktop' if x.startswith(('com8cc', 'terwd', '8cc')) else 'Laptop'
    )

    scatter_fig = px.scatter(
        df,
        x='asset_tag',
        y='u_build_machine_use',
        color='Device_Type',
        title='Device Type vs Build Machine Use',
        hover_data=['name', 'department', 'location']
    )

    scatter_chart = dbc.Card(
        [
            dbc.CardHeader("Device Type Scatter Plot"),
            dbc.CardBody(dcc.Graph(figure=scatter_fig))
        ],
        className="mb-4"
    )

    # Multi-select dropdown to choose columns to display
    available_columns = df.columns.tolist()

    main_table = dbc.Card(
        [
            dbc.CardHeader("CI Computer Data (Customizable Columns)"),
            dbc.CardBody(
                [
                    html.Label("Select Columns to Display:"),
                    dcc.Dropdown(
                        id='column-selector',
                        options=[{'label': col, 'value': col} for col in available_columns],
                        value=available_columns,  # Default to all columns
                        multi=True,
                        style={'marginBottom': '20px'}
                    ),
                    dash_table.DataTable(
                        id='main-table',
                        data=df.to_dict('records'),
                        columns=[{"name": col, "id": col} for col in available_columns],
                        page_size=100,
                        style_table={'overflowX': 'auto', 'maxHeight': '600px', 'overflowY': 'auto'},
                        style_cell={'textAlign': 'left', 'padding': '5px'},
                        style_header={'backgroundColor': '#f8f9fa', 'fontWeight': 'bold'},
                        style_data_conditional=[
                            {'if': {'state': 'active'}, 'backgroundColor': '#D6EAF8', 'color': 'black'}
                        ]
                    )
                ]
            )
        ]
    )

    tbl_app.layout = dbc.Container(
        [
            html.H2("Mayenne Computer Asset Summary", className="mt-4 mb-4"),
            pie_chart,
            scatter_chart,
            main_table
        ],
        fluid=True,
        className="p-4"
    )

    @tbl_app.callback(
        Output('main-table', 'columns'),
        Input('column-selector', 'value')
    )
    def update_table_columns(selected_cols):
        return [{"name": col, "id": col} for col in selected_cols]

    return tbl_app
