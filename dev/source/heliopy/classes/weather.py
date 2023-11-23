import logging
import requests
import os
from . import geodata


class Weather:
    """
    Weather class:
    Using the OpenWeatherMap API, get current weather
    infomation for given time and location.
    """

    def __init__(self,
                 geo_data: geodata.Geo,
                 api_key_path=None,
                 api_key=None):
        self.geodata = geo_data
        self.api_weather = '/data/2.5/weather?'
        self._cloud_coverage = None
        self.api_key_path = os.path.join(
            os.path.dirname(
                api_key_path),
            'api_key.txt') if api_key_path is not None else None
        self.api_key = api_key if api_key is not None else self.get_api_key()

    def get_api_key(self):
        """
        Get the OpenWeatherMap API key.
        Returns:
            str: The OpenWeatherMap API key.
        Raises:
            ValueError: If the API key is not found or is not valid.
        """
        try:
            return os.environ.get(
                'OPENWEATHERMAP_API_KEY') or open(
                    self.api_key_path, encoding='utf-8').read().strip()
        except Exception as exc:
            raise ValueError(
                'OpenWeatherMap API key not found or is not valid.') from exc
    
    def get_weather(self):
        """
        Calls OpenWeatherMap API to get cloud coverage of the city and
        returns it as "cloud_coverage".
        """
        _parameters = {
            "lat": self.geodata.latitude,
            "lon": self.geodata.longitude,
            }
        _api_suburl = self.api_weather
        _api_response = self.requester(_api_suburl, _parameters)
        # _api_response = _api_response_raw.json()
        _cloud_coverage = _api_response['clouds']['all']
        self._cloud_coverage = float(_cloud_coverage)

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

    def requester(self, _api_suburl: str, parameters: dict):
        """
        Returns the response of the API request.
        Takes the specific sub-url and parameters as input.
        """
        logging.debug('using requester')
        _api_url: str = f"https://api.openweathermap.org{_api_suburl}"
        parameters["appid"] = self.api_key
        _parameters = parameters
        logging.debug(f"parameters: {_parameters}")
        try:
            _response = requests.get(_api_url, params=_parameters, timeout=10)
            _response.raise_for_status()
            logging.debug(f"response: {_response.json()}")
            return _response.json()
        except requests.HTTPError as err:
            raise SystemExit(err) from err
         
