
import dash
from dash.dependencies import Input, Output
import dash_table
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd

# df = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/gapminder2007.csv')
df = pd.read_json("test3/ParsedLogs/MouseClicks.JSON")

############################

available_indicators = df['start'].unique()

# for i in range(len(df)):
#     available_indicators = df.loc[i,'start']
                
dropdownsystem = html.Div([
    dcc.Dropdown(id='my-dropdown',
    options=[{'label': i, 'value': i} for i in available_indicators],
    value='')
    # dash_table.DataTable(
    #     id='datatable-interactivity')
])

####################


app = dash.Dash(__name__)

app.layout = html.Div([
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
            # style_cell={
            # 'minWidth': '0px',
            # 'maxWidth': '180px',
            # 'whiteSpace': 'no-wrap',
            # 'overflow': 'hidden',
            # 'textOverflow': 'ellipsis'},
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

@app.callback(
    Output('datatable-interactivity', 'style_data_conditional'),
    [Input('datatable-interactivity', 'selected_columns')]
)
def update_styles(selected_columns):
    return [{
        'if': { 'column_id': i },
        'background_color': '#D2F3FF'
    } for i in selected_columns]

@app.callback(
    Output('datatable-interactivity-container', "children"),
    [Input('datatable-interactivity', "derived_virtual_data"),
     Input('datatable-interactivity', "derived_virtual_selected_rows")])


##########TEST dropdown############
# @app.callback(Output('datatable-interactivity', 'selected_rows'), [Input('my-dropdown', 'value')])
# def update_rows(selected_value):
#     dff = df[df[‘Number of Solar Plants’] == selected_value]
#     return dff.to_dict(‘records’)



############################



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