#!/usr/bin/env python3
"""
Geodata Class
"""
import logging
import geopy


class Geo:
    def __init__(self,
                 city_input: str,
                 country_input: str = None
                 ):
        self.geo = geopy.Nominatim(user_agent="heliopy")
        self._city = city_input
        self._country = country_input
        self.get_geodata()

    
    @property
    def city(self):
        return self._city
    
    @city.setter
    def city(self, value):
        self._city = value
        self.get_geodata()
        
    @property
    def country(self):
        return self._country
    
    @country.setter
    def country(self, value):
        self._country = value
        self.get_geodata()
    
    @property
    def longitude(self):
        return self._longitude
    
    @longitude.setter
    def longitude(self, value):
        self._longitude = value
    
    @property
    def latitude(self):
        return self._latitude
    
    @latitude.setter
    def latitude(self, value):
        self._latitude = value  
        
    def get_geodata(self):
        if self.city is None:
            raise ValueError("City is not set")
        location_parms = "{_cty}{_Country}".format(
            _city=self.city, _country=f", {self.country}" if self.country is not None else None)
        location = self.geo.geocode(location_parms)
        self.longitude = location.longitude
        self.latitude = location.latitude
        
