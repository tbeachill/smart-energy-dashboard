import plotly.express as px
from sql_utils import sql_utils as sql
import pandas as pd
from datetime import date, datetime
from dateutil.relativedelta import relativedelta
from const import *
from style import *


class graph_utils():
    def addition(df, tariff, region):
        deet = df.loc[df['legend'] == "current time"]['Unit Rate (p/KWh)'].values[0]
        row = {'Date':date.today() + relativedelta(days=1), 'tariff':tariff, 'region_code':region, 'Unit Rate (p/KWh)':deet}
        new_df = pd.DataFrame([row])
        df = pd.concat([df, new_df], axis=0, ignore_index=True)
        df['Date'] = pd.to_datetime(df['Date'])

        return df
    
    def price(tariff, region, start_date, end_date, direction="Import", type="Electricity"):
        if direction == "Import":
            hline = sql.query(f"SELECT unit_rate FROM ElectricityImport WHERE tariff = 'V' AND region_code = '{region}'")['unit_rate'][0]
            table = "ElectricityImport"
        else:
            hline = 15
            table = "ElectricityExport"

        if type == "Gas":
            hline = sql.query(f"SELECT unit_rate FROM GasImport WHERE tariff = 'V' AND region_code = '{region}'")['unit_rate'][0]
            table = "GasImport"

        if tariff == "T":
            t_convert = False
        else:
            t_convert = True

        df = sql.query(f"SELECT * FROM {table} WHERE tariff = '{tariff}' AND region_code = '{region}' AND date >= '{start_date}' AND date <= '{end_date}'", t_convert=t_convert)
        df.rename({'date': 'Date', 'unit_rate': 'Unit Rate (p/KWh)'}, axis=1, inplace=True)

        if tariff == "T" or tariff == "G":
            if datetime.utcnow().time() > datetime.strptime('00:15', "%H:%M").time():
                df = graph_utils.addition(df, tariff, region)

        figure=px.line(df, x='Date', y='Unit Rate (p/KWh)', line_shape='hv', template=template)
        figure.add_hline(y=hline)
        figure.add_vline(datetime.now())

        if tariff == "T" or tariff == "G":
            df = df[:-1]
        if tariff != 'T':
            df['Date'] = df['Date'].dt.strftime('%d-%m-%Y %H:%M')
        else:
            df['Date'] = df['Date'].dt.strftime('%d-%m-%Y')

        return [figure, df[['Date', 'Unit Rate (p/KWh)', 'legend']].to_dict('records')]
    
    def dist(tariff, region, start_date, end_date, direction="Import", type="Electricity"):
        if type == "Electricity":
            if direction == "Import":
                bins = [-100,0,3,5,7,10,15,20,25,30,35,40,50,100]
                labels = ['<0p', '<3p', '<5p', '<7p', '<10p', '<15p', '<20p', '<25p', '<30p', '<35p', '<40p', '<50p', '>50p']
                table = "ElectricityImport"
            else:
                bins=[0,3,5,7,10,15,20,25,30,35,40,50,100,1000]
                labels = ['<3p', '<5p', '<7p', '<10p', '<15p', '<20p', '<25p', '<30p', '<35p', '<40p', '<50p', '<100p', '>100p']
                table = "ElectricityExport"
        else:
            bins=[0,2,4,6,8,10,12,14,16,18,20,22,100]
            labels = ['<2p', '<4p', '<6p', '<8p', '<10p', '<12p', '<14p', '<16p', '<18p', '<20p', '<22p', '>22p']
            table = "GasImport"

        df = sql.query(f"SELECT * FROM {table} WHERE tariff = '{tariff}' AND region_code = '{region}' AND date >= '{start_date}' AND date <= '{end_date}'")

        groups = df.groupby(pd.cut(df.unit_rate, bins, labels=labels))
        group_df = pd.DataFrame(groups.unit_rate.count())
        group_df.columns = ['Count']
        group_df['Unit Rate (p/KWh)'] = labels
        
        figure=px.bar(group_df, x='Unit Rate (p/KWh)', y='Count', color='Unit Rate (p/KWh)', color_discrete_sequence=dist_plot_cmap, template=template)

        return [figure, group_df[['Count']].T.to_dict('records')]
