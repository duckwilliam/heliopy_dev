from classes import solardata, weather, timedata, geodata
import logging

class SolarMain:
    """
    **Class**: `SolarMain`

    Initializes the `SolarMain` class.
    """
    def __init__(self,
                 city: str,
                 name=None,
                 country: str = None,
                 requested_day: str = None,
                 requested_hour=None,
                 requested_timezone: str = None,
                 api_key_path=None,
                 api_key=None
                 ):
        """
        Initializes the `SolarMain` class.

        Args:
            city (str): The city for which to calculate solar data.
            name (str, optional): The name of the solar data instance. Defaults to None.
            country (str, optional): The country of the city. Defaults to None.
            requested_day (str, optional): The requested day for solar data. Defaults to None.
            requested_hour (str, optional): The requested hour for solar data. Defaults to None.
            requested_timezone (str, optional): The requested timezone for solar data. Defaults to None.
        """
        logging.info("Initializing BaseData class.")
        self.name = name if name is not None else "Helios"
        self.city = city
        self.country = country
        self.requested_day = requested_day
        self.requested_hour = requested_hour
        self.requested_timezone = requested_timezone
        self.api_key = api_key
        self.api_key_path = api_key_path
        self.time_init()
        self.geo_init()
        self.weather_init()
        self.solar_init()
        
    def time_init(self):
        self.time_data = timedata.Time(
            time_input=self.requested_hour,
            day_input=self.requested_day,
            timezone_input=self.requested_timezone)
        
    def geo_init(self):
        self.geo_data = geodata.Geo(
            city_input=self.city,
            country_input=self.country)
            
    def weather_init(self):
        self.weather = weather.Weather(
            geo_data=self.geo_data,
            api_key_path=self.api_key_path,
            api_key=self.api_key)
            
    def solar_init(self):
        self.solar_data = solardata.Sun(
            timedata=self.time_data,
            geodata=self.geo_data,
            weather=self.weather)
            
            
    @property
    def city(self):
        """Returns the city for solar data."""
        return self._city

    @city.setter
    def city(self, value):
        """setter for city"""
        logging.info(f"Setting city: {value}")
        self._city = str(value)

    @property
    def country(self):
        """Returns the country for solar data. """
        return self._country

    @country.setter
    def country(self, value):
        """Sets the country for solar data."""
        logging.info(f"Setting country: {value}")
        self._country = str(value)

    @property
    def requested_day(self):
        """Returns the requested day for solar data."""
        return self._requested_day

    @requested_day.setter
    def requested_day(self, value):
        """Sets the requested day for solar data."""
        logging.info(f"Setting requested_day: {value}")
        self._requested_day = value

    @property
    def requested_hour(self):
        """Returns the requested hour for solar data."""
        return self._requested_hour

    @requested_hour.setter
    def requested_hour(self, value):
        """Sets the requested hour for solar data."""
        logging.info(f"Setting requested_hour: {value}")
        self._requested_hour = value

