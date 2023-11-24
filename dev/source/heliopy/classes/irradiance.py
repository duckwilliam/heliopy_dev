#!/usr/bin/env python3

"""
A module for calculating solar irradiance attributes.

This module provides functions and classes for calculating various
solar attributes, such as module irradiance, 
optimal tilt and azimuth angles, and effective length of illuminated panels.

Classes:
- Irradiance: Calculate solar irradiance for a
   given module tilt and orientation.

Functions:
- area_total: Calculate the total surface area of illuminated panels.
- module_lit_optimal: Calculate the optimal tilt and azimuth angles
  that maximize the module illumination.
- effective_length: Calculate the effective length of an illuminated panel.
"""

import itertools
import math
from classes import solardata, geodata


class Irradiance:
    """
    Calculate solar irradiance for a given module tilt and orientation.

    Args:
        module_degree (int): The degree of the module orientation (0-359).
        module_tilt (int): The tilt angle of the module (0-89).
        solar_data (solardata.Sun):
            An instance of the solardata.Sun class containing solar data.
        geo_data (geodata.Geo):
            An instance of the geodata.Geo class containing geographical data.

    Attributes:
        alt_rad (float): The solar altitude angle in radians.
        azi_rad (float): The solar azimuth angle in radians.
        tilt_rad (float): The module tilt angle in radians.
        deg_rad (float): The module orientation angle in radians.
        incident (float): The direct illuminance from solar data.
        horizontal (float): The horizontal illuminance calculated
        based on the incident illuminance and solar altitude.
        latitude (float): The latitude from geographical data.

    Properties:
        module (float): The solar module irradiance calculated
        based on the tilt and orientation angles.
        tilt_optimal (int):
            The optimal tilt angle that maximizes the module irradiance.
        deg_optimal (int):
            The optimal orientation angle that maximizes the module irradiance.
        module_optimal (float): The optimal module irradiance calculated
        based on the optimal tilt and orientation angles.
    """
    def __init__(self,
                 module_degree: int,
                 module_tilt: int,
                 solardata: solardata.Sun,
                 geodata: geodata.Geo,
                 module_degree_base: int = None,
                 module_tilt_min: int = None
                 ):
        """
        Initialize the Irradiance object.

        Args:
            module_degree (int): The degree of the module orientation (0-359).
            module_tilt (int): The tilt angle of the module (0-89).
            solar_data (solardata.Sun): An instance of the
            solardata.Sun class containing solar data.
            geo_data (geodata.Geo): An instance of the
            geodata.Geo class containing geographical data.
        """
        self.alt_rad = math.radians(solardata.altitude)
        self.azi_rad = math.radians(solardata.solar_azimuth)
        self.tilt_rad = math.radians(module_tilt)
        self.deg_rad = math.radians(module_degree)
        self.tilt_min = module_tilt_min if module_tilt_min is not None else 0
        self.deg_base = module_degree_base if module_degree_base is not None else 180
        self.incident = solardata.direct_illuminance
        self.horizontal = self.incident * math.sin(self.alt_rad)
        self.latitude = geodata.latitude

    def module(self,
               tilt: int = None,
               deg: int = None):
        """
        Calculate the solar module irradiance based on
        the tilt and orientation angles.

        Args:
            tilt (int, optional): The tilt angle of the module (0-89). 
            Defaults to None.
            deg (int, optional): The degree of the module orientation (0-359). 
            Defaults to None.

        Returns:
            float: The calculated solar module irradiance.
        """
        tilt_rad = self.tilt_rad if tilt is None else math.radians(tilt)
        deg_rad = self.deg_rad if deg is None else math.radians(deg)
        _s_module = self.incident * (
            math.cos(
                self.alt_rad) * math.sin(
                    tilt_rad) * math.cos(
                        deg_rad - self.azi_rad) + math.sin(
                            self.alt_rad) * math.cos(
                                tilt_rad))
        return _s_module
            
    def angles_array(self) -> dict:
        """
        Create dictionary with all module tilt and azimuth 
        combinations and respective irradiance values
        """
        deg_range = range(180) if self.latitude > 0 else range(181, 360)
        angles_dict = {
            (tilt, azimuth): self.module(tilt=tilt, deg=azimuth)
            for tilt, azimuth in itertools.product(
                range(self.tilt_min, 90), deg_range
            )
        }
        return angles_dict
    
    @property
    def tilt_array(self):
        """
        Calculate the optimal tilt angle that maximizes
        the solar module irradiance.

        Returns:
            dict: the module irradiance for every angle
        """
        tilt_dict = {angle: self.module(tilt=angle) for angle in range(
            self.tilt_min, 90)}
        return tilt_dict
        # return max(tilt_dict, key=tilt_dict.get)
    
    @property
    def deg_array(self):
        """
        Calculate the optimal azimuth angle that maximizes
        the solar module irradiance.

        Returns:
            dict: the module irradiance for every angle
        """
        deg_range = range(180) if self.latitude > 0 else range(181, 360)
        deg_dict = {angle: self.module(deg=angle) for angle in deg_range}
        return deg_dict
        # return max(deg_dict, key=deg_dict.get)
    
    @property
    def module_optimal(self):
        """
        Calculate the optimal module irradiance based on the
        optimal tilt and orientation angles.

        Returns:
            float: The optimal module irradiance.
        """
        tilt_optimal = max(self.tilt_array, key=self.tilt_array.get)
        deg_optimal = max(self.deg_array, key=self.deg_array.get)
        return self.module(tilt=tilt_optimal, deg=deg_optimal)

    def effective_length(self,
                         panel_distance: int,
                         panel_size: int,
                         panel_inclination
                         ):
        """
        Calculate the illuminated length of a panel edge.

        Args:
            panel_distance (int): The distance between panels.
            panel_size (int): The size of a single panel.
            panel_inclination: The inclination angle of the panel.

        Returns:
            float: The effective length of the illuminated panel.
        """    
        _dark = math.sin(
            math.degrees(
                panel_inclination)) - math.sin(
                    90 - math.degrees(
                        panel_inclination)) * panel_distance
        _lit = panel_size - _dark
        return _lit

