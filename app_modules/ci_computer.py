import pandas as pd
import os
import dash
from dash import dash_table
from dash import html

robotoFont = [
    "https://fonts.googleapis.com/css2?family=Roboto&display=swap"
]

def init_dataTbl(server):
    base_dir = os.path.dirname(os.path.dirname(__file__))

    # Initialize Dash app with Flask server and route prefix
    tbl_app = dash.Dash(
        __name__,
        server=server,
        url_base_pathname='/tbl/',
        external_stylesheets=robotoFont
    )
    
    # Construct path to CSV file
    csv_path = os.path.join(os.path.dirname(__file__), 'cmdb_ci_computer.csv')
    # csv_path = os.path.join(base_dir, 'static', 'cmdb_ci_computer.csv')

    # Read CSV into DataFrame with safe encoding
    df = pd.read_csv(csv_path, encoding='ISO-8859-1')

    # Filter and Count 'asset_tag' based on specific prefixes
    prefixes = ['21H', '22H', '23H', '24H', '25H']
    count_data = []

    for prefix in prefixes:
        count = df['asset_tag'].astype(str).str.startswith(prefix).sum()
        count_data.append({'Prefix': prefix, 'Count': count})

    # Create Summary Table for Counts
    count_table = dash_table.DataTable(
        columns=[
            {"name": "Asset_Yr", "id": "Prefix"},
            {"name": "Count", "id": "Count"}
        ],
        data=count_data,
        style_table={'width': 'max-content', 'margin-bottom': '20px'},
        style_cell={'textAlign': 'left', 'padding': '5px'},
        style_header={'backgroundColor': 'lightgrey', 'fontWeight': 'bold'}
    )

    # Create Main Data Table
    main_table = dash_table.DataTable(
        columns=[{"name": i, "id": i} for i in df.columns],
        data=df.to_dict('records'),
        page_size=100,
        style_table={'overflowX': 'auto'},
        style_cell={'textAlign': 'left', 'padding': '5px'},
        style_header={'backgroundColor': 'lightgrey', 'fontWeight': 'bold'}
    )

    tbl_app.layout = html.Div([
        html.H3("Asset Tag Count Summary"),
        html.H4(os.path.join(base_dir, 'static', 'cmdb_ci_computer.csv')),
        count_table,
        html.H3("CI Computer Data"),
        main_table
    ])

    return tbl_app
