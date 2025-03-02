#!/usr/bin/env python3

"""
Runs the Game!
"""

import argparse
import logging
import sys

import Game

def setup_logging(args):
    log_level = logging.ERROR  # Default log level
    if args.verbose == 1:
        log_level = logging.WARNING
    elif args.verbose == 2:
        log_level = logging.INFO
    elif args.verbose == 3:
        log_level = logging.DEBUG
    elif args.verbose > 3:
        log_level = logging.NOTSET

    log_format = '%(asctime)s - %(levelname)s: %(message)s'
    if args.logfile:
        logging.basicConfig(filename=args.logfile, level=log_level, format=log_format)
    else:
        logging.basicConfig(stream=sys.stdout, level=log_level, format=log_format)

def main():
    parser = argparse.ArgumentParser(description="Jetpack-Man Game")
    parser.add_argument('-v', '--verbose', action='count', default=0, help="Increase verbosity level (use -vv for more, -vvv for even more)")
    parser.add_argument('-l', '--logfile', type=str, help="Log to a file instead of stdout")

    args = parser.parse_args()
    setup_logging(args)

    game = Game.Game()

if __name__ == "__main__":
    main()
