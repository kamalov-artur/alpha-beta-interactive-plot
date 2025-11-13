from dash import Dash
from .layout import build_layout
from .callbacks import register_callbacks

def create_app():
    app = Dash(__name__)
    app.title = "alpha-beta explorer"
    app.layout = build_layout()
    register_callbacks(app)
    server = app.server
    return app, server
