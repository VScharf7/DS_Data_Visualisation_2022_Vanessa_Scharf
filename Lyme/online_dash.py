
import dash
from dash import dcc
from dash import html
import pandas as pd
import plotly.graph_objects as go
from dash.dependencies import Input, Output

analytics = pd.read_csv('aggregated_states.csv')

# ======================== Setting the margins
layout = go.Layout(
    margin=go.layout.Margin(
        l=40,  # left margin
        r=40,  # right margin
        b=10,  # bottom margin
        t=35  # top margin
    )
)



# ======================== Plotly Graphs
def get_bar_chart():
    barChart = dcc.Graph(figure=go.Figure(layout=layout).add_trace(go.Bar(x=analytics['State'],
                                                                          y=analytics['Count_Total'],
                                                                          marker=dict(color='#351e15'))).update_layout(
        title='Counts per States', plot_bgcolor='rgba(0,0,0,0)'),
        style={'width': '50%', 'height': '40vh', 'display': 'inline-block'})
    return barChart


def get_line_chart():
    lineChart = dcc.Graph(figure=go.Figure(layout=layout).add_trace(go.Scatter(x=analytics['Year'],
                                                                               y=analytics['Count_Total'],
                                                                               marker=dict(
                                                                                   color='#351e15'))).update_layout(
        title='Cases per year', plot_bgcolor='rgba(0,0,0,0)'),
        style={'width': '50%', 'height': '40vh', 'display': 'inline-block'})
    return lineChart


def get_scatter_plot():
    scatterPlot = dcc.Graph(figure=go.Figure(layout=layout).add_trace(go.Scatter(x=analytics['State'],
                                                                                 y=analytics['Count_Total'],
                                                                                 marker=dict(
                                                                                     color='#351e15'),
                                                                                 mode='markers')).update_layout(
        title='Count per State', plot_bgcolor='rgba(0,0,0,0)'),
        style={'width': '50%', 'height': '40vh', 'display': 'inline-block'})
    return scatterPlot


#def get_map():
    lyme_map = dcc.Graph(
        figure=go.Figure(layout=layout).add_trace(go.Pie(
            labels=analytics['state_code'],
            values=analytics['Count_Total'],
            marker=dict(colors=['#120303', '#300f0f', '#381b1b', '#4f2f2f', '#573f3f', '#695a5a', '#8a7d7d'],
                        line=dict(color='#ffffff', width=2)))).update_layout(title='Counts per state',
                                                                             plot_bgcolor='rgba(0,0,0,0)',
                                                                             showlegend=False),
        style={'width': '50%', 'height': '40vh', 'display': 'inline-block'})
    return lyme_map

# ======================== Dash App
app = dash.Dash(__name__)

# ======================== App Layout
app.layout = html.Div([
    html.H1('Lyme Disease Cases - USA from 2000 - 2019', style={'text-align': 'center', 'background-color': '#ede9e8'}),
    dcc.Dropdown(id="select_year", 
                 options=[
                     {"label": "2000", "value": 2000},
                     {"label": "2001", "value": 2001},
                     {"label": "2002", "value": 2002},
                     {"label": "2003", "value": 2003}, 
                     {"label": "2004", "value": 2004},
                     {"label": "2005", "value": 2005},
                     {"label": "2006", "value": 2006},
                     {"label": "2007", "value": 2007},
                     {"label": "2008", "value": 2008},
                     {"label": "2009", "value": 2009},
                     {"label": "2010", "value": 2010},
                     {"label": "2011", "value": 2011},
                     {"label": "2012", "value": 2012},
                     {"label": "2013", "value": 2013},
                     {"label": "2014", "value": 2014}, 
                     {"label": "2015", "value": 2015},
                     {"label": "2016", "value": 2016},
                     {"label": "2017", "value": 2017},
                     {"label": "2018", "value": 2018},
                     {"label": "2019", "value": 2019}],
                multi=False,
                value=2019,
                style={'width': "40%"}
                ),
        html.Div(id='output_container', children=[]),
    html.Br(),
    get_bar_chart(),
    get_line_chart(),
    get_scatter_plot(),
    get_map()
])



if __name__ == '__main__':
    app.run_server()