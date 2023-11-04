import classes.wrapper as wrapper


def main(city: str,
         time: str = None,
         day: str = None,
         country: str = None,
         timezone: str = None):
    helios = wrapper.SolarMain(city=city,
                               country=country,
                               requested_day=day,
                               requested_hour=time,
                               requested_timezone=timezone)
    
    print(helios.latitude)
    
    