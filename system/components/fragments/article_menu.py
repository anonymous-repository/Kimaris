# Python Standard Libraries

# External Libraries
import dash_bootstrap_components as dbc

menu_items = dbc.Row(
    [
        dbc.Col(
            dbc.NavLink(dbc.Button("Return", id="return-article-button", n_clicks=0),
            href="/",
            id="return-article-link"
            ),
            id="return-article-col", 
            width="auto"),
    ],
    no_gutters=True,
    className="flex-nowrap mt-3 mt-md-3",
    align="center",
)
ARTICLE_MENU = dbc.Navbar(
    [
        menu_items,
        dbc.NavbarToggler(id="navbar-toggler")
    ],
    color="dark",
    dark=True,
    style={"position": "absolute", "bottom": 0, "left":0, "width": "100%"},
    id="menu")