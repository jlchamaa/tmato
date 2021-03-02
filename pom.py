#!/usr/bin/env python3.6
import argparse
from datetime import datetime, timedelta
import re
from os.path import expanduser, join, exists
POMO_DIR = join(expanduser("~"), ".pomodoro")
CURRENT_FILE = join(POMO_DIR, "current")
HISTORY_FILE = join(POMO_DIR, "history")


class Pomodoro:
    def __init__(self, start_time, duration):
        self.start_time = start_time
        self.duration = duration
        self.validate()

    @classmethod
    def from_file(cls):
        if not exists(CURRENT_FILE):
            return None
        with open(CURRENT_FILE) as f:
            line = f.readline()
        if line == "":
            return None
        m = re.match("""([\\d\\.]*) dur=([\\d]*)m""", line)
        if not hasattr(m, "groups") or len(m.groups()) < 2:
            print("badline")
            return None

        start_time = datetime.fromtimestamp(float(m.group(1)))
        return Pomodoro(start_time, int(m.group(2)))

    def wipe(self):
        # os.remo(_)
        pass

    def to_file(self):
        t = datetime.timestamp(datetime.now())
        with open(CURRENT_FILE, "w") as f:
            f.write(f"{t} dur={self.duration}m")

    def to_history(self):
        pass

    def validate(self):
        pass

    @property
    def elapsed(self):
        delta = datetime.now() - self.start_time
        return delta

    @property
    def finished(self):
        return self.elapsed > timedelta(minutes=self.duration)

    def __repr__(self):
        return f"Pomodoro started {self.start_time} with length {self.duration}m - Finished: {self.finished} ({self.elapsed})"


def get_current_pomodoro():
    return Pomodoro.from_file()


def parse_args():
    parser = argparse.ArgumentParser(description='Options')
    parser.add_argument('action')
    parser.add_argument('arg', nargs="?")
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
        if current is not None:
            if current.finished:
                current.to_history()
            else:
                print("There's a pomodoro already in progress")
                return
        p = Pomodoro(datetime.now(), args.arg)
        p.to_file()

    elif args.action == "stop":
        if current is not None:
            if current.finished:
                current.to_history()
            else:
                # Pomodoro.wipe()
                print("Ended the Pomodoro")
                return
        print("There's no pomodoro in progress")
        return
    else:
        print("I ain't heard of this action")


if __name__ == "__main__":
    main()
