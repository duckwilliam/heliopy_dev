#!/usr/bin/env python3
"""
Classes for Getting and Calculating Data.
General-purpose solar irradiance and brightness calculator.
"""
import logging
import datetime
import re
import functools
import tzlocal
import pytz


def updater(func):
    @functools.wraps(func)
    def wrapper(self, *args, **kwargs):
        print("wrapper start")
        method = func(self, *args, **kwargs)
        print(f"method {func} called")
        for level in self.dependent_attributes.keys():
            for attr in self.dependent_attributes[level]:
                setattr(self, attr, None)
                raise AttributeError(f"The {attr} is None.")\
                    if getattr(self, attr) else None
        return method
    return wrapper


class Time:
    def __init__(self,
                 time_input=None,
                 day_input: str = None,
                 timezone_input: str = None,
                 ):
        self.init_complete = False
        self.time = None if time_input is None else time_input
        self.day = day_input
        self.timezone = timezone_input
        self.dependent_attributes = {}
        self.init_complete = True
        self._date = None
        self._utc_time = None
                
    def append_dependent(self, level, attribute):
        _dic = self.dependent_attributes
        if level not in _dic:
            _dic[level] = [attribute]
        elif attribute not in _dic[level]:
            _dic[level].append(attribute)
            
    @property
    def time(self):
        """
        Gets the time property.
        """
        return self._time
    
   # @updater
    @time.setter
    def time(self, value):
        """
        Sets the time property.
        Args:
            value: The value to set the time property to.
        Raises:
            ValueError: If the time is not in the correct format.
        Examples:
            >>> obj = MyClass()
            >>> obj.time = '12:34:56'
        """
        if value is not None:
            self._time = self.convert_timestr(value)
        else:
            self._time = self.current_time

    @property
    def current_time(self):
        return datetime.datetime.time(datetime.datetime.now())

    def convert_timestr(self, time_string: str):
        re_hhmmss = re.compile('(\d{1,2}:){2}\d{1,2}')
        re_hhmm = re.compile('(\d{1,2}:){1}\d{1,2}$')
        _time_valid = f"{time_string}:00" if re_hhmm.match(
            time_string) is not None else time_string
        if re_hhmmss.match(_time_valid) is None:
            raise ValueError("Time is not in HH:MM:SS format")
        return datetime.datetime.time(datetime.datetime.strptime(
            _time_valid, "%H:%M:%S"))
    
    
    @property
    def day(self):
        return self._day
    
 #  @updater
    @day.setter
    def day(self, value):
        if value is not None:
            print(f"value is not None, value is {value}")
            print(type(value)) 
            self._day = self.convert_daystr(value)
        else:
            self._day = self.current_day
        
    @property
    def current_day(self):
        return datetime.datetime.date(datetime.datetime.now())

    def convert_daystr(self, day_string: str):
        re_yyyymmdd = re.compile(
            '^\d{4}\-(0[1-9]|1[012])\-(0[1-9]|[12][0-9]|3[01])$')
        if re_yyyymmdd.match(day_string) is None:
            raise ValueError("Date is not in yyyy-mm-dd format")
        return datetime.datetime.time(datetime.datetime.strptime(
            day_string, "%y-%m-%d"))

    @property
    def timezone(self):
        return self._timezone
    
  #  @updater
    @timezone.setter
    def timezone(self, value):
        _timezone_set = value if value is not None else tzlocal.get_localzone().key
        self._timezone = _timezone_set if isinstance(
            _timezone_set, pytz.BaseTzInfo) else pytz.timezone(_timezone_set)
        # self._date = None
        # self.__refresh_date__ = self.date if self.init_complete else None
        
    @property
    def date(self):
        if self._date is None:
            self.date = datetime.datetime.combine(self.day, self.time)
        return self._date

    @date.setter
    def date(self, value):
        self._date = self.timezone.localize(value)
        self.append_dependent(1, 'date')
        
    @property
    def utc_time(self):
        if self._utc_time is None:
            self.utc_time = self.date
        return self._utc_time
    
    @utc_time.setter
    def utc_time(self, value):
        self._utc_time = value.astimezone(pytz.utc)
        self.append_dependent(2, 'utc_time')
    
    @property
    def day_of_the_year(self):
        """
         @brief Returns the day of the year. It is defined as the number of days since January 1 1970 00 : 00 : 00.
         @return a tuple of the form ( year month day )
        """
        _date_object = self.date
        _day_of_the_year = _date_object.timetuple().tm_yday
        logging.info(f"calculated day of the year: {_day_of_the_year}")
        return _day_of_the_year