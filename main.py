
from app_settings import create_app  # Import the factory function

# Initialize the Flask application
app = create_app()

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8051, debug=True)
