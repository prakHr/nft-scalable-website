# app.py
from dash import Dash, html
import dash
from flask import Flask
from flask_login import LoginManager

from users import User

# --- Flask server ---
server = Flask(__name__)
# It's better to use environment variable for security
import os
server.secret_key = os.environ.get("SECRET_KEY", "supersecretkey")

login_manager = LoginManager()
login_manager.init_app(server)
login_manager.login_view = "/login"

@login_manager.user_loader
def load_user(user_id):
    return User(user_id)

# --- Dash app ---
app = Dash(__name__, server=server, use_pages=True)

# Layout is just page container
# Individual pages handle login checks
app.layout = html.Div([
    dash.page_container
])
app.title = "NFT Gallery"

if __name__ == "__main__":
    app.run(debug=True)


