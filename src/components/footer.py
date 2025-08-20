
from dash import html
import dash_bootstrap_components as dbc

footer_links = [
    {"icon": "fa-solid fa-envelope", "url": "mailto:kowelcarter@gmail.com"},
    {"icon": "fa-brands fa-github", "url": "https://github.com/carterkowel"},
    {"icon": "fa-brands fa-linkedin", "url": "https://www.linkedin.com/in/carter-kowel-60bb3b1a2/"}
]

footer = html.Footer(
    dbc.Container(
        [
            html.Hr(),
            html.Div(
                [
                    html.A(
                        html.I(className=f"{link['icon']} fa-lg"),
                        href=link["url"],
                        target="_blank",
                        className="me-4 text-dark"
                    )
                    for link in footer_links
                ],
                className="text-center py-3"
            )
        ]
    )
)