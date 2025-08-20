
from dash import html, callback, Output, Input, State
import dash_bootstrap_components as dbc

navbar = dbc.Navbar(
    dbc.Container(
        [
            dbc.NavbarToggler(id='navbar-toggler', n_clicks=0),
            dbc.Collapse(
                dbc.Nav(
                    [
                        dbc.NavItem(
                            dbc.NavLink(
                                'Edit & Upload',
                                href='/'
                            )
                        ),
                        dbc.NavItem(
                            dbc.NavLink(
                                'Analysis',
                                href='/analysis'
                            )
                        ),
                        dbc.DropdownMenu(
                            label="Tools",
                            nav=True,
                            in_navbar=True,
                            children=[
                                dbc.DropdownMenuItem("Cashback Calculator", href="/tools/cashback"),
                                dbc.DropdownMenuItem("50/30/20 Budgeting", href="/tools/50_30_20"),
                            ],
                        ),
                    ],
                    className="ml-auto",
                    navbar=True
                ),
                id='navbar-collapse',
                navbar=True
            ),
        ]
    ),
    color='dark',
    dark=True,
)

# added callback for toggling the collapse on small screens
@callback(
    Output('navbar-collapse', 'is_open'),
    Input('navbar-toggler', 'n_clicks'),
    State('navbar-collapse', 'is_open'),
)
def toggle_navbar_collapse(n, is_open):
    if n:
        return not is_open
    return is_open