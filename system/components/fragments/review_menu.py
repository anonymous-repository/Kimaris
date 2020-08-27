# External Libraries
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html

review_menu_items = dbc.Row(
    [
        dbc.Col(
            dbc.NavLink(dbc.Button("Go back", id="return-review-button", n_clicks=0),
            href="/page-3",
            id="page-3-link"
            ),
            id="return-review-col", 
            width="auto"
        ),
        dbc.Col(
            dbc.Button("Search", id="search-button", n_clicks=0),
            id="search-col", 
            width="auto"
        ),
    ],
    no_gutters=True,
    className="flex-nowrap mt-3 mt-md-3",
    align="center",

)

help_items = dbc.Row(
    [
        dbc.Col(
            dbc.Button("Info", id="info-open-button", n_clicks=0),
            id="info-open-col", 
            width="auto"
        ),
        dbc.Modal(
            [
                dbc.ModalHeader("Instructions"),
                dbc.ModalBody(
                    dcc.Tabs([
                        dcc.Tab([
                            html.Div([
                                html.Br(),
                                html.H5("Search string"),html.P(" - The content you want to search."),
                                html.P('Example (query): ("code summarization" OR "code clone") AND ("neural network" OR "deep learning")', style={"font-size": "10px"}),
                                html.P('Example (query): Deep code summarization', style={"font-size": "10px"}),
                                html.P('Example (author): Avram Noam Chomsky', style={"font-size": "10px"}),
                                html.P('Example (keyword): Computer Graphics', style={"font-size": "10px"}),
                                html.Br(),
                                html.H5("Date"), html.P(" - Low and top year for the search. It does not count days or months."),
                            ])
                        ], label="Search"),
                        dcc.Tab([
                            html.Div([ 
                                html.Br(),
                                html.H5("Number of results"), html.P(" - The maximum number of articles returned at each forward step."),
                                html.Br(),
                                html.H5("Forward steps"), html.P("(Recommended = 3) - Number of forward steps of the search. Each extra step adds much more time than the previous step. More detailed information of Forward tab. Not yet implemented."),  
                                html.Br(),
                                html.H5("Solve captchas manually"),
                                html.P("Yes (Recommended) - Will ask you to solve the captchas. Results are incredibly faster."),
                                html.P("No - Will reject captchas and try again. Takes a good while."),
                                html.Br(),
                                html.H5("Databases - Only Google Scholar available at the moment.")
                            ])
                        ], label="Parameters"),
                        dcc.Tab([
                            html.Div([
                                html.Br(),
                                html.P("The log panel will update you on the current state of the search."),
                                html.P("If you are on the middle of a search and the log panel doesn't update after 2 minutes, consider restarting the search by refreshing the page and inputing the information again."),
                            ])
                        ], label="Log Panel")
                    ])
                ),
                dbc.ModalFooter(
                    dbc.Button("Close", id="info-close-button", className="ml-auto")
                ),
            ],
            id="info-modal", size="lg"
        ),
    ],
    style={"right": "0", "position": "absolute"}
)

REVIEW_MENU = dbc.Navbar(
    [
        review_menu_items,
        help_items,
        dbc.NavbarToggler(id="navbar-toggler")
    ],
    color="dark",
    dark=True,
    style={"position": "absolute", "bottom": 0, "left":0, "width": "100%"},
    id="review-menu")
