# pages/set_password.py
from dash import html, dcc, Input, Output, State, callback
import dash
import hashlib
from .cache import hashed_pw_cache, save_cache  # ✅ import save

dash.register_page(__name__, path="/set-password")

layout = html.Div([
    html.H2("Set Password / Register"),
    dcc.Input(id="username", type="text", placeholder="Username"),
    dcc.Input(id="password", type="password", placeholder="Password"),
    html.Button("Submit", id="setpw-btn"),
    html.Div(id="setpw-msg")
])

@callback(
    Output("setpw-msg", "children"),
    Input("setpw-btn", "n_clicks"),
    State("username", "value"),
    State("password", "value"),
    prevent_initial_call=True
)
def set_password(n_clicks, username, password):

    if not username or not password:
        return "Enter both username and password."

    hashed_pw = hashlib.sha256(password.encode()).hexdigest()

    # --- Username already exists ---
    if username in hashed_pw_cache:
        if hashed_pw_cache[username] == hashed_pw:
            return "User already exists. Please login."
        else:
            return "Username already exists. Choose a different password."

    # --- Store new user ---
    hashed_pw_cache[username] = hashed_pw
    save_cache(hashed_pw_cache)  # ✅ persist to file

    # --- Redirect to login ---
    return dcc.Location(pathname="/login", id="redirect")