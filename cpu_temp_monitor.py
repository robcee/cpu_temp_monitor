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
import socket
import redis
import sched, time

_cpu_temp = '/sys/class/thermal/thermal_zone0/temp'

def get_temp():
    with open(_cpu_temp, "r") as f:
        temp = int(f.read())
    
    return temp

def write_to_redis():
    hostname = socket.gethostname()
    temperature = get_temp()
    r = redis.Redis(host='localhost', port=6379, db=0)
    r.set(hostname + '.temperature', temperature / 1000)

def write_to_console():
    temperature = get_temp()
    print(f"{temperature / 1000}℃")

def main(args):
    """ Main entry point of the app """

    freq = args.frequency
    scheduler = sched.scheduler()

    print("cpu_temp_monitor starting up, " + args)

    # First one is free!
    if args.redis:
        # store values in redis
        write_to_redis()
    else:
        write_to_console()

    while freq > 0:
        if args.verbose:
            print("cpu_temp_monitor, scheduler loop tick")
        if args.redis:
            # store values in redis
            scheduler.enter(freq, 1, write_to_redis)
        else:
            scheduler.enter(freq, 1, write_to_console)
        
        scheduler.run()


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
