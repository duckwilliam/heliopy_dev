#!/usr/bin/env python3
"""
Classes for Getting and Calculating Data.
General-purpose solar irradiance and brightness calculator.
"""
import logging
from datetime import datetime, timedelta
import requests
from requests.exceptions import HTTPError
import geodata
import timedata

class SolarMain:
    def __init__(self,
                 city: str,
                 name=None,
                 country: str = None,
                 requested_day: str = None,
                 requested_hour: str = None,
                 requested_timezone: str = None
                 
                 ):
        logging.info("Initializing BaseData class.")
        self.name = name if name is not None else "Helios"
        self.city = city
        self.country = country
        self.requested_day = requested_day
        self.requested_hour = requested_hour
        self.requested_timezone = requested_timezone
        self.time_data = timedata.Time(time_input = self.requested_hour,
                              day_input = self.requested_day,
                              timezone_input = self.requested_timezone
                              )
        self.geo_data = geodata.Geo(city_input = city, country_input = country)
    
    
    @property
    def date(self):
        return self.time_data.date
        
    @property
    def utc_time(self):
        return self.time_data.utc_time
        
    @property
    def time(self):
        return self.time_data.time
        
    @time.setter
    def time(self, value):
        self.time_data.time = value
        
    @property
    def day(self):
        return self.time_data.day
        
    @day.setter
    def day(self, value):
        self.time_data.day = value
        
    @property
    def day_of_year(self):
        return self.time_data.day_of_the_year
        
        
    @property
    def latitude(self):
        return self.geo_data.latitude
        
    @property
    def longitude(self):
        return self.geo_data.longitude
     
    @property
    def sunrise_datetime(self):
        return self._sunrise_datetime
    
    @sunrise_datetime.setter
    def sunrise_datetime(self, value):
        logging.debug(f'set _sunrise_datetime to {value}')
        self._sunrise_datetime = value
    
    @property
    def sunset_datetime(self):
        return self._sunset_datetime
    
    @sunset_datetime.setter
    def sunset_datetime(self, value):
        logging.debug(f'set _sunset_datetime to {value}')
        self._sunset_datetime = value
    
    @property
    def api_key(self):
        return self._api_key
    
    @api_key.setter
    def api_key(self, value):
        logging.info(f"Setting api_key: {value}")
        self._api_key = str(value)
        
    @property
    def city(self):
        return self._city
    
    @city.setter
    def city(self, value):
        logging.info(f"Setting city: {value}")
        self._city = str(value)
    
    @property
    def country(self):
        return self._country
    
    @country.setter
    def country(self, value):
        logging.info(f"Setting country: {value}")
        self._country = str(value)
    
    @property
    def requested_day(self):
        return self._requested_day
    
    @requested_day.setter
    def requested_day(self, value):
        logging.info(f"Setting requested_day: {value}")
        self._requested_day = str(value)

    @property
    def requested_hour(self):
        return self._requested_hour
    
    @requested_hour.setter
    def requested_hour(self, value):
        logging.info(f"Setting requested_hour: {value}")
        self._requested_hour = str(value)

    @property
    def current_date(self):
        """
        Returns current date as string (YYY-MM-DD),
        If a custom value is provided (self.requested_day)
        it will be returned instead.
        """
        if self.requested_day is not None and isinstance(self.requested_day, str):
            _current_date = self.requested_day
            logging.debug(f"{self.requested_day} is a valid date")
        else:
            logging.debug(f"{self.requested_day} is a not valid date")
            now = datetime.now()
            _current_date = now.strftime("%Y-%m-%d")
        logging.info(f"set current date to {_current_date}")
        return _current_date

    @property
    def day_of_the_year(self):
        """
        @brief Returns the day of the year. It is defined as the number of days since January 1 1970 00 : 00 : 00.
        @return a tuple of the form ( year month day )
        """
        _date_object = datetime.strptime(self.current_date, "%Y-%m-%d")
        _day_of_the_year = _date_object.timetuple().tm_yday
        logging.info(f"calculated day of the year: {_day_of_the_year}")
        return _day_of_the_year

    @property
    def current_time(self):
        """
        Returns current hour of day as string (e.g. 12),
        If a custom value is provided (self.requested_hour)
        it will be returned instead.
        """
        #print("current_time accessed")
        if self.requested_hour is not None and isinstance(self.requested_hour, str):
            _current_time = self.requested_hour
            logging.debug(f"{self.requested_hour} is a valid hour")
        else:
            now = datetime.now()
            logging.debug(f"{self.requested_hour} is a not valid hour")
            logging.debug(f'setting current_time to actual time')
            _current_time = now.strftime("%-H")
        logging.info(f"set current time to {_current_time}")
        return _current_time

    @property
    def latitude(self):
        """
        Calls OpenWeatherMap API to get latitude of the city and
        returns it as "latitude".
        """
        logging.debug('getting latitude')
        _parameters = {
            "q": f"{self.city},{self.country}",
            "limit": 1
        }
        logging.debug(f"parameters: {_parameters}")
        _api_suburl = self.api_loc
        _api_response = self.requester(_api_suburl, _parameters)
        # _api_response = _api_response_raw
        _latitude = _api_response[0]['lat']
        logging.info(f"latitude: {_latitude}")
        return float(_latitude)

    @property
    def longitude(self):
        """
        Calls OpenWeatherMap API to get longitude of the city and
        returns it as "longitude".
        """
        logging.debug('getting longitude')
        _parameters = {
            "q": f"{self.city},{self.country}",
            "limit": 1
        }
        logging.debug(f"parameters: {_parameters}")
        _api_suburl = str(self.api_loc)
        _api_response = self.requester(_api_suburl, _parameters)
        # _api_response = _api_response_raw.json()
        _longitude = _api_response[0]['lon']
        logging.info(f"longitude: {_longitude}")
        return float(_longitude)

    def requester(self, _api_suburl: str, parameters: dict):
        """
        Returns the response of the API request.
        Takes the specific sub-url and parameters as input.
        """
        logging.debug('using requester')
        _api_url: str = f"{self.api_base}{_api_suburl}"
        parameters["appid"] = self.api_key
        _parameters = parameters
        logging.debug(f"parameters: {_parameters}")
        try:
            _response = requests.get(_api_url, params=_parameters, timeout=10)
            _response.raise_for_status()
            # _response = _response_raw.json()
            logging.debug(f"response: {_response.json()}")
            return _response.json()
        except HTTPError as err:
            raise SystemExit(err) from err
       
    @property
    def tester(self):
        """
        test function.
        """
        _parameters = {
            "q": f"{self.city},{self.country}",
            "limit": 1
            }
        _api_suburl = self.api_loc
        _api_response = self.requester(_api_suburl, _parameters)
        # _api_response = _api_response_raw
        testdata = (_api_response)[0]['name']
        return testdata


