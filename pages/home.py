# pages/home.py
from dash import html, dash_table, dcc, Input, Output, State, callback
import dash
from flask_login import current_user
from io import BytesIO
import base64
import random, colorsys, hashlib
from PIL import Image, ImageDraw, ImageChops
from .cache import hashed_pw_cache  
dash.register_page(__name__, path="/")  # Home page

# ---------------- Image Generation ----------------
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

# ---------------- In-memory cache ----------------
PAGE_SIZE = 10
cache = {}  # {(username, hashed_pw, page): [images]}

def get_page_images(username, hashed_pw, page):
    key = (username, hashed_pw, page)
    if key in cache:
        return cache[key]

    # --- Seed random with username + hashed password + page for reproducible per-user NFTs ---
    seed = int(hashlib.sha256(f"{username}-{hashed_pw}-{page}".encode()).hexdigest(), 16) % (2**32)
    random.seed(seed)

    images = [generate_art() for _ in range(PAGE_SIZE)]
    cache[key] = images
    return images

# ---------------- Layout ----------------
def layout():
    if not current_user.is_authenticated:
        return html.Div([
            html.A("Go to Login", href="/login")
        ])

    table = dash_table.DataTable(
        id="datatable-pagination",
        columns=[{"name": "ID", "id": "id"}],
        page_current=0,
        page_size=PAGE_SIZE,
        page_action="custom",
    )

    # Hidden store to receive password hash from login
    password_store = dcc.Store(id="user-password-store")

    nft_container = html.Div(
        id="nft-container",
        style={"display": "flex", "flexWrap": "wrap", "marginTop": "20px"},
    )

    return html.Div([
        html.A("Go to About", href="/about"),
        html.A("Logout", href="/logout", style={"marginLeft": "20px"}),
        html.H2(f"Welcome {current_user.get_id()}!"),
        html.P("This is your unique NFT gallery."),
        password_store,
        table,
        nft_container
    ])

# ---------------- Callbacks ----------------
@callback(
    Output("datatable-pagination", "data"),
    Output("nft-container", "children"),
    Input("datatable-pagination", "page_current"),
    Input("datatable-pagination", "page_size"),
    State("user-password-store", "data")
)
def update(page_current, page_size, hashed_pw):
    # if not current_user.is_authenticated:
    #     return [], [html.Div("Access Denied. Please login again.")]

    # Check authentication and verify hashed password against cache
    username = current_user.get_id()
    hashed_pw_from_store = hashed_pw_cache.get(username)
    if not username or hashed_pw_cache.get(username) != hashed_pw_from_store:
        return [], [html.Div("Access Denied. Please login again.")]
    username = current_user.get_id()
    images = get_page_images(username, hashed_pw_from_store, page_current)

    children = [
        html.Div([
            html.P(f"ID: {page_current * page_size + i + 1}"),
            html.Img(
                src=f"data:image/webp;base64,{img}",
                style={"width": "128px", "border": "1px solid blue", "margin": "5px"},
            )
        ]) for i, img in enumerate(images)
    ]

    data = [{"id": page_current * page_size + i + 1} for i in range(len(images))]
    return data, children