### Data
import pandas as pd
import pickle### Graphing
import plotly.graph_objects as go### Dash
import dash
import dash_table
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Output, Input

## Navbar
from navbar import Navbar
# from throughput import Throughput

#Value for color
color = 'rgba(255, 159, 216, 0.4)'

#need to fix path
df = pd.read_json("test3/ParsedLogs/MouseClicks.JSON")

##########dropdown##########
available_indicators = df['start'].unique()
dropdownsystem = html.Div([
    dcc.Dropdown(id='my-dropdown',
    options=[{'label': i, 'value': i} for i in available_indicators],
    value='')
    # dash_table.DataTable(
    #     id='datatable-interactivity')
])

#######################


def MouseClicks():
    layout = html.Div([

        ##adding dropdown
        dropdownsystem,

        dash_table.DataTable(
            id='datatable-interactivity',
            columns=[{
                "name": i, 
                "id": i,
                'renamable': True
                # "selectable": True
            } 
            for i in df.columns
            ],
            style_cell={
            'minWidth': '0px',
            'maxWidth': '50px',
            'height': '60px',
            'textAlign': 'left',
            'whiteSpace': 'no-wrap',
            'overflow': 'hidden',
            'textOverflow': 'ellipsis',
            'backgroundColor': color
            # 'color': 'white'
            },
            data=df.to_dict('records'),
            editable=True,
            filter_action="native",
            sort_action="native",
            sort_mode="multi",
            column_selectable="single",
            # row_selectable="multi",
            row_deletable=True,
            selected_columns=[],
            selected_rows=[],
            page_action="native",
            page_current= 0,
            page_size= 10,
            style_table={'overflowX': 'scroll'}
        ),
        html.Div(id='datatable-interactivity-container')
    ])

    return layout

