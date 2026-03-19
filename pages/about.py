from dash import html
import dash
from flask_login import current_user

dash.register_page(__name__, path="/about")

def layout():
    if not current_user.is_authenticated:
        return html.Div([
            html.H2("Access Denied"),
            html.P("You must log in to view this page."),
            html.A("Go to Login", href="/login")
            
        ])
    return html.Div([
        html.A("Go to Logout", href="/logout"),
        html.H2("About Page"),
        html.P("Secured Login.")
    ])