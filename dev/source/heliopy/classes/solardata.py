#!/usr/bin/env python3
"""
General-purpose solar irradiance and brightness calculator.
"""
import logging
import math
import datetime
from . import timedata
from . import geodata
from . import weather


def rounder(decimals: int):
    def decorator(func):
        def wrapper(*args, **kwargs):
            result = func(*args, **kwargs)
            return round(result+10**(-len(str(result))-1), decimals)
        return wrapper
    return decorator


class Sun:
    """
    Class Illuminaion:
    Calculate Outside Illumination in Lux
    for given location and time
    """

    def __init__(self,
                 timedata: timedata.Time,
                 geodata: geodata.Geo,
                 weather: weather.Weather
                 ):
        self.timedata = timedata
        self.geodata = geodata
        self.weather = weather
       
    @property
    def utc_time_delta(self):
        delta = self.timedata.date - self.timedata.date_utc
        delta_seconds = delta.total_seconds() 
        delta_hours = divmod(delta_seconds, 3600)[0]
        return int(delta_hours)

    @property
    def hour(self):
        return int(self.timedata.date.strftime('%-H')) 

    @property
    def day(self):
        return self.timedata.date.date()

    @property
    @rounder(2)
    def et_illuminance(self):
        _day_of_the_year = self.timedata.day_of_the_year
        _et_illuminance = float(129) * (1 + 0.034 * math.cos(((
            2 * math.pi)/356) * (_day_of_the_year - 2)))
        logging.info(f'calculated extraterrestrial_illuminance: {_et_illuminance}')
        return _et_illuminance

    @property
    @rounder(2)
    def local_standard_time_meridian_rad(self):
        _lstm_rad = math.radians(15) * self.utc_time_delta
        return _lstm_rad

    @property
    @rounder(2)
    def equation_of_time_rad(self):
        _doy = self.timedata.day_of_the_year
        _B_rad = math.radians((360/365) * (_doy - 81))
        _eot_rad = 9.87 * math.sin(
            2 * _B_rad) - 7.53 * math.cos(
                _B_rad) - 1.5 * math.sin(
                    _B_rad)
        return _eot_rad

    @property
    @rounder(2)
    def time_correction_factor_rad(self):
        _eot_rad = self.equation_of_time_rad
        _lsmt_rad = self.local_standard_time_meridian_rad
        long_rad = math.radians(self.geodata.longitude)
        _tcf_rad = 4 * (long_rad - _lsmt_rad) + _eot_rad
        return _tcf_rad

    @property
    @rounder(2)
    def local_solar_time_rad(self):
        _lt = self.hour
        _tcf_rad = self.time_correction_factor_rad
        _lst = _lt + (_tcf_rad / 60)
        return _lst

    @property
    @rounder(2)
    def hour_angle_rad(self):
        _lst = self.local_solar_time_rad
        _hra_rad = math.radians(15) * (_lst - 12)
        return _hra_rad

    @property
    @rounder(2)
    def declination_angle_rad(self):
        _doy = self.timedata.day_of_the_year
        _da_rad = math.radians(-23.45) * math.cos(
            math.radians((360/365) * (_doy + 10)))
        return _da_rad

    @property
    def sun_extr(self):  
        _lat = math.radians(self.geodata.latitude)
        _da = self.declination_angle_rad
        _corr_rad = math.radians(90.833)
        _sun_extr = math.acos(
            ((math.cos(_corr_rad))/(
                math.cos(_lat) * math.cos(_da))) - (
                    math.tan(_lat) * math.tan(_da)))
        return _sun_extr

    @property
    def sunrise_datetime(self):
        _tcf_rad = self.time_correction_factor_rad
        _hra = -1 * self.sun_extr
        sunrise_hour = (_hra / math.radians(15)) - (_tcf_rad / 60) + 12
        sunrise_hour_td = datetime.timedelta(seconds=sunrise_hour * 3600)
        _sunrise = datetime.datetime.combine(
            self.day, datetime.datetime.min.time()) + sunrise_hour_td
        return _sunrise

    @property
    def sunset_datetime(self):
        _tcf_rad = self.time_correction_factor_rad
        _hra = self.sun_extr
        sunset_hour = (_hra / math.radians(15)) - (_tcf_rad / 60) + 12
        sunset_hour_td = datetime.timedelta(seconds=sunset_hour * 3600)
        _sunset = datetime.datetime.combine(
            self.day, datetime.datetime.min.time()) + sunset_hour_td
        return _sunset

    @property
    @rounder(2)
    def altitude(self):
        _lat_rad = math.radians(self.geodata.latitude)
        _hra_rad = self.hour_angle_rad
        _da_rad = self.declination_angle_rad
        _alt_rad = math.asin(math.sin(_da_rad) * math.sin(
            _lat_rad) + math.cos(
                _da_rad) * math.cos(
                    _lat_rad) * math.cos(
                        _hra_rad))
        _alt_deg = math.degrees(_alt_rad)
        logging.info(f"altitude: {_alt_deg}")
        return _alt_deg

    @property 
    @rounder(2)
    def solar_azimuth(self):
        _lat_rad = math.radians(self.geodata.latitude)
        _alt_rad = math.radians(self.altitude)
        _hra_rad = self.hour_angle_rad
        _da_rad = self.declination_angle_rad
        _azi_rad = math.acos(
            ((math.sin(_da_rad) * math.cos(_lat_rad)) - (
                math.cos(_da_rad) * math.sin(
                    _lat_rad) * math.cos(
                        _hra_rad))) / math.cos(_alt_rad))
        _azi_deg = math.degrees(_azi_rad)
        return _azi_deg

    @property
    @rounder(2)
    def clear_sky(self):
        cloud_fraction = self.weather.cloud_coverage / 100
        cloud_oct = 1.0882 if cloud_fraction == 1 else cloud_fraction
        csi = 0.75 * (cloud_oct)**3.4
        return csi

    @property
    @rounder(2)
    def irradiance_clear(self):
        _alt_rad = self.altitude
        _irradiance_clear = 910 * math.sin(_alt_rad) - 30
        return _irradiance_clear

    @property
    @rounder(2)
    def irradiance_cloud(self):
        _irradiance_clear = self.irradiance_clear
        _csi = self.clear_sky
        _irradiance_cloud = _irradiance_clear * (1 - _csi) 
        return _irradiance_cloud

    @property
    @rounder(2)
    def air_mass(self):
        _altitude = self.altitude
        _am_rad = 1/(
            math.cos(
                math.radians(
                    90 - _altitude)) + 0.50572/(
                        96.07995 - math.radians(
                            90 - _altitude))**1.6364)
        logging.info(f"air_mass: {_am_rad}")
        return _am_rad

    @property
    def cloud_coefficients(self):
        _clear_sky = self.clear_sky
        if _clear_sky < 0.3:
            return 0.21, 0.8, 15.5, 0.5
        elif _clear_sky < 0.8:
            return 0.8, 0.3, 45.0, 1.0
        else:
            return None, 0.3, 21.0, 1.0

    @property
    @rounder(2)
    def direct_illuminance(self):
        _c, _, _, _ = self.cloud_coefficients
        _air_mass = self.air_mass
        _et_illuminance = self.et_illuminance
        if _c is None:
            _direct_illuminance = 0
        else:
            _direct_illuminance = _et_illuminance * math.exp(
                -1 * _c * _air_mass)
        logging.info(f"direct_illuminance: {_direct_illuminance}")
        return _direct_illuminance

    @property
    @rounder(2)
    def horizontal_illuminance(self):
        _altitude = self.altitude
        _direct_illuminance = self.direct_illuminance
        _horizontal_illuminance = _direct_illuminance * math.sin(_altitude)
        logging.info(f"horizontal_illuminance: {_horizontal_illuminance}")
        return _horizontal_illuminance

    @property
    @rounder(2)
    def horizontal_sky_illuminance(self):
        _altitude = self.altitude
        _, _A, _B, _C = self.cloud_coefficients
        _sky_illuminance = _A + (_B * (math.sin(_altitude))**_C)
        return _sky_illuminance

    @property
    def daylight_illuminance(self):
        if self.sun_up:
            _sky_illuminance = self.horizontal_sky_illuminance
            _horizontal_illuminance = self.horizontal_illuminance        
            _daylight = (_sky_illuminance + _horizontal_illuminance) * 1000
        else:
            _daylight = 0
        return int(_daylight)

    @property
    def sun_up(self):
        _now = self.timedata.date
        return (self.timedata.timezone.localize(self.sunrise_datetime) <
                _now <
                self.timedata.timezone.localize(self.sunset_datetime))

