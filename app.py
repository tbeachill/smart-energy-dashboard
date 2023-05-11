from dash import html, dash_table, dcc, Dash
from callbacks import get_callbacks
from const import *
import dash_bootstrap_components as dbc
from style import *
from sql_utils import sql_utils as sql
from datetime import date
from dateutil.relativedelta import relativedelta

# Initialize the app
dash_app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP], suppress_callback_exceptions=True)
sql.connect()

dash_app.index_string = '''
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

get_callbacks(dash_app)

# App layout
dash_app.layout = html.Div([
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
    
    # tabs
    html.Div(dcc.Tabs([
        dcc.Tab(label='Agile', style=tab_style, selected_style=selected_tab_style, value='A', id='A'),
        dcc.Tab(label='Tracker', style=tab_style, selected_style=selected_tab_style, value='T', id='T'),
        dcc.Tab(label='Go', style=tab_style, selected_style=selected_tab_style, value='G', id='G'),
        dcc.Tab(label='Cosy', style=tab_style, selected_style=selected_tab_style, value='C', id='C'),
        dcc.Tab(label='Flux', style=tab_style, selected_style=selected_tab_style, value='F', id='F'),
        dcc.Tab(label='Intelligent', style=tab_style, selected_style=selected_tab_style, value='I', id='I'),
    ], style=tab_row_style, id="tabs"), hidden=True, id="tariff-tab-div",),
    
    # intro
    html.H2(id="intro", hidden=False, children=intro_text, style={'color': colors['text'], 'textAlign' : 'center'}),
    html.Div(id="intro2", hidden=False, children=intro_text_2, style={'color': colors['text'],
                                                                      'textAlign' : 'left', 'padding-left':'30px'}),
    
    # cards
    html.Div(dbc.Row([dbc.Col(html.Div(id='join-card')), dbc.Col(html.Div(id='sc-card')),
                      dbc.Col(html.Div(id='card-1')), dbc.Col(html.Div(id='card-2', hidden=True))],
                      style=card_row_style), hidden=True, id="card-row-div"),
    
    # agile today stats
    html.Div(dash_table.DataTable(id='agile-stats-today', style_header=table_style_header,
                                  style_data=table_style_data, style_as_list_view=True),
                                  hidden=True, id="stats-today-tab-div"),
    
    # date / direction / energy type
    html.Div(dbc.Row([                        
        dbc.Col(html.Div(dcc.DatePickerRange(
            id='date-picker',
            display_format='DD/MM/YYYY',
            min_date_allowed=date(2022, 12, 1),
            max_date_allowed=date(date.today().year, date.today().month, date.today().day),
            initial_visible_month=date(date.today().year, date.today().month, 1),
            start_date=date.today() - relativedelta(days=1),
            end_date=date.today() + relativedelta(days=2),
            style=date_picker_style
        ), id="date-picker-div"), width=6),
        dbc.Col(html.Div(dcc.RadioItems(['Import', 'Export'], 'Import', inline=True,
                                        style=radio_style, inputStyle=radio_input_style, id="type-radio"),
                                        id="type-radio-div"), width=6)], justify='between'), hidden=True,
                                        id='date-direction-div'),
    
    # price graph
    html.Div(dcc.Graph(id='price-plot'), hidden=True, id="price-plot-div"),
    
    # best time calculator
    html.Div(dbc.Row([dbc.Col(html.Div(children='Select a time period to find the cheapest import or \
                                       highest export period (import or export are selected at the top-right)',
                                       style=title_style))]), hidden=True, id="price-calculator-title-div"),
    html.Div(dbc.Row([dbc.Col(dcc.Dropdown([{'label': '0:30', 'value': 1}, {'label': '1:00', 'value': 2},
                                            {'label': '1:30', 'value': 3}, {'label': '2:00', 'value': 4},
                                            {'label': '2:30', 'value': 5}, {'label': '3:00', 'value': 6},
                                            {'label': '3:30', 'value': 7}, {'label': '4:00', 'value': 8},
                                            {'label': '4:30', 'value': 9}, {'label': '5:00', 'value': 10},
                                            {'label': '5:30', 'value': 11}, {'label': '6:00', 'value': 12}, ],
                                            '0:30', id='best-dropdown', placeholder="SELECT TIME PERIOD",
                                            style=date_picker_style)),
                dbc.Col(width=1),
                dbc.Col(dash_table.DataTable(id='table-best', style_header=table_style_header,
                                             style_data=table_style_data, style_cell=table_style_cell_cheapest)),
                dbc.Col(width=1)]), hidden=True, id='price-calculator-div'),
    
    # distribution
    html.Div(dcc.Graph(id='dist-plot'), hidden=True, id='dist-plot-div'),
    html.Div(dash_table.DataTable(id='dist-table', style_header=table_style_header,
                                  style_data=table_style_data), hidden=True, id="dist-tab-div"),
    
    # boxplot
    html.Div(dcc.Graph(id='box-plot'), hidden=True, id="box-plot-div"),
    
    # data table
    html.Div(dbc.Row([dbc.Col(),
                dbc.Col(dash_table.DataTable(id='data-table', hidden_columns=['legend'],
                                             style_data=table_style_data, style_data_conditional=table_style_data_conditional,
                                             style_header=table_style_header, style_header_conditional=table_style_header_conditional,
                                             style_cell=table_style_cell, style_cell_conditional=table_style_cell_conditional,
                                             style_as_list_view=True, css=[{"selector": ".show-hide", "rule": "display: none"}])),
                dbc.Col()]), hidden=True, id="data-tab-div"),
    html.Div("This website was created by a satisfied customer and is not affiliated with Octopus Energy.", style=text_style)
])

app = dash_app.server

# Run the app
if __name__ == '__main__':
    dash_app.run(host='0.0.0.0', port='8000')
