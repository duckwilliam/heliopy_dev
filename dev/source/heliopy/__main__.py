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
                        help="Date as YYYY-MM-DD,\
                            if none is provided, current date will be used",
                        )
    parser.add_argument("-t",
                        "--time",
                        help="Time as hh:mm:ss,\
                            if none is provided, current time will be used"
                        )
    parser.add_argument("-tz",
                        "--timezone",
                        type=str,
                        help="Timezone as\
                            [REGION/CITY], if none is provided,\
                                local timezone will be used.")

    args = parser.parse_args()

    build(city=args.city,
          time=args.time,
          day=args.day,
          country=args.country,
          timezone=args.timezone)
