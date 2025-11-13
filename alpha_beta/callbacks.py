from dash import Output, Input, State, ctx
from .stats import se_from_sigma_n, critical_from_alpha, errors_from_c
from .figure import make_figure

def register_callbacks(app):
    @app.callback(
        Output("fig", "figure"),
        Output("stats", "children"),
        Output("alpha_block", "style"),
        Output("c_block", "style"),
        Output("c_slider", "value"),
        Input("mu0", "value"),
        Input("mu1", "value"),
        Input("sigma", "value"),
        Input("n", "value"),
        Input("tail", "value"),
        Input("crit_mode", "value"),
        Input("alpha_slider", "value"),
        Input("c_slider", "value"),
    )
    def update(mu0, mu1, sigma, n, tail, crit_mode, alpha_val, c_val):
        se = se_from_sigma_n(sigma, n)

        if crit_mode == "alpha":
            cL, cR = critical_from_alpha(mu0, se, alpha_val, tail)
        else:
            if tail == "two-sided":
                cR = c_val
                if cR < mu0:
                    cR = mu0 + abs(cR - mu0)
                cL = 2 * mu0 - cR
            elif tail == "right":
                cL, cR = None, c_val
            else:
                cL, cR = c_val, None

        a, b, p, cL_eff, cR_eff = errors_from_c(mu0, mu1, se, cL, cR, tail)

        stats_row = f"α = {a:.4f}    β = {b:.4f}    1−β = {p:.4f}"
        if tail == "two-sided":
            stats_row += f"    (cL = {cL_eff:.3f}, cR = {cR_eff:.3f})"
        stats_row += f"    SE = σ/√n = {se:.4f}"

        fig = make_figure(mu0, mu1, se, tail, cL_eff, cR_eff, a, b, p)

        alpha_style = {"marginTop": "10px"} if crit_mode == "alpha" else {"display": "none"}
        c_style     = {"marginTop": "10px"} if crit_mode == "c"     else {"display": "none"}
        c_out = (cR_eff if tail != "left" else cL_eff) if crit_mode == "alpha" else c_val

        return fig, stats_row, alpha_style, c_style, c_out
