# pages/login.py
from dash import html, dcc, Input, Output, State, callback
import dash
from flask_login import login_user, current_user
from users import User

dash.register_page(__name__, path="/login")

layout = html.Div([
    html.H2("Login"),
    dcc.Input(id="username", type="text", placeholder="Username"),
    html.Br(),
    dcc.Input(id="password", type="password", placeholder="Password"),
    html.Br(),
    html.Button("Login", id="login-btn"),
    html.Div(id="login-msg")
])

@callback(
    Output("login-msg", "children"),
    Input("login-btn", "n_clicks"),
    State("username", "value"),
    State("password", "value"),
    prevent_initial_call=True
)
def login_callback(n_clicks, username, password):
    # Already logged in? Redirect to home
    if current_user.is_authenticated:
        return dcc.Location(pathname="/", id="redirect")

    # Check input
    if not username or not password:
        return "Enter both username and password."

   
    # Log in the user
    user = User(username)
    login_user(user)
    return html.A("Go to Home", href="/")  # redirect to home

# --- Callback to clear inputs on page load ---
@callback(
    Output("username", "value"),
    Output("password", "value"),
    Input("login-url", "pathname")  # triggers whenever the login page is loaded
)
def clear_inputs_on_load(pathname):
    return "", ""
