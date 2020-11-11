import sys
import dash
import dash_daq as daq
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
from dash.dependencies import Input, Output
from flask_caching import Cache

def Throughput(df):
    throughput_dataframe = df
    MIN = 0
    MAX = int(len(throughput_dataframe)/2)

    theme =  {
        'dark': True,
        'detail': '#6c7a73',
        'primary': '#00EA64',
        'secondary': '#6E6E6E',
}
    layout = html.Div([
        dbc.Container(
            html.Div([
                html.Div([
                    html.Div(#[     #Removed for simplifying sync behavior
                        #dcc.Dropdown( #dropdown menu for updating throughput graph
                        #    id='live-dropdown',
                        #    options=[{'label': throughput_dataframe.loc[i, 'start'].replace('T',' '), 'value': i} for i in throughput_dataframe.index], #displays timestamps
                        #    placeholder = 'Select Timestamp',
                        #    ), html.Div(id='dd-container')
                        #],
                        #style = {'width': '30%','float':'left','background-color':'#303030'}
                        ),
                    html.Div(#[     #Removed for simplifying sync behavior
                        #daq.NumericInput( #Input field for selecting timeframe value(in seconds) to be highlighted in graph
                            #id='timeframe', 
                            #type='number', 
                            #placeholder = "0s (max: "+str(MAX)+"s)", 
                            #min = MIN, 
                            #max = MAX, #max value is (length of dataframe)/2
                            #)
                        #],
                        #style = {'width' :'10%','float': 'left','display':'inline-block', 'padding': '0px 0px 10px 20px'}
                    ),
                    html.Div([
                        daq.BooleanSwitch(
                            on=False,
                            id='switch',
                            label="Sync",
                            labelPosition="left",
                            #className='sync-control',
                            style= {'float':'right','padding': '5px'}
                        ),
                        html.Div(id='switch-container')
                    ])
                  ]),
                html.Div([
                    dcc.Graph(id='live-graph', #throughput graph
                    style={'width': '100%','float':'left', 'padding': '10px'}),
                    
                ]),
                html.Div([
                    dcc.Interval(
                        id='interval',
                        disabled=True,
                        n_intervals= 0)
                ]),
                html.Div([
                    dcc.Markdown(),
                    html.Pre(id='click-data')
                ])
            ], style = {'float':'left', 'background-color':'#303030', 'color':'white'})
    )
    ], style = {'background-color':'#303030', 'color':'white'})
    return daq.DarkThemeProvider(theme=theme, children = layout)