from datetime import date, datetime
from dateutil.relativedelta import relativedelta

class stats:
    def date_range(df, start_date, end_date):
        pass

    def monthly(df):
        month_list = []
        month = date.today().month

        i = 6
        while i > 1:
            month = month - relativedelta(months=1)
            month_list.append(month)