from dash import html, dcc
import dash
from flask_login import logout_user
from flask import redirect
from flask_login import current_user

dash.register_page(__name__, path="/logout")

# Layout: immediately redirect after logging out
layout = html.Div([
    html.H2("Logging out..."),
    dcc.Location(pathname="/login", id="redirect")  # redirect to login
])

# Use a server-side callback to log out immediately
@dash.callback(
    dash.Output("redirect", "pathname"),
    dash.Input("redirect", "id"),  # Dummy input to trigger callback
    
)
def do_logout(_):
    logout_user()  # This is Flask-Login's logout
    return "/login"