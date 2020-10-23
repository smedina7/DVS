import sys
import dash_bootstrap_components as dbc
import pandas as pd
from flask_caching import Cache
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
from keypresses import Keypresses
from throughput import Throughput
from navbar import Navbar

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.config.suppress_callback_exceptions = True

nav = Navbar()

throughput_file = sys.argv[1]  #filename passed through manager

def throughput_dataframe():
    #return pd.read_json(query_throughput_data()) #for future use when caching?
    return pd.read_json(throughput_file) 

app.layout = html.Div([
    dcc.Location(id = 'url', refresh = False),
    html.Div(id = 'page-content')
])

@app.callback(Output('page-content', 'children'),
            [Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/keypresses':
        return Keypresses()
    
    # else if:
    #     pathname == '/mouseclicks':
    #     return 

    else:
        throughput_df = throughput_dataframe()
        return Throughput(throughput_df)



@app.callback(Output('live-dropdown', 'value'),[Input('live-graph', 'clickData')])
def update_dropdown(value):
    df = throughput_dataframe()
    key = 0

    if value is None:
        return key
    else:
        x = value["points"]
        for d in x:
            timestamp = d['x'].replace(' ','T')
        for i in range(len(df)):
            if timestamp == df.loc[i,'start']:
                key = int(df.loc[i,'traffic_xy_id'])
                return key

#this call back method allows to update graph based on the selected value in the dropdown menu
#we can have multiple callbacks (probably one for each dataline) --this is most likely how we can acheive the sync behavior 
@app.callback(Output('live-graph', 'figure'),[Input('live-dropdown', 'value'), Input('timeframe', 'value'), Input('color-picker','value')])
def update_live_graph(timestamp, t_frame, color):
    df = throughput_dataframe()

    if color is None:
        margin_color = 'rgba(211,211,211,.7)' #default light gray background
        highlight_color = 'rgba(211,211,235,.2)'
    else:
        rgb = color.split(".")
        margin_color = color
        highlight_color = rgb[0]+".2)"

    if t_frame is None: 
        timeframe = 0 # seconds
    else:
        timeframe = t_frame # in seconds

    if timestamp is not None: 
        start_time = df.loc[timestamp, 'start']

        if timestamp <= ((len(df)-1)-timeframe):
            end_time = df.loc[timestamp+timeframe, 'start']
        else:
            start_time = df.loc[(len(df)-1)-timeframe, 'start']
            end_time = df.loc[len(df)-1, 'start']
    else:
        start_time = df.loc[0, 'start']
        end_time = df.loc[0, 'start']

    return {
        'data': [{
            'x': df['start'], # x axis is timestamp
            'y': df['y'], # y axis is number of packets since previous timestamp
            'line': {
                'width': 1,
                'color': 'Black',
                'shape': 'spline'
            },
            'text': {'color': 'Black'}
        }],
        'layout': {
            'height': 225,
            'width': 675,
            'paper_bgcolor' : margin_color,
            #'plot_bgcolor' : plot_color, 
            # when updating graph, here we can manipulate the following to show a certain range or specific info (based on input 'value')
            'shapes': [{
                'type': 'rect',
                'xref': 'x', 'x0': start_time, 'x1': end_time, #highlights a time range (timeframe) from selected dropdown timestamp value
                'yref': 'paper', 'y0': 0, 'y1': 1,
                'line': {'color': 'Black', 'width': 1},
                'fillcolor': highlight_color,
                'text': {'color': 'Black'}
            }]
            ,
            'annotations': [{
                'showarrow': False,
                'xref': 'x', 'x': start_time, 'xanchor': 'right',
                'yref': 'paper', 'y': 0.95, 'yanchor': 'top',
                'text': '',
                'bgcolor': 'rgba(255, 255, 255, 0.8)'
            }],
            # aesthetic options
            'margin': {'l': 40, 'b': 30, 'r': 20, 't': 20},
            'xaxis': {'showgrid': True, 'zeroline': False},
            'yaxis': {'showgrid': True, 'zeroline': False},
            'text': {'color': 'Black'}
            
        }
    }

if __name__ == '__main__':
    app.run_server(debug=False)

