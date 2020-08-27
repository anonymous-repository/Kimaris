# Python Standard Libraries
import math
# External Libraries
import igraph as ig
import chart_studio.plotly as py
import plotly.graph_objs as go
import dash_core_components as dcc

# Database
from components.database.graph import get_standard_graph


def get_figure(nodes=None, links=None, sizes_=None, name="", standard=False, source="https://scholar.google.com.br/"):
    # Standard graph
    if standard:
        nodes, links, sizes_ =  get_standard_graph()
    
    # Re-scale sizes
    # Big values (x > 40) make the graph awful
    sizes__ = []
    for size in sizes_:
        if size != "No citations": 
            sizes__.append(size)
        else:
            sizes__.append(1)

    MAX = max(sizes__)
    if MAX != 0:   
        sizes = []
        if MAX > 3000:
            DIVIDE = 40
        elif MAX > 1500:
            DIVIDE = 30
        elif MAX > 750:
            DIVIDE = 25
        elif MAX > 300:
            DIVIDE = 17
        elif MAX > 100:
            DIVIDE = 12
        elif MAX > 30:
            DIVIDE = 5
        else:
            DIVIDE = 1
        for size in sizes__:
            size = (size+MAX)//(MAX//DIVIDE)
            sizes.append(size)
    else:
        sizes= [1]
    
    
    nl = len(links)/len(nodes)
    print(nl)
    ns = (sum(sizes__) - len(sizes__))/len(nodes)
    print(ns)
    
        
    N=len(nodes)
    L=len(links)
    Edges=[(links[k]['source'], links[k]['target']) for k in range(L)]

    G=ig.Graph(Edges, directed=True)

    
    if len(sizes) ==1:
        G.add_vertices(1)
    else:
        G.add_vertices(N)


    
    labels=[]
    group=[]
    for node in nodes:
        labels.append(node['name'])
        group.append(node['group'])
        
    
    layt=G.layout_fruchterman_reingold(grid=True,dim=3)
    #layt=G.layout_auto(dim=3)
    
    Xn=[layt[k][0] for k in range(N)]# x-coordinates of nodes
    Yn=[layt[k][1] for k in range(N)]# y-coordinates
    Zn=[layt[k][2] for k in range(N)]# z-coordinates
    #dxe=[layt[k][0] for k in range(N)]
    #dye=[layt[k][1] for k in range(N)]
    #dze=[layt[k][2] for k in range(N)]
    
    Xe=[]
    Ye=[]
    Ze=[]
    dxe=[]
    dye=[]
    dze=[]

    import numpy as np

    for e in Edges:
        dxe.append(layt[e[0]][0])
        dye.append(layt[e[0]][1])
        dze.append(layt[e[0]][2])
        Xe+=[layt[e[0]][0],layt[e[1]][0], None]
        Ye+=[layt[e[0]][1],layt[e[1]][1], None]
        Ze+=[layt[e[0]][2],layt[e[1]][2], None]
    
    
    if len(labels) == 2:
        Xn=[0,1]
        Yn=[0,2]
        Zn=[0,1]
        Xe=[0,1, None]
        Ye=[0,2, None]
        Ze=[0,1, None]
        dxe=[0]
        dye=[0]
        dze=[0]

    trace3=go.Scatter3d(x=dxe,
                y=dye,
                z=dze,
                mode='markers',
                name='actors',
                opacity=0.7,
                marker=dict(symbol='circle',
                                size=2 if not standard else 0.2,
                                color="red"
                                ),
                text=[f"{'<br>'.join([label[index : index + 30] for index in range(0, len(label), 30)])}<br>Cited by: {size}" for label, size in zip(labels, sizes_)],
                hoverinfo='none'
                )

    trace1=go.Scatter3d(x=Xe,
                y=Ye,
                z=Ze,
                mode='lines',
                line=dict(color='rgb(125,125,125)', width=1),
                hoverinfo='skip',
                )

    trace2=go.Scatter3d(x=Xn,
                y=Yn,
                z=Zn,
                mode='markers',
                name='actors',
                opacity=1,
                marker=dict(symbol='circle',
                                size=[x for x in sizes],
                                color=group,
                                colorscale='haline',
                                line=dict(color='rgb(50,50,50)', width=0.5)
                                ),
                text=[f"{'<br>'.join([label[index : index + 30] for index in range(0, len(label), 30)])}<br>Cited by: {size}" for label, size in zip(labels, sizes_)],
                hoverinfo='text'
                )

    axis=dict(showbackground=False,
            showline=False,
            zeroline=False,
            showgrid=False,
            showticklabels=False,
            title=''
            )

    layout = go.Layout(
            title=name,
            showlegend=False,
            scene=dict(
                xaxis=dict(axis),
                yaxis=dict(axis),
                zaxis=dict(axis),
            ),
        margin=dict(l=0, r=0, t=0, b=0),
        hovermode='closest',
        annotations=[
            dict(
            showarrow=False,
                text=f"Data source: <a href='{source}'>Google Scholar</a>",
                xref='paper',
                yref='paper',
                x=0.1,
                y=0.1,
                xanchor='left',
                yanchor='bottom',
                font=dict(
                size=14
                )
                )
            ],    
        hoverlabel = dict(
            bgcolor = 'white'
        )
    )

    data=[trace1, trace2, trace3]
    fig=go.Figure(data=data, layout=layout)
    fig.update_layout(
        title={
        'y':0.9,
        'x':0.5,
        'xanchor': 'center',
        'yanchor': 'top'},
    autosize=True)
    
    return fig

def get_graph(figure):
    config = {'responsive': True, "displaylogo": False, \
        'modeBarButtonsToRemove': ['pan3d', 'lasso3d', 'zoom3d', 'orbitRotation', 'tableRotation', \
            'resetCameraDefault3d', 'hoverClosest3d', 'resetCameraLastSave3d']}
    graph = dcc.Graph(figure=figure, id="graph", config = config, style={"height": "92vh", "width": "100%"})
    
    return graph