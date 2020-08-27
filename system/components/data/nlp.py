
# External Libraries
import dash_core_components as dcc
import plotly.express as px
from plotly.subplots import make_subplots
import plotly.graph_objects as go

from components.fragments.nlp_tools import get_most_common_words, remove_common_stop_words, get_most_common_bigrams, topic_modelling

def get_common_words_graph(data, number):
    
    
    common_words = get_most_common_bigrams(data)
    common_words = remove_common_stop_words(common_words)

    counts = []
    words = []
    for word, count in common_words.most_common(number):
        counts.append(count)
        words.append(word)

    fig = make_subplots(rows=1, cols=1, subplot_titles=["True", "True/Fake", "Fake"], shared_xaxes=True)

    fig.add_trace(
        go.Bar(x=counts, y=words, name="True", orientation='h'),
        row=1, col=1
    )

    fig.update_layout(margin=dict(l=0, r=0, t=0, b=0), xaxis_title="Count", yaxis_title="Words")

    graph = dcc.Graph(id="em", figure = fig, config={ 'displayModeBar': False}, responsive=True, style={"height": "80vh"})
    
    return graph

def get_topics(title, data):
    topic_modelling(title, data)
    pass