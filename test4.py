import dash
from dash.dependencies import Input, Output
import dash_table
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
import pandas as pd

# df = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/gapminder2007.csv')
# df = pd.read_json("test3/ParsedLogs/MouseClicks.JSON")

###############
color = 'rgba(255, 159, 216, 0.4)'
button = html.Div(
    [
        # dbc.Button("Large button", size="lg", className="mr-1"),
        # dbc.Button("Regular button", className="mr-1"),
        dbc.Button("Small button", size="sm",  color="blue"),
    ]
)

# url1 = '![myImage-1](assets/test.png)'
url1 = '![myImage-1; style = max-height:50px](assets/1602036122.2287035_main.py_root.png)'

data = [['Item 1', url1], ['Item 2', url1]]
# Create the pandas DataFrame 
df = pd.DataFrame(data, columns = ['Name', 'Image']) 


###########



app = dash.Dash(__name__, assets_folder='test3/Clicks/')



app.layout = html.Div([
        button,
        dash_table.DataTable(
            id='datatable-interactivity',
            columns=[{
                "name": i, 
                "id": i,
                'presentation': 'markdown',
                'renamable': True
                # "selectable": True
            } 
            for i in df.columns
            ],
            style_cell={
            'minWidth': '0px',
            'maxWidth': '50px',
            # 'height': '60px',
            'textAlign': 'left',
            # 'whiteSpace': 'no-wrap',
            # 'overflow': 'hidden'
            # 'textOverflow': 'ellipsis'
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
        # button
    ])

@app.callback(
    Output('datatable-interactivity', 'style_data_conditional'),
    [Input('datatable-interactivity', 'selected_columns')]
)
def update_styles(selected_columns):
    return [{
        'if': { 'column_id': i },
        'background_color': '#D2F3FF',
    } for i in selected_columns]

@app.callback(
    Output('datatable-interactivity-container', "children"),
    [Input('datatable-interactivity', "derived_virtual_data"),
     Input('datatable-interactivity', "derived_virtual_selected_rows")])
def update_graphs(rows, derived_virtual_selected_rows):
    # When the table is first rendered, `derived_virtual_data` and
    # `derived_virtual_selected_rows` will be `None`. This is due to an
    # idiosyncrasy in Dash (unsupplied properties are always None and Dash
    # calls the dependent callbacks when the component is first rendered).
    # So, if `rows` is `None`, then the component was just rendered
    # and its value will be the same as the component's dataframe.
    # Instead of setting `None` in here, you could also set
    # `derived_virtual_data=df.to_rows('dict')` when you initialize
    # the component.
    if derived_virtual_selected_rows is None:
        derived_virtual_selected_rows = []

    dff = df if rows is None else pd.DataFrame(rows)

    colors = ['#7FDBFF' if i in derived_virtual_selected_rows else '#0074D9'
              for i in range(len(dff))]

    return [
       
        # check if column exists - user may have deleted it
        # If `column.deletable=False`, then you don't
        # need to do this check.
        
    ]





if __name__ == '__main__':
    app.run_server(debug=True)