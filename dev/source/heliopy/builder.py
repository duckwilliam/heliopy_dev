"""
Heliopy Builder Module:
use the main() function in this module to create a 'helios' object
which stores and calculates the desired values. For a full description 
of available parameters, check the main() docstring. 
"""

import classes.wrapper as wrapper
import datetime

def main(city: str,
         time = None,
         day = None,
         country: str = None,
         timezone: str = None):
             
    """ Main function:
    Creates an object 'helios' that generates, stores and 
    updates the desired data. 
    Returns the object itself for further Processing.
    
    The following arguments can be passed to this function:
        city=[city] *required*
        country=[country]
        day=[date as YYYY-MM-DD]
        time=[time as HH:MM:SS]
        timezone=[timezone as 'REGION/CITY']
    If no arguments for day, time and timezone are provided
    the system time, date and timezoe will be used.
    
    The following attributes can be read after successful creation:
    
    helios.
        city                set/get city for which lat/long will be determined
        country             set/get country city is in
        timezone            set/get timezone
        time                set time as string/get time as datetime object
        day                 set day as string/get date as datetime object 
        date                get full date as datetime object
        day_of_year         get day of the year as integer 
        longitide           get longitude as float
        latitude            get latitude as float
        sunrise_datetime    get time of sunrise as datetime object
        sunset_datetime     get time of sunset as datetime object 
        cloud_coverage      get current cloud coverage in % as integer 
        illumination        get outside Illumination in Lux as float
        time_init()         reinitialise time_dsta object 
        geo_init()          reinitialise geo_data object 
        weather_init()      reinitialise weather object
        solar_init()        reinitialise solar_data object 
        
        
        
        
        
        
        ['illuminance']: Outside Brightness in Lux
        ['time']: Time used as %-H (e.g. 4 or 12)
        ['date']: Date used as YYYY-MM-DD
        ['city']: City Used
        ['country']: Country Used
        ['cloud_coverage']: Cloud coverage in %
        ['et_illuminance']: Extraterrestrial Illuminance in Lux
        ['direct_illuminance']: Direct Illuminance in Lux
        ['horizontal_illuminance']: Horizontal Illuminance in Lux
        ['horizontal_sky_illuminance']: Horizontal Sky Illuminance in Lux
        ['sunrise']: Time of Sunrise as hh:mm
        ['sunset']: Time of sunset as hh:mm
        ['sun_altitude']: Sund altitude at [Time] in degrees.
        ['day']: True if there is daylight at [Time].
        ['clear_sky_index'] = Aproximation of Clear Sky Index based on cloud coverage
        ['cs_irradiance'] = Estimated Clear Sky Irradiance in W/m^2 based on solar altitude.
        ['irradiance'] = Estimated current Irradiance in W/m^2 based on solar altitude and cloud coverage.
    Takes the following arguments:
        time: str=[0-24], date: str=[YYYY-MM-DD], city: str=['City'],
        country: str=['Country'], api_key: str=['api key']
    If no arguments are provided, defaults to values defined in main.py.
    """
    
    helios = wrapper.SolarMain(city=city,
                               country=country,
                               requested_day=day,
                               requested_hour=time,
                               requested_timezone=timezone)
    
    print(helios.latitude)
    sunrise = datetime.datetime.strftime(helios.sunrise_datetime, '%H:%M')
    sunset = datetime.datetime.strftime(helios.sunset_datetime, '%H:%M')
    print(f"Sunrise: {sunrise}, Sunset: {sunset}")
    