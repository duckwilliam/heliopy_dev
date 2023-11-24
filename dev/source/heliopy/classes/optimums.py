#!/usr/bin/env python3

from . import irradiance

class Optimums:
    def __init__(self,
                 irradiance_data: irradiance.Irradiance,
                 panel_width: int,
                 panel_height: int,
                 panel_amount: int,
                 panel_rows: int,
                 panel_spacing_horizontal: int = None,
                 panel_spacing_vertical: int = None,
                 module_azimuth: int = None,
                 module_tilt: int = None):
        self.irradiance_data = irradiance_data
        self.panel_width = panel_width
        self.panel_height = panel_height
        self.panel_amount = panel_amount
        self.panel_rows = panel_rows
        self.panel_spacing_horizontal = panel_spacing_horizontal if panel_spacing_horizontal is not None else 0
        self.panel_spacing_vertical = panel_spacing_vertical if panel_spacing_vertical is not None else 0
        self.module_azimuth = module_azimuth if module_azimuth is not None else self.irradiance_data.deg_base
        self.module_tilt = module_tilt if module_tilt is not None else self.irradiance_data.tilt_min

    def area_total(self,
                   module_azimuth: int,
                   module_tilt: int):
        """
        Calculate the total illuminated surface area of panels at
        given tilt and azimuth.

        Args:
            panel_width (int): The width of a single panel.
            panel_height (int): The height of a single panel.
            panel_amount (int): The total number of panels.
            panel_rows (int): The number of rows of panels.
            panel_spacing_horizontal (int):
                The horizontal spacing between panels.
            panel_spacing_vertical (int): The vertical spacing between panels.
            module_azimuth (int): The azimuth angle of the module.
            module_tilt (int): The tilt angle of the module.

        Returns:
            float: The total illuminated surface area.
        """
        surface_single = self.panel_amount * self.panel_width 
        panel_columns = self.panel_amount // self.panel_rows
        base_degree_deviation = abs(self.irradiance_data.deg_base - module_azimuth)
        min_tilt_deviation = abs(self.irradiance_data.tilt_min - module_tilt)
        width_total_lit = (
            self.irradiance_data.effective_length(
                panel_distance=self.panel_spacing_horizontal,
                panel_size=self.panel_width,
                panel_inclination=base_degree_deviation) * (
                    panel_columns - 1) * self.panel_rows) + (
                        surface_single * self.panel_rows)

        height_total_lit = (
            self.irradiance_data.effective_length(
                panel_distance=self.panel_spacing_vertical,
                panel_size=self.panel_height,
                panel_inclination=min_tilt_deviation) * (
                    self.panel_rows - 1) * panel_columns) + (
                        surface_single * panel_columns)
        
        surface_lit = height_total_lit * width_total_lit
        return surface_lit
        # surface_lit_ratio = surface_lit / surface_total * 100
        # return surface_lit_ratio
    
    def module_lit_optimal(self) -> tuple:
        """
        Calculate the optimal tilt and azimuth angles that maximize 
        the module illumination.

        Returns:
            tuple: The optimal tilt and azimuth angles as a tuple
            (tilt, azimuth).
        """
        lit_optimal_dict = {
            (tilt, azi): illumination
            * self.area_total(module_azimuth=azi, module_tilt=tilt)
            for (
                tilt,
                azi), illumination in self.irradiance_data.angles_array().items()
        }
        max_illumination = max(lit_optimal_dict, key=lit_optimal_dict.get)
        _tilt_optimal = max_illumination[0]
        _azimuth_optimal = max_illumination[1]
        return (_tilt_optimal, _azimuth_optimal)