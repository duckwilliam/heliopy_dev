
import math


def angle_of_incidence(module_degree: 0 < int < 360,
                       module_tilt: 0 < int < 90,
                       solar_altitude: 0 < int < 90,
                       solar_azimuth: 0 < int < 360,
                       direct_normal_irradiance: float):
    
 
    _AOI_alt = solar_altitude + module_tilt
    _AOI_azim = 90 + (module_degree - solar_azimuth)
    direct_normal_irradiance * math.cos()
