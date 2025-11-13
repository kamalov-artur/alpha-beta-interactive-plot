import numpy as np
import plotly.graph_objects as go
from scipy.stats import norm
from .stats import errors

def make_figure(mu0, mu1, sigma, c, tail):
    xmin = min(mu0, mu1) - 4*sigma
    xmax = max(mu0, mu1) + 4*sigma
    x = np.linspace(xmin, xmax, 1200)

    y0 = norm.pdf(x, loc=mu0, scale=sigma)
    y1 = norm.pdf(x, loc=mu1, scale=sigma)

    alpha, beta, power, cL, cR = errors(mu0, mu1, sigma, c, tail)

    fig = go.Figure()
    # кривые
    fig.add_trace(go.Scatter(x=x, y=y0, mode="lines", name="H₀ ~ N(μ₀, σ)", line=dict(width=2)))
    fig.add_trace(go.Scatter(x=x, y=y1, mode="lines", name="H₁ ~ N(μ₁, σ)", line=dict(width=2)))

    if tail in ("right", "left"):
        if tail == "right":
            alpha_mask = x >= c; beta_mask = x < c; power_mask = x >= c; crits = [c]
        else:
            alpha_mask = x <= c; beta_mask = x > c; power_mask = x <= c; crits = [c]

        fig.add_trace(go.Scatter(x=x, y=np.where(power_mask, y1, np.nan),
                                 mode="lines", name="Мощность 1−β",
                                 fill="tozeroy", opacity=0.30,
                                 line=dict(color="rgba(56,189,248,1)")))
        fig.add_trace(go.Scatter(x=x, y=np.where(alpha_mask, y0, np.nan),
                                 mode="lines", name="α (Type I)",
                                 fill="tozeroy", opacity=0.35,
                                 line=dict(color="rgba(239,68,68,1)")))
        fig.add_trace(go.Scatter(x=x, y=np.where(beta_mask, y1, np.nan),
                                 mode="lines", name="β (Type II)",
                                 fill="tozeroy", opacity=0.35,
                                 line=dict(color="rgba(245,158,11,1)")))
    else:
        left  = x <= cL
        mid   = (x >= cL) & (x <= cR)
        right = x >= cR
        crits = [cL, cR]

        # мощность 1−β (два хвоста под H1)
        fig.add_trace(go.Scatter(x=x, y=np.where(left,  y1, np.nan),
                                 mode="lines", name="Мощность 1−β",
                                 fill="tozeroy", opacity=0.30,
                                 line=dict(color="rgba(56,189,248,1)")))
        fig.add_trace(go.Scatter(x=x, y=np.where(right, y1, np.nan),
                                 mode="lines", name="Мощность 1−β",
                                 fill="tozeroy", opacity=0.30,
                                 line=dict(color="rgba(56,189,248,1)"),
                                 showlegend=False))

        # α под H0 (левый и правый хвост)
        fig.add_trace(go.Scatter(x=x, y=np.where(left, y0, np.nan),
                                 mode="lines", name="α (Type I)",
                                 fill="tozeroy", opacity=0.35,
                                 line=dict(color="rgba(239,68,68,1)")))
        fig.add_trace(go.Scatter(x=x, y=np.where(right, y0, np.nan),
                                 mode="lines", name="α (Type I)",
                                 fill="tozeroy", opacity=0.35,
                                 line=dict(color="rgba(239,68,68,1)"),
                                 showlegend=False))

        # β под H1 — середина
        fig.add_trace(go.Scatter(x=x, y=np.where(mid, y1, np.nan),
                                 mode="lines", name="β (Type II)",
                                 fill="tozeroy", opacity=0.35,
                                 line=dict(color="rgba(245,158,11,1)")))

    # критические вертикали
    ymax = max(np.nanmax(y0), np.nanmax(y1))
    for cc in crits:
        fig.add_shape(type="line", x0=cc, x1=cc, y0=0, y1=ymax, line=dict(width=2, dash="dash"))

    subtitle = f"α={alpha:.4f}   β={beta:.4f}   1−β={power:.4f}"
    if tail == "two-sided":
        subtitle += f"   (cL={cL:.3f}, cR={cR:.3f})"

    fig.update_layout(
        title=f"Ошибки I и II рода — "
              f"{dict(right='правосторонний', left='левосторонний', **{'two-sided':'двусторонний'})[tail]} тест"
              f"<br><sup>{subtitle}</sup>",
        template="plotly_white",
        margin=dict(l=40, r=20, t=60, b=40),
        xaxis_title="значение",
        yaxis_title="плотность",
        legend=dict(orientation="h", y=1.14, x=0),
        height=560,
    )
    return fig
