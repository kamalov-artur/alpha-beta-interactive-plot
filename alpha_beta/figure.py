import numpy as np
import plotly.graph_objects as go
from scipy.stats import norm
from .stats import errors_from_c

def make_figure(mu0, mu1, se, tail, cL, cR, alpha_val, beta_val, power_val):
    xmin = min(mu0, mu1) - 4 * se
    xmax = max(mu0, mu1) + 4 * se
    x = np.linspace(xmin, xmax, 1200)

    y0 = norm.pdf(x, loc=mu0, scale=se)
    y1 = norm.pdf(x, loc=mu1, scale=se)

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=x,
                             y=y0,
                             mode="lines",
                             name="H₀ ~ N(μ₀, SE)",
                             line=dict(width=2)))
    fig.add_trace(go.Scatter(x=x,
                             y=y1,
                             mode="lines",
                             name="H₁ ~ N(μ₁, SE)",
                             line=dict(width=2)))

    if tail in ("right", "left"):
        c = cR if tail == "right" else cL
        if tail == "right":
            alpha_mask = x >= c; beta_mask  = x <  c; power_mask = x >= c; crits = [c]
        else:
            alpha_mask = x <= c; beta_mask  = x >  c; power_mask = x <= c; crits = [c]

        fig.add_trace(go.Scatter(x=x,
                                 y=np.where(power_mask, y1, np.nan),
                                 mode="lines",
                                 name="Мощность 1−β",
                                 fill="tozeroy",
                                 opacity=0.30,
                                 line=dict(color="rgba(56,189,248,1)"),
                                 customdata=np.full_like(x, power_val),
                                 hovertemplate="x=%{x:.3f}<br>f₁(x)=%{y:.4f}<br>Площадь(1−β)=%{customdata:.4f}<extra></extra>"))
        fig.add_trace(go.Scatter(x=x,
                                 y=np.where(alpha_mask, y0, np.nan),
                                 mode="lines",
                                 name="α (ошибка I рода)",
                                 fill="tozeroy",
                                 opacity=0.35,
                                 line=dict(color="rgba(239,68,68,1)"),
                                 customdata=np.full_like(x, alpha_val),
                                 hovertemplate="x=%{x:.3f}<br>f₀(x)=%{y:.4f}<br>Площадь(α)=%{customdata:.4f}<extra></extra>"))
        fig.add_trace(go.Scatter(x=x,
                                 y=np.where(beta_mask, y1, np.nan),
                                 mode="lines",
                                 name="β (ошибка II рода)",
                                 fill="tozeroy",
                                 opacity=0.35,
                                 line=dict(color="rgba(245,158,11,1)"),
                                 customdata=np.full_like(x, beta_val),
                                 hovertemplate="x=%{x:.3f}<br>f₁(x)=%{y:.4f}<br>Площадь(β)=%{customdata:.4f}<extra></extra>"))
    else:
        left  = x <= cL; mid = (x >= cL) & (x <= cR); right = x >= cR; crits = [cL, cR]

        alpha_left  = norm.cdf(cL, loc=mu0, scale=se)
        alpha_right = 1 - norm.cdf(cR, loc=mu0, scale=se)
        power_left  = norm.cdf(cL, loc=mu1, scale=se)
        power_right = 1 - norm.cdf(cR, loc=mu1, scale=se)

        fig.add_trace(go.Scatter(x=x,
                                 y=np.where(left,  y1, np.nan),
                                 mode="lines",
                                 name="Мощность 1−β (лев.)",
                                 fill="tozeroy",
                                 opacity=0.30,
                                 line=dict(color="rgba(56,189,248,1)"),
                                 customdata=np.full_like(x, power_left),
                                 hovertemplate="x=%{x:.3f}<br>f₁(x)=%{y:.4f}<br>Площадь(1−β, лев.)=%{customdata:.4f}<extra></extra>"))
        fig.add_trace(go.Scatter(x=x,
                                 y=np.where(right, y1, np.nan),
                                 mode="lines",
                                 name="Мощность 1−β (прав.)",
                                 fill="tozeroy",
                                 opacity=0.30,
                                 line=dict(color="rgba(56,189,248,1)"),
                                 customdata=np.full_like(x, power_right),
                                 hovertemplate="x=%{x:.3f}<br>f₁(x)=%{y:.4f}<br>Площадь(1−β, прав.)=%{customdata:.4f}<extra></extra>"))
        fig.add_trace(go.Scatter(x=x,
                                 y=np.where(left,  y0, np.nan),
                                 mode="lines",
                                 name="α (лев.)",
                                 fill="tozeroy",
                                 opacity=0.35,
                                 line=dict(color="rgba(239,68,68,1)"),
                                 customdata=np.full_like(x, alpha_left),
                                 hovertemplate="x=%{x:.3f}<br>f₀(x)=%{y:.4f}<br>Площадь(α, лев.)=%{customdata:.4f}<extra></extra>"))
        fig.add_trace(go.Scatter(x=x,
                                 y=np.where(right, y0, np.nan),
                                 mode="lines",
                                 name="α (прав.)",
                                 fill="tozeroy",
                                 opacity=0.35,
                                 line=dict(color="rgba(239,68,68,1)"),
                                 customdata=np.full_like(x, alpha_right),
                                 hovertemplate="x=%{x:.3f}<br>f₀(x)=%{y:.4f}<br>Площадь(α, прав.)=%{customdata:.4f}<extra></extra>"))
        fig.add_trace(go.Scatter(x=x,
                                 y=np.where(mid, y1, np.nan),
                                 mode="lines",
                                 name="β (ошибка II рода)",
                                 fill="tozeroy",
                                 opacity=0.35,
                                 line=dict(color="rgba(245,158,11,1)"),
                                 customdata=np.full_like(x, beta_val),
                                 hovertemplate="x=%{x:.3f}<br>f₁(x)=%{y:.4f}<br>Площадь(β)=%{customdata:.4f}<extra></extra>"))

    ymax = max(np.nanmax(y0), np.nanmax(y1))
    for cc in crits:
        fig.add_shape(
            type="line",
            x0=cc,
            x1=cc,
            y0=0,
            y1=ymax,
            line=dict(width=2, dash="dash")
        )
    
    fig.update_layout(
        template="plotly_white",
        margin=dict(l=40, r=20, t=60, b=40),
        xaxis_title="Значение статистики",
        yaxis_title="Вероятность",
        legend=dict(orientation="h", y=1.14, x=0),
        height=560)
    return fig