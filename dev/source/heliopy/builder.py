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
    sunrise = datetime.datetime.strftime(helios.sunrise_datetime, '%H:%M')
    sunset = datetime.datetime.strftime(helios.sunset_datetime, '%H:%M')
    print(f"Sunrise: {sunrise}, Sunset: {sunset}")
    