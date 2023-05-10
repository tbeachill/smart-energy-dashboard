from dash import Dash, html, dcc
from callbacks import get_callbacks
from const import *
import dash_bootstrap_components as dbc
from style import *

# Initialize the app
app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP], suppress_callback_exceptions=True)

app.index_string = '''
<!DOCTYPE html>
<html>
    <head>
        {%metas%}
        <meta name="description" content="Find out the latest Octopus Energy prices and compare their smart tariffs. Save money by switching to a smart tariff like Agile, Tracker, or Go. View daily tracker prices and half-hourly Octopus Agile rates." />
        <meta name="keywords" content="octopus energy, smart energy, smart meter, smart tariff, agile octopus, octopus go, intelligent octopus, octopus flux, octopus tracker, cosy octopus, referral link, octopus referral code, save money, switch, octopus energy prices, octopus energy rates, octopus energy tariffs, electricity, gas" />
        <link rel="canonical" href="https://smartenergydashboard.co.uk"/>
        <title>Smart Energy Dashboard - Save Money With Smart Tariffs</title>
        {%favicon%}
        {%css%}
    </head>
    <body>
        {%app_entry%}
        <footer>
            {%config%}
            {%scripts%}
            {%renderer%}
        </footer>
    </body>
</html>
'''

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
    dcc.Tabs(id='tariff-tabs', style=tab_row_style),
    html.H2(id="intro", hidden=False, children=intro_text, style={'color': colors['text'], 'textAlign' : 'center'}),
    html.Div(id="intro2", hidden=False, children=intro_text_2, style={'color': colors['text'], 'textAlign' : 'left', 'padding-left':'30px'}),
    dbc.Row(id='card-row', style=card_row_style),
    html.Div(id="tab-content")
])

server = app.server

# Run the app
if __name__ == '__main__':
    app.run(host='0.0.0.0', port='8000')
