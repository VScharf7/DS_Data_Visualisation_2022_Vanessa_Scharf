import dash
from dash import dcc, html, Input, Output
from flask import Flask
import pandas as pd
import dash_bootstrap_components as dbc
import plotly.express as px
#import plotly.graph_objects as go


# initiate app

server = Flask(__name__)
app = dash.Dash(__name__, server = server, external_stylesheets=[dbc.themes.BOOTSTRAP, dbc.icons.BOOTSTRAP])


# read file
df = pd.read_csv('aggregated_states2.csv')


# build header components 

header = html.H1("Lyme Disease Spread Across the USA from 2000 - 2019", style = {'text-align':'center', 'font-size':'50px'})
header2 = html.H2("Cases of Infection in Humans", style = {'text-align':'center', 'font-size':'30px'})
source = html.H3("data source = https://lymediseaseassociation.org/lyme-tbd/cases-stats-maps-a-graphs/reported-lyme-disease-cases-in-the-u-s-by-county/", style = {'text-align':'left', 'font-size':'15px'})

# Visual components

# Component 1 MAP

fig = px.choropleth(
        data_frame=df,
        locationmode='USA-states',
        locations='state_code',
        scope="usa",
        color='Count_Total',
        hover_data=['State'],
        color_continuous_scale=px.colors.sequential.Reds)

fig.update_layout(title = 'Most Affected States' )

# Component 2 
# LineChart

line = px.line(
    data_frame = df,
     x = df['Year'],
     y = df['Count_Total'],
     #template = 'plotly_dark'
     )
line.update_layout(title = 'Total Infection Counts 2000 - 2019')


# Component 3
# barplot adding!
#barplot = px.bar(
#    data_frame = df, x = df['State'], y = df['Count_Total'],  #template = 'plotly_dark'
#     )
#barplot.update_layout(title = 'Total Infection Counts per State')    


# design layout

app.layout = html.Div(
    [dbc.Row([header]
         ),
     dbc.Row([header2]
         ),
     
     dbc.Row(
         [dbc.Col(
             [dcc.Graph(figure = fig)]),

          dbc.Col(
             [dcc.Graph(figure = line)])]
         ),

     dbc.Row(
         
          html.Div([
             dcc.Dropdown(id="dropdown", 
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
                style={'width': "40%"}),

             
         

             html.Div(id='output_container', children=[]),
             html.Br(),
             dcc.Graph(figure = {}, id = 'BarP')
             ])
                          

                          # Create Range Slider (Year)

),
     
     
     dbc.Row([source])])



### Callback

# ------------------------------------------------------------------------------
# Connect the Plotly graphs with Dash Components
@app.callback(
    [Output(component_id='output_container', component_property='children'),
     Output(component_id='BarP', component_property='figure')],
    [Input(component_id='dropdown', component_property='value')]
)
def update_graph(option_slctd):
    print(option_slctd)
    print(type(option_slctd))

    container = "The year chosen by user was: {}".format(option_slctd)

    # Plotly Express
    fig = px.bar(data_frame = df,
                 x = df['State'],
                 y = df['Count_Total'],  #template = 'plotly_dark'
)
    fig.update_layout(title = 'Total Infection Counts per State')    

    
    return container, fig



# run the app
app.run_server(debug=True)