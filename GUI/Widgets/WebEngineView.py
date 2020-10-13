import logging
import os
import subprocess
from PyQt5.QtCore import QThread, pyqtSignal
import time
import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
from dash.dependencies import Input, Output
from flask_caching import Cache
from PyQt5 import QtWidgets

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
cache = Cache(app.server, config={'CACHE_TYPE': 'filesystem','CACHE_DIR': 'cache-directory'})

class WebEngine():
    def __init__(self, throughput_file):
        self.file = throughput_file
        df = self.throughput_dataframe()

        app.layout = html.Div([
        dcc.Dropdown( #dropdown menu for updating throughput graph
            id='live-dropdown',
            options=[{'label': df.loc[i, 'start'], 'value': i} for i in df.index] #displays timestamps
        ),
        dcc.Graph(id='live-graph') #throughput graph

        #can add more dcc objects here for displaying other dataline info
        
        ])
        
        app.run_server(debug=False)

    # def load(self, url):
    #     self.load(QUrl(url))

    def throughput_dataframe(self):
        return pd.read_json(self.file) 

    #probably need to have the following functions as well
    def keypresses_dataframe():
        return
    def mouseclicks_dataframe():
        return
    def systemcalls_dataframe():
        return

    #this call back method allows to update graph based on the selected value in the dropdown menu
    #we can have multiple callbacks (probably one for each dataline) --this is most likely how we can acheive the sync behavior 
    @app.callback(Output('live-graph', 'figure'),[Input('live-dropdown', 'value')])
    def update_live_graph(value):
        df = self.throughput_dataframe()
        start_time = df.loc[0, 'start']

        return {
            'data': [{
                'x': df['start'], # x axis is timestamp
                'y': df['y'], # y axis is number of packets
                'line': {
                    'width': 1,
                    'color': '#0074D9',
                    'shape': 'spline'
                }
            }],
            'layout': {
                'height': 225,
                'width': 670,
                # when updating graph, here we can manipulate the following to show a certain range or specific info (based on input 'value')
                'shapes': [{
                    'type': 'line',
                    'xref': 'x', 'x0': start_time, 'x1': start_time, #x axis range is the 1st timestamp to last timestamp on json
                    'yref': 'paper', 'y0': 0, 'y1': 0,
                    'line': {'color': 'darkgrey', 'width': 1}
                }],
                'annotations': [{
                    'showarrow': False,
                    'xref': 'x', 'x': start_time, 'xanchor': 'right',
                    'yref': 'paper', 'y': 0.95, 'yanchor': 'top',
                    'text': '',
                    'bgcolor': 'rgba(255, 255, 255, 0.8)'
                }],
                # aesthetic options
                'margin': {'l': 20, 'b': 20, 'r': 10, 't': 5},
                'xaxis': {'showgrid': False, 'zeroline': False},
                'yaxis': {'showgrid': False, 'zeroline': False}
            }
        }
    
    #This callback can be used for caching later
    #@cache.memoize(timeout=60)
    #def query_throughput_data():
    #if __name__ == '__main__':
     #   app.run_server(debug=False)