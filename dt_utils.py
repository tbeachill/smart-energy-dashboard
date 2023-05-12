from datetime import date, datetime
from dateutil.relativedelta import relativedelta
import pytz

tz_utc = pytz.timezone('UTC')

class dt_utils:
    def get_times():
        return [datetime.utcnow(), date.today() - relativedelta(days=1)]
    
    def get_period(tariff):
        match tariff:
            case "A":
                return dt_utils.period_30m()
            case "T":
                return datetime.utcnow().date()
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
        return dt_now - relativedelta(hours=1, minutes=(dt_now.minute % 30),
                                      seconds=dt_now.second, microseconds=dt_now.microsecond)
    
    def period_go():
        dt_now, dt_yday = dt_utils.get_times()

        times = [datetime.strptime('03:30', "%H:%M").time(), datetime.strptime('23:30', "%H:%M").time()]
        if dt_now.time() < times[0]:
            return datetime(dt_yday.year, dt_yday.month, dt_yday.day, 23, 30, 0)
        elif dt_now.time() < times[1]:
            return datetime(dt_now.year, dt_now.month, dt_now.day, 3, 30, 0)
        else:
            return datetime(dt_now.year, dt_now.month, dt_now.day, 23, 30, 0)
        
    def period_cosy():
        dt_now, dt_yday = dt_utils.get_times()
    
        times = [datetime.strptime('03:00', "%H:%M").time(), datetime.strptime('06:00', "%H:%M").time(),
                 datetime.strptime('12:00', "%H:%M").time(), datetime.strptime('15:00', "%H:%M").time(),
                 datetime.strptime('18:00', "%H:%M").time()]
        if dt_now.time() < times[0]:
            return datetime(dt_yday.year, dt_yday.month, dt_yday.day, 18, 0, 0)
        elif dt_now.time() < times[1]:
            return datetime(dt_now.year, dt_now.month, dt_now.day, 3, 0, 0)
        elif dt_now.time() < times[2]:
            return datetime(dt_now.year, dt_now.month, dt_now.day, 6, 0, 0)
        elif dt_now.time() < times[3]:
            return datetime(dt_now.year, dt_now.month, dt_now.day, 12, 0, 0)
        elif dt_now.time() < times[4]:
            return datetime(dt_now.year, dt_now.month, dt_now.day, 15, 0, 0)
        else:
            return datetime(dt_now.year, dt_now.month, dt_now.day, 18, 0, 0)
        
    def period_flux():
        dt_now, dt_yday = dt_utils.get_times()
    
        times = [datetime.strptime('01:00', "%H:%M").time(), datetime.strptime('04:00', "%H:%M").time(),
                 datetime.strptime('15:00', "%H:%M").time(), datetime.strptime('18:00', "%H:%M").time()]
        if dt_now.time() < times[0]:
            return datetime(dt_yday.year, dt_yday.month, dt_yday.day, 18, 0, 0)
        elif dt_now.time() < times[1]:
            return datetime(dt_now.year, dt_now.month, dt_now.day, 1, 0, 0)
        elif dt_now.time() < times[2]:
            return datetime(dt_now.year, dt_now.month, dt_now.day, 4, 0, 0)
        elif dt_now.time() < times[3]:
            return datetime(dt_now.year, dt_now.month, dt_now.day, 15, 0, 0)
        else:
            return datetime(dt_now.year, dt_now.month, dt_now.day, 18, 0, 0)
        
    def period_intel():
        dt_now, dt_yday = dt_utils.get_times()
    
        times = [datetime.strptime('04:30', "%H:%M").time(), datetime.strptime('22:30', "%H:%M").time()]
        if dt_now.time() < times[0]:
            return datetime(dt_yday.year, dt_yday.month, dt_yday.day, 22, 30, 0)
        elif dt_now.time() < times[1]:
            return datetime(dt_now.year, dt_now.month, dt_now.day, 4, 30, 0)
        else:
            return datetime(dt_now.year, dt_now.month, dt_now.day, 22, 30, 0)
