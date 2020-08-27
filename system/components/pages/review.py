# External Libraries
import dash_core_components as dcc
import dash_html_components as html

# Data
from components.data.table import get_table
from components.data.graph import get_graph, get_figure

# Fragments
from components.fragments.bottom_menu import BOTTOM_MENU

# Graph
# ID: GRAPH = graph
FIGURE = get_figure(standard=True)
GRAPH = get_graph(FIGURE)


# Table
# ID: table
TABLE = get_table()


review_page = html.Div([
            html.Div([
                    html.Div([
                        GRAPH
                    ], style={"width": "35%", "float": "left"}, className="columns"),
                    
                    html.Div([
                        TABLE
                    ], style={"width": "65%", "float": "right"}, className="columns", id="table-div"),
                    
            ], className="row"),
                
            html.Div([
                BOTTOM_MENU
            ]),
        ])