# tf-state

A simple wrapper for `terraform state` that supports glob-style matching.

Written one morning because I was tired of having having to work on lots of states in a single module.

## Usage
* `pip3 install -r requirements.txt`
* Make sure `terraform` is in your `$PATH`
* Consult the help:
```
Usage:
  tf_state.py get STATE
  tf_state.py (rm|remove) STATE
  tf_state.py (mv|move) FROM_STATE TO_STATE
  tf_state.py (-h | --help)
  tf_state.py --version

Options:
  -h --help     Show this screen.
  --version     Show version.
```

## Todo
* Actually implement mv/move

## License
This software is licensed under the Apache license. See LICENSE for details.
