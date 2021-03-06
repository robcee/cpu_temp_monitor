#!python


"""
cpu_temp_monitor: display or store system CPU temperature on stdout or Redis at [hostname].cpu.temperature.

version 0.2.0: added hostname.uptime to stored information.
"""

__desc__ = """
cpu_temp_monitor: display or store system CPU temperature on stdout or Redis at [hostname].cpu.temperature.

USAGE: python cpu_temp_monitor [-r|--redis] [-f|--frequency seconds] -h|--help

-r, --redis: (optional) log values to redis, otherwise stdout
-f, --frequency: (optional) number of seconds between samples, if omitted, run once and exit.
"""

__author__ = "Rob Campbell"
__version__ = "0.2.0"
__license__ = "The Unlicense"

import argparse
import socket
import redis
import sched, time
import math
import subprocess

_cpu_temp = '/sys/class/thermal/thermal_zone0/temp'

def get_uptime():
    completedProcess = subprocess.run("uptime", capture_output=True, text=True)
    return completedProcess.stdout.strip()

def get_temp():
    with open(_cpu_temp, "r") as f:
        temp = int(f.read())
    
    return temp / 1000

def write_to_redis():
    hostname = socket.gethostname()
    temperature = get_temp()
    uptime = get_uptime()
    r = redis.Redis(host='localhost', port=6379, db=0)
    r.set(hostname + '.cpu.temperature', temperature)
    r.set(hostname + '.cpu.temperature.time', math.floor(time.time()))
    r.set(hostname + '.uptime', uptime)

def write_to_console():
    temperature = get_temp()
    uptime = get_uptime()
    print(f"{temperature}℃")
    print(uptime)

def main(args):
    """ Main entry point of the app """

    freq = args.frequency
    scheduler = sched.scheduler()

    if args.redis:
        action = write_to_redis
    else:
        action = write_to_console

    print("cpu_temp_monitor starting up")
    print(args)

    # First one is free!
    action()

    while freq > 0:
        # print("cpu_temp_monitor, scheduler loop tick")
        scheduler.enter(freq, 1, action)
        
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
