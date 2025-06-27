from flask import Flask


def create_app():
    app = Flask(__name__)

    # Register Flask routes
    from .routes import main
    app.register_blueprint(main)

    # Register Dash apps from app_module
    from app_modules.ci_computer import init_dataTbl
    init_dataTbl(app)

    from app_modules.qr_gen import create_qr_code_app
    create_qr_code_app(app)


    return app
