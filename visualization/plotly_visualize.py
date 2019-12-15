from plotly.graph_objs import *
from plotly.offline import plot as offpy
import networkx as nx
from networkx.drawing.nx_agraph import graphviz_layout
import plotly.graph_objs as go


def visualize(G, node_size, weights, filename="netwrokx", title=""):
    keys = G.nodes()
    values = range(len(G.nodes()))
    dictionary = dict(zip(keys, values))
    inv_map = {v: k for k, v in dictionary.items()}
    G = nx.relabel_nodes(G, dictionary)
    try:
        pos = graphviz_layout(G)
    except:
        raise Exception("there is something wrong with graphviz")

    edge_trace = go.Scatter(
        x=[],
        y=[],
        # line=Line(width=[], color='rgba(136, 136, 136, .8)'),
        hoverinfo='none',
        mode='lines')

    for edge in G.edges():
        x0, y0 = pos[edge[0]]
        x1, y1 = pos[edge[1]]
        edge_trace['x'] += (x0, x1, None)
        edge_trace['y'] += (y0, y1, None)

    # for weight in weights:
    #     print(weight)
    #     edge_trace['line']['width'].append(weight)

    node_trace = go.Scatter(
        x=[],
        y=[],
        text=[],
        mode='markers+text',
        textfont=dict(family='Calibri (Body)', size=25, color='black'),
        opacity=1,
        # hoverinfo='text',
        marker=go.scatter.Marker(
            showscale=True,
            # colorscale options
            # 'Greys' | 'Greens' | 'Bluered' | 'Hot' | 'Picnic' | 'Portland' |
            # Jet' | 'RdBu' | 'Blackbody' | 'Earth' | 'Electric' | 'YIOrRd' | 'YIGnBu'
            colorscale='Hot',
            reversescale=True,
            color=[],
            size=[],
            colorbar=dict(
                thickness=15,
                title='Node Connections',
                xanchor='left',
                titleside='right'
            ),
            line=dict(width=2)))

    for node in G.nodes():
        x, y = pos[node]
        node_trace['x'] += (x,)
        node_trace['y'] += (y,)

    for i, adjacencies in G.adjacency():
        node_trace['marker']['color'] += (len(adjacencies),)

    for node in G.nodes():
        node_trace['text'] += (inv_map[node],)

    for size in node_size:
        node_trace['marker']['size'] += (size * 20,)

    fig = go.Figure(data=[edge_trace, node_trace],
                    layout=go.Layout(
                        title='<br>' + title,
                        titlefont=dict(size=16),
                        showlegend=False,
                        width=1500,
                        height=800,
                        hovermode='closest',
                        margin=dict(b=20, l=350, r=5, t=200),
                        # family='Courier New, monospace', size=18, color='#7f7f7f',
                        annotations=[dict(
                            text="",
                            showarrow=False,
                            xref="paper", yref="paper",
                            x=0.005, y=-0.002)],
                        xaxis=go.layout.XAxis(showgrid=False, zeroline=False, showticklabels=False),
                        yaxis=go.layout.YAxis(showgrid=False, zeroline=False, showticklabels=False)))

    offpy(fig, filename=filename, auto_open=True, show_link=False)


def scale_color_graph_visualize(Graph, color_list,
                                filename="plotly",
                                colorscale='Hot',
                                title="",
                                reverse_scale=True,
                                node_size=20):
    keys = Graph.nodes()
    values = range(len(Graph.nodes()))
    dictionary = dict(zip(keys, values))
    inv_map = {v: k for k, v in dictionary.items()}
    G = nx.relabel_nodes(Graph, dictionary)
    pos = graphviz_layout(G)

    edge_trace = Scatter(
        x=[],
        y=[],
        line=Line(width=3, color='rgba(136, 136, 136, .8)'),
        # hoverinfo=[],
        text=[],
        mode='lines+markers+text')

    for edge in G.edges():
        x0, y0 = pos[edge[0]]
        x1, y1 = pos[edge[1]]
        edge_trace['x'] += [x0, x1, None]
        edge_trace['y'] += [y0, y1, None]
        # edge_trace['hoverinfo'].append('ddd')
        # edge_trace['text'].append('888888888')

    # def make_text(X):
    #    return ''

    node_trace = Scatter(
        x=[],
        y=[],
        text=[],
        # text=X.apply(make_text, axis=1).tolist(),
        mode='markers+text',
        # mode='markers',
        textfont=dict(family='Calibri (Body)', size=15, color='black'),
        opacity=100,
        hoverinfo='none',
        marker=Marker(
            showscale=True,
            # colorscale options
            # 'Greys' | 'Greens' | 'Bluered' | 'Hot' | 'Picnic' | 'Portland' |
            # Jet' | 'RdBu' | 'Blackbody' | 'Earth' | 'Electric' | 'YIOrRd' | 'YIGnBu'
            colorscale=colorscale,
            reversescale=reverse_scale,
            color=[],
            size=node_size,
            colorbar=dict(
                thickness=15,
                title='',
                xanchor='left',
                titleside='right'
            ),
            line=dict(width=2)))

    for node in G.nodes():
        x, y = pos[node]
        node_trace['x'].append(x)
        node_trace['y'].append(y)
    # for node in G.nodes():
    # node_trace['hoverinfo'][0]='1212121212121'#.append('888888880')

    for adjacencies, color in zip(G.adjacency_list(), color_list):
        node_trace['marker']['color'].append(color)

    for node in G.nodes():
        node_trace['text'].append(inv_map[node])

    fig = Figure(data=Data(
        [edge_trace, node_trace]),
        layout=Layout(
            title='<br>' + title,
            titlefont=dict(size=16),
            showlegend=False,
            width=1500,
            height=800,
            # hovermode='closest',
            hovermode='closest',
            margin=dict(b=20, l=400, r=5, t=200),
            # family='Courier New, monospace', size=18, color='#7f7f7f',
            annotations=[dict(
                text="",
                showarrow=False,
                xref="paper", yref="paper",
                x=0.005, y=-0.002)],
            xaxis=XAxis(showgrid=False, zeroline=False, showticklabels=False),
            yaxis=YAxis(showgrid=False, zeroline=False, showticklabels=False)))

    # j=0
    # for x in fig.data:
    #    print(x)
    # for node in G.nodes():
    #    fig.data[0]['text'].append('asasa'+str(j))
    #    j+=1

    offpy(fig, filename=filename, auto_open=True, show_link=False)


