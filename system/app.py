# Python Standard Libraries
import base64
import time
# External Libraries
import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import pandas as pd
from tika import parser

# Pages
from components.pages.pages import pages

# Manager
from components.manager.search import do_search

# Data
from components.data.table import get_table
from components.data.graph import get_graph, get_figure
from components.data.nlp import get_common_words_graph, get_topics

# Database
from components.database.graph import get_selected_graph, get_name_by_id, populate_database, delete_node
from components.database.article import get_article


from components.fragments.menu import MENU
from components.fragments.article_menu import ARTICLE_MENU

# Neural Network
from components.neural_network.summarization import create_network, summarize

# App Stylesheet
external_stylesheets = [dbc.themes.LUX]

# App
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
app.config.suppress_callback_exceptions = True

# Table
# ID: table
TABLE = get_table()

# Graph
# ID: GRAPH = graph
FIGURE = get_figure(standard=True)
GRAPH = get_graph(FIGURE)


# App Layout
layout = html.Div([
    html.Div([
    MENU
    ],id="menu-div", style={"padding-bottom": "6vh"}),
    html.Div(id="page-content"),
    html.Div(id="SELECTED_ARTICLE")
], id="root", style={"height": "100vh"})

app.layout = html.Div([dcc.Location(id="url"), layout], id="layout")

@app.callback(Output("page-content", "children"), [Input("url", "pathname")])
def render_page_content(pathname):
    if pathname in ["/", "/review"]:
        return pages["review"]
    elif pathname in ["/article"]:
        return pages["article"]
    elif pathname in ["/reviews"]:
        return pages["reviews"]
    # If the user tries to reach a different page, return a 404 message
    return dbc.Jumbotron(
        [
            html.H1("404: Not found", className="text-danger"),
            html.Hr(),
            html.P(f"The pathname {pathname} was not recognised..."),
        ]
    )

RESET = 0
OPEN = 0
DELETE = 0
@app.callback(
    [Output("graph", "figure"),
    Output("table", "active_cell")],
    [Input("open-graph-button", "n_clicks"),
     Input("reset-graph-button", "n_clicks"),
     Input("delete-article-button", "n_clicks"),
     Input("graph", "clickData")],
    [State("graph", "figure"),
     State("table", "data"),
     State("table", "active_cell"),
     State('table', "page_current")]
)
def update_graph(open_, reset, delete, node, figure, value, cell, page):
    global FIGURE, RESET, DELETE, OPEN
    if reset > RESET:
        RESET = reset
        return FIGURE, None
    
    elif DELETE < delete:
        DELETE = delete
        if cell != None:
            name = value[cell["row"]]
            name = name["Title"]
            delete_node(name)
            time.sleep(5)
            FIGURE = get_figure(standard=True)
            return FIGURE, None
        elif node != None:
            name = node["points"][0]["text"]  
            
            delete_node(name)
            time.sleep(3)
            FIGURE = get_figure(standard=True)
            return FIGURE, None
        else:
            return FIGURE, None
    elif OPEN < open_:
        OPEN = open_
        if cell != None:
            if page != None:
                name = value[cell["row"] + (10 * page)]
            else:
                name = value[cell["row"]]
            name = name["Title"]
            nodes, links, sizes = get_selected_graph(name)
            figure = get_figure(nodes, links, sizes, name)
            return figure, None
        
        return FIGURE, None
    elif node != None:
        if "text" in node["points"][0]:
            name = node["points"][0]["text"]  
            nodes, links, sizes = get_selected_graph(name)
            figure = get_figure(nodes, links, sizes, name)
            return figure, None
        else:
            return figure, None
    
    return FIGURE, None

SELECTED_ARTICLE = ""
NODE_CLICK = 0
@app.callback(
    Output("SELECTED_ARTICLE", "children"),
    [Input("select-article-button", "n_clicks"),
     Input("select-node-button", "n_clicks"),
     Input("graph", "clickData"),
     Input("table", "data")],
    [State("table", "active_cell")])
