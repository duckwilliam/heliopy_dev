#!/usr/bin/env python3
"""
General-purpose solar irradiance and brightness calculator.
"""
import logging
import math
import datetime


class Sun:
    """
    Class Illuminaion:
    Calculate Outside Illumination in Lux
    for given location and time
    """
 
    def __init__(self,
                 latitude: float, 
                 longitude: float,
                 date: datetime.datetime,
                 date_utc: datetime.datetime,
                 day_of_the_year: int,
                 cloud_coverage: int,
                 timezone
                 ):
        self.latitude = latitude
        self.longitude = longitude
        self.date = date
        self.date_utc = date_utc
        self.day_of_the_year = day_of_the_year
        self.cloud_coverage = cloud_coverage
        self.timezone = timezone

    def rounder(self, number: float, decimals: int):
        """
        Rounds a number to a specific number of decimals.
        """
        return round(number+10**(-len(str(number))-1), decimals)

    @property
    def utc_time_delta(self):
        delta = self.date - self.date_utc
        delta_seconds = delta.total_seconds() 
        delta_hours = divmod(delta_seconds, 3600)[0]
        return int(delta_hours)

    @property
    def hour(self):
        return int(self.date.strftime('%-H')) 
        
    @property
    def day(self):
        return self.date.date()
        

    @property
    def et_illuminance(self):
        """
        Returns the ET Illuminance in Lux
        based on time of the year.
        """
        _day_of_the_year = self.day_of_the_year
        _et_illuminance = float(129) * (1 + 0.034 * math.cos(((
            2 * math.pi)/356) * (_day_of_the_year - 2)))
        logging.info(f'calculated extraterrestrial_illuminance: {_et_illuminance}')
        return self.rounder(_et_illuminance, 2)

    @property
    def local_standard_time_meridian_rad(self):
        """
        calculates local standard time meridian
        """
        _lstm_rad = math.radians(15) * self.utc_time_delta
        return self.rounder(_lstm_rad, 2)

    @property
    def equation_of_time_rad(self):
        _doy = self.day_of_the_year
        _B_rad = math.radians((360/365) * (_doy - 81))
        _eot_rad = 9.87 * math.sin(
            2 * _B_rad) - 7.53 * math.cos(
                _B_rad) - 1.5 * math.sin(
                    _B_rad)
                
        return self.rounder(_eot_rad, 2)

    @property
    def time_correction_factor_rad(self):
        _eot_rad = self.equation_of_time_rad
        _lsmt_rad = self.local_standard_time_meridian_rad
        long_rad = math.radians(self.longitude)
        _tcf_rad = 4 * (long_rad - _lsmt_rad) + _eot_rad
        return self.rounder(_tcf_rad, 2)

    @property
    def local_solar_time_rad(self):
        _lt = self.hour
        _tcf_rad = self.time_correction_factor_rad
        _lst = _lt + (_tcf_rad / 60)
        return self.rounder(_lst, 2)

    @property
    def hour_angle_rad(self):
        _lst = self.local_solar_time_rad
        _hra_rad = math.radians(15) * (_lst - 12)
        return self.rounder(_hra_rad, 2)

    @property
    def declination_angle_rad(self):
        _doy = self.day_of_the_year
        _da_rad = math.radians(-23.45) * math.cos(
            math.radians((360/365) * (_doy + 10)))
        return self.rounder(_da_rad, 2)

    @property
    def sun_extr(self):
        _lat = math.radians(self.latitude)
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
        _sunrise = datetime.datetime.combine(self.day, datetime.datetime.min.time()) + sunrise_hour_td
        return _sunrise
      
    @property
    def sunset_datetime(self):
        
        _tcf_rad = self.time_correction_factor_rad
        _hra = self.sun_extr
        sunset_hour = (_hra / math.radians(15)) - (_tcf_rad / 60) + 12
        sunset_hour_td = datetime.timedelta(seconds=sunset_hour * 3600)
        _sunset = datetime.datetime.combine(self.day, datetime.datetime.min.time()) + sunset_hour_td
        return _sunset

    @property
    def altitude(self):
        """
        Calculates the solar altitude for a given longitude, date and time.
        Returns solar altitude in degrees.
        """
        _lat_rad = math.radians(self.latitude)
        _hra_rad = self.hour_angle_rad
        _da_rad = self.declination_angle_rad
        _alt_rad = math.asin(math.sin(_da_rad) * math.sin(
            _lat_rad) + math.cos(
                _da_rad) * math.cos(
                    _lat_rad) * math.cos(
                        _hra_rad))
        _alt_deg = math.degrees(_alt_rad)
        logging.info(f"altitude: {_alt_deg}")
        return self.rounder(_alt_deg, 2)

    @property 
    def solar_azimuth(self):
        _lat_rad = math.radians(self.latitude)
        _alt_rad = math.radians(self.altitude)
        _hra_rad = self.hour_angle_rad
        _da_rad = self.declination_angle_rad
        _azi_rad = math.acos(
            ((math.sin(_da_rad) * math.cos(_lat_rad)) - (
                math.cos(_da_rad) * math.sin(
                    _lat_rad) * math.cos(
                        _hra_rad))) / math.cos(_alt_rad))
        _azi_deg = math.degrees(_azi_rad)
        return self.rounder(_azi_deg, 2)

    @property
    def clear_sky(self):
        """
        calculate clear sky index from cloud cover
        """
        cloud_fraction = self.cloud_coverage / 100
        cloud_oct = 1.0882 if cloud_fraction == 1 else cloud_fraction
        csi = 0.75 * (cloud_oct)**3.4
        return self.rounder(csi, 2)

    @property
    def irradiance_clear(self):
        """
        Calculates solar irradiance for clear skies 
        """
        _alt_rad = self.altitude
        _irradiance_clear = 910 * math.sin(_alt_rad) - 30
        return self.rounder(_irradiance_clear, 2)


    @property
    def irradiance_cloud(self):
        """
        calculates solar irradiance for given 
        cloud level 
        """
        _irradiance_clear = self.irradiance_clear
        _csi = self.clear_sky
        _irradiance_cloud = _irradiance_clear * (1 - _csi) 
        return self.rounder(_irradiance_cloud, 2)

    @property
    def air_mass(self):
        """
        Calculates the air mass for a given solar altitude.
        """
        _altitude = self.altitude
        _am_rad = 1/(
            math.cos(
                math.radians(
                    90 - _altitude)) + 0.50572/(
                        96.07995 - math.radians(
                            90 - _altitude))**1.6364)
        logging.info(f"air_mass: {_am_rad}")
        return self.rounder(_am_rad, 2)

    @property
    def cloud_coefficients(self):
        """
        Gets current cloud coverage from OpenWeather API and
        uses it to set coefficients for later calculation.
        """
        _clear_sky = self.clear_sky
        if _clear_sky < 0.3:
            _cloud_coefficients = {
                "c": 0.21,
                "A": 0.8,
                "B": 15.5,
                "C": 0.5
            }
        elif _clear_sky < 0.8:
            _cloud_coefficients = {
                "c": 0.8,
                "A": 0.3,
                "B": 45.0,
                "C": 1.0
            }
        else:
            _cloud_coefficients = {
                "c": None,
                "A": 0.3,
                "B": 21.0,
                "C": 1.0
            }
        logging.info(f"cloud_coefficients: {_cloud_coefficients}")
        return _cloud_coefficients

    @property
    def direct_illuminance(self):
        """
        converts extraterrestrial illuminance into
        direct illuminance by factoring in air mass and atmospheric
        extinction, estimated by cloud coverage.
        """
        _c = self.cloud_coefficients.get('c')
        _air_mass = self.air_mass
        _et_illuminance = self.et_illuminance
        if _c is None:
            _direct_illuminance = 0
        else:
            _direct_illuminance = _et_illuminance * math.exp(
                -1 * _c * _air_mass)
        logging.info(f"direct_illuminance: {_direct_illuminance}")
        return self.rounder(_direct_illuminance, 2)

    @property
    def horizontal_illuminance(self):
        """
        converts direct illuminance into horizontal illuminence
        by taking into account the current solar altitude.
        """
        _altitude = self.altitude
        _direct_illuminance = self.direct_illuminance
        _horizontal_illuminance = _direct_illuminance * math.sin(_altitude)
        logging.info(f"horizontal_illuminance: {_horizontal_illuminance}")
        return self.rounder(_horizontal_illuminance, 2)

    @property
    def horizontal_sky_illuminance(self):
        """
          @brief Returns the illuminance of the sky. This is defined as A + B * ( sin ( theta ) ** C )) where theta is the altitude in degrees. The coefficients A B and C are used to calculate the illuminance.
          @return sky illuminance as a floating point number
        """         
        _altitude_temp = self.altitude
        # This function sets the altitude to the given value.
        if isinstance(_altitude_temp, float):
            _altitude = _altitude_temp
        else:
            _altitude = float(_altitude_temp)

        _coefficients = self.cloud_coefficients
        _A_temp = _coefficients.get('A')
        _B_temp = _coefficients.get('B')
        _C_temp = _coefficients.get('C')
        # float _C_temp float _C_temp float _C_temp
        _A = _A_temp if isinstance(_A_temp, float) else float(_A_temp)
        _B = _B_temp if isinstance(_B_temp, float) else float(_B_temp)
        _C = _C_temp if isinstance(_C_temp, float) else float(_C_temp)
        _sky_illuminance = _A + (_B * (math.sin(_altitude))**_C)
        return self.rounder(_sky_illuminance, 2)

    @property
    def daylight_illuminance(self):
        """
        @brief Returns the illuminance of the sky. This is defined as A + B * ( sin ( theta ) ** C )) where theta is
        the altitude in degrees. The coefficients A B and C are used to calculate the illuminance.
        @return sky illuminance as a floating point number
        """
        if self.sun_up is True:
            _sky_illuminance = self.horizontal_sky_illuminance
            _horizontal_illuminance = self.horizontal_illuminance        
            _daylight = (_sky_illuminance + _horizontal_illuminance) * 1000
        elif self.sun_up is False:
            _daylight = 0
        else:
            raise ValueError("Invalid value for day.")
        return int(self.rounder(number=_daylight, decimals=0))
        
       
    @property
    def sun_up(self):
        _rise: datetime = self.timezone.localize(self.sunrise_datetime) 
        _set: datetime = self.timezone.localize(self.sunset_datetime) 
        _now = self.date
        return _rise < _now < _set
      