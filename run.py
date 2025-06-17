# here in run.py to run the Flask application.

from app import create_app
from app.models import create_tables

app = create_app()

if __name__ == '__main__':
    # Create tables if they do not exist
    # usind try-except to handle any potential errors
    try:
        create_tables()
        print("Tables created successfully.")
    except Exception as e:
        print(f"Error creating tables: {e}")
    app.run(debug=True)