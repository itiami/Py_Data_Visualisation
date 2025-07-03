from flask import Flask


def create_app():
    app = Flask(__name__)

    # Register Flask routes
    from .routes import main
    app.register_blueprint(main)

    # Register Dash apps from app_module
    from app_modules.ci_computer_v1 import init_dataTbl
    init_dataTbl(app)

    from app_modules.ci_computer_v2 import init_dataTbl
    init_dataTbl(app)

    from app_modules.ci_computer_v3 import init_dataTbl
    init_dataTbl(app)

    from app_modules.qr_gen import create_qr_code_app
    create_qr_code_app(app)

    from app_modules.ci_computer_v4 import init_dataTbl
    init_dataTbl(app)


    return app