def color_graph_visualize(Graph, color_list, filename="plotly", title=""):
    keys = Graph.nodes()
    values = range(len(Graph.nodes()))
    dictionary = dict(zip(keys, values))
    inv_map = {v: k for k, v in dictionary.items()}
    G = nx.relabel_nodes(Graph, dictionary)
    pos = graphviz_layout(G)

    edge_trace = Scatter(
        x=[],
        y=[],
        line=Line(width=3, color='rgba(136, 136, 136, .8)'),
        hoverinfo='none',
        mode='lines',
        text=[])

    for edge in G.edges():
        x0, y0 = pos[edge[0]]
        x1, y1 = pos[edge[1]]
        edge_trace['x'] += [x0, x1, None]
        edge_trace['y'] += [y0, y1, None]
        edge_trace['text'].append('label')

    node_trace = Scatter(
        x=[],
        y=[],
        text=[],
        mode='markers+text',
        textfont=dict(family='Calibri (Body)', size=15, color='black'),
        opacity=100,
        hoverinfo='text',
        marker=Marker(
            color=[],
            size=30,
            line=dict(width=2)))

    for node in G.nodes():
        x, y = pos[node]
        node_trace['x'].append(x)
        node_trace['y'].append(y)

    for adjacencies, color in zip(G.adjacency_list(), color_list):
        node_trace['marker']['color'].append(color)

    for node in G.nodes():
        node_trace['text'].append(inv_map[node])

    fig = Figure(data=Data([edge_trace, node_trace]),
                 layout=Layout(
                     title='<br>' + title,
                     titlefont=dict(size=16),
                     showlegend=False,
                     width=1500,
                     height=800,
                     hovermode='closest',
                     margin=dict(b=20, l=350, r=5, t=200),
                     # family='Courier New, monospace', size=18, color='#7f7f7f',
                     # paper_bgcolor='#7f7f7f',
                     # plot_bgcolor='#c7c7c7',
                     annotations=[dict(
                         text="",
                         showarrow=False,
                         xref="paper", yref="paper",
                         x=0.005, y=-0.002)],
                     xaxis=XAxis(showgrid=False, zeroline=False, showticklabels=False),
                     yaxis=YAxis(showgrid=False, zeroline=False, showticklabels=False)))

    offpy(fig, filename=filename, auto_open=True, show_link=False)


def three_d_nework_graph(x_positions, y_positions, z_positions, colors, labels="unknown"):
    trace2 = Scatter3d(x=x_positions,
                       y=y_positions,
                       z=z_positions,
                       mode='markers',
                       name='actors',
                       marker=Marker(symbol='dot',
                                     size=6,
                                     color=colors,
                                     colorscale='Viridis',
                                     line=Line(color='rgb(50,50,50)', width=0.5)
                                     ),
                       text=labels,
                       hoverinfo='text'
                       )
    axis = dict(showbackground=True,
                showline=True,
                zeroline=True,
                showgrid=True,
                showticklabels=True,
                title=''
                )
    layout = Layout(
        title="Network of coappearances of documents in the whole repository(3D visualization)",
        width=1000,
        height=1000,
        showlegend=False,
        scene=Scene(
            xaxis=XAxis(axis),
            yaxis=YAxis(axis),
            zaxis=ZAxis(axis),
        ),
        margin=Margin(
            t=100
        ),
        hovermode='closest',
        annotations=Annotations([
            Annotation(
                showarrow=False,
                text="",
                xref='paper',
                yref='paper',
                x=0,
                y=0.1,
                xanchor='left',
                yanchor='bottom',
                font=Font(
                    size=14
                )
            )
        ]), )
    data = Data([trace2])
    fig = Figure(data=data, layout=layout)

    offpy(fig, filename="dd", auto_open=True, show_link=False)
