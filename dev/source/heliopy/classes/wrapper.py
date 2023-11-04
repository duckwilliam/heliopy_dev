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
                 requested_hour = None,
                 requested_timezone: str = None
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
        self.requested_hour = None if requested_hour is None else requested_hour
        print(self, type(self.requested_hour))
        self.requested_timezone = requested_timezone
        self.time_data = timedata.Time(
            time_input=self.requested_hour,
            day_input=self.requested_day,
            timezone_input=self.requested_timezone)
        self.geo_data = geodata.Geo(
            city_input=city,
            country_input=country)
        self.weather = weather.Weather(
            latitude=self.latitude,
            longitude=self.longitude)
        self.solar_data = solardata.Sun(
            latitude=self.latitude,
            longitude=self.longitude,
            date=self.date,
            date_utc=self.utc_time,
            day_of_the_year=self.day_of_year,
            cloud_coverage=self.cloud_coverage)

    @property
    def date(self):
        """
        Returns the date for solar data.
        """
        return self.time_data.date

    @property
    def utc_time(self):
        """
        Returns the UTC time for solar data.
        """
        return self.time_data.utc_time

    @property
    def time(self):
        """
        Returns the time for solar data.
        """
        return self.time_data.time

    @time.setter
    def time(self, value):
        """
        Sets the time for solar data.

        Args:
            value: The value to set the time.
        """
        self.time_data.time = value

    @property
    def day(self):
        """
        Returns the day for solar data.
        """
        return self.time_data.day

    @day.setter
    def day(self, value):
        """
        Sets the day for solar data.

        Args:
            value: The value to set the day.
        """
        self.time_data.day = value

    @property
    def day_of_year(self):
        """
        Returns the day of the year for solar data.
        """
        return self.time_data.day_of_the_year

    @property
    def latitude(self):
        """
        Returns the latitude of the city.
        """
        return self.geo_data.latitude

    @property
    def longitude(self):
        """
        Returns the longitude of the city.
        """
        return self.geo_data.longitude

    @property
    def sunrise_datetime(self):
        """
        Returns the sunrise datetime.
        """
        return self.time_data.sunrise_datetime

    @sunrise_datetime.setter
    def sunrise_datetime(self, value):
        """
        Sets the sunrise datetime.

        Args:
            value: The value to set the sunrise datetime.
        """
        logging.debug(f'set _sunrise_datetime to {value}')
        self._sunrise_datetime = value

    @property
    def sunset_datetime(self):
        """
        Returns the sunset datetime.
        """
        return self.time_data.sunset_datetime

    @sunset_datetime.setter
    def sunset_datetime(self, value):
        """
        Sets the sunset datetime.

        Args:
            value: The value to set the sunset datetime.
        """
        logging.debug(f'set _sunset_datetime to {value}')
        self._sunset_datetime = value

    @property
    def city(self):
        """
        Returns the city for solar data.
        """
        return self._city

    @city.setter
    def city(self, value):
        """
        Sets the city for solar data.

        Args:
            value: The value to set the city.
        """
        logging.info(f"Setting city: {value}")
        self._city = str(value)

    @property
    def country(self):
        """
        Returns the country for solar data.
        """
        return self._country

    @country.setter
    def country(self, value):
        """
        Sets the country for solar data.

        Args:
            value: The value to set the country.
        """
        logging.info(f"Setting country: {value}")
        self._country = str(value)

    @property
    def requested_day(self):
        """
        Returns the requested day for solar data.
        """
        return self._requested_day

    @requested_day.setter
    def requested_day(self, value):
        """
        Sets the requested day for solar data.

        Args:
            value: The value to set the requested day.
        """
        logging.info(f"Setting requested_day: {value}")
        self._requested_day = value

    @property
    def requested_hour(self):
        """
        Returns the requested hour for solar data.
        """
        return self._requested_hour

    @requested_hour.setter
    def requested_hour(self, value):
        """
        Sets the requested hour for solar data.

        Args:
            value: The value to set the requested hour.
        """
        logging.info(f"Setting requested_hour: {value}")
        self._requested_hour = value

    @property
    def cloud_coverage(self):
        """
        Returns the cloud coverage for the city.
        """
        return self.weather.cloud_coverage
