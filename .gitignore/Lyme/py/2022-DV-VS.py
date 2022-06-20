import dash
from dash import dcc, html
from flask import Flask
import pandas as pd
import dash_bootstrap_components as dbc
import plotly.express as px
import plotly.graph_objects as go


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
        color_continuous_scale=px.colors.sequential.Reds,# YlOrRd,-
         
        #labels={'Count_Total:' 'Total Count of infection'},
        #template='plotly_dark'
        )
fig.update_layout(title = 'Most Affected States' )

# Component 2 LineChart

countfig_year = px.line(
    data_frame = df,
     x = df['Year'],
     y = df['Count_Total'],
     #template = 'plotly_dark'
     )
countfig_year.update_layout(title = 'Total Infection Counts 2000 - 2019')


# Component 3

# barplot adding! fig = px.bar(df, x="State", y="Count_Total", color="Year", barmode="group")


countfig = go.FigureWidget()
countfig.add_scatter(name = "Count per States", x = df['State'], y = df['Count_Total'], fill = 'tonexty', line_shape = 'spline')
countfig.update_layout(title = 'Total Infection Counts per State')                



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
             [dcc.Graph(figure = countfig)])]
         ),
     

     
     dbc.Row(
         [dbc.Col(
             [dcc.Graph(figure = countfig_year)])]
         ),
     
     
         dbc.Row([source]
         )]
        )


# run the app
app.run_server(debug=True)