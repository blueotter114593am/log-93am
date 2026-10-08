"""Log parsing helper.

Parse simple log lines and output them as JSON.
"""

import sys
import re
import json
import argparse
import datetime

LOG_RE = re.compile(r'^(?P<ts>\S+)\s+(?P<level>\w+)\s+(?P<msg>.+)$')

def parse_line(line: str):
    m = LOG_RE.match(line.strip())
    if not m:
        return None
    ts_str = m.group('ts')
    try:
        ts = datetime.datetime.fromisoformat(ts_str.replace('Z', '+00:00'))
    except ValueError:
        ts = ts_str
    return {
        'timestamp': ts.isoformat() if isinstance(ts, datetime.datetime) else ts,
        'level': m.group('level'),
        'message': m.group('msg')
    }

def filter_entry(entry, level=None):
    if entry is None:
        return False
    return level is None or entry['level'].lower() == level.lower()

def main():
    parser = argparse.ArgumentParser(description='Parse log file and output JSON.')
    parser.add_argument('file', nargs='?', type=argparse.FileType('r'), default=sys.stdin,
                        help='Log file to parse (default: stdin)')
    parser.add_argument('-l', '--level', help='Filter by log level')
    args = parser.parse_args()

    for line in args.file:
        entry = parse_line(line)
        if filter_entry(entry, args.level):
            sys.stdout.write(json.dumps(entry) + '\n')

if __name__ == '__main__':
    main()