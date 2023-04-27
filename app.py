from dash import Dash, html, dash_table, dcc, Input, Output
from dash.exceptions import PreventUpdate
import os
from sqlalchemy import create_engine, text
from dotenv import load_dotenv
import pandas as pd
import plotly.express as px
from datetime import date
from dateutil.relativedelta import relativedelta
import dash_bootstrap_components as dbc

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

def sql_query(query):
    # take in a sql query and return the result as a pandas dataframe
    with engine.connect() as conn:
        return pd.read_sql_query(text(query), conn)

# Initialize the app
app = Dash(__name__)

colors = {
    'background': '#111111',
    'text': '#7FDBFF'
}

# date 6 months in the past
date_6m = date.today() - relativedelta(months=6)

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
        searchable=False
    ),
    dcc.Tabs(id="tariff-tabs", children=[
        dcc.Tab(label='Agile', value='A'),
        dcc.Tab(label='Tracker', value='T'),
        dcc.Tab(label='Go', value='G'),
        dcc.Tab(label='Cosy', value='C'),
        dcc.Tab(label='Flux', value='F'),
        dcc.Tab(label='Intelligent', value='I'),
    ]),
    html.Div(id="tab-content")
])

@app.callback(Output('tab-content', 'children'),
              Input('tariff-tabs', 'value'))
def render_content(tab):
    if tab == 'A':
        return html.Div([dbc.Card(id='sc-card'),
                        dash_table.DataTable(data=sql_query("SELECT * FROM StandingCharges").to_dict('records'), page_size=10),
                        dcc.Graph(figure=px.histogram(sql_query("SELECT * FROM ElectricityImport WHERE tariff = 'A' AND region_code = 'M' AND date > '" + date_6m.strftime("%Y-%m-%d") + "'").to_dict('records'), x='date', y='unit_rate', histfunc='avg'))
                ])
    if tab == 'T':
        return html.Div([dbc.Card(id='sc-card'),
                        dash_table.DataTable(data=sql_query("SELECT * FROM StandingCharges").to_dict('records'), page_size=10),
                        dcc.Graph(figure=px.histogram(sql_query("SELECT * FROM ElectricityImport WHERE tariff = 'T' AND region_code = 'M' AND date > '" + date_6m.strftime("%Y-%m-%d") + "'").to_dict('records'), x='date', y='unit_rate', histfunc='avg'))
                ])
    if tab == 'G':
        return html.Div([dbc.Card(id='sc-card'),
                        dash_table.DataTable(data=sql_query("SELECT * FROM StandingCharges").to_dict('records'), page_size=10),
                        dcc.Graph(figure=px.histogram(sql_query("SELECT * FROM ElectricityImport WHERE tariff = 'G' AND region_code = 'M' AND date > '" + date_6m.strftime("%Y-%m-%d") + "'").to_dict('records'), x='date', y='unit_rate', histfunc='avg'))
                ])
    if tab == 'C':
        return html.Div([dbc.Card(id='sc-card'),
                        dash_table.DataTable(data=sql_query("SELECT * FROM StandingCharges").to_dict('records'), page_size=10),
                        dcc.Graph(figure=px.histogram(sql_query("SELECT * FROM ElectricityImport WHERE tariff = 'C' AND region_code = 'M' AND date > '" + date_6m.strftime("%Y-%m-%d") + "'").to_dict('records'), x='date', y='unit_rate', histfunc='avg'))
                ])
    if tab == 'F':
        return html.Div([dbc.Card(id='sc-card'),
                        dash_table.DataTable(data=sql_query("SELECT * FROM StandingCharges").to_dict('records'), page_size=10),
                        dcc.Graph(figure=px.histogram(sql_query("SELECT * FROM ElectricityImport WHERE tariff = 'F' AND region_code = 'M' AND date > '" + date_6m.strftime("%Y-%m-%d") + "'").to_dict('records'), x='date', y='unit_rate', histfunc='avg'))
                ])
    if tab == 'I':
        return html.Div([dbc.Card(id='sc-card'),
                        dash_table.DataTable(data=sql_query("SELECT * FROM StandingCharges").to_dict('records'), page_size=10),
                        dcc.Graph(figure=px.histogram(sql_query("SELECT * FROM ElectricityImport WHERE tariff = 'I' AND region_code = 'M' AND date > '" + date_6m.strftime("%Y-%m-%d") + "'").to_dict('records'), x='date', y='unit_rate', histfunc='avg'))
                ])

@app.callback(
    Output("sc-card", "children"),
    [Input("region-dropdown", "value"), Input("tariff-tabs", "value")]
)
def update_options(region, tariff):
    if not region:
        raise PreventUpdate

    return sc_card(tariff, region)

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
