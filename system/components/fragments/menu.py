# Python Standard Libraries

# External Libraries
import dash_bootstrap_components as dbc
import dash_html_components as html


menu_items = dbc.Row(
    [
        dbc.Col(
            dbc.NavLink(dbc.Button("Reviews", id="reviews-button", n_clicks=0),
            href="/reviews",
            id="reviews-link"
            ),
            id="reviews-col", 
            width="auto"
        )
    ],
    no_gutters=True,
    className="ml-auto flex-nowrap mt-3",
    align="center",

)

MENU = dbc.Navbar(
    [   
        html.A(
            dbc.Row(
                [   
                    dbc.Col(html.Img(src="assets/logo2.svg", height="67vh")),
                    dbc.Col(dbc.NavbarBrand("Kimaris", className="ml-2")),
                ],
                align="center",
                no_gutters=True,
                ),
            href="/",
            id="logo"
        ),
        menu_items,
        dbc.NavbarToggler(id="navbar-toggler")
    ],
    color="dark",
    dark=True,
    style={"position": "absolute", "top": 0, "left":0, "width": "100%"},
    id="menu")