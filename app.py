from dash import Dash, html, dcc
from callbacks import get_callbacks
from const import *
from sql_utils import sql_utils as sql
import dash_bootstrap_components as dbc
from style import *

# Initialize the app
app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP], suppress_callback_exceptions=True)
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
        dcc.Tab(label='Agile',       style=tab_style, selected_style=selected_tab_style, value='A', id='A', disabled=True),
        dcc.Tab(label='Tracker',     style=tab_style, selected_style=selected_tab_style, value='T', id='T', disabled=True),
        dcc.Tab(label='Go',          style=tab_style, selected_style=selected_tab_style, value='G', id='G', disabled=True),
        dcc.Tab(label='Cosy',        style=tab_style, selected_style=selected_tab_style, value='C', id='C', disabled=True),
        dcc.Tab(label='Flux',        style=tab_style, selected_style=selected_tab_style, value='F', id='F', disabled=True),
        dcc.Tab(label='Intelligent', style=tab_style, selected_style=selected_tab_style, value='I', id='I', disabled=True),
    ], style=tabs_styles_hidden),
    html.H2(id="intro", hidden=False, children="Welcome. Select a region from the dropdown at the top to get started.", style={'color': colors['text'], 'textAlign' : 'center'}),
    html.Div(id='card-row', style=card_row_style),
    html.Div(id="tab-content"),
])

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
