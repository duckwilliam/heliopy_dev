#!/usr/bin/env python3
"""
Geodata Class
"""
import geopy


class Geo:
    def __init__(self,
                 city_input: str,
                 country_input: str = None
                 ):
        self.geo = geopy.Nominatim(user_agent="heliopy")
        self.city = city_input
        self.country = country_input
        self.get_geodata()

    def get_geodata(self):
        if self.city is None:
            raise ValueError("City is not set")
        location_parms = "{_city}{_country}".format(
            _city=self.city,
            _country=f", {self.country}" if self.country is not None else None)
        location = self.geo.geocode(location_parms)
        self.longitude = location.longitude
        self.latitude = location.latitude
