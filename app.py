from dash import Dash, html, dash_table, dcc, Input, Output
from dash.exceptions import PreventUpdate
import os
from sqlalchemy import create_engine, text
from dotenv import load_dotenv
import pandas as pd
import plotly.express as px
from datetime import date, datetime
from dateutil.relativedelta import relativedelta
import dash_bootstrap_components as dbc
import pytz
import calendar
import matplotlib

# regions
r_codes = [
    {"label": "East England", "value": 'A'},
    {"label": "East Midlands", "value": 'B'},
    {"label": "London", "value": 'C'},
    {"label": "Merseyside and North Wales", "value": 'D'},
    {"label": "West Midlands", "value": 'E'},
    {"label": "North-East England", "value": 'F'},
    {"label": "North-West England", "value": 'G'},
    {"label": "South England", "value": 'H'},
    {"label": "South-East England", "value": 'J'},
    {"label": "South Wales", "value": 'K'},
    {"label": "South-West England", "value": 'L'},
    {"label": "Yorkshire", "value": 'M'},
    {"label": "South Scotland", "value": 'N'},
    {"label": "North Scotland", "value": 'P'},
]

# set up sql connection
load_dotenv('.env')
server = os.getenv('SQL_SERVER')
database = os.getenv('SQL_DATABASE')
username = os.getenv('SQL_USERNAME')
password = os.getenv('SQL_PASSWORD') 
driver= os.getenv('SQL_DRIVER')
odbc_params = f'DRIVER={driver};SERVER=tcp:{server};PORT=1433;DATABASE={database};UID={username};PWD={password}'
connection_string = f'mssql+pyodbc:///?odbc_connect={odbc_params}'
engine = create_engine(connection_string)

def sql_query(query, no_time=False, t_convert=True):
    # take in a sql query and return the result as a pandas dataframe
    with engine.connect() as conn:
        df = pd.read_sql_query(text(query), conn, dtype_backend='pyarrow')

    if 'date' in df.columns:
        if t_convert:
            df['date'] = pd.DatetimeIndex(df['date']).tz_localize('UTC').tz_convert('Europe/London')
        df['legend'] = ''
        
        if "tariff = 'T'" in query:
            df.loc[df['date'] == date_today, 'legend'] = 'current time'
        else:
            df.loc[df['date'] == date_now_30m, 'legend'] = 'current time'
    
    if no_time:
        df['date'] = df['date'].dt.strftime('%d/%m/%Y')

    return df

# Initialize the app
app = Dash(__name__, suppress_callback_exceptions=True)

colors = {
    'background': '#111111',
    'text': '#7FDBFF'
}

# date 6 months in the past
tz_london = pytz.timezone('Europe/London')
tz_utc = pytz.timezone('UTC')
date_today = date.today()
date_yday = date.today() - relativedelta(days=1)
date_now = datetime.now()
date_now_30m = date_now.astimezone(tz_utc) - relativedelta(minutes=(date_now.minute % 30), seconds=date_now.second, microseconds=date_now.microsecond)
date_6m = date.today() - relativedelta(months=6)
date_48h = date.today() - relativedelta(hours=48)
date_24h = date.today() - relativedelta(hours=24)
date_14d = date.today() - relativedelta(months=1)

# standing charge card
def sc_card(tariff, region):
    card = dbc.Card(
        dbc.CardBody(
            [
                html.H3("Standing Charge", className="card-title"),
                html.H2(str(sql_query(f"SELECT cost FROM StandingCharges WHERE tariff = '{tariff}' AND region_code = '{region}' AND type = 'E'")['cost'][0]) + "p", className="card-subtitle"),
            ]
        ),
        style={"width": "10rem",
            'textAlign': 'center',
                'color': colors['text']},
        className="w-75 mb-3",
    )

    return card

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
    html.Div(id="tab-content")
])

# enable the tariff tabs and remove the intro text once a region has been selected
@app.callback(
    [Output("A", "disabled"), Output("T", "disabled"), Output("G", "disabled"), Output("C", "disabled"), Output("F", "disabled"), Output("I", "disabled"), Output("intro", "hidden")],
    Input('region-dropdown', 'value'),
    prevent_initial_call=True
)
def enable_tab(region):
    return False, False, False, False, False, False, True

@app.callback(Output('card-row', 'children'),
              [Input('tariff-tabs', 'value'), Input("region-dropdown", "value")])
def render_cards(tab, region):
    return html.Div([html.Div([dbc.Card(id='sc-card')],style={'width': '32%', 'display': 'inline-block'}), html.Div([dbc.Card(id='current-price-1')],style={'width': '32%', 'display': 'inline-block'}), html.Div([dbc.Card(id='current-price-2')],style={'width': '32%', 'display': 'inline-block'})])

# display content for each tab once selected
@app.callback(Output('tab-content', 'children'),
              [Input('tariff-tabs', 'value'), Input("region-dropdown", "value")])
