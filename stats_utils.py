from datetime import date, datetime
from dateutil.relativedelta import relativedelta
from sql_utils import sql_utils as sql
import pandas as pd
import numpy as np

class stats_utils:
    def today(tariff, region, direction="Import"):
        if direction == "Import":
            table = "ElectricityImport"
        else:
            table = "ElectricityExport"

        df = sql.query(f"SELECT * FROM {table} WHERE tariff = '{tariff}' AND region_code = '{region}' AND date >= '{date.today()}'")

        df_all = pd.DataFrame([round(df['unit_rate'].mean(), 2), df['unit_rate'].median(), df['unit_rate'].min(), df['unit_rate'].max()])
        df_all.columns=["Today's Stats (p/KWh)"]
        df_all = df_all.T
        df_all = df_all.reset_index()
        df_all.columns=['', 'Average', 'Median', 'Min', 'Max']
        df_all[' '] = '  '
        df_all['  '] = '  '
        df_all['   '] = '  '

        return df_all.to_dict('records')
    
    def cheapest_time(direction, region, period):
        # find the time period with the cheapest average unit cost or highest for export
        if direction == "Import":
            table = "ElectricityImport"
        else:
            table = "ElectricityExport"

        df = sql.query(f"SELECT * FROM {table} WHERE tariff = 'A' AND region_code = '{region}' AND date >= '{datetime.now()}'")
        i = 0
        j = period

        if direction == "Import":
            average = 100
            while j < len(df):
                if df['unit_rate'][i:j].mean() < average:
                    average = df['unit_rate'][i:j].mean()
                    i_ = i
                    j_ = j
                i += 1
                j += 1
        else:
            average = 0
            while j < len(df):
                if df['unit_rate'][i:j].mean() > average:
                    average = df['unit_rate'][i:j].mean()
                    i_ = i
                    j_ = j
                i += 1
                j += 1

        end = df[i_:j_]['date'].max() + relativedelta(minutes=30)

        df2 = pd.DataFrame([df[i_:j_]['date'].min().strftime('%d-%m-%Y %H:%M'), end.strftime('%d-%m-%Y %H:%M'), round(average, 2)]).T
        df2.columns = ['Start time', 'End time', 'Average unit rate (p/KWh)']
        
        return df2.to_dict('records')
