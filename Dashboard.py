import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd
 
# Initialize App
app = dash.Dash(__name__)
 
df = pd.read_csv("House_market_Dynamics.csv")

region = df["region_name"].unique()
region_dropdown = dcc.Dropdown(id="region_dropdown",
                               options=[{"label": x, "value": x} for x in region],
                               value=region[0],
                               clearable=False)
            
app.layout = html.Div(children=[
    html.H1(children='UN Housing Market Dynamics'),
    html.H2(children='Average Number Of Houses Sold from 2017 to 2022'),region_dropdown,
    dcc.Graph(id='price-graph'),

    html.P("Age of Inventory :",style={'fontSize':25}),
    dcc.RangeSlider(
        id='range-slider',
        min=1, max=350, step=1,
        marks={1:'1',50:'50',100:'100',150:'150',200:'200',250:'250',300:'300',350:'350'},
        value=[1, 150]
    )
],style={'textAlign': 'center'})

 
# Set up the callback function
@app.callback(
    Output("price-graph", "figure"),
    [Input("region_dropdown", "value"),
    Input("range-slider","value")
    ]
)
 
def update_graph(selected_region,slider_range):
    start_val, end_val = slider_range  
    filtered_region = (df['region_name'] == selected_region) & (df["age_of_inventory"] > start_val) & (df["age_of_inventory"] <end_val)
    bar_fig = px.bar(df[filtered_region],
                       x='period_begin', y='average_homes_sold',
                       color='duration',
                       title=f'Average Homes Sold in {selected_region}')
    return bar_fig
 
 
if __name__ == "__main__":
    app.run_server(debug=True)