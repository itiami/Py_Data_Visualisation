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
    # Read CSV into DataFrame with safe encoding
    df = pd.read_csv(csv_path, encoding='ISO-8859-1')

    # Initialize Dash app with Flask server and Bootstrap theme
    tbl_app = dash.Dash(
        __name__,
        server=server,
        url_base_pathname='/v3/',
        external_stylesheets=[dbc.themes.BOOTSTRAP] # [2]
    )

 # [2]

    # 1. Pie Chart Data - Count of assets by asset_tag prefix
    prefixes = ['21H', '22H', '23H', '24H', '25H'] # [2]
    count_data = [] # [2]
    for prefix in prefixes: # [2]
        count = df['asset_tag'].astype(str).str.startswith(prefix).sum() # [2]
        count_data.append({'Prefix': prefix, 'Count': count}) # [2]
    count_df = pd.DataFrame(count_data) # [2]

    pie_fig = px.pie( # [2]
        count_df,
        names='Prefix',
        values='Count',
        title='Asset Tag Distribution by Year' # [3]
    )

    pie_chart = dbc.Card( # [3]
        [
            dbc.CardHeader("Asset Tag Distribution"), # [3]
            dbc.CardBody( # [3]
                dcc.Graph(figure=pie_fig) # [3]
            )
        ],
        className="mb-4" # [3]
    )

    # Prepare data for Bar Chart and Multi-select
    # Determine device type based on name prefix
    df['Device_Type'] = df['name'].apply( # [3]
        lambda x: 'Desktop' if str(x).startswith(('com8cc', 'terwd', '8cc')) else 'Laptop' # [3]
    )
    # Group data to count build types by device type
    grouped_df = df.groupby(['Device_Type', 'u_build_machine_use']).size().reset_index(name='Count') # [3]

    # Create initial Bar Chart
    initial_bar_fig = px.bar( # Replacing line chart with bar chart
        grouped_df,
        x='u_build_machine_use',
        y='Count',
        color='Device_Type',
        title='Device Type vs Build Type Count', # [1]
        labels={ # [1]
            'u_build_machine_use': 'Build Type', # [1]
            'Count': 'Count' # [1]
        },
        barmode='group' # To show bars side-by-side for different Device_Types
    )

    bar_chart = dbc.Card(
        [
            dbc.CardHeader("Device Type vs Build Type (Bar Plot)"), # Updated header
            dbc.CardBody(
                dcc.Graph(id='bar-chart-graph', figure=initial_bar_fig) # Added ID for callback
            )
        ],
        className="mb-4"
    )

    # Multi-select option for "u_build_machine_use"
    machine_use_options = sorted([{'label': val, 'value': val} for val in df['u_build_machine_use'].unique() if pd.notna(val)], key=lambda x: x['label'])
    
    machine_use_dropdown = dbc.Card(
        [
            dbc.CardHeader("Select Build Machine Use(s)"),
            dbc.CardBody(
                dcc.Dropdown(
                    id='machine-use-select',
                    options=machine_use_options,
                    value=[option['value'] for option in machine_use_options], # Default: all selected
                    multi=True,
                    clearable=False
                )
            )
        ],
        className="mb-4"
    )

    # 3. Main Table with Sorting and Column Selection
    all_columns = [ # [1, 4]
        'name', 'asset_tag', 'asset', 'assigned_to', 'department', 'location', # [4]
        'u_build_business_owner', 'u_build_deployment_type', 'u_build_primary_user', # [4]
        'u_build_machine_use', 'u_build_site', 'u_build_use', 'install_status', # [4]
        'hardware_substatus', 'u_primary_pc' # [4]
    ]

    # Dropdown for column selection
    column_dropdown = dbc.Card( # [4]
        [
            dbc.CardHeader("Select Columns to Display"), # [4]
            dbc.CardBody( # [4]
                dcc.Dropdown( # [4]
                    id='column-select', # [4]
                    options=[{'label': col, 'value': col} for col in all_columns], # [4]
                    value=all_columns, # Default: all columns # [4]
                    multi=True, # [4]
                    clearable=False # [4]
                )
            )
        ],
        className="mb-4" # [4]
    )

    main_table = dbc.Card( # [4]
        [
            dbc.CardHeader("CI Computer Data"), # [5]
            dbc.CardBody( # [5]
                [ # [5]
                    dash_table.DataTable( # [5]
                        id='main-table', # [5]
                        columns=[{"name": col, "id": col} for col in all_columns], # [5]
                        data=df.to_dict('records'), # [5]
                        page_size=100, # [5]
                        sort_action='native', # Enable sorting # [5]
                        style_table={'overflowX': 'auto', 'maxHeight': '600px', 'overflowY': 'auto'}, # [5]
                        style_cell={'textAlign': 'left', 'padding': '5px'}, # [5]
                        style_header={'backgroundColor': '#f8f9fa', 'fontWeight': 'bold'}, # [5]
                        style_data_conditional=[{ # [5]
                            'if': {'state': 'active'}, # [5]
                            'backgroundColor': '#D6EAF8', # [6]
                            'color': 'black', # [6]
                            'cursor': 'pointer' # [6]
                        }] # [6]
                    ) # [6]
                ]
            )
        ]
    )

    # Full Layout with Bootstrap Grid
    tbl_app.layout = dbc.Container( # [6]
        [
            html.H2("Mayenne Computer Asset Summary", className="mt-4 mb-4"), # [6]
            pie_chart, # [6]
            machine_use_dropdown, # Added the new dropdown
            bar_chart,            # Replaced line_chart with bar_chart
            column_dropdown, # [6]
            main_table # [6]
        ],
        fluid=True, # [6]
        className="p-4" # [6]
    )

    # Callback to update table columns based on dropdown selection
    @tbl_app.callback( # [6]
        Output('main-table', 'columns'), # [6]
        Input('column-select', 'value') # [6]
    )
    def update_table_columns(selected_columns): # [6]
        return [{"name": col, "id": col} for col in selected_columns] # [6]

    # Callback to update bar chart based on multi-select dropdown selection
    @tbl_app.callback(
        Output('bar-chart-graph', 'figure'),
        Input('machine-use-select', 'value')
    )
    def update_bar_chart(selected_machine_uses):
        if not selected_machine_uses:
            # Return an empty figure or a message if nothing is selected
            filtered_df = pd.DataFrame(columns=['Device_Type', 'u_build_machine_use', 'Count'])
            title = 'Device Type vs Build Type Count (No selection)'
        else:
            # Filter the grouped data based on selected machine uses
            filtered_df = grouped_df[grouped_df['u_build_machine_use'].isin(selected_machine_uses)]
            title = 'Device Type vs Build Type Count (Filtered)'

        updated_bar_fig = px.bar(
            filtered_df,
            x='u_build_machine_use',
            y='Count',
            color='Device_Type',
            title=title,
            labels={
                'u_build_machine_use': 'Build Type',
                'Count': 'Count'
            },
            barmode='group'
        )
        return updated_bar_fig

    return tbl_app