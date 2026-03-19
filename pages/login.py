# pages/login.py
from dash import html, dcc, Input, Output, State, callback
import dash
from flask_login import login_user, current_user
from users import User
import hashlib
from .cache import hashed_pw_cache  # global cache for username -> hashed_pw

dash.register_page(__name__, path="/login")

layout = html.Div([
    dcc.Store(id="user-password-store"),  # hidden store for NFT seeding
    dcc.Input(id="username", type="text", placeholder="Username"),
    dcc.Input(id="password", type="password", placeholder="Password"),
    html.Button("Login", id="login-btn"),
    html.Div(id="login-msg")
])

@callback(
    Output("login-msg", "children"),
    Output("user-password-store", "data"),  # store hashed password for NFTs
    Input("login-btn", "n_clicks"),
    State("username", "value"),
    State("password", "value"),
    prevent_initial_call=True
)
def login_callback(n_clicks, username, password):
    # Already logged in? Redirect to home
    if current_user.is_authenticated:
        return dcc.Location(pathname="/", id="redirect"), None

    # Check input

    if not username or not password:
        return "Please enter both username and password.", None

    if not username:
        return "Username can not be empty.", None

    hashed_pw = hashlib.sha256(password.encode()).hexdigest()

    # --- User exists, check password ---
    try:
        if hashed_pw_cache[username] != hashed_pw:
            return "Incorrect password. Please try again.", None
    except KeyError:
        # --- User does not exist, redirect to set-password page ---
        return html.A("User does not exist. Click here to register.", href="/set-password"), None
    # --- User not registered → redirect to set-password page ---
    if username not in hashed_pw_cache:
        return dcc.Location(pathname="/setpassword", id="redirect-setpw"), None

    
    # --- Successful login ---
    user = User(username)
    login_user(user)

    # Pass hashed_pw to NFT logic
    return dcc.Location(pathname="/", id="redirect-home"), hashed_pw