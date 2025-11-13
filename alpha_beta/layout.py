from dash import dcc, html


def build_layout():
    return html.Div([
        html.H3("Интерактивный график ошибок I (α), II (β) рода и мощности"),
        html.Div([
            html.Div([
                html.Label("μ₀ (H₀)"),
                dcc.Slider(id="mu0", min=0, max=15, step=None, value=5, marks=None,
                           tooltip={"placement": "bottom", "always_visible": True}),
                html.Label("μ₁ (H₁)"),
                dcc.Slider(id="mu1", min=0, max=15, step=None, value=7, marks=None,
                           tooltip={"placement": "bottom", "always_visible": True}),
                html.Label("σ (стандартное отклонение)"),
                dcc.Slider(id="sigma", min=1, max=15, step=None, value=5, marks=None,
                           tooltip={"placement": "bottom", "always_visible": True}),
                html.Label("n (размер выборки)"),
                dcc.Slider(id="n", min=2, max=1000, step=1, value=30, marks=None,
                           tooltip={"placement": "bottom", "always_visible": True}),
            ], style={"flex": "1", "minWidth": "320px", "paddingRight": "12px"}),

            html.Div([
                html.Label("Как задаём критическую область:"),
                dcc.RadioItems(
                    id="crit_mode",
                    options=[
                        {"label": "через уровень значимости α", "value": "alpha"},
                        {"label": "через критическое значение С", "value": "c"},
                    ],
                    value="alpha", inline=False
                ),

                html.Div([
                    html.Label("α (уровень значимости)"),
                    dcc.Slider(
                        id="alpha_slider", min=0.001, max=0.1, step=None, value=0.05, marks=None,
                        tooltip={"placement": "bottom",
                                 "always_visible": True},
                    ),
                ], id="alpha_block", style={"marginTop": "10px"}),

                html.Div([
                    html.Label("критическое значение С"),
                    dcc.Slider(
                        id="c_slider", min=0, max=15, step=None, value=30, marks=None,
                        tooltip={"placement": "bottom",
                                 "always_visible": True},
                    ),
                ], id="c_block", style={"marginTop": "10px", "display": "none"}),

                html.Div([
                    html.Label("Альтернатива, заложенная в H₁:"),
                    dcc.RadioItems(
                        id="tail",
                        options=[
                            {"label": "Правосторонняя", "value": "right"},
                            {"label": "Левосторонняя", "value": "left"},
                            {"label": "Двусторонняя",
                                "value": "two-sided"},
                        ],
                        value="right", inline=True
                    )
                ], style={"marginTop": "12px"}),

                html.Div(
                    id="stats",
                    style={"marginTop": "12px", "fontWeight": "700",
                           "fontFamily": "ui-monospace, SFMono-Regular, Menlo, Consolas, 'Liberation Mono', monospace"}
                ),
            ], style={"flex": "1", "minWidth": "320px"}),
        ], style={"display": "flex", "gap": "14px", "flexWrap": "wrap", "marginBottom": "8px"}),

        dcc.Graph(id="fig", config={"displaylogo": False}),
        html.Hr(),
        html.Footer([
            "tg автора: ",
            html.A("@ArturKamalov", href="https://t.me/ArturKamalov",
                   target="_blank", rel="noopener noreferrer")
        ], style={"textAlign": "center", "margin": "10px 0 30px", "color": "#555"})
    ], style={"maxWidth": "1100px", "margin": "18px auto", "padding": "0 16px"})
