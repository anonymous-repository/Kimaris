import dash_bootstrap_components as dbc
import dash_html_components as html
import dash_core_components as dcc

search_string_input = dbc.FormGroup(
    [
        dbc.Label("Search String", html_for="search-string-row", width=2),
        dbc.Col(
            dbc.Input(
                type="text", id="search-string", placeholder="Enter title"
            ),
            width=10,
        ),
    ],
    row=True,
)

date_input = dbc.FormGroup(
    [
        dbc.Label("Date", html_for="date-row", width=2),
        dbc.Col(
            dcc.DatePickerRange(
                id="date-row",
                display_format="Y"
            ),
            width=10,
        ),
    ],
    row=True,
)

n_input = dbc.FormGroup(
    [
        dbc.Label("Number of results", html_for="n-row", width=2),
        dbc.Col(
            dcc.RangeSlider(
                min=0,
                max=10,
                step=None,
                marks={
                    0: '10',
                    2: '100',
                    4: '500',
                    6: '1000',
                    8: '3000',
                    10: 'All'
                },
                value=[4]
            ),
            width=10,
        ),
    ],
    row=True,
)


databases_input = dbc.FormGroup(
    [
        dbc.Label("Databases", html_for="databases-row", width=2),
        dbc.Col(
            dbc.Checklist(
                id="databases-row",
                options=[
                    {"label": "Google Scholar", "value": 1},
                    
                    {
                        "label": "ACM Library", 
                        "value": 2,
                        "disabled": True,
                    },
                    
                    {
                        "label": "Elsevier",
                        "value": 3,
                        "disabled": True,
                    },
                ],
            ),
            width=10,
        ),
    ],
    row=True,
)

captchas_input = dbc.FormGroup(
    [
        dbc.Label("Solve captchas manually", html_for="captchas-row", width=2),
        dbc.Col(
            dcc.RadioItems(
                options=[
                    {'label': ' Yes', 'value': '1'},
                    {'label': ' No', 'value': '0'}
                ],
                value='1', id="captchas-radio", labelStyle={ "padding": "0.5em"}
            ),
            width=10,
        ),
    ],
    row=True,
)



review_form = dbc.Form([search_string_input, date_input, n_input, captchas_input, databases_input], style={"width": "50%"})