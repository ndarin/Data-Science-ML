#!/usr/bin/python
# Import required libraries
import pandas as pd
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import plotly.express as px

# Read the airline data into pandas dataframe
spacex_df = pd.read_csv("spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()

sites = ['CCAFS LC-40', 'CCAFS SLC-40', 'KSC LC-39A', 'VAFB SLC-4E']

# Create a dash application
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

# Create an app layout
app.layout = html.Div(children=[html.H1('SpaceX Launch Records Dashboard',
                                        style={'textAlign': 'center', 'color': '#503D36',
                                               'font-size': 40}),
                                # Add a dropdown list to enable Launch Site selection
                                # The default select value is for ALL sites
                                dcc.Dropdown(id='site-dropdown', 
                                        # Add dropdown values 
                                        options=[
                                            {'label': 'All Sites', 'value': 'ALL'},
                                            {'label': sites[0], 'value': sites[0]},
                                            {'label': sites[1], 'value': sites[1]},
                                            {'label': sites[2], 'value': sites[2]},
                                            {'label': sites[3], 'value': sites[3]}
                                            ],
                                        value='ALL',
                                        placeholder="Select a site"),
                                html.Br(),

                                # Add a pie chart to show the total successful launches count for all sites
                                # If a specific launch site is selected, it will show the Success vs. Failed counts for the site
                                html.Div(dcc.Graph(id='success-pie-chart')),
                                html.Br(),

                                html.P("Payload range (Kg):"),
                                # Add a slider to select payload range
                                dcc.RangeSlider(id='payload-slider',
                                                min=0,
                                                max=10000,
                                                step=1000,
                                                value=[min_payload, max_payload],
                                                marks={
                                                0: '0',
                                                1000: '1000',
                                                2000: '2000',
                                                3000: '3000',
                                                4000: '4000',
                                                5000: '5000',
                                                6000: '6000',
                                                7000: '7000',
                                                8000: '8000',
                                                9000: '9000',
                                                10000: '10000'}),
                                
                                # Add a scatter chart to show the correlation between payload and launch success
                                html.Div(dcc.Graph(id='success-payload-scatter-chart')),
                                ])


# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output
@app.callback(  Output(component_id='success-pie-chart', component_property='figure'),
                Input(component_id='site-dropdown', component_property='value')
            )
            
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output
def get_pie_chart(entered_site):
    if entered_site == 'ALL':
        data = spacex_df[spacex_df['Mission Outcome'] == 'Success']
        fig = px.pie(data, values='class',
        names='Launch Site',
        title='Total Success Launches by Site')
        return fig
    else:
        data = spacex_df[spacex_df['Launch Site'] == entered_site]
        fig = px.pie(data, values='class',
        names='class',
        title='Total Success vs Failure for Site')
        return fig

@app.callback(  Output(component_id='success-payload-scatter-chart', component_property='figure'),
                [Input(component_id='site-dropdown', component_property='value'),
                 Input(component_id='payload-slider', component_property='value')]
            )

def get_scatter_plot(entered_site, payload):
    data  = spacex_df.loc[(spacex_df['Payload Mass (kg)'] >= payload[0]) & (spacex_df['Payload Mass (kg)'] <= payload[1]), :]
    if entered_site == 'ALL':
        fig = px.scatter(data, 
                        x='Payload Mass (kg)',
                        y='class', 
                        color='Booster Version Category',
                        symbol='Booster Version Category',
                        title='Correlation between Payload and Success for All Sites')
        return fig
    else:
        data  = data[data['Launch Site'] == entered_site]
        fig = px.scatter(data, 
                        x='Payload Mass (kg)',
                        y='class', 
                        color='Booster Version Category',
                        symbol='Booster Version Category',
                        title='Correlation between Payload and Success for Site')
        return fig

# Run the app
if __name__ == '__main__':
    app.run_server()
