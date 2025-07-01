import pandas as pd
import plotly.express as px
import os
import dash
from dash import Dash, html, dcc, dash_table
import dash_bootstrap_components as dbc

BASE_DIR = os.path.dirname(os.path.dirname(__file__))


def init_dataTbl(server):
    # Construct path to CSV file
    csv_path = os.path.join(BASE_DIR, 'app_modules', 'assets', 'data', 'cmdb_ci_computer.csv')

    # Initialize Dash app with Flask server and Bootstrap theme
    tbl_app = dash.Dash(
        __name__,
        server=server,
        url_base_pathname='/v1/',
        external_stylesheets=[dbc.themes.BOOTSTRAP]
    )

    # Read CSV into DataFrame with safe encoding
    df = pd.read_csv(csv_path, encoding='ISO-8859-1')

    # Filter and Count 'asset_tag' based on specific prefixes
    prefixes = ['21H', '22H', '23H', '24H', '25H']
    count_data = []

    for prefix in prefixes:
        count = df['asset_tag'].astype(str).str.startswith(prefix).sum()
        count_data.append({'Prefix': prefix, 'Count': count})

    # Create Summary Table wrapped in Bootstrap Card
    count_table = dbc.Card(
        [
            dbc.CardHeader("Asset Tag Count Summary"),
            dbc.CardBody(
                dash_table.DataTable(
                    columns=[
                        {"name": "Asset_Yr", "id": "Prefix"},
                        {"name": "Count", "id": "Count"}
                    ],
                    data=count_data,
                    style_table={'overflowX': 'auto', 'width': '100%'},
                    style_cell={'textAlign': 'left', 'padding': '5px'},
                    style_header={'backgroundColor': '#f8f9fa', 'fontWeight': 'bold'}
                )
            )
        ],
        className="mb-4"
    )

    # Create Bar Chart wrapped in Bootstrap Card
    count_df = pd.DataFrame(count_data)
    bar_fig = px.bar(
        count_df,
        x='Prefix',
        y='Count',
        title='Asset Tag Count by Year',
        text='Count'
    )
    bar_fig.update_traces(textposition='outside')

    bar_chart = dbc.Card(
        [
            dbc.CardHeader("Asset Tag Yearly Distribution"),
            dbc.CardBody(
                dcc.Graph(figure=bar_fig)
            )
        ],
        className="mb-4"
    )

    # Main Data Table wrapped in Bootstrap Card
    main_table = dbc.Card(
        [
            dbc.CardHeader("CI Computer Data"),
            dbc.CardBody(
                [
                    html.P("Available Columns:"),
                    html.Code(", ".join(df.columns)),
                    dash_table.DataTable(
                        columns=[{"name": i, "id": i} for i in df.columns],
                        data=df.to_dict('records'),
                        page_size=100,
                        style_table={'overflowX': 'auto', 'maxHeight': '600px', 'overflowY': 'auto'},
                        style_cell={'textAlign': 'left', 'padding': '5px'},
                        style_header={'backgroundColor': '#f8f9fa', 'fontWeight': 'bold'},
                        style_data_conditional=[{
                                                'if': {'state': 'active'},  # This targets hovered cells
                                                'backgroundColor': '#D6EAF8',  # Light blue, you can customize
                                                'color': 'black',
                                                'cursor': 'pointer'  # Optional, adds pointer cursor on hover
                                                }]
                    )
                ]
            )
        ]
    )

    # Full Layout with Bootstrap Grid
    tbl_app.layout = dbc.Container(
        [
            html.H2("Mayenne Computer Asset Summary", className="mt-4 mb-4"),
            count_table,
            bar_chart,
            main_table
        ],
        fluid=True,
        className="p-4"
    )

    return tbl_app
