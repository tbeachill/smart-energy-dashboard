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
    html.Div(id="tab-content"),
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
    if tab == 'A' or tab == 'T':    
        return html.Div([html.Div([dbc.Card(id='sc-card')],style={'width': '32%', 'display': 'inline-block'}), html.Div([dbc.Card(id='current-price-1')],style={'width': '32%', 'display': 'inline-block'}), html.Div([dbc.Card(id='current-price-2')],style={'width': '32%', 'display': 'inline-block'})])
    else:
        return html.Div([html.Div([dbc.Card(id='sc-card')],style={'width': '32%', 'display': 'inline-block'}), html.Div([dbc.Card(id='current-price-1')],style={'width': '32%', 'display': 'inline-block'})])
    
# display content for each tab once selected
@app.callback(Output('tab-content', 'children'),
              [Input('tariff-tabs', 'value'), Input("region-dropdown", "value")])
def render_content(tab, region):
    if tab == 'A':
        return html.Div([                        
                        dcc.RadioItems(['Import', 'Export'], 'Import', id='impex', inline=True),
                        dcc.DatePickerRange(
                            id='datepicker1',
                            display_format='DD/MM/YYYY',
                            min_date_allowed=date(2022, 12, 1),
                            max_date_allowed=date(date_today.year, date_today.month, date_today.day),
                            initial_visible_month=date(date_today.year, date_today.month - 1, 1),
                            start_date=date_today - relativedelta(days=1),
                            end_date=date_today + relativedelta(days=1)
                        ),
                        dcc.Graph(id='im-ex'),
                        dcc.Graph(id='agile-dist'),
                        dash_table.DataTable(id='table-a-dist'),
                        dash_table.DataTable(id='table-a', hidden_columns=['legend'], style_data_conditional=[
                            {
                                'if': {
                                    'filter_query': '{legend} eq "current time"'
                                },
                                'backgroundColor': 'green',
                            },
                        ])
                    ])
    if tab == 'T':
        return html.Div([
                        dcc.RadioItems(['Electricity', 'Gas'], 'Electricity', id='energy-type', inline=True),
                        dcc.DatePickerRange(
                            id='datepicker2',
                            display_format='DD/MM/YYYY',
                            min_date_allowed=date(2022, 12, 1),
                            max_date_allowed=date(date_today.year, date_today.month, date_today.day),
                            initial_visible_month=date(date_today.year, date_today.month - 1, 1),
                            start_date=date_today - relativedelta(months=1),
                            end_date=date_today + relativedelta(days=1)
                        ),
                        dcc.Graph(id='gas-elec'),
                        dcc.Graph(id='tracker-dist'),
                        dash_table.DataTable(id='table-t-dist'),
                        dash_table.DataTable(id='table-t', hidden_columns=['legend'], style_data_conditional=[
                            {
                                'if': {
                                    'filter_query': '{legend} eq "current time"'
                                },
                                'backgroundColor': 'green',
                            },
                        ])
                ])
    if tab == 'G':
        return html.Div([
                        dash_table.DataTable(data=sql_query("SELECT * FROM StandingCharges").to_dict('records'), page_size=10),
                        dcc.Graph(figure=px.histogram(sql_query(f"SELECT * FROM ElectricityImport WHERE tariff = 'G' AND region_code = '{region}' AND date > '" + date_6m.strftime("%Y-%m-%d") + "'").to_dict('records'), x='date', y='unit_rate', histfunc='avg'))
                ])
    if tab == 'C':
        return html.Div([
                        dash_table.DataTable(data=sql_query("SELECT * FROM StandingCharges").to_dict('records'), page_size=10),
                        dcc.Graph(figure=px.histogram(sql_query(f"SELECT * FROM ElectricityImport WHERE tariff = 'C' AND region_code = '{region}' AND date > '" + date_6m.strftime("%Y-%m-%d") + "'").to_dict('records'), x='date', y='unit_rate', histfunc='avg'))
                ])
    if tab == 'F':
        return html.Div([
                        dash_table.DataTable(data=sql_query("SELECT * FROM StandingCharges").to_dict('records'), page_size=10),
                        dcc.Graph(figure=px.histogram(sql_query(f"SELECT * FROM ElectricityImport WHERE tariff = 'F' AND region_code = '{region}' AND date > '" + date_6m.strftime("%Y-%m-%d") + "'").to_dict('records'), x='date', y='unit_rate', histfunc='avg'))
                ])
    if tab == 'I':
        return html.Div([
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
    Output("current-price-1", "children"),
    [Input("region-dropdown", "value"), Input("tariff-tabs", "value")]
)
def current_price_card(region, tariff):
    if not region:
        raise PreventUpdate
    
    match tariff:
        case "T":
            title_1 = "Current Electricity Cost"
            date_query = f"= '{date_today}'"
        case "A":
            title_1 = "Current Import"
            date_query = f"= '{date_now.astimezone(tz_utc) - relativedelta(minutes=(date_now.minute % 30), seconds=date_now.second, microseconds=date_now.microsecond)}'"
        case "G":
            title_1 = "Current Import"
            times = [datetime.strptime('03:30', "%H:%M").time(), datetime.strptime('23:30', "%H:%M").time()]
            if date_now.time() < times[0]:
                date_query = "= '" + date_yday.strftime("%Y-%m-%d") + " 23:30'"
            elif date_now.time() < times[1]:
                date_query = "= '" + date_now.strftime("%Y-%m-%d") + " 03:30'"
            else:
                date_query = "= '" + date_now.strftime("%Y-%m-%d") + " 23:30'"
        case "C": # 3 6 12 15 18
            title_1 = "Current Import"
            times = [datetime.strptime('03:00', "%H:%M").time(), datetime.strptime('06:00', "%H:%M").time(), datetime.strptime('12:00', "%H:%M").time(), datetime.strptime('15:00', "%H:%M").time(), datetime.strptime('18:00', "%H:%M").time()]
            if date_now.time() < times[0]:
                date_query = "= '" + date_yday.strftime("%Y-%m-%d") + " 18:00'"
            elif date_now.time() < times[1]:
                date_query = "= '" + date_now.strftime("%Y-%m-%d") + " 03:00'"
            elif date_now.time() < times[2]:
                date_query = "= '" + date_now.strftime("%Y-%m-%d") + " 06:00'"
            elif date_now.time() < times[3]:
                date_query = "= '" + date_now.strftime("%Y-%m-%d") + " 12:00'"
            elif date_now.time() < times[4]:
                date_query = "= '" + date_now.strftime("%Y-%m-%d") + " 15:00'"
            else:
                date_query = "= '" + date_now.strftime("%Y-%m-%d") + " 18:00'"
        case "F": # 1 4 15 18
            title_1 = "Current Import"
            times = [datetime.strptime('01:00', "%H:%M").time(), datetime.strptime('04:00', "%H:%M").time(), datetime.strptime('15:00', "%H:%M").time(), datetime.strptime('18:00', "%H:%M").time()]
            if date_now.time() < times[0]:
                date_query = "= '" + date_yday.strftime("%Y-%m-%d") + " 18:00'"
            elif date_now.time() < times[1]:
                date_query = "= '" + date_now.strftime("%Y-%m-%d") + " 01:00'"
            elif date_now.time() < times[2]:
                date_query = "= '" + date_now.strftime("%Y-%m-%d") + " 04:00'"
            elif date_now.time() < times[3]:
                date_query = "= '" + date_now.strftime("%Y-%m-%d") + " 15:00'"
            else:
                date_query = "= '" + date_now.strftime("%Y-%m-%d") + " 18:00'"
        case "I": # 1 4 15 18
            title_1 = "Current Import"
            times = [datetime.strptime('04:30', "%H:%M").time(), datetime.strptime('22:30', "%H:%M").time()]
            if date_now.time() < times[0]:
                date_query = "= '" + date_yday.strftime("%Y-%m-%d") + " 22:30'"
            elif date_now.time() < times[1]:
                date_query = "= '" + date_now.strftime("%Y-%m-%d") + " 04:30'"
            else:
                date_query = "= '" + date_now.strftime("%Y-%m-%d") + " 22:30'"
        
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

    return card_1

# card 3
@app.callback(
    Output("current-price-2", "children"),
    [Input("region-dropdown", "value"), Input("tariff-tabs", "value")]
)
def current_price_card(region, tariff):
    if tariff == "T":
        title_2 = "Current Gas Cost"
        table = "GasImport"
        date_query = f"= '{date_today}'"
    if tariff == "A":
        title_2 = "Current Export"
        table = "ElectricityExport"
        date_query = f"= '{date_now.astimezone(tz_utc) - relativedelta(minutes=(date_now.minute % 30), seconds=date_now.second, microseconds=date_now.microsecond)}'"

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

    return card_2


# return import or export graph based on selection
@app.callback(
    [Output("im-ex", "figure"), Output("table-a", "data")],
    [Input("impex", "value"), Input("region-dropdown", "value"), Input("tariff-tabs", "value"), Input("datepicker1", "start_date"), Input("datepicker1", "end_date")]
)
def change_impex(value, region, tariff, start_date, end_date):
    if value == "Import":
        df = sql_query(f"SELECT * FROM ElectricityImport WHERE tariff = '{tariff}' AND region_code = '{region}' AND date >= '{start_date}' AND date <= '{end_date}'")
        figure=px.bar(df, x='date', y='unit_rate', color='legend')
        figure.add_hline(y=sql_query(f"SELECT unit_rate FROM ElectricityImport WHERE tariff = 'V' AND region_code = '{region}'")['unit_rate'][0])
        
        return [figure, df[['date', 'unit_rate', 'legend']].to_dict('records')]
    else:
        df = sql_query(f"SELECT * FROM ElectricityExport WHERE tariff = '{tariff}' AND region_code = '{region}' AND date >= '{start_date}' AND date <= '{end_date}'")
        figure=px.bar(df, x='date', y='unit_rate', color='legend')
        figure.add_hline(y=15)

        return [figure, df[['date', 'unit_rate', 'legend']].to_dict('records')]
    
# return agile distribution graph based on date selection
@app.callback(
    [Output("agile-dist", "figure"), Output("table-a-dist", "data")],
    [Input("impex", "value"), Input("region-dropdown", "value"), Input("datepicker1", "start_date"), Input("datepicker1", "end_date"), Input("tariff-tabs", "value")]
)
def change_distribution(impex, region, start_date, end_date, tariff):
    if impex == "Import":
        df = sql_query(f"SELECT * FROM ElectricityImport WHERE tariff = '{tariff}' AND region_code = '{region}' AND date >= '{start_date}' AND date <= '{end_date}'")

        bins=[-100,0,3,5,7,10,15,20,25,30,35,40,50,100]
        labels=['<0p', '<3p', '<5p', '<7p', '<10p', '<15p', '<20p', '<25p', '<30p', '<35p', '<40p', '<50p', '>50p']
        groups = df.groupby(pd.cut(df.unit_rate, bins, labels=labels))
        group_df = pd.DataFrame(groups.unit_rate.count())
        group_df.columns = ['count']
        group_df['label'] = labels
        
        figure=px.bar(group_df, x='label', y='count')

        return [figure, group_df[['count']].T.to_dict('records')]
    else:
        df = sql_query(f"SELECT * FROM ElectricityExport WHERE tariff = '{tariff}' AND region_code = '{region}' AND date >= '{start_date}' AND date <= '{end_date}'")
        bins=[0,3,5,7,10,15,20,25,30,35,40,50,100,1000]
        labels=['<3p', '<5p', '<7p', '<10p', '<15p', '<20p', '<25p', '<30p', '<35p', '<40p', '<50p', '<100p', '>100p']
        groups = df.groupby(pd.cut(df.unit_rate, bins, labels=labels))
        group_df = pd.DataFrame(groups.unit_rate.count())
        group_df.columns = ['count']
        group_df['label'] = labels
        
        figure=px.bar(group_df, x='label', y='count')

        return [figure, group_df[['count']].T.to_dict('records')]
    
# return tracker gas or electric graph based on selection
@app.callback(
    [Output("gas-elec", "figure"), Output("table-t", "data")],
    [Input("energy-type", "value"), Input("region-dropdown", "value"), Input("tariff-tabs", "value"), Input("datepicker2", "start_date"), Input("datepicker2", "end_date")]
)
def change_energy(value, region, tariff, start_date, end_date):
    if value == "Electricity":
        df = sql_query(f"SELECT * FROM ElectricityImport WHERE tariff = '{tariff}' AND region_code = '{region}' AND date >= '{start_date}' AND date <= '{end_date}'", t_convert=False)
        figure=px.bar(df, x='date', y='unit_rate', color='legend')
        figure.add_hline(y=sql_query(f"SELECT unit_rate FROM ElectricityImport WHERE tariff = 'V' AND region_code = '{region}'")['unit_rate'][0])

        return [figure, df[['date', 'unit_rate', 'legend']].to_dict('records')]
    else:
        df = sql_query(f"SELECT * FROM GasImport WHERE tariff = '{tariff}' AND region_code = '{region}' AND date >= '{start_date}' AND date <= '{end_date}'", t_convert=False)
        figure=px.bar(df, x='date', y='unit_rate', color='legend')
        figure.add_hline(y=sql_query(f"SELECT unit_rate FROM GasImport WHERE tariff = 'V' AND region_code = '{region}'")['unit_rate'][0])

        return [figure, df[['date', 'unit_rate', 'legend']].to_dict('records')]

# return tracker distribution graph based on date selection
@app.callback(
    [Output("tracker-dist", "figure"), Output("table-t-dist", "data")],
    [Input("energy-type", "value"), Input("region-dropdown", "value"), Input("datepicker2", "start_date"), Input("datepicker2", "end_date"), Input("tariff-tabs", "value")]
)
def change_distribution(energy_type, region, start_date, end_date, tariff):
    if energy_type == "Electricity":
        df = sql_query(f"SELECT * FROM ElectricityImport WHERE tariff = '{tariff}' AND region_code = '{region}' AND date >= '{start_date}' AND date <= '{end_date}'")
        bins=[0,3,5,7,10,15,20,25,30,35,40,50,100]
        labels=['<3p', '<5p', '<7p', '<10p', '<15p', '<20p', '<25p', '<30p', '<35p', '<40p', '<50p', '>50p']
        groups = df.groupby(pd.cut(df.unit_rate, bins, labels=labels))
        group_df = pd.DataFrame(groups.unit_rate.count())
        group_df.columns = ['count']
        group_df['label'] = labels
        
        figure=px.bar(group_df, x='label', y='count')

        return [figure, group_df[['count']].T.to_dict('records')]
    else:
        df = sql_query(f"SELECT * FROM GasImport WHERE tariff = '{tariff}' AND region_code = '{region}' AND date >= '{start_date}' AND date <= '{end_date}'")
        bins=[0,2,4,6,8,10,12,14,16,18,20,22,100]
        labels=['<2p', '<4p', '<6p', '<8p', '<10p', '<12p', '<14p', '<16p', '<18p', '<20p', '<22p', '>22p']
        groups = df.groupby(pd.cut(df.unit_rate, bins, labels=labels))
        group_df = pd.DataFrame(groups.unit_rate.count())
        group_df.columns = ['count']
        group_df['label'] = labels
        
        figure=px.bar(group_df, x='label', y='count')

        return [figure, group_df[['count']].T.to_dict('records')]

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
