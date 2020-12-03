import sys
import pandas as pd
from flask_caching import Cache
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
from throughput import Throughput
from Timestamp import Timestamp


#external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__)

app.config.suppress_callback_exceptions = True

inputfile = sys.argv[1] #filename passed through manager (has file path and dataline color info)
info = open(inputfile, 'r')

throughput_info = info.readlines()
    
throughput_file = throughput_info[0].strip('\n')
info.close()

def throughput_dataframe():
    #return pd.read_json(query_throughput_data()) #for future use when caching?
    return pd.read_json(throughput_file) 

throughput_df = throughput_dataframe()


app.layout = html.Div([
    dcc.Location(id = 'url', refresh = True),
    html.Div(id = 'page-content')
])

@app.callback(Output('page-content', 'children'),
            [Input('url', 'pathname')])
def display_page(pathname):
    return Throughput(throughput_df)

@app.callback(Output('switch', 'on'), Input('live-graph', 'clickData'))
def disable_interval(click):
    
    if click is not None:
        x = click["points"]
        for d in x:
            timestamp = d['x'].replace(' ','T')
            Timestamp.update_timestamp(timestamp)
            
    return False
    
#this call back method allows to update graph based on the selected value in the dropdown menu
#we can have multiple callbacks (probably one for each dataline) --this is most likely how we can acheive the sync behavior 
@app.callback([Output('live-graph', 'figure'), Output('interval', 'disabled'), Output('legend', 'children')],
               [Input('interval','n_intervals'),Input('live-graph', 'clickData'), Input('switch','on')])
def update_live_graph(intervals, click, on):
    df = throughput_df
    disabled = not on
    
    start_time = df.loc[0,'start']
    key = 0

    info = open(inputfile, 'r')
    
    throughput_info = info.readlines()
    throughput_color = 'rgba'+throughput_info[1].strip('\n')
    h = throughput_color.split(",")

    plot_color = h[0]+","+h[1]+","+h[2]+","+",.2)"
    info.close()
    legend = 'Enable switch to sync graph with corresponding data from other datalines'
    if(on):
        legend = ''
        currTimestamp = Timestamp.get_current_timestamp()
        timestamp = currTimestamp
        #for clickable graph actions during sync
        """ if click is not None:
            #disabled=False
            x = click["points"]
            for d in x:
                timestamp = d['x'].replace(' ','T') """

        for i in range(len(df)):
            if timestamp == df.loc[i,'start']:
                #key = int(df.loc[i,'traffic_xy_id'])
                start_time = timestamp
                #if start_time is not currTimestamp:
                    #Timestamp.update_timestamp(start_time)
                    #switch = False
                    #disabled = True                    
        """
        else:
            currTimestamp = Timestamp.get_current_timestamp()
            for i in range(len(df)):
                if currTimestamp == df.loc[i,'start']:
                    start_time = currTimestamp 
                    key = int(df.loc[i,'traffic_xy_id'])
        """

    else:
        currTimestamp = Timestamp.get_current_timestamp()
        for i in range(len(df)):
            if currTimestamp == df.loc[i,'start']:
                start_time = currTimestamp 
                key = int(df.loc[i,'traffic_xy_id'])
        
        if click is not None:
            #disabled=False
            x = click["points"]
            for d in x:
                timestamp = d['x'].replace(' ','T')
            for i in range(len(df)):
                if timestamp == df.loc[i,'start']:
                    key = int(df.loc[i,'traffic_xy_id'])
                    start_time = df.loc[i,'start']

            
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
            'paper_bgcolor' : throughput_color,
            'plot_bgcolor' : throughput_color, 
            # when updating graph, here we can manipulate the following to show a certain range or specific info (based on input 'value')
            'shapes': [{
                'type': 'rect',
                'xref': 'x', 'x0': start_time, 'x1': start_time, #highlights a time range (timeframe) from selected dropdown timestamp value
                'yref': 'paper', 'y0': 0, 'y1': 1,
                'line': {'color': 'Black', 'width': 1},
                'fillcolor': plot_color,
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
    }, disabled, legend


if __name__ == '__main__':
    app.run_server(debug=False)