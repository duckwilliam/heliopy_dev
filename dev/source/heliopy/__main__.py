
import argparse
from builder import main as build

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Scratchpad Testcript")
    parser.add_argument("-c",
                        "--city",
                        type=str,
                        help="City to be used as location (e.g. 'Vienna'),\
                            if none is provided, current date will be used",
                        default=None,
                        required=True
                        )
    parser.add_argument("-C",
                        "--country",
                        type=str,
                        help="Country to be used as location (e.g. 'Austria'),\
                            if none is provided, will try to use city only",
                        default=None
                        )
    parser.add_argument("-d",
                        "--day",
                        type=str,
                        help="Date as YYYY-MM-DD,\
                            if none is provided, current date will be used",
                        default=None
                        )
    parser.add_argument("-t",
                        "--time",
                        type=str,
                        help="Time as hh:mm:ss,\
                            if none is provided, current time will be used",
                        default=None
                        )
    parser.add_argument("-tz",
                        "--timezone",
                        type=str,
                        help="Timezone as\
                            [REGION/CITY], if none is provided,\
                                local timezone will be used.")
    
    args = parser.parse_args()
    _city = args.city
    _country = args.country
    _day = args.day
    _time = args.time
    _timezone = args.timezone
    
    build(city=_city,
          time=_time,
          day=_day,
          country=_country,
          timezone=_timezone)
    