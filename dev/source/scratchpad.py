import re
from datetime import datetime
import argparse
import tzlocal
import pytz


current_day = datetime.date(datetime.now())
current_time = datetime.time(datetime.now())


def get_local_timezone(timezone: str = None):
    """
    Takes timezone string and returns pytz timezone object. 
    If no timezone is specified, it will return the local timezone.
    """
    _timezone = tzlocal.get_localzone().key if timezone is None else timezone
    return pytz.timezone(_timezone)


def assign_timezone(date: datetime, timezone):
    """
    Takes date as datetime object and assigns it a timezone.
    Returns datetime object with timezone.
    """
    return timezone.localize(date)


def get_utc_time(local_date: datetime):
    """
    Shows converts date as datetime object to UTC.
    Returns UTC time as datetime object.
    """
    return local_date.astimezone(pytz.utc)


def main(date: datetime, local_timezone: str = None):
    """
    Main function, runs all other functions.
    """
    _local_timezone = get_local_timezone(local_timezone) if local_timezone is\
        not None else get_local_timezone()
    date_with_timezone = assign_timezone(date, _local_timezone)
    utc_time = get_utc_time(date_with_timezone)
    print(f"Local Time: {date_with_timezone}")
    print(f"UTC Time: {utc_time}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Scratchpad Testcript")
    parser.add_argument("-d",
                        "--date",
                        type=str,
                        help="Date as YYYY-MM-DD,\
                            if none is provided, current date will be used",
                        default=current_day.strftime("%Y-%m-%d")
                        )
    parser.add_argument("-t",
                        "--time",
                        type=str,
                        help="Time as hh:mm:ss,\
                            if none is provided, current time will be used",
                        default=current_time.strftime("%H:%M:%S")
                        )
    parser.add_argument("-tz", "--timezone", type=str, help="Timezone as\
        [REGION/CITY], if none is provided, local timezone will be used.")
    args = parser.parse_args()
    re_hhmmss = re.compile('(\d{1,2}:){2}\d{1,2}')
    re_hhmm = re.compile('(\d{1,2}:){1}\d{1,2}$')
    _time_valid = f"{args.time}:00" if re_hhmm.match(args.time) is not None\
        else args.time
    _day = datetime.strptime(args.date, "%Y-%m-%d")
    if re_hhmmss.match(_time_valid) is None:
        raise ValueError("Time is not in HH:MM:SS format")
    _time = datetime.time(datetime.strptime(_time_valid, "%H:%M:%S"))
    _date = datetime.combine(_day, _time)
    timezone = args.timezone if args.timezone is not None else None
    main(_date, timezone)
