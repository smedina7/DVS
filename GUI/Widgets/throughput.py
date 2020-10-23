import sys
import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import dash_table
from dash.dependencies import Input, Output
from flask_caching import Cache
from navbar import Navbar

#external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
#app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

#throughput_file = '/home/kali/eceld-netsys/ProjectData/s7/ecel-export_1601930197/parsed/tshark/networkDataXY.JSON' 


#def throughput_dataframe():
    #return pd.read_json(query_throughput_data()) #for future use when caching?
#    return pd.read_json(throughput_file) 

#min and max values are the range of possible inputs for timeframe input field


#nav = Navbar()

#body = 

def Throughput(df):
    throughput_dataframe = df
    MIN = 0
    MAX = int(len(throughput_dataframe)/2)
    layout = html.Div([
        dbc.Container(
            html.Div([
                html.Div([
                    html.Div([
                        dcc.Dropdown( #dropdown menu for updating throughput graph
                            id='live-dropdown',
                            options=[{'label': throughput_dataframe.loc[i, 'start'].replace('T',' '), 'value': i} for i in throughput_dataframe.index], #displays timestamps
                            placeholder = 'Select Timestamp',
                            )
                        ],
                        style = {'width' :'30%','float': 'left','display':'inline-block'}),
                    html.Div([
                        dcc.Input( #Input field for selecting timeframe value(in seconds) to be highlighted in graph
                            id='timeframe', 
                            type='number', 
                            placeholder = "0s (max: "+str(MAX)+"s)", 
                            min = MIN, 
                            max = MAX, #max value is (length of dataframe)/2
                            )
                        ],
                        style = {'width' :'10%','float': 'left','display':'inline-block', 'padding': '0px 0px 10px 20px'}),
                    html.Div([
                        dcc.Dropdown( #very basic color picker that changes margin colors of graph
                            id = 'color-picker',
                            options=[{'label':'red', 'value':'rgba(200,10,10,.7)'},
                                {'label':'pink', 'value':'rgba(200,10,100,.7)'}, 
                                {'label':'blue', 'value':'rgba(20,40,210,.6)'},
                                {'label':'green', 'value':'rgba(40,170,100,.7)'},
                                {'label':'orange', 'value':'rgba(200,100,10,.7)'},
                                {'label':'yellow', 'value':'rgba(255,235,30,.7)'},
                                {'label':'purple', 'value':'rgba(120,20,130,.7)'}],
                            )
                        ],
                        style = {'width' :'15%','float': 'right','display':'inline-block','padding': '0px 50px 10px 20px'})
                  ]),
                html.Div([
                    dcc.Graph(id='live-graph', #throughput graph
                    style={'width': '100%','float':'left', 'padding': '0px'})
                ])
            ], style = {'float':'left','padding': '0px'})
    )

    ])
    return layout
