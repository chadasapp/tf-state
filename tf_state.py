#!/usr/bin/env python3
"""Script to help with (re)moving states.

Usage:
  tf_state.py get STATE
  tf_state.py (rm|remove) STATE
  tf_state.py (mv|move) FROM_PREFIX TO_PREFIX
  tf_state.py plan STATE
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
    elif args['plan']:
        plan(args['STATE'])
    elif args['remove'] or args['rm']:
        remove(args['STATE'])
    elif args['move'] or args['mv']:
        move(args['FROM_PREFIX'], args['TO_PREFIX'])


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


def plan(state):
    """Plan all (or some) of the things."""
    tf_plan = ['terraform', 'plan']
    for target in _state_matches(state):
        tf_plan.append('-target={}'.format(target))
    subprocess.check_call(tf_plan)


def move(from_prefix, to_prefix):
    """Move a state or states."""
    if not from_prefix.endswith('*'):
        print('Moving requires a common prefix, no pattern was specified.')
        sys.exit(1)

    old_to_new = {}
    old_prefix = from_prefix[:-1]
    new_prefix = to_prefix
    if new_prefix.endswith('*'):
        new_prefix = new_prefix[:-1]

    print("The following renamings will occur:")
    for old_state in _state_matches(from_prefix):
        new_state = old_state.replace(old_prefix, new_prefix)
        old_to_new[old_state] = new_state
        print('{} => {}'.format(old_state, new_state))

    if _prompt():
        for old, new in old_to_new:
            subprocess.check_call(['terraform', 'state', 'mv', old, new])

if __name__ == '__main__':
    main()
