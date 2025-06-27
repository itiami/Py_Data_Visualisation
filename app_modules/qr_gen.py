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

    app.layout = html.Div(children=html.Div(
        [
        html.H1('QR Code Generator'),
        dcc.Input(id='input-text', type='text', placeholder='Enter text', style={'width': '50%'}),
        html.Button('Generate QR Code', id='generate-btn', n_clicks=0),
        html.Br(),
        html.Div(id='qr-output')
    ]
    ), className='qrCode')

    @app.callback(
        Output('qr-output', 'children'),
        Input('generate-btn', 'n_clicks'),
        State('input-text', 'value')
    )
    def update_qr_code(n_clicks, text):
        if n_clicks > 0 and text:
            # Generate QR code image
            qr = qrcode.QRCode(box_size=10, border=4)
            qr.add_data(text)
            qr.make(fit=True)
            img = qr.make_image(fill_color='black', back_color='white')

            # Save to buffer
            buf = io.BytesIO()
            img.save(buf, format='PNG')
            buf.seek(0)
            img_base64 = base64.b64encode(buf.read()).decode('ascii')

            return html.Img(src=f'data:image/png;base64,{img_base64}')

        return ''

    return app
