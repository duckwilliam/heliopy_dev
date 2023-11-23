

import math
from . import solardata, geodata


class Irradiance:
    """
    Calculate solar irradiance for a given module tilt and orientation.

    Args:
        module_degree (int): The degree of the module orientation (0-359).
        module_tilt (int): The tilt angle of the module (0-89).
        solar_data (solardata.Sun): An instance of the solardata.Sun class containing solar data.
        geo_data (geodata.Geo): An instance of the geodata.Geo class containing geographical data.

    Attributes:
        alt_rad (float): The solar altitude angle in radians.
        azi_rad (float): The solar azimuth angle in radians.
        tilt_rad (float): The module tilt angle in radians.
        deg_rad (float): The module orientation angle in radians.
        incident (float): The direct illuminance from solar data.
        horizontal (float): The horizontal illuminance calculated based on the incident illuminance and solar altitude.
        latitude (float): The latitude from geographical data.

    Properties:
        module (float): The solar module irradiance calculated based on the tilt and orientation angles.
        tilt_optimal (int): The optimal tilt angle that maximizes the module irradiance.
        deg_optimal (int): The optimal orientation angle that maximizes the module irradiance.
        module_optimal (float): The optimal module irradiance calculated based on the optimal tilt and orientation angles.
    """
    def __init__(self,
                 module_degree: 0 < int < 360,
                 module_tilt: 0 < int < 90,
                 solar_data: solardata.Sun,
                 geo_data: geodata.Geo
                 ):
        """
        Initialize the Irradiance object.

        Args:
            module_degree (int): The degree of the module orientation (0-359).
            module_tilt (int): The tilt angle of the module (0-89).
            solar_data (solardata.Sun): An instance of the solardata.Sun class containing solar data.
            geo_data (geodata.Geo): An instance of the geodata.Geo class containing geographical data.
        """
        self.alt_rad = math.radians(solar_data.altitude)
        self.azi_rad = math.radians(solar_data.solar_azimuth)
        self.tilt_rad = math.radians(module_tilt)
        self.deg_rad = math.radians(module_degree)
        self.incident = solar_data.direct_illuminance
        self.horizontal = self.incident * math.sin(self.alt_rad)
        self.latitude = geo_data.latitude

    @property
    def module(self,
               tilt: int = None,
               deg: int = None):
        """
        Calculate the solar module irradiance based on the tilt and orientation angles.

        Args:
            tilt (int, optional): The tilt angle of the module (0-89). Defaults to None.
            deg (int, optional): The degree of the module orientation (0-359). Defaults to None.

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
            
    @property
    def tilt_optimal(self):
        """
        Calculate the optimal tilt angle that maximizes the solar module irradiance.

        Returns:
            int: The optimal tilt angle in degrees.
        """
        tilt_dict = {angle: self.module(tilt=angle) for angle in range(90)}
        return max(tilt_dict, key=tilt_dict.get)
    
    @property
    def deg_optimal(self):
        """
        Calculate the optimal azimuth angle that maximizes the solar module irradiance.

        Returns:
            int: The optimal azimuth angle in degrees.
        """
        deg_range = range(180) if self.latitude > 0 else range(181, 360)
        deg_dict = {angle: self.module(deg=angle) for angle in deg_range}
        return max(deg_dict, key=deg_dict.get)
    
    @property
    def module_optimal(self):
        """
        Calculate the optimal module irradiance based on the optimal tilt and orientation angles.

        Returns:
            float: The optimal module irradiance.
        """
        tilt_optimal = self.tilt_optimal
        deg_optimal = self.deg_optimal
        return self.module(tilt=tilt_optimal, deg=deg_optimal)
