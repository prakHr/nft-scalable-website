# pages/login.py
from dash import html, dcc, Input, Output, State, callback
import dash
from flask_login import login_user, current_user
from users import User
import hashlib
from .cache import hashed_pw_cache 

dash.register_page(__name__, path="/login")

# pages/login.py
from dash import html, dcc

layout = html.Div([
    dcc.Store(id="user-password-store"),  # hidden store for NFT seeding
    dcc.Input(id="username", type="text", placeholder="Username"),
    dcc.Input(id="password", type="password", placeholder="Password"),
    html.Button("Login", id="login-btn"),
    html.Div(id="login-msg")
])
# layout = html.Div([
#     html.H2("Login"),
#     dcc.Input(id="username", type="text", placeholder="Username"),
#     html.Br(),
#     dcc.Input(id="password", type="password", placeholder="Password"),
#     html.Br(),
#     html.Button("Login", id="login-btn"),
#     html.Div(id="login-msg")
# ])

@callback(
    Output("login-msg", "children"),
    Output("user-password-store", "data"),  # store hashed password
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
        return "Enter both username and password.", None
    hashed_pw = hashlib.sha256(password.encode()).hexdigest()
    if username in hashed_pw_cache and hashed_pw_cache[username] == hashed_pw:
        return "User already logged in with this password.", hashed_pw


   
    # Log in the user
    user = User(username)
    login_user(user)
    # Store hashed password in global cache
    hashed_pw_cache[username] = hashed_pw
    return html.A("Go to Home", href="/"), hashed_pw  # redirect to home

