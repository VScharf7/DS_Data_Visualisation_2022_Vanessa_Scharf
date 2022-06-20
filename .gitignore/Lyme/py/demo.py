import dash
from dash import dcc, html
from flask import Flask
import pandas as pd
import dash_bootstrap_components as dbc
import plotly.express as px
import plotly.graph_objects as go


# initiate the app =================================

server = Flask(__name__)
app = dash.Dash(__name__, server = server, external_stylesheets=[dbc.themes.BOOTSTRAP, dbc.icons.BOOTSTRAP])


# read the files

df = pd.read_csv('aggregated_states2.csv')


# build components ==================================

header = html.H1("Lyme Disease Spread Across the USA from 2000 - 2019", style = {'text_align':'center', 'font-size':'50px'})
header2 = html.H2("Cases of Infection in Humans")

# Visual components

# Component 1

countfig = go.FigureWidget()
countfig.add_scatter(name = "Count per States", x = df['State'], y = df['Count_Total'], fill = 'tonexty', line_shape = 'spline')
#countfig.add_scatter(name = "Count per Year", x = df['Year'], y = df['Count_Total'], fill = 'tonexty')
countfig.update_layout(title = 'Infection Count across the States')

# Component 2

countfig_year = go.FigureWidget()

countfig_year.add_scatter(name = "Count per Year", x = df['Year'], y = df['Count_Total'], fill = 'tonexty')
#countfig_year.add_scatter(name = "Count per Year", x = df['Year'], y = df['Count_Total'], fill = 'tonexty')
countfig_year.update_layout(title = 'Infection Counts over the Year')
                





# Component 3 MAP

fig = px.choropleth(
        data_frame=df,
        locationmode='USA-states',
        locations='state_code',
        scope="usa",
        color='Count_Total',
        hover_data=['State', 'Count_Total'],
        color_continuous_scale=px.colors.sequential.YlOrRd,
        labels={'Count_Total:' 'Total Count of infection'},
       # template='plotly_dark'
        )
fig.update_layout(title = 'Most Affected States' )





# design the app layout =============================

app.layout = html.Div(
    [dbc.Row(
         [header]
         ),
     
     dbc.Row(
         [header2]
         ),
     
     dbc.Row(
         [dbc.Col(
             [dcc.Graph(figure = fig)]),
             
             
          dbc.Col(
             [dcc.Graph(figure = countfig_year)])]
         ),
     

     
     dbc.Row(
         [dbc.Col(
             [dcc.Graph(figure = countfig)]
             )])
     
     ]
        )


# run the app
app.run_server(debug=True)