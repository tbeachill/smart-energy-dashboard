from dash import Dash, html, dash_table, dcc
import os
from sqlalchemy import create_engine, text
from dotenv import load_dotenv
import pandas as pd
import plotly.express as px
from datetime import date
from dateutil.relativedelta import relativedelta
import dash_bootstrap_components as dbc

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
def sc_card(tariff):
    card = dbc.Card(
        dbc.CardBody(
            [
                html.H3("Standing Charge", className="card-title"),
                html.H2(str(sql_query(f"SELECT cost FROM StandingCharges WHERE tariff = '{tariff}' AND region_code = 'M' AND type = 'E'")['cost'][0]) + "p", className="card-subtitle"),
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
    dcc.Tabs([
            dcc.Tab(label='Agile', children=[
                sc_card("A"),
                dash_table.DataTable(data=sql_query("SELECT * FROM StandingCharges").to_dict('records'), page_size=10),
                dcc.Graph(figure=px.histogram(sql_query("SELECT * FROM ElectricityImport WHERE tariff = 'A' AND region_code = 'M' AND date > '" + date_6m.strftime("%Y-%m-%d") + "'").to_dict('records'), x='date', y='unit_rate', histfunc='avg'))
            ]),
            dcc.Tab(label='Tracker', children=[
                sc_card("T"),
                dash_table.DataTable(data=sql_query("SELECT * FROM StandingCharges").to_dict('records'), page_size=10),
                dcc.Graph(figure=px.histogram(sql_query("SELECT * FROM ElectricityImport WHERE tariff = 'T' AND region_code = 'M' AND date > '" + date_6m.strftime("%Y-%m-%d") + "'").to_dict('records'), x='date', y='unit_rate', histfunc='avg'))
            ]),
                dcc.Tab(label='Go', children=[
                sc_card("G"),
                dash_table.DataTable(data=sql_query("SELECT * FROM StandingCharges").to_dict('records'), page_size=10),
                dcc.Graph(figure=px.histogram(sql_query("SELECT * FROM ElectricityImport WHERE tariff = 'G' AND region_code = 'M' AND date > '" + date_6m.strftime("%Y-%m-%d") + "'").to_dict('records'), x='date', y='unit_rate', histfunc='avg'))
            ]),
                dcc.Tab(label='Cosy', children=[
                sc_card("C"),
                dash_table.DataTable(data=sql_query("SELECT * FROM StandingCharges").to_dict('records'), page_size=10),
                dcc.Graph(figure=px.histogram(sql_query("SELECT * FROM ElectricityImport WHERE tariff = 'C' AND region_code = 'M' AND date > '" + date_6m.strftime("%Y-%m-%d") + "'").to_dict('records'), x='date', y='unit_rate', histfunc='avg'))
            ]),
                dcc.Tab(label='Flux', children=[
                sc_card("F"),
                dash_table.DataTable(data=sql_query("SELECT * FROM StandingCharges").to_dict('records'), page_size=10),
                dcc.Graph(figure=px.histogram(sql_query("SELECT * FROM ElectricityImport WHERE tariff = 'F' AND region_code = 'M' AND date > '" + date_6m.strftime("%Y-%m-%d") + "'").to_dict('records'), x='date', y='unit_rate', histfunc='avg'))
            ]),
                dcc.Tab(label='Intelligent', children=[
                sc_card("I"),
                dash_table.DataTable(data=sql_query("SELECT * FROM StandingCharges").to_dict('records'), page_size=10),
                dcc.Graph(figure=px.histogram(sql_query("SELECT * FROM ElectricityImport WHERE tariff = 'I' AND region_code = 'M' AND date > '" + date_6m.strftime("%Y-%m-%d") + "'").to_dict('records'), x='date', y='unit_rate', histfunc='avg'))
            ]),
    ])
])

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
