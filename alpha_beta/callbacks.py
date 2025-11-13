import os
from dash import Output, Input, ctx
from .figure import make_figure
from .stats import errors

def register_callbacks(app):
    @app.callback(
        Output("fig", "figure"),
        Output("stats", "children"),
        Output("c_slider", "value"),
        Output("c_input", "value"),
        Input("mu0", "value"),
        Input("mu1", "value"),
        Input("sigma", "value"),
        Input("c_slider", "value"),
        Input("c_input", "value"),
        Input("tail", "value"),
    )
    def update(mu0, mu1, sigma, c_slider, c_input, tail):
        trig = ctx.triggered_id
        if trig == "c_slider":
            c = c_slider
        elif trig == "c_input":
            c = c_input if c_input is not None else c_slider
        else:
            c = c_input if c_input is not None else c_slider

        if tail == "two-sided" and c < mu0:
            c = mu0 + abs(c - mu0)

        fig = make_figure(mu0, mu1, sigma, c, tail)
        a, b, p, cL, cR = errors(mu0, mu1, sigma, c, tail)
        txt = f"α = {a:.4f}   β = {b:.4f}   1−β = {p:.4f}"
        if tail == "two-sided":
            txt += f"   (cL = {cL:.3f}, cR = {cR:.3f})"
        return fig, txt, c, c
