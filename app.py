from dash import Dash, html, dcc, Input, Output
import dash
import dash_bootstrap_components as dbc
from flask import Flask
from flask_login import LoginManager
from users import User
from pages.cache import hashed_pw_cache
import os

server = Flask(__name__)
server.secret_key = os.environ.get("SECRET_KEY", "supersecretkey")

login_manager = LoginManager()
login_manager.init_app(server)
login_manager.login_view = "/login"

@login_manager.user_loader
def load_user(user_id):
    if user_id in hashed_pw_cache:
        return User(user_id)
    return None

THEMES = {
    "Bootstrap": dbc.themes.BOOTSTRAP,
    "Cyborg": dbc.themes.CYBORG,
    "Slate": dbc.themes.SLATE,
    "Lux": dbc.themes.LUX,
    "Minty": dbc.themes.MINTY,
    "Darkly": dbc.themes.DARKLY,
    "Flatly": dbc.themes.FLATLY,
    "Quartz": dbc.themes.QUARTZ,
    "Solar": dbc.themes.SOLAR,
    "Superhero": dbc.themes.SUPERHERO,
}

app = Dash(
    __name__,
    server=server,
    use_pages=True,
    suppress_callback_exceptions=True
)

app.layout = html.Div([

    # ⚡ Dynamic theme loader (NO REFRESH)
    html.Link(
        id="theme-link",
        rel="stylesheet",
        href=dbc.themes.BOOTSTRAP
    ),

    dbc.Container([
        dbc.Row([
            dbc.Col(html.H5("🎨 Picasso theme"), width="auto",style={"margin": "10px","background-color":"yellow","color":"black"}),
            dbc.Col(html.H5("Blockchain Webapp"), width="auto"),
            dbc.Col(html.H5("Its scalable upto millions of images with real-time updates"), width="auto",style={"margin": "10px","background-color":"yellow","color":"black"}),
            dbc.Col(html.H5("No need to use db"), width="auto"),
            dbc.Col(html.H5("With randomization of nft images"), width="auto",style={"margin": "10px","background-color":"yellow","color":"black"}),
            
            
            dbc.Col(
                dcc.Dropdown(
                    id="theme-dropdown",
                    options=[{"label": k, "value": v} for k, v in THEMES.items()],
                    value=dbc.themes.BOOTSTRAP,
                    clearable=False
                ),
                width=3
            )
        ], className="my-2")
    ], fluid=True),

    dash.page_container
])

# ⚡ Instant theme switch
@app.callback(
    Output("theme-link", "href"),
    Input("theme-dropdown", "value")
)
def switch_theme(theme):
    return theme

if __name__ == "__main__":
    app.run(debug=True)
