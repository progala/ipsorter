#!/usr/bin/env python
"""
ipsorter - Sorts IP addresses read from a file, or passed from standard input.

Usage:

- Sort IP addresses read from a file

$ ipsorter random_ips.txt

- Sort IP addresses piped from other program

$ grep "10\.2\." * | ipsorter

- Sort IP addresses redirected from other source

$ ipsorter < random_ips.txt
"""

import re
import sys

__author__ = 'Przemek Rogala'


IPREGEX = re.compile(r'\b(?:\d{1,3}\.){3}\d{1,3}\b')


def ip_sort_key(key):
    """Function used as a sorting key"""
    return '{:>3}{:>3}{:>3}{:>3}'.format(*key.split('.'))


def print_usage():
    """Print usage"""
    print('Usage: ipsorter [FILE]')


def read_and_sort(source):
    """Read lines from stdin/file and sort them"""
    ips = [l.strip() for l in source if IPREGEX.match(l)]
    for ip in sorted(ips, key=ip_sort_key):
        print(ip)


def main():
    # If we are not at tty, take piped, or redirected, input
    if not sys.stdin.isatty():
        read_and_sort(sys.stdin)
    elif len(sys.argv) == 2:
        fname = sys.argv[1]
        try:
            with open(fname) as fp:
                read_and_sort(fp.readlines())
        except IOError:
            print('Error. Unable to read file: {}.'.format(fname))
            raise SystemExit(1)
    else:
        print_usage()


if __name__ == '__main__':
    main()
