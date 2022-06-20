#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import pandas as pd
import plotly.express as px
import plotly.graph_objs as go

import dash 
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output



app = dash.Dash(__name__)

# Import and clean data
df = pd.read_csv("aggregated_states.csv", encoding='utf-8')


# # ======================== Setting the margins
layout = go.Layout(
    margin=go.layout.Margin(
        l=40,  # left margin
        r=40,  # right margin
        b=10,  # bottom margin
        t=35  # top margin
    )
)

# Dashboard layout

app.layout = html.Div([
    
    html.H1("Lyme Disease - United States from 2000 - 2019",
            style={'text-align': 'center'}), 
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

    dcc.Graph(id='lyme_disease_map', style={'width': '90vh', 'height': '70vh'}, figure={})


])
    
# Connect Graphs with Components
@app.callback(
    [Output(component_id='output_container', component_property='children'),
     Output(component_id='lyme_disease_map', component_property='figure')],
    [Input(component_id='select_year', component_property='value')]
)

def update_graph(option_selected):
    print(option_selected)
    print(type(option_selected))
    
    container = "You are checking counts from year: {}".format(option_selected)
    
    dff = df.copy()
    dff = dff[dff["Year"] == option_selected]

    
# Plotly Express
    
    fig = px.choropleth(
        data_frame=dff,
        locationmode='USA-states',
        locations='state_code',
        scope="usa",
        color='Count_Total',
        hover_data=['State', 'Count_Total'],
        color_continuous_scale=px.colors.sequential.YlOrRd,
        labels={'Count_Total:' 'Total Count of infection'},
        template='plotly_dark'
)


# Plotly Graph Objects (GO)
#    fig = go.Figure(
#         data=[go.Choropleth(
#             locationmode='USA-states',
#             locations=dff['state_code'],
#             z=dff["Count_Total"].astype(int),
#             colorscale='Reds',
#         )]
#     )
#    
#    fig.update_layout(
#         title_text="Humans affected by Lyme Disease",
#         title_xanchor="center",
#         title_font=dict(size=24),
#         title_x=0.5,
#         geo=dict(scope='usa'),
#     )



    return container, fig

# ======================== Bar Chart
def get_bar_chart():
    barChart = dcc.Graph(figure=go.Figure(layout=layout).add_trace(go.Bar(x=df['State'],
                                                                          y=df['Count_Total'],
                                                                          marker=dict(color='#351e15'))).update_layout(
        title='Infections per State', plot_bgcolor='rgba(0,0,0,0)'),
        style={'width': '50%', 'height': '40vh', 'display': 'inline-block'})
    return barChart


# ======================== Line Chart
def get_line_chart():
    lineChart = dcc.Graph(figure=go.Figure().add_trace(go.Scatter(x=df['Year'],
                                                                               y=df['Count_Total'],
                                                                               marker=dict(
                                                                                   color='#351e15'))).update_layout(
        title='Infections', plot_bgcolor='rgba(0,0,0,0)'),
        style={'width': '50%', 'height': '40vh', 'display': 'inline-block'})
    return lineChart



 
# run
if __name__ == '__main__':
    app.run_server(debug=True)    
    



























