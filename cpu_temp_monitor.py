#!python

__desc__ = """
cpu_temp_monitor: display or store system CPU temperature on stdout or Redis.

USAGE: python cpu_temp_monitor [-r|--redis] [-f|--frequency seconds] -h|--help

-r, --redis: (optional) log values to redis, otherwise stdout
-f, --frequency: (optional) number of seconds between samples, if omitted, run once and exit.
"""

__author__ = "Rob Campbell"
__version__ = "0.1.0"
__license__ = "MIT"

import argparse

_cpu_temp = '/sys/class/thermal/thermal_zone0/temp'

def get_temp():
    with open(_cpu_temp, "r") as f:
        temp = int(f.read())
    
    return temp

def main(args):
    """ Main entry point of the app """

    temperature = get_temp()
    
    if args.redis:
        # store values in redis
        print(f"{temperature / 1000}℃   tbd")
    else:
        print(f"{temperature / 1000}℃")
    
    # print(args)


if __name__ == "__main__":
    """ This is executed when run from the command line """
    parser = argparse.ArgumentParser(usage=__desc__)

    # Optional argument flag which defaults to False
    parser.add_argument("-r", "--redis", help="store values in redis", action="store_true")

    # Optional argument which requires a parameter (eg. -d test)
    parser.add_argument("-f", "--frequency", help="set frequency in seconds, if omitted, run once and exit", type=int, default=0)

       # Specify output of "--version"
    parser.add_argument(
        "--version",
        action="version",
        version="%(prog)s (version {version})".format(version=__version__))

    args = parser.parse_args()
    main(args)
