"""
Heliopy Builder Module:
use the main() function in this module to create a 'helios' object
which stores and calculates the desired values. For a full description 
of available parameters, check the main() docstring. 
"""

from .classes import wrapper


def main(city: str,
         text: bool = False,
         time=None,
         day=None,
         country: str = None,
         timezone: str = None,
         api_key_path: str = None,
         api_key: str = None
         ):
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
        time_data. 
                utc_time                get UTC time as datetime object
        solar_data. 
                et_illuminance          get extraterrestrial illuminance 
                local_standard_time_meridian_rad
                                        get LSTM in radians 
                equation_of_time_rad    get EOT in radians
                time_correction_factor_rad
                                        get time correction factor in radians 
                local_solar_time_rad    get local solar time in radians 
                hour_angle_rad          get hour angle in radians 
                declination_angle_rad   get solar declination in radians 
                altitide                get solar altitude in degrees
                solar_azimut            get solar azimuth in degrees 

    """

    helios = wrapper.SolarMain(city=city,
                               country=country,
                               requested_day=day,
                               requested_hour=time,
                               requested_timezone=timezone,
                               api_key_path=api_key_path,
                               api_key=api_key)
    if text:
        print(helios)
    else:
        return helios
