from dotenv import load_dotenv
from sqlalchemy import create_engine, text
import os
import pandas as pd
from dt_utils import dt_utils as dt
from datetime import date

class sql_utils:
    def connect():
        load_dotenv('.env')
        server = os.getenv('SQL_SERVER')
        database = os.getenv('SQL_DATABASE')
        username = os.getenv('SQL_USERNAME')
        password = os.getenv('SQL_PASSWORD') 
        driver= os.getenv('SQL_DRIVER')
        odbc_params = f'DRIVER={driver};SERVER=tcp:{server};PORT=1433;DATABASE={database};UID={username};PWD={password}'
        connection_string = f'mssql+pyodbc:///?odbc_connect={odbc_params}'
        
        global engine
        engine = create_engine(connection_string)

    def query(query, no_time=False, t_convert=True):
        # take in a sql query and return the result as a pandas dataframe
        with engine.connect() as conn:
            df = pd.read_sql_query(text(query), conn, dtype_backend='pyarrow')

        if 'date' in df.columns:
            if t_convert:
                df['date'] = pd.DatetimeIndex(df['date']).tz_localize('UTC').tz_convert('Europe/London')
            df['legend'] = ''
            
            if "tariff = 'T'" in query:
                df.loc[df['date'] == date.today(), 'legend'] = 'current time'
            else:
                df.loc[df['date'] == dt.period_30m(), 'legend'] = 'current time'
        
        if no_time:
            df['date'] = df['date'].dt.strftime('%d/%m/%Y')

        return df
