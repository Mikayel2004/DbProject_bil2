from main import app, initialize_database

if __name__ == "__main__":
    print("Initializing database...")
    initialize_database()
    print("Starting Flask server...")
    app.run(debug=True)
