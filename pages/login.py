# pages/login.py
from dash import html, dcc, Input, Output, State, callback
import dash
from flask_login import login_user, current_user
from users import User
import hashlib
from .cache import hashed_pw_cache

dash.register_page(__name__, path="/login")

layout = html.Div([
    dcc.Store(id="user-password-store"),
    dcc.Input(id="username", type="text", placeholder="Username"),
    dcc.Input(id="password", type="password", placeholder="Password"),
    html.Button("Login", id="login-btn"),
    html.Div(id="login-msg")
])

@callback(
    Output("login-msg", "children"),
    Output("user-password-store", "data"),
    Input("login-btn", "n_clicks"),
    State("username", "value"),
    State("password", "value"),
    prevent_initial_call=True
)
def login_callback(n_clicks, username, password):

    if current_user.is_authenticated:
        return dcc.Location(pathname="/", id="redirect"), None

    if not username or not password:
        return "Please enter both username and password.", None

    hashed_pw = hashlib.sha256(password.encode()).hexdigest()

    # --- User does not exist ---
    if username not in hashed_pw_cache:
        return html.A("User does not exist. Click here to register.", href="/set-password"), None

    # --- Wrong password ---
    if hashed_pw_cache[username] != hashed_pw:
        return "Incorrect password. Please try again.", None

    # --- Success ---
    user = User(username)
    login_user(user)

    return dcc.Location(pathname="/", id="redirect-home"), hashed_pw