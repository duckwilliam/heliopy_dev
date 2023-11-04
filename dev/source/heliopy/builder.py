"""
Heliopy Builder Module:
use the main() function in this module to create a 'helios' object
which stores and calculates the desired values. For a full description 
of available parameters, check the main() docstring. 
"""


import classes.wrapper as wrapper
import datetime

def main(city: str,
    """ Main function:
    Creates Illuminance object to calculate Relevant data and
    returns a dictionary object with the following information:
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
    