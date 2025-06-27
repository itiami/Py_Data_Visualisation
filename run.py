from app_settings import create_app # Import create_app method from app directory..
import os

app_settings = create_app()

if __name__ == "__main__":
    app_settings.run(host='0.0.0.0', port=8051, debug=True)
