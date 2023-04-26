from dash import Dash, html, dash_table
import os
from sqlalchemy import create_engine, text
from dotenv import load_dotenv
import pandas as pd

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

# App layout
app.layout = html.Div([
    html.Div(children='My First App with Data'),
    dash_table.DataTable(data=sql_query("SELECT * FROM StandingCharges").to_dict('records'), page_size=10)
])

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
