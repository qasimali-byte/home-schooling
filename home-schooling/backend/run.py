"""Module import for running app"""
from api import app

# RUN API
if __name__ == "__main__":
    app.run(debug=True, port=5001)  # add host='----'
