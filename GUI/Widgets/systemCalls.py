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
from throughput import Throughput


df = pd.read_json("test3/ParsedLogs/SystemCalls.JSON")


def SystemCalls():
    layout = html.Div([

        dash_table.DataTable(
            id='datatable-interactivity',
            columns=[{
                "name": i, 
                "id": i,
                'renamable': True,
                "selectable": True
            } for i in df.columns],
            data=df.to_dict('records'),
            editable=True,
            filter_action="native",
            sort_action="native",
            sort_mode="multi",
            column_selectable="single",
            row_selectable="multi",
            row_deletable=True,
            selected_columns=[],
            selected_rows=[],
            page_action="native",
            page_current= 0,
            page_size= 10,
        ),
        html.Div(id='datatable-interactivity-container')
    ])

    return layout