def render_content(tab, region):
    if tab == 'A':
        return html.Div([                        
                        dcc.RadioItems(['Import', 'Export'], 'Import', id='impex', inline=True),
                        html.Div(id='im-ex'),
                        dcc.DatePickerRange(
                            id='datepicker',
                            display_format='DD/MM/YYYY',
                            min_date_allowed=date(2022, 12, 1),
                            max_date_allowed=date(date_today.year, date_today.month, date_today.day),
                            initial_visible_month=date(date_today.year, date_today.month - 1, 1),
                            start_date=date(date_today.year, date_today.month - 1, 1),
                            end_date=date(date_today.year, date_today.month - 1, calendar.monthrange(date_today.year, date_today.month - 1)[1])
                        ),
                        html.Div(id='agile-dist'),
                        
                ])
    if tab == 'T':
        return html.Div([
                        dcc.RadioItems(['Electricity', 'Gas'], 'Electricity', id='energy-type', inline=True),
                        html.Div(id='gas-elec'),
                        dcc.DatePickerRange(
                            id='datepicker',
                            display_format='DD/MM/YYYY',
                            min_date_allowed=date(2022, 12, 1),
                            max_date_allowed=date(date_today.year, date_today.month, date_today.day),
                            initial_visible_month=date(date_today.year, date_today.month - 1, 1),
                            start_date=date(date_today.year, date_today.month - 1, 1),
                            end_date=date(date_today.year, date_today.month - 1, calendar.monthrange(date_today.year, date_today.month - 1)[1])
                        ),
                        html.Div(id='tracker-dist'),
                ])
    if tab == 'G':
        return html.Div([dbc.Card(id='sc-card'),
                        dash_table.DataTable(data=sql_query("SELECT * FROM StandingCharges").to_dict('records'), page_size=10),
                        dcc.Graph(figure=px.histogram(sql_query(f"SELECT * FROM ElectricityImport WHERE tariff = 'G' AND region_code = '{region}' AND date > '" + date_6m.strftime("%Y-%m-%d") + "'").to_dict('records'), x='date', y='unit_rate', histfunc='avg'))
                ])
    if tab == 'C':
        return html.Div([dbc.Card(id='sc-card'),
                        dash_table.DataTable(data=sql_query("SELECT * FROM StandingCharges").to_dict('records'), page_size=10),
                        dcc.Graph(figure=px.histogram(sql_query(f"SELECT * FROM ElectricityImport WHERE tariff = 'C' AND region_code = '{region}' AND date > '" + date_6m.strftime("%Y-%m-%d") + "'").to_dict('records'), x='date', y='unit_rate', histfunc='avg'))
                ])
    if tab == 'F':
        return html.Div([dbc.Card(id='sc-card'),
                        dash_table.DataTable(data=sql_query("SELECT * FROM StandingCharges").to_dict('records'), page_size=10),
                        dcc.Graph(figure=px.histogram(sql_query(f"SELECT * FROM ElectricityImport WHERE tariff = 'F' AND region_code = '{region}' AND date > '" + date_6m.strftime("%Y-%m-%d") + "'").to_dict('records'), x='date', y='unit_rate', histfunc='avg'))
                ])
    if tab == 'I':
        return html.Div([dbc.Card(id='sc-card'),
                        dash_table.DataTable(data=sql_query("SELECT * FROM StandingCharges").to_dict('records'), page_size=10),
                        dcc.Graph(figure=px.histogram(sql_query(f"SELECT * FROM ElectricityImport WHERE tariff = 'I' AND region_code = '{region}' AND date > '" + date_6m.strftime("%Y-%m-%d") + "'").to_dict('records'), x='date', y='unit_rate', histfunc='avg'))
                ])


# standing charge card to update with tariff and region
@app.callback(
    Output("sc-card", "children"),
    [Input("region-dropdown", "value"), Input("tariff-tabs", "value")]
)
def update_options(region, tariff):
    if not region:
        raise PreventUpdate
    
    global tabs_disabled
    tabs_disabled = False

    return sc_card(tariff, region)

