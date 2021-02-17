#!/usr/bin/env python3.6
import argparse
import datetime
import re
from os.path import expanduser, join, exists
pomo_dir = join(expanduser("~"), ".pomodoro")


class Pomodoro:
    @classmethod
    def from_file(cls):
        current_file = join(pomo_dir, "current")
        if not exists(current_file):
            return None
        with open(current_file) as f:
            line = f.readline()
        if line == "":
            return None
        m = re.match("""([\\d\\.]*) dur=([\\d]*)m""", line)
        if len(m.groups()) < 2:
            print("badline")
        start_time = datetime.datetime.fromtimestamp(float(m.group(1)))
        return Pomodoro(start_time, m.group(2))

    def __init__(self, start_time, duration):
        self.start_time = start_time
        self.duration = duration

    def __repr__(self):
        return f"Pomodoro started {self.start_time} with length {self.duration}m"


def get_current_pomodoro():
    return Pomodoro.from_file()


def parse_args():
    parser = argparse.ArgumentParser(description='Options')
    parser.add_argument('action')
    return parser.parse_args()


def main():
    args = parse_args()
    current = get_current_pomodoro()
    if args.action == "status":
        if current is None:
            print("No current Pomodoro")
        else:
            print(current)
    elif args.action == "start":
        pass
    elif args.action == "stop":
        pass
    else:
        print("I ain't heard of this action")


if __name__ == "__main__":
    main()
