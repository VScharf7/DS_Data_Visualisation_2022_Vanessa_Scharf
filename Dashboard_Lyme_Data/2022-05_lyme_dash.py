import dash
from dash import dcc, html, Input, Output
from flask import Flask
import pandas as pd
import dash_bootstrap_components as dbc
import plotly.express as px


# initiate app

server = Flask(__name__)
app = dash.Dash(__name__, server = server, external_stylesheets=[dbc.themes.BOOTSTRAP, dbc.icons.BOOTSTRAP])


# read files
#df = pd.read_csv('df_add_total.csv')
df = pd.read_csv('aggregated_states.csv')
dff = pd.read_csv('years_summed.csv')

# build header components

header = html.H1("Lyme Disease Spread Across the USA from 2000 - 2019", style = {'text-align':'center', 'font-size':'50px'})
header2 = html.H2("Cases of Infection in Humans", style = {'text-align':'center', 'font-size':'30px'})
source = html.H3("Vanessa Scharf, Data Visualisation 2022", style = {'text-align':'left', 'font-size':'15px'})

# Visual components

# Component 2
# Barplot per Year Total
bar_total = px.bar(
    data_frame = dff,
     x = dff['Year'],
     y = dff['Total'],
     color = None)
bar_total.update_traces(marker_color='red')
bar_total.update_layout(title = 'Total Infection Counts 2000 - 2019')

# Component 3
# Barplot per State
barplot_states = px.bar(data_frame = df,
                 x = df['State'],
                 y = df['Count_Total'],
                color = 'Year',
                color_continuous_scale=px.colors.sequential.Reds)
barplot_states.update_layout(title = 'Total Infection Counts per State')


# Layout

app.layout = html.Div([
    
     dbc.Row([header]),
     dbc.Row([header2]),

     dbc.Row([
         # First Column of Row
         dbc.Col(
             html.Div([
                 dcc.Dropdown(id='dropdown',
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

             dcc.Graph(id='lyme_map', figure = {})
            ])),
         
        # Second column of Row
        dbc.Col(
            html.Div([
                dcc.Graph(figure = bar_total)
                ]))
        ]),
        
     dbc.Row(html.Div([
         dcc.Graph(figure = barplot_states)])),

     dbc.Row([source])
     
     ])


# ------------------------------------------------------------------------------
# Connect the Plotly graphs with Dash Components
@app.callback(
    [Output(component_id='output_container', component_property='children'),
     Output(component_id='lyme_map', component_property='figure')],
    [Input(component_id='dropdown', component_property='value')])

def update_graph(option_slctd):
    print(option_slctd)
    print(type(option_slctd))

    container = "The map shows the Counts from year: {}".format(option_slctd)

    dff = df.copy()
    dff = dff[dff["Year"] == option_slctd]


    # Plotly Express
    fig = px.choropleth(
        data_frame=dff,
        locationmode='USA-states',
        locations='state_code',
        scope="usa",
        color='Count_Total',
        hover_data=['State', 'Count_Total'],
        color_continuous_scale=px.colors.sequential.YlOrRd,)

    return container, fig



# run the app
app.run_server(debug=True)
