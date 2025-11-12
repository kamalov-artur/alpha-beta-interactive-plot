import os
import numpy as np
import plotly.graph_objects as go

from dash import Dash, dcc, html, Output, Input, ctx
from scipy.stats import norm 


def errors(mu0, mu1, sigma, c, tail):
    if tail == "right":
        alpha = 1 - norm.cdf(c, loc=mu0, scale=sigma)
        beta  = norm.cdf(c, loc=mu1, scale=sigma)
        power = 1 - beta
        return float(alpha), float(beta), float(power), None, float(c)

    if tail == "left":
        alpha = norm.cdf(c, loc=mu0, scale=sigma)
        beta  = 1 - norm.cdf(c, loc=mu1, scale=sigma)
        power = 1 - beta
        return float(alpha), float(beta), float(power), float(c), None

    cR = float(c)
    cL = float(2*mu0 - cR)
    alpha = (1 - norm.cdf(cR, loc=mu0, scale=sigma)) + norm.cdf(cL, loc=mu0, scale=sigma)
    beta  = norm.cdf(cR, loc=mu1, scale=sigma) - norm.cdf(cL, loc=mu1, scale=sigma)
    power = 1 - beta
    return float(alpha), float(beta), float(power), cL, cR


def make_figure(mu0, mu1, sigma, c, tail):
    xmin = min(mu0, mu1) - 4*sigma
    xmax = max(mu0, mu1) + 4*sigma
    x = np.linspace(xmin, xmax, 1200)

    y0 = norm.pdf(x, loc=mu0, scale=sigma)
    y1 = norm.pdf(x, loc=mu1, scale=sigma)

    alpha, beta, power, cL, cR = errors(mu0, mu1, sigma, c, tail)

    if tail == "right":
        alpha_mask = x >= c
        beta_mask  = x <  c
        power_mask = x >= c
        crits = [c]
    elif tail == "left":
        alpha_mask = x <= c
        beta_mask  = x >  c
        power_mask = x <= c
        crits = [c]
    else:
        alpha_mask = (x <= cL) | (x >= cR)
        beta_mask  = (x >= cL) & (x <= cR)
        power_mask = (x <= cL) | (x >= cR)
        crits = [cL, cR]

    y0_alpha = np.where(alpha_mask, y0, np.nan)
    y1_beta  = np.where(beta_mask,  y1, np.nan)
    y1_power = np.where(power_mask, y1, np.nan)

    fig = go.Figure()

    fig.add_trace(go.Scatter(x=x, y=y0, mode="lines", name="H₀ ~ N(μ₀, σ)", line=dict(width=2)))
    fig.add_trace(go.Scatter(x=x, y=y1, mode="lines", name="H₁ ~ N(μ₁, σ)", line=dict(width=2)))

    fig.add_trace(go.Scatter(
        x=x, y=y1_power, mode="lines", name="Мощность 1−β",
        fill="tozeroy", opacity=0.30,
        line=dict(color="rgba(56,189,248,1)")
    ))

    fig.add_trace(go.Scatter(
        x=x, y=y0_alpha, mode="lines", name="α (Type I)",
        fill="tozeroy", opacity=0.35,
        line=dict(color="rgba(239,68,68,1)")
    ))
    fig.add_trace(go.Scatter(
        x=x, y=y1_beta, mode="lines", name="β (Type II)",
        fill="tozeroy", opacity=0.35,
        line=dict(color="rgba(245,158,11,1)")
    ))

    ymax = max(np.nanmax(y0), np.nanmax(y1))
    for cc in crits:
        fig.add_shape(type="line", x0=cc, x1=cc, y0=0, y1=ymax, line=dict(width=2, dash="dash"))

    subtitle = f"α={alpha:.4f}   β={beta:.4f}   1−β={power:.4f}"
    if tail == "two-sided":
        subtitle += f"   (cL={cL:.3f}, cR={cR:.3f})"

    fig.update_layout(
        title=f"Ошибки I и II рода — {dict(right='правосторонний', left='левосторонний', **{'two-sided':'двусторонний'})[tail]} тест"
              f"<br><sup>{subtitle}</sup>",
        template="plotly_white",
        margin=dict(l=40, r=20, t=60, b=40),
        xaxis_title="значение",
        yaxis_title="плотность",
        legend=dict(orientation="h", y=1.14, x=0),
        height=560,
    )
    return fig


app = Dash(__name__)
app.title = "α–β Explorer (SciPy)"

app.layout = html.Div([
    html.H3("Интерактивный график ошибок I (α), II (β) рода и мощности — SciPy, Dash"),
    html.Div([
        html.Div([
            html.Label("μ₀ (H₀)"),
            dcc.Slider(id="mu0", min=-50, max=50, step=0.1, value=25,
                       tooltip={"placement":"bottom", "always_visible": True}),
            html.Label("μ₁ (H₁)"),
            dcc.Slider(id="mu1", min=-50, max=50, step=0.1, value=30,
                       tooltip={"placement":"bottom", "always_visible": True}),
            html.Label("σ"),
            dcc.Slider(id="sigma", min=0.5, max=20, step=0.1, value=5,
                       tooltip={"placement":"bottom", "always_visible": True}),
        ], style={"flex":"1", "minWidth":"280px", "paddingRight":"12px"}),

        html.Div([
            html.Label("критическое значение c"),
            dcc.Slider(id="c_slider", min=-50, max=50, step=0.1, value=30),
            dcc.Input(
                id="c_input", type="number", step=0.1, value=30,
                debounce=True, style={"width":"140px", "marginTop":"6px"}
            ),
            html.Div([
                dcc.RadioItems(
                    id="tail",
                    options=[
                        {"label":"Правый хвост", "value":"right"},
                        {"label":"Левый хвост",  "value":"left"},
                        {"label":"Двусторонний", "value":"two-sided"},
                    ],
                    value="right", inline=True
                )
            ], style={"marginTop":"10px"}),
            html.Div(id="stats", style={"marginTop":"10px", "fontSize":"16px", "fontFamily":"monospace"}),
        ], style={"flex":"1", "minWidth":"280px"}),
    ], style={"display":"flex", "gap":"14px", "flexWrap":"wrap", "marginBottom":"8px"}),

    dcc.Graph(id="fig", config={"displaylogo": False})
], style={"maxWidth":"1100px", "margin":"18px auto", "padding":"0 16px"})


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

if __name__ == "__main__":
    app.run_server(host="0.0.0.0", port=int(os.environ.get("PORT", 8050)))
