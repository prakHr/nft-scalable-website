from dash import Dash, html
import dash
from flask import Flask
from flask_login import LoginManager

from users import User

# --- Flask server ---
server = Flask(__name__)
server.secret_key = "supersecretkey"

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

if __name__ == "__main__":
    app.run_server(debug=True)