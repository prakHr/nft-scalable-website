# app.py
from dash import Dash, html
import dash
from flask import Flask
from flask_login import LoginManager
from users import User
from pages.cache import hashed_pw_cache  # global cache

# --- Flask server ---
server = Flask(__name__)
import os
server.secret_key = os.environ.get("SECRET_KEY", "supersecretkey")  # use env variable in production

# --- Flask-Login setup ---
login_manager = LoginManager()
login_manager.init_app(server)
login_manager.login_view = "/login"

# Load user by username
@login_manager.user_loader
def load_user(user_id):
    # Return a User object only if username exists in cache
    if user_id in hashed_pw_cache:
        return User(user_id)
    return None

# --- Dash app ---
app = Dash(__name__, server=server, use_pages=True, suppress_callback_exceptions=True)
app.title = "NFT Gallery"

# Layout just serves page container; individual pages handle login/password logic
app.layout = html.Div([
    dash.page_container
])

if __name__ == "__main__":
    # Use debug=True only in development
    app.run(debug=True)