from dash import Output, Input, ctx
from .figure import make_figure
from .stats import errors

def register_callbacks(app):
    @app.callback(
        Output("fig", "figure"),
        Output("stats", "children"),
        Output("c_slider", "value"),
        Input("mu0", "value"),
        Input("mu1", "value"),
        Input("sigma", "value"),
        Input("c_slider", "value"),
        Input("tail", "value"),
    )
    def update(mu0, mu1, sigma, c_slider, tail):
        # TODO 
        c = c_slider

        if tail == "two-sided" and c < mu0:
            c = mu0 + abs(c - mu0)

        fig = make_figure(mu0, mu1, sigma, c, tail)
        a, b, p, cL, cR = errors(mu0, mu1, sigma, c, tail)

        txt = f"α = {a:.4f}   β = {b:.4f}   1−β = {p:.4f}"
        if tail == "two-sided":
            txt += f"   (cL = {cL:.3f}, cR = {cR:.3f})"

        return fig, txt, c
