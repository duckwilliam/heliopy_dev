

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
                 module_degree_base: int,
                 module_tilt_min: int,
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
        self.tilt_min = module_tilt_min
        self.deg_base = module_degree_base
        self.incident = solar_data.direct_illuminance
        self.horizontal = self.incident * math.sin(self.alt_rad)
        self.latitude = geo_data.latitude

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
            
    def angles_array(self) -> dict:
        """
        Create dictionary with all module tilt and azimuth 
        combinations and respective irradiance values
        """
        angles_dict = {}
        deg_range = range(180) if self.latitude > 0 else range(181, 360)
        for tilt in range(self.tilt_min, 90):
            for azimuth in deg_range:
                angles_dict[(tilt, azimuth)] = self.module(
                    tilt=tilt, deg=azimuth)
        return angles_dict
    
    @property
    def tilt_array(self):
        """
        Calculate the optimal tilt angle that maximizes the solar module irradiance.

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
        Calculate the optimal azimuth angle that maximizes the solar module irradiance.

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
        Calculate the optimal module irradiance based on the optimal tilt and orientation angles.

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
        _dark = math.sin(
            math.degrees(
                panel_inclination)) - math.sin(
                    90 - math.degrees(
                        panel_inclination)) * panel_distance
        _lit = panel_size - _dark
        return _lit
    
    def area_total(self,
                   panel_width: int,
                   panel_height: int,
                   panel_amount: int,
                   panel_rows: int,
                   panel_spacing_horizontal: int,
                   panel_spacing_vertical: int,
                   module_azimuth: int,
                   module_tilt: int):
        surface_single = panel_amount * panel_width 
        surface_total = surface_single * panel_height
        panel_columns = panel_amount // panel_rows
        base_degree_deviation = abs(self.deg_base - module_azimuth)
        min_tilt_deviation = abs(self.tilt_min - module_tilt)
        width_total_lit = (
            self.effective_length(
                panel_distance=panel_spacing_horizontal,
                panel_size=panel_width,
                panel_inclination=base_degree_deviation) * (
                    panel_columns - 1) * panel_rows) + (
                        surface_single * panel_rows)

        height_total_lit = (
            self.effective_length(
                panel_distance=panel_spacing_vertical,
                panel_size=panel_height,
                panel_inclination=min_tilt_deviation) * (
                    panel_rows - 1) * panel_columns) + (
                        surface_single * panel_columns)
        
        surface_lit = height_total_lit * width_total_lit
        return surface_lit
        # surface_lit_ratio = surface_lit / surface_total * 100
        # return surface_lit_ratio
    
    def module_lit_optimal(self,
                           panel_w: int,
                           panel_h: int,
                           panel_a: int,
                           panel_r: int,
                           panel_spacing_h: int,
                           panel_spacing_v: int) -> tuple:
        lit_optimal_dict = {
            (tilt, azi): illumination
            * self.area_total(
                panel_width=panel_w,
                panel_height=panel_h,
                panel_amount=panel_a,
                panel_rows=panel_r,
                panel_spacing_horizontal=panel_spacing_h,
                panel_spacing_vertical=panel_spacing_v,
                module_azimuth=azi,
                module_tilt=tilt,
            )
            for (tilt, azi), illumination in self.angles_array().items()
        }
        max_illumination = max(lit_optimal_dict, key=lit_optimal_dict.get)
        _tilt_optimal = max_illumination[0]
        _azimuth_optimal = max_illumination[1]
        return (_tilt_optimal, _azimuth_optimal)