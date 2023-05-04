from dash import Dash, html, dcc
import dash_bootstrap_components as dbc
from callbacks import get_callbacks
from const import *
from sql_utils import sql_utils as sql

# Initialize the app
app = Dash(__name__, suppress_callback_exceptions=True)
sql.connect()
get_callbacks(app)

# App layout
app.layout = html.Div([
    html.Div(children='Smart Energy Dashboard', style={
            'textAlign': 'center',
            'color': colors['text']
        }),
    dcc.Dropdown(
        r_codes,
        id='region-dropdown',
        placeholder='REGION',
        searchable=False
    ),
    dcc.Tabs(id="tariff-tabs", children=[
        dcc.Tab(label='Agile', value='A', id='A', disabled=True),
        dcc.Tab(label='Tracker', value='T', id='T', disabled=True),
        dcc.Tab(label='Go', value='G', id='G', disabled=True),
        dcc.Tab(label='Cosy', value='C', id='C', disabled=True),
        dcc.Tab(label='Flux', value='F', id='F', disabled=True),
        dcc.Tab(label='Intelligent', value='I', id='I', disabled=True),
    ]),
    html.H2(id="intro", hidden=False, children="Welcome. Select a region from the dropdown at the top to get started.", style={'color': colors['text'], 'textAlign' : 'center'}),
    html.Div(id='card-row'),
    html.Div(id="tab-content"),
])

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
