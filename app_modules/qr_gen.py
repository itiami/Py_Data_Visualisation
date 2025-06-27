import io
import base64
import qrcode
import dash
from dash import html, dcc, Input, Output, State
from flask import Blueprint

# Blueprint for the QR code app
qr_code_bp = Blueprint('qr_code_bp', __name__)

# Dash app factory
def create_qr_code_app(server):
    app = dash.Dash(__name__, server=server, url_base_pathname='/qrGen/')   

    app.layout = html.Div(children=[
        html.H1('QR Code Generator'),

        html.Div([
            html.H2('Single Line QR Generator'),
            html.Div([
                dcc.Input(id='input-single-line', type='text', placeholder='Enter text', className='inputCls'),
                html.Button('Generate QR Code', id='generate-btn-single', n_clicks=0),
                html.Br(),
                html.Div(id='qr-output-single')
            ],style={'display': 'flex', 'flex-direction':'column'})
        ], style={'margin-bottom': '50px'}),

        html.Div([
            html.H2('Multi Line QR Generator'),
            html.Div([
                dcc.Textarea(id='input-multi-line', placeholder='Enter text', className='textareaCls'),
                html.Button('Generate QR Code', id='generate-btn-multi', n_clicks=0, style={'margin': '5px'}),
                html.Br(),
                html.Div(id='qr-output-multi')
            ],style={'display': 'flex', 'flex-direction':'column'})
        ])
    ],className='qrCode')

    # Callback for single-line QR generation
    @app.callback(
        Output('qr-output-single', 'children'),
        Input('generate-btn-single', 'n_clicks'),
        State('input-single-line', 'value')
    )
    def generate_single_line_qr(n_clicks, text):
        if n_clicks > 0 and text:
            img_src = generate_qr_image_base64(text)
            return html.Img(src=img_src)
        return ''

    # Callback for multi-line QR generation
    @app.callback(
        Output('qr-output-multi', 'children'),
        Input('generate-btn-multi', 'n_clicks'),
        State('input-multi-line', 'value')
    )
    def generate_multi_line_qr(n_clicks, text):
        if n_clicks > 0 and text:
            img_src = generate_qr_image_base64(text)
            return html.Img(src=img_src)
        return ''

    # Helper function to generate base64 QR code image
    def generate_qr_image_base64(text):
        qr = qrcode.QRCode(box_size=10, border=4)
        qr.add_data(text)
        qr.make(fit=True)
        img = qr.make_image(fill_color='black', back_color='white')

        buf = io.BytesIO()
        img.save(buf, format='PNG')
        buf.seek(0)
        img_base64 = base64.b64encode(buf.read()).decode('ascii')
        return f'data:image/png;base64,{img_base64}'

    return app
