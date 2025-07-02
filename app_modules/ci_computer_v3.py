import pandas as pd
import plotly.express as px
import os
import dash
from dash import Dash, html, dcc, dash_table, Input, Output
import dash_bootstrap_components as dbc

def init_dataTbl(server):
    BASE_DIR = os.path.dirname(os.path.dirname(__file__))
    # Construct path to CSV file
    csv_path = os.path.join(BASE_DIR, 'app_modules', 'assets', 'data', 'cmdb_ci_computer.csv')

    # Initialize Dash app with Flask server and Bootstrap theme
    tbl_app = dash.Dash(
        __name__,
        server=server,
        url_base_pathname='/v3/',
        external_stylesheets=[dbc.themes.BOOTSTRAP]
    )

    # Read CSV into DataFrame with safe encoding
    df = pd.read_csv(csv_path, encoding='ISO-8859-1')

    # 1. Pie Chart Data - Count of assets by asset_tag prefix
    prefixes = ['21H', '22H', '23H', '24H', '25H']
    count_data = []
    for prefix in prefixes:
        count = df['asset_tag'].astype(str).str.startswith(prefix).sum()
        count_data.append({'Prefix': prefix, 'Count': count})
    count_df = pd.DataFrame(count_data)

    pie_fig = px.pie(
        count_df,
        names='Prefix',
        values='Count',
        title='Asset Tag Distribution by Year'
    )
    pie_chart = dbc.Card(
        [
            dbc.CardHeader("Asset Tag Distribution"),
            dbc.CardBody(
                dcc.Graph(figure=pie_fig)
            )
        ],
        className="mb-4"
    )

    # 2. Line Plot - Device Type vs Build Type Count
    # Determine device type based on name prefix
    df['Device_Type'] = df['name'].apply(
        lambda x: 'Desktop' if str(x).startswith(('com8cc', 'terwd', '8cc')) else 'Laptop'
    )
    
    # Group data to count build types by device type
    grouped_df = df.groupby(['Device_Type', 'u_build_machine_use']).size().reset_index(name='Count')

    line_fig = px.line(
        grouped_df,
        x='u_build_machine_use',
        y='Count',
        color='Device_Type',
        title='Device Type vs Build Type Count',
        markers=True,
        labels={
            'u_build_machine_use': 'Build Type',
            'Count': 'Count'
        }
    )
    
    line_chart = dbc.Card(
        [
            dbc.CardHeader("Device Type vs Build Type (Line Plot)"),
            dbc.CardBody(
                dcc.Graph(figure=line_fig)
            )
        ],
        className="mb-4"
    )

    # 3. Main Table with Sorting and Column Selection
    all_columns = [
        'name', 'asset_tag', 'asset', 'assigned_to', 'department', 'location',
        'u_build_business_owner', 'u_build_deployment_type', 'u_build_primary_user',
        'u_build_machine_use', 'u_build_site', 'u_build_use', 'install_status',
        'hardware_substatus', 'u_primary_pc'
    ]

    # Dropdown for column selection
    column_dropdown = dbc.Card(
        [
            dbc.CardHeader("Select Columns to Display"),
            dbc.CardBody(
                dcc.Dropdown(
                    id='column-select',
                    options=[{'label': col, 'value': col} for col in all_columns],
                    value=all_columns,  # Default: all columns
                    multi=True,
                    clearable=False
                )
            )
        ],
        className="mb-4"
    )

    main_table = dbc.Card(
        [
            dbc.CardHeader("CI Computer Data"),
            dbc.CardBody(
                [
                    dash_table.DataTable(
                        id='main-table',
                        columns=[{"name": col, "id": col} for col in all_columns],
                        data=df.to_dict('records'),
                        page_size=100,
                        sort_action='native',  # Enable sorting
                        style_table={'overflowX': 'auto', 'maxHeight': '600px', 'overflowY': 'auto'},
                        style_cell={'textAlign': 'left', 'padding': '5px'},
                        style_header={'backgroundColor': '#f8f9fa', 'fontWeight': 'bold'},
                        style_data_conditional=[{
                            'if': {'state': 'active'},
                            'backgroundColor': '#D6EAF8',
                            'color': 'black',
                            'cursor': 'pointer'
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
            pie_chart,
            line_chart,
            column_dropdown,
            main_table
        ],
        fluid=True,
        className="p-4"
    )

    # Callback to update table columns based on dropdown selection
    @tbl_app.callback(
        Output('main-table', 'columns'),
        Input('column-select', 'value')
    )
    def update_table_columns(selected_columns):
        return [{"name": col, "id": col} for col in selected_columns]

    return tbl_app
