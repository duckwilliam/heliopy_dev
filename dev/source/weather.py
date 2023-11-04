import math

class Weather(Basedata):
    """
    Weather class:
    Using the OpenWeatherMap API, get current weather
    infomation for given time and location.
    """
    def __init__(self,
                 name=None,
                 api_key=None,
                 api_base=None,
                 api_loc=None,
                 api_weather=None,
                 city=None,
                 country=None,
                 ):
        if name is None:
            name = "weather"
        self.name = name
        super().__init__(self)
        # self.api_key = api_key
        # self.api_base = api_base
        # self.city = city
        # self.country = country
        # self.api_loc = api_loc

        if api_weather is None:
            self.api_weather: str = '/data/2.5/weather?'
        elif isinstance(api_weather, str):
            self.api_weather = api_weather
        self._cloud_coverage = None
 


    def get_weather(self):
        """
        Calls OpenWeatherMap API to get cloud coverage of the city and
        returns it as "cloud_coverage".
        """
        logging.debug('getting weather data')
        _parameters = {
            "lat": self.latitude,
            "lon": self.longitude,
            }
        _api_suburl = self.api_weather
        _api_response = self.requester(_api_suburl, _parameters)
        # _api_response = _api_response_raw.json()
        _sunrise = _api_response['sys']['sunrise']
        _sunset = _api_response['sys']['sunset']
        _timezone= _api_response['timezone']
        logging.info(f"sunrise: {_sunrise}")
        logging.info(f"sunset: {_sunset}")
        # _time_shift = _api_response['timezone']
        self.timezone = int(_timezone)
        self.sunrise_unix = int(_sunrise)
        self.sunset_unix = int(_sunset)
        if self.requested_day is not None:
            _cloud_coverage = 0
        else:
            _cloud_coverage = _api_response['clouds']['all']
        self._cloud_coverage = float(_cloud_coverage)
        logging.info(f"cloud coverage: {_cloud_coverage}")


    @property
    def cloud_coverage(self):
        logging.debug('getting cloud coverage')
        if self._cloud_coverage is None:
            self.get_weather()
        if isinstance(self._cloud_coverage, float):
            _cloud_coverage = self._cloud_coverage
            return _cloud_coverage
        else:
            raise TypeError("Cloud coverage must be a float.")

    def suntimes(self):
        if self.sunrise_unix or self.sunset_unix is None:
            self.get_weather()
        if isinstance(self.sunrise_unix, int) and isinstance(self.sunset_unix, int):
            _rise = datetime.fromtimestamp(self.sunrise_unix)
            _set = datetime.fromtimestamp(self.sunset_unix)
        else:
            raise TypeError("Sunrise and Sunset must be unix timestamps.")

        self.sunrise_datetime = _rise
        self.sunset_datetime = _set
