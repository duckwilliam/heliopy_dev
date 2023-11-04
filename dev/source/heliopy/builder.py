import classes.wrapper as wrapper
import datetime

def main(city: str,
         time = None,
         day = None,
         country: str = None,
         timezone: str = None):
    helios = wrapper.SolarMain(city=city,
                               country=country,
                               requested_day=day,
                               requested_hour=time,
                               requested_timezone=timezone)
    
    print(helios.latitude)
    print(datetime.datetime.strftime(helios.sunrise_datetime, '%H:%M')) 
    
    