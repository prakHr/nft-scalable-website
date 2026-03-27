from dash import html, dash_table, dcc, Input, Output, State, callback
import dash
import dash_bootstrap_components as dbc
from flask_login import current_user
from io import BytesIO
import base64
import random, colorsys, hashlib
from PIL import Image, ImageDraw, ImageChops
from .cache import hashed_pw_cache  

dash.register_page(__name__, path="/")

PAGE_SIZE = 10
cache = {}

def random_point(size, padding=5):
    return random.randint(padding, size - padding)

def random_color():
    h = random.random()
    r, g, b = colorsys.hsv_to_rgb(h, 1, 1)
    return int(r * 255), int(g * 255), int(b * 255)

def interpolate(c1, c2, f):
    return tuple(int((1 - f) * a + f * b) for a, b in zip(c1, c2))

def generate_art(size=128):
    points = [(random_point(size), random_point(size)) for _ in range(5)]
    start_color, end_color = random_color(), random_color()
    image = Image.new("RGB", (size, size), (0, 0, 0))
    for i, p in enumerate(points):
        overlay = Image.new("RGB", (size, size), (0, 0, 0))
        draw = ImageDraw.Draw(overlay)
        next_p = points[0] if i == len(points) - 1 else points[i + 1]
        draw.line([p, next_p], fill=interpolate(start_color, end_color, i / 4), width=2)
        image = ImageChops.add(image, overlay)
    buff = BytesIO()
    image.save(buff, format="WEBP", quality=70)
    return base64.b64encode(buff.getvalue()).decode()

def get_page_images(username, hashed_pw, page):
    key = (username, hashed_pw, page)
    if key in cache:
        return cache[key]

    seed = int(hashlib.sha256(f"{username}-{hashed_pw}-{page}".encode()).hexdigest(), 16) % (2**32)
    random.seed(seed)

    images = [generate_art() for _ in range(PAGE_SIZE)]
    cache[key] = images
    return images

def layout():
    if not current_user.is_authenticated:
        return dbc.Container([
            dbc.Button("User seen once successfully!, Please use secure login", href="/login", color="primary")
        ])

    table = dash_table.DataTable(
        id="datatable-pagination",
       
        columns=[{"name": "ID", "id": "id"}],
        page_current=0,
        page_size=PAGE_SIZE,
        page_action="custom",

        style_table={
            "overflowX": "auto",
            "border": "1px solid var(--bs-border-color)",
        },

        style_header={
            "backgroundColor": "var(--bs-tertiary-bg)",
            "color": "var(--bs-body-color)",
        },

        style_cell={
            "backgroundColor": "var(--bs-body-bg)",
            "color": "var(--bs-body-color)",
            "border": "1px solid var(--bs-border-color)",
        },
    )

    return dbc.Container([

        dbc.Row([
            dbc.Col(html.A("About", href="/about", className="btn btn-secondary"), width="auto"),
            dbc.Col(html.A("Logout", href="/login", className="btn btn-danger ms-2"), width="auto"),
        ], className="mb-3"),

        html.H2(f"Welcome {current_user.get_id()}"),
        html.P("Your NFT gallery"),

        dcc.Store(id="user-password-store"),
        table,
        html.Div(id="nft-container", className="d-flex flex-wrap mt-4")

    ], fluid=True)

@callback(
    Output("datatable-pagination", "data"),
    Output("nft-container", "children"),
    Input("datatable-pagination", "page_current"),
    Input("datatable-pagination", "page_size"),
    Input("theme-dropdown", "value"),  # 👈 live update trigger
    State("user-password-store", "data")
)
def update(page_current, page_size, theme, hashed_pw):

    username = current_user.get_id()
    hashed_pw_from_store = hashed_pw_cache.get(username)

    if not username or hashed_pw_cache.get(username) != hashed_pw_from_store:
        return [], [dbc.Alert("Access Denied", color="danger")]

    images = get_page_images(username, hashed_pw_from_store, page_current)

    cards = [
        dbc.Card(
            dbc.CardBody([
                html.P(f"ID: {i+1}"),
                html.Img(src=f"data:image/webp;base64,{img}", className="img-fluid")
            ]),
            className="m-2",
            style={"width": "250px"}
        )
        for i, img in enumerate(images)
    ]

    data = [{"id": i+1} for i in range(len(images))]
    return data, cards
