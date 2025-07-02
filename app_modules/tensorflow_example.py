import pandas as pd
import plotly.express as px
import os
import dash
from dash import Dash, html, dcc, dash_table, Input, Output
import dash_bootstrap_components as dbc
import tensorflow as tf
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder, StandardScaler
import numpy as np

def tflow(server):
    BASE_DIR = os.path.dirname(os.path.dirname(__file__))
    csv_path = os.path.join(BASE_DIR, 'app_modules', 'assets', 'data', 'cmdb_ci_computer.csv')

    df = pd.read_csv(csv_path, encoding='latin1')

    # Preprocess data: select columns and encode categorical variables
    data = df[['location', 'u_build_machine_use', 'install_status']].dropna()

    le_location = LabelEncoder()
    le_use = LabelEncoder()
    le_status = LabelEncoder()

    data['location'] = le_location.fit_transform(data['location'])
    data['u_build_machine_use'] = le_use.fit_transform(data['u_build_machine_use'])
    data['install_status'] = le_status.fit_transform(data['install_status'])

    X = data[['location', 'u_build_machine_use']].values
    y = data['install_status'].values

    scaler = StandardScaler()
    X = scaler.fit_transform(X)

    # Split data
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Define simple TensorFlow model
    model = tf.keras.Sequential([
        tf.keras.layers.Input(shape=(X.shape[1],)),
        tf.keras.layers.Dense(16, activation='relu'),
        tf.keras.layers.Dense(8, activation='relu'),
        tf.keras.layers.Dense(len(np.unique(y)), activation='softmax')
    ])

    model.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])

    # Train model
    history = model.fit(X_train, y_train, epochs=20, validation_data=(X_test, y_test), verbose=0)

    # Prepare Dash app
    tbl_app = dash.Dash(
        __name__,
        server=server,
        url_base_pathname='/tensorflow/',
        external_stylesheets=[dbc.themes.BOOTSTRAP]
    )

    # Plot training history
    fig = px.line({
        'epoch': list(range(1, len(history.history['loss']) + 1)),
        'loss': history.history['loss'],
        'val_loss': history.history['val_loss']
    }, x='epoch', y=['loss', 'val_loss'], title='Model Training Loss')

    tbl_app.layout = dbc.Container([
        html.H2("TensorFlow Model with CMDB Data"),
        html.Hr(),
        dcc.Graph(figure=fig),
        html.Br(),
        dash_table.DataTable(data=df.head(10).to_dict('records'), page_size=5, style_table={'overflowX': 'auto'})
    ])

    return tbl_app
