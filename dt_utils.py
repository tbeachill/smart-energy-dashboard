from datetime import date, datetime
from dateutil.relativedelta import relativedelta
import pytz

tz_utc = pytz.timezone('UTC')

class dt_utils:
    def get_times():
        return [datetime.now(), date.today() - relativedelta(days=1)]
    
    def get_period(tariff):
        match tariff:
            case "A":
                return dt_utils.period_30m()
            case "T":
                return datetime.now().strftime("%Y-%m-%d")
            case "G":
                return dt_utils.period_go()
            case "C":
                return dt_utils.period_cosy()
            case "F":
                return dt_utils.period_flux()
            case "I":
                return dt_utils.period_intel()
    
    def period_30m():
        dt_now = datetime.now()
        return dt_now.astimezone(tz_utc) - relativedelta(minutes=(dt_now.minute % 30), seconds=dt_now.second, microseconds=dt_now.microsecond)
    
    def period_go():
        dt_now, dt_yday = dt_utils.get_times()

        times = [datetime.strptime('03:30', "%H:%M").time(), datetime.strptime('23:30', "%H:%M").time()]
        if dt_now.time() < times[0]:
            return dt_yday.strftime("%Y-%m-%d") + " 23:30"
        elif dt_now.time() < times[1]:
            return dt_now.strftime("%Y-%m-%d") + " 03:30"
        else:
            return dt_now.strftime("%Y-%m-%d") + " 23:30"
        
    def period_cosy():
        dt_now, dt_yday = dt_utils.get_times()
    
        times = [datetime.strptime('03:00', "%H:%M").time(), datetime.strptime('06:00', "%H:%M").time(), datetime.strptime('12:00', "%H:%M").time(), datetime.strptime('15:00', "%H:%M").time(), datetime.strptime('18:00', "%H:%M").time()]
        if dt_now.time() < times[0]:
            return dt_yday.strftime("%Y-%m-%d") + " 18:00"
        elif dt_now.time() < times[1]:
            return dt_now.strftime("%Y-%m-%d") + " 03:00"
        elif dt_now.time() < times[2]:
            return dt_now.strftime("%Y-%m-%d") + " 06:00"
        elif dt_now.time() < times[3]:
            return dt_now.strftime("%Y-%m-%d") + " 12:00"
        elif dt_now.time() < times[4]:
            return dt_now.strftime("%Y-%m-%d") + " 15:00"
        else:
            return dt_now.strftime("%Y-%m-%d") + " 18:00"
        
    def period_flux():
        dt_now, dt_yday = dt_utils.get_times()
    
        times = [datetime.strptime('01:00', "%H:%M").time(), datetime.strptime('04:00', "%H:%M").time(), datetime.strptime('15:00', "%H:%M").time(), datetime.strptime('18:00', "%H:%M").time()]
        if dt_now.time() < times[0]:
            return dt_yday.strftime("%Y-%m-%d") + " 18:00"
        elif dt_now.time() < times[1]:
            return dt_now.strftime("%Y-%m-%d") + " 01:00"
        elif dt_now.time() < times[2]:
            return dt_now.strftime("%Y-%m-%d") + " 04:00"
        elif dt_now.time() < times[3]:
            return dt_now.strftime("%Y-%m-%d") + " 15:00"
        else:
            return dt_now.strftime("%Y-%m-%d") + " 18:00"
        
    def period_intel():
        dt_now, dt_yday = dt_utils.get_times()
    
        times = [datetime.strptime('04:30', "%H:%M").time(), datetime.strptime('22:30', "%H:%M").time()]
        if dt_now.time() < times[0]:
            return dt_yday.strftime("%Y-%m-%d") + " 22:30"
        elif dt_now.time() < times[1]:
            return dt_now.strftime("%Y-%m-%d") + " 04:30"
        else:
            return dt_now.strftime("%Y-%m-%d") + " 22:30"
