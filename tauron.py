import datetime
import elicznik
import os

env_var = os.environ

cache = {}


def GetData():
    """
    It allows you to get energy balance of yesterday.

    After getting the data, it will be cached for next time. (To avoid the rate limit)
    """

    yesterday = datetime.date.today() - datetime.timedelta(days=1)

    if str(yesterday.strftime("%Y-%m-%d")) not in cache.keys():
        try:
            with elicznik.ELicznik(env_var['TAURON_USER'], env_var['TAURON_PASS']) as m:

                readings = m.get_readings(yesterday)

                consumed_yest = sum(n[1] for n in readings)
                produced_yest = sum(n[2] for n in readings)

                bilans = round(produced_yest - consumed_yest, 2)

                cache[str(yesterday.strftime("%Y-%m-%d"))] = bilans
                return cache[str(yesterday.strftime("%Y-%m-%d"))], True
        except:
            return 0, False
    else:
        return cache[str(yesterday.strftime("%Y-%m-%d"))], True


def GetDataForSpecifiedDay(day: datetime.date):
    """
    It allows you to get energy balance of specified day.
    """

    if day == datetime.date.today():
        return False, False  # nie dziala :?

    if str(day.strftime("%Y-%m-%d")) not in cache.keys():
        with elicznik.ELicznik(env_var['TAURON_USER'], env_var['TAURON_PASS']) as m:

            readings = m.get_readings(day)

            consumed_yest = sum(n[1] for n in readings)
            produced_yest = sum(n[2] for n in readings)

            bilans = round(produced_yest - consumed_yest, 2)

            cache[str(day.strftime("%Y-%m-%d"))] = bilans
            return cache[str(day.strftime("%Y-%m-%d"))], True
    else:
        return cache[str(day.strftime("%Y-%m-%d"))], True
