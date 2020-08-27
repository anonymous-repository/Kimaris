# External Libraries
import dash_core_components as dcc
import dash_html_components as html
# Fragments
from components.fragments.review_form import review_form
from components.fragments.review_menu import REVIEW_MENU


reviews_page = html.Div([
                html.Div([
                    html.Div([
                        review_form,
                        html.P(id="log-search", style={'whiteSpace': 'pre-wrap',"padding-left": "1em", "width": "50%", "height": "82vh", "overflow-y": "scroll", "display": "flex", "flex-direction" : "column-reverse"}),
                    ], className="row"),
                    html.Div(id="search-callback"),
                    dcc.Interval(
                            id="interval-component",
                            interval=1*1000,
                            n_intervals=0
                        ),
                    REVIEW_MENU
                ], id="reviews", style={"padding": "2em"})
            ])