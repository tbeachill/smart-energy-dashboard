from datetime import date, datetime
from dateutil.relativedelta import relativedelta
from sql_utils import sql_utils as sql
import pandas as pd

class stats_utils:
    def today(tariff, region, direction="Import"):
        if direction == "Import":
            table = "ElectricityImport"
        else:
            table = "ElectricityExport"

        df = sql.query(f"SELECT * FROM {table} WHERE tariff = '{tariff}' AND region_code = '{region}' AND date >= '{date.today()}'")

        df_all = pd.DataFrame([df['unit_rate'].mean(), df['unit_rate'].median(), df['unit_rate'].min(), df['unit_rate'].max()])
        df_all.columns=["Today's Stats"]
        df_all = df_all.T
        df_all = df_all.reset_index()
        df_all.columns=['', 'Average', 'Median', 'Min', 'Max']

        return df_all.to_dict('records')
