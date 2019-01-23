#!/usr/bin/env python3
"""Script to help with (re)moving states.

Usage:
  tf_state.py get STATE
  tf_state.py (rm|remove) STATE
  tf_state.py (mv|move) FROM_STATE TO_STATE
  tf_state.py (-h | --help)
  tf_state.py --version

Options:
  -h --help     Show this screen.
  --version     Show version.
"""

import fnmatch
import subprocess
import sys

from docopt import docopt

__version__ = '0.1'


def main():
    """Do the main entry functions."""
    args = docopt(__doc__, version=__version__)
    if args['get']:
        get(args['STATE'])
    elif args['remove'] or args['rm']:
        remove(args['STATE'])
    elif args['move'] or args['mv']:
        move(args['FROM_STATE'], args['TO_STATE'])


def _prompt():
    """Prompt yes/no."""
    while True:
        sys.stdout.write('Do you wish to continue? [y/N] ')
        choice = input().lower()
        if choice in ['y', 'ye', 'yes']:
            return True
        if choice in ['n', 'no', '']:
            return False
        sys.stdout.write('Please respond with "yes" or "no" '
                         '(or "y" or "n").\n')


def _state_matches(state):
    """Get all states matching a pattern."""
    output = subprocess.check_output(
        ['terraform', 'state', 'list']).decode('utf-8').splitlines()
    state_list = fnmatch.filter(output, state)
    if not state_list:
        print('No state exists')
        sys.exit(1)
    return state_list


def get(state):
    """Print all states matching a pattern."""
    state_list = _state_matches(state)
    for match in state_list:
        print(match)


def remove(state):
    """Remove a state or states."""
    state_list = _state_matches(state)
    print('Removing the following states: {}'.format(', '.join(state_list)))
    if _prompt():
        rm_cmd = ['terraform', 'state', 'rm']
        rm_cmd.extend(state_list)
        subprocess.check_call(rm_cmd)
        print('Done')
        sys.exit(0)


def move(from_state, to_state):
    """Move a state or states."""
    state_list = _state_matches(from_state)


if __name__ == '__main__':
    main()
