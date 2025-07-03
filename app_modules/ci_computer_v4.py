import pandas as pd
import plotly.express as px
import os
import dash
from dash import Dash, html, dcc, dash_table, Input, Output
import dash_bootstrap_components as dbc

def init_dataTbl(server):
    BASE_DIR = os.path.dirname(os.path.dirname(__file__))
    csv_path = os.path.join(BASE_DIR, 'app_modules', 'assets', 'data', 'cmdb_ci_computer.csv')

    # Load CSV data
    df = pd.read_csv(csv_path, encoding='ISO-8859-1')

    # Prepare data for pie chart (count of assets by asset_tag)
    asset_counts = df['asset_tag'].value_counts().reset_index()
    asset_counts.columns = ['asset_tag', 'count']
    
    # Create pie chart
    pie_chart = dcc.Graph(
        id='asset-pie-chart',
        figure=px.pie(
            asset_counts,
            names='asset_tag',
            values='count',
            title='Asset Distribution by Tag'
        ).update_layout(
            margin=dict(t=50, b=50, l=50, r=50),
            height=400
        )
    )

    # Machine use dropdown
    machine_use_options = [{'label': val, 'value': val} for val in df['u_build_machine_use'].unique()]
    machine_use_dropdown = html.Div([
        html.Label("Select Machine Use:", className="form-label"),
        dcc.Dropdown(
            id='machine-use-dropdown',
            options=machine_use_options,
            multi=True,
            value=[machine_use_options[0]['value']] if machine_use_options else [],
            className="mb-3"
        )
    ])

    # Bar chart placeholder
    bar_chart = dcc.Graph(id='machine-use-bar-chart')

    # Column selector for table
    column_options = [{'label': col, 'value': col} for col in df.columns]
    column_dropdown = html.Div([
        html.Label("Select Columns to Display:", className="form-label"),
        dcc.Dropdown(
            id='column-selector',
            options=column_options,
            multi=True,
            value=['name', 'asset_tag', 'asset', 'department', 'location'],
            className="mb-3"
        )
    ])

    # Data table
    main_table = dash_table.DataTable(
        id='main-table',
        columns=[{'name': col, 'id': col, 'sortable': True} for col in ['name', 'asset_tag', 'asset', 'department', 'location']],
        data=df.to_dict('records'),
        style_table={'overflowX': 'auto'},
        style_cell={'textAlign': 'left', 'padding': '5px'},
        style_header={
            'backgroundColor': 'rgb(230, 230, 230)',
            'fontWeight': 'bold'
        },
        sort_action='native',
        page_size=10
    )

    # Full Layout with Bootstrap Grid
    tbl_app = dash.Dash(
        __name__,
        server=server,
        url_base_pathname='/v4/',
        external_stylesheets=[dbc.themes.BOOTSTRAP]
    )

    tbl_app.layout = dbc.Container(
        [
            html.H2("Mayenne Computer Asset Summary", className="mt-4 mb-4"),
            dbc.Row([
                dbc.Col(pie_chart, width=12, lg=6, className="mb-4"),
                dbc.Col([
                    machine_use_dropdown,
                    bar_chart
                ], width=12, lg=6, className="mb-4"),
            ]),
            dbc.Row([
                dbc.Col(column_dropdown, width=12, className="mb-3"),
                dbc.Col(main_table, width=12)
            ])
        ],
        fluid=True,
        className="p-4"
    )

    # Callback for updating bar chart based on machine use selection
    @tbl_app.callback(
        Output('machine-use-bar-chart', 'figure'),
        Input('machine-use-dropdown', 'value')
    )
    def update_bar_chart(selected_uses):
        if not selected_uses:
            return px.bar(title="Please select machine use types")
            
        # Filter data based on selected machine uses
        filtered_df = df[df['u_build_machine_use'].isin(selected_uses)]
        
        # Determine device type (Desktop/Laptop)
        filtered_df['device_type'] = filtered_df['name'].apply(
            lambda x: 'Desktop' if x.startswith(('com8cc', 'terwd', '8cc')) else 'Laptop'
        )
        
        # Extract version (21H, 22H, etc.) - assuming version is in name or another column
        # For this example, we'll assume version is in 'u_build_use' or similar
        filtered_df['version'] = filtered_df['u_build_use'].str.extract(r'(\d{2}H)')  # Adjust regex as needed
        
        # Group by version and device type
        grouped_data = filtered_df.groupby(['version', 'device_type']).size().reset_index(name='count')
        
        # Create bar chart
        fig = px.bar(
            grouped_data,
            x='version',
            y='count',
            color='device_type',
            color_discrete_map={'Desktop': 'red', 'Laptop': 'green'},
            title='Desktop vs Laptop Count by Version',
            barmode='group'
        ).update_layout(
            xaxis_title="Version",
            yaxis_title="Number of Computers",
            margin=dict(t=50, b=50, l=50, r=50),
            height=400
        )
        
        return fig

    # Callback for updating table columns
    @tbl_app.callback(
        Output('main-table', 'columns'),
        Output('main-table', 'data'),
        Input('column-selector', 'value')
    )
    def update_table_columns(selected_columns):
        if not selected_columns:
            return [], []
            
        columns = [{'name': col, 'id': col, 'sortable': True} for col in selected_columns]
        data = df[selected_columns].to_dict('records')
        return columns, data

    return tbl_app