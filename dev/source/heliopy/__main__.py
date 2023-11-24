import argparse
from builder import main as build

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Scratchpad Testcript")
    parser.add_argument(
        "-c",
        "--city",
        type=str,
        help="City to be used as location (e.g. 'Vienna'),\
            if none is provided, current date will be used",
        default=None,
        required=True)
    parser.add_argument(
        "-C",
        "--country",
        type=str,
        help="Country to be used as location (e.g. 'Austria'),\
            if none is provided, will try to use city only",
        default=None)
    parser.add_argument(
        "-P",
        "--print",
        type=bool,
        help="Print output to stdout",
        default=False)
    parser.add_argument(
        "-d",
        "--day",
        help="Date as YYYY-MM-DD,\
            if none is provided, current date will be used")
    parser.add_argument(
        "-t",
        "--time",
        help="Time as hh:mm:ss,\
            if none is provided, current time will be used")
    parser.add_argument(
        "-tz",
        "--timezone",
        type=str,
        help="Timezone as\
            [REGION/CITY], if none is provided,\
                local timezone will be used.")
    parser.add_argument(
        "-k",
        "--api_key",
        type=str,
        help="OpenWeatherMap API key as string. \
            Alternatively a path to api_key.txt \
                can be provided (use -p [path])\
                    If neither is provided, will try \
                        to look for 'OPENWEATHERMAP_API_KEY' \
                            in OS environment")
    parser.add_argument(
        "-p",
        "--key_path",
        type=str,
        help="Location of the api_key.txt file \
            containing the \
                OpenWeatherMap API key. \
                    Alternatively an API key can be \
                        provided (use -k [API-KEY])\
                            If neither is provided, will try \
                                to look for 'OPENWEATHERMAP_API_KEY' \
                                    in OS environment")

    args = parser.parse_args()
    build(city=args.city,
          time=args.time,
          day=args.day,
          country=args.country,
          timezone=args.timezone,
          api_key_path=args.key_path,
          api_key=args.api_key,
          text=args.print)
