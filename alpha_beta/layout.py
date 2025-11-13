from dash import dcc, html

def build_layout():
    return html.Div([
        html.H3("Интерактивный график ошибок I (α), II (β) рода и мощности"),
        html.Div([
            html.Div([
                html.Label("μ₀ (H₀)"),
                dcc.Slider(
                    id="mu0", min=-50, max=50,
                    step=None,              # непрерывный
                    value=25,
                    marks=None,             # убираем серые метки
                    tooltip={"placement": "bottom", "always_visible": True},
                ),
                html.Label("μ₁ (H₁)"),
                dcc.Slider(
                    id="mu1", min=-50, max=50,
                    step=None,
                    value=30,
                    marks=None,
                    tooltip={"placement": "bottom", "always_visible": True},
                ),
                html.Label("σ"),
                dcc.Slider(
                    id="sigma", min=0.5, max=20,
                    step=None,
                    value=5,
                    marks=None,
                    tooltip={"placement": "bottom", "always_visible": True},
                ),
            ], style={"flex": "1", "minWidth": "280px", "paddingRight": "12px"}),

            html.Div([
                html.Label("критическое значение c"),
                dcc.Slider(
                    id="c_slider", min=-50, max=50,
                    step=None,              # непрерывный
                    value=30,
                    marks=None,             # без меток
                    tooltip={"placement": "bottom", "always_visible": True},
                ),
                html.Div([
                    dcc.RadioItems(
                        id="tail",
                        options=[
                            {"label": "Правый хвост", "value": "right"},
                            {"label": "Левый хвост",  "value": "left"},
                            {"label": "Двусторонний", "value": "two-sided"},
                        ],
                        value="right", inline=True
                    )
                ], style={"marginTop": "10px"}),
                html.Div(
                    id="stats",
                    style={"marginTop": "10px", "fontSize": "16px", "fontFamily": "monospace"}
                ),
            ], style={"flex": "1", "minWidth": "280px"}),
        ], style={"display": "flex", "gap": "14px", "flexWrap": "wrap", "marginBottom": "8px"}),

        dcc.Graph(id="fig", config={"displaylogo": False}),
        html.Hr(),
        html.Footer([
            "tg автора: ",
            html.A(
                "@ArturKamalov",
                href="https://t.me/ArturKamalov",
                target="_blank", rel="noopener noreferrer"
            )
        ], style={"textAlign": "center", "margin": "10px 0 30px", "color": "#555"})
    ], style={"maxWidth": "1100px", "margin": "18px auto", "padding": "0 16px"})