# current price card
@app.callback(
    [Output("current-price-1", "children"), Output("current-price-2", "children")],
    [Input("region-dropdown", "value"), Input("tariff-tabs", "value")]
)
def current_price_card(region, tariff):
    if not region:
        raise PreventUpdate
    if tariff == "A":
        title_1 = "Current Import"
        title_2 = "Current Export"
        table = "ElectricityExport"
        date_query = f"= '{date_now.astimezone(tz_utc) - relativedelta(minutes=(date_now.minute % 30), seconds=date_now.second, microseconds=date_now.microsecond)}'"
    elif tariff == "T":
        title_1 = "Current Electricity Cost"
        title_2 = "Current Gas Cost"
        table = "GasImport"
        date_query = f"= '{date_today}'"

    card_1 = dbc.Card(
        dbc.CardBody(
            [
                html.H3(title_1, className="card-title"),
                html.H2(str(sql_query(f"SELECT unit_rate FROM ElectricityImport WHERE tariff = '{tariff}' AND region_code = '{region}' AND date {date_query}")['unit_rate'][0]) + "p", className="card-subtitle"),
            ]
        ),
        style={"width": "10rem",
            'textAlign': 'center',
                'color': colors['text']},
        className="w-75 mb-3",
    )

    card_2 = dbc.Card(
        dbc.CardBody(
            [
                html.H3(title_2, className="card-title"),
                html.H2(str(sql_query(f"SELECT unit_rate FROM {table} WHERE tariff = '{tariff}' AND region_code = '{region}' AND date {date_query}")['unit_rate'][0]) + "p", className="card-subtitle"),
            ]
        ),
        style={"width": "10rem",
            'textAlign': 'center',
                'color': colors['text']},
        className="w-75 mb-3",
    )

    return [card_1, card_2]

# return import or export graph based on selection
@app.callback(
    Output("im-ex", "children"),
    [Input("impex", "value"), Input("region-dropdown", "value"), Input("tariff-tabs", "value")]
)
def change_impex(value, region, tariff):
    if value == "Import":
        return dcc.Graph(figure=px.bar(sql_query(f"SELECT * FROM ElectricityImport WHERE tariff = '{tariff}' AND region_code = '{region}' AND date > '" + date_24h.strftime("%Y-%m-%d") + "'").to_dict('records'),
                                                x='date', y='unit_rate', color='legend'))
    else:
        return dcc.Graph(figure=px.bar(sql_query(f"SELECT * FROM ElectricityExport WHERE tariff = '{tariff}' AND region_code = '{region}' AND date > '" + date_24h.strftime("%Y-%m-%d") + "'").to_dict('records'),
                                                x='date', y='unit_rate', color='legend'))
    
# return agile distribution graph based on date selection
@app.callback(
    Output("agile-dist", "children"),
    [Input("impex", "value"), Input("region-dropdown", "value"), Input("datepicker", "start_date"), Input("datepicker", "end_date"), Input("tariff-tabs", "value")]
)
def change_distribution(impex, region, start_date, end_date, tariff):
    if impex == "Import":
        return dcc.Graph(figure=px.histogram(sql_query(f"SELECT * FROM ElectricityImport WHERE tariff = '{tariff}' AND region_code = '{region}' AND date >= '{start_date}' AND date <= '{end_date}'").to_dict('records'),
                                                      x='unit_rate'))
    else:
        return dcc.Graph(figure=px.histogram(sql_query(f"SELECT * FROM ElectricityExport WHERE tariff = '{tariff}' AND region_code = '{region}' AND date >= '{start_date}' AND date <= '{end_date}'").to_dict('records'),
                                                      x='unit_rate'))
    
# return tracker gas or electric graph based on selection
@app.callback(
    Output("gas-elec", "children"),
    [Input("energy-type", "value"), Input("region-dropdown", "value"), Input("tariff-tabs", "value")]
)
def change_energy(value, region, tariff):
    if value == "Electricity":
        return dcc.Graph(figure=px.bar(sql_query(f"SELECT * FROM ElectricityImport WHERE tariff = '{tariff}' AND region_code = '{region}' AND date > '" + date_14d.strftime("%Y-%m-%d") + "'", t_convert=False).to_dict('records'),
                                                x='date', y='unit_rate', color='legend'))
    else:
        return dcc.Graph(figure=px.bar(sql_query(f"SELECT * FROM GasImport WHERE tariff = '{tariff}' AND region_code = '{region}' AND date > '" + date_14d.strftime("%Y-%m-%d") + "'", t_convert=False).to_dict('records'),
                                                x='date', y='unit_rate', color='legend'))

# return tracker distribution graph based on date selection
@app.callback(
    Output("tracker-dist", "children"),
    [Input("energy-type", "value"), Input("region-dropdown", "value"), Input("datepicker", "start_date"), Input("datepicker", "end_date"), Input("tariff-tabs", "value")]
)
def change_distribution(energy_type, region, start_date, end_date, tariff):
    if energy_type == "Electricity":
        return dcc.Graph(figure=px.histogram(sql_query(f"SELECT * FROM ElectricityImport WHERE tariff = '{tariff}' AND region_code = '{region}' AND date >= '{start_date}' AND date <= '{end_date}'").to_dict('records'),
                                                      x='unit_rate'))
    else:
        return dcc.Graph(figure=px.histogram(sql_query(f"SELECT * FROM GasImport WHERE tariff = '{tariff}' AND region_code = '{region}' AND date >= '{start_date}' AND date <= '{end_date}'").to_dict('records'),
                                                      x='unit_rate'))

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