def select_article(click, node_click, node, value, article):
    global NODE_CLICK, SELECTED_ARTICLE, RESET, OPEN
    OPEN = 0
    RESET = 0
    name = ""
    if node_click > NODE_CLICK:
        NODE_CLICK = 0
        if node != None:
            if "text" in node["points"][0]:
                name = node["points"][0]["text"]
                SELECTED_ARTICLE = name
                return name
            
            
    if article != None:
        name = value[article["row"]]
        name = name["Title"]
    
    REVIEW_NAME = name
    SELECTED_ARTICLE = name
    return name

import re
@app.callback(
    [Output("article-info", "children"),
     Output("article-graph", "children")],
    [Input("article-div", "children")],
    [State("SELECTED_ARTICLE", "children")])
def article(click, name):
    global NODE_CLICK, SELECTED_ARTICLE
    if "Cited" in SELECTED_ARTICLE:
        SELECTED_ARTICLE = re.sub("<br>", "", SELECTED_ARTICLE)
        SELECTED_ARTICLE = re.sub("(Cited by: \d+)", "", SELECTED_ARTICLE)
    df_article = get_article(SELECTED_ARTICLE)
    json_article = df_article.to_json()
    df_article = pd.read_json(json_article)
    nodes, links, sizes = get_selected_graph(SELECTED_ARTICLE)
    figure = get_figure(nodes, links, sizes)
    name = df_article["article_title"]
    abstract = df_article["article_abstract"]
    # Remember to change link structure 
    link = df_article["article_link"][0]
    article = html.Div([
        html.H3(name),
        html.P(abstract),
        html.P(f"Article link: {link}"),
        ARTICLE_MENU
    ], id="article-content", style={'word-wrap': 'break-word'})
    config = {'responsive': True}
    graph = html.Div([dcc.Graph(figure=figure, id="graph", config = config)], style={"height": "100vh"})
    return article, graph
             
def get_pdf(contents, filename, date):
    content_type, content_string = contents.split(',')
    try:
        if "pdf" in content_type:   
            decoded = base64.b64decode(content_string)
            
            frame = html.Iframe(src=f"data:application/pdf;base64,{content_string}", style={"width": "100%", "height": "85vh"})
            raw = parser.from_buffer(decoded)
            
            content = raw["content"]
            
            # Common words
            common_words = get_common_words_graph(content, 50)
            
            # Topic Modelling
            topics = get_topics(SELECTED_ARTICLE, content)
            
            # Summarization
            model = create_network()
            
            content = summarize(model, content)
           
            return frame, content, common_words, None
    except Exception as e:
        print(e)
        return [html.Div([
            'There was an error processing this file.'
        ]), None, None, None]
    return [html.Div([
            'There was no error processing this file.'
        ]), None, None, None]

@app.callback([Output('iframe-article-div', 'children'),
               Output('text-article', 'children'),
               Output('common-words-div', 'children'),
               Output('topic-modelling-div', 'children')],
              [Input('upload-article-pdf', 'contents')],
              [State('upload-article-pdf', 'filename'),
               State('upload-article-pdf', 'last_modified')])
def update_output(content, name, date):
    if content is not None:
        children = get_pdf(content, name, date)
        return children
    return [html.Div([
            'No pdf sent.'
        ]), None, None, None]

CLICK = 0
@app.callback([Output("search-callback", "children")],
              [Input("search-button", "n_clicks")],
              [State("search-string", "value"),
               State("captchas-radio", "value")])
def search(click, search_string, captchas):
    global CLICK
    if click > CLICK:
        CLICK = click
        print(captchas)
        captchas = False
        if captchas == "1":
            captchas = True    
        articles = do_search(search_string, n=100, captchas=True)
        populate_database(articles)
    return [None]

@app.callback([Output("log-search", "children")],
              [Input("interval-component", "n_intervals")])
def update_log(interval):
    data = ""
    try:
        with open("scholar.log", "r") as f:
            data = f.readlines()
    except:
        pass
    
    return [data]


@app.callback(Output("info-modal", "is_open"),
              [Input("info-open-button", "n_clicks"),
               Input("info-close-button", "n_clicks")],
              [State("info-modal", "is_open")])
def info_model(open_, close, is_open):
    if open_ or close:
        return not is_open
    return is_open


@app.callback(
    Output("popover", "is_open"),
    [Input("popover-target", "n_clicks")],
    [State("popover", "is_open")],
)
def toggle_popover(n, is_open):
    if n:
        return not is_open
    return is_open


app.run_server(debug=True)