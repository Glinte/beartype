#!/usr/bin/env -S python -m beartype
# --------------------( LICENSE                            )--------------------
# Copyright (c) 2014-2026 Beartype authors.
# See "LICENSE" for further details.

'''
Data script failing runtime type-checking under ``python -m beartype``.
'''

# ....................{ IMPORTS                            }....................
from sys import argv

# ....................{ CALLABLES                          }....................
def swallowed_in_vastness(but_what_art_thou: int) -> str:
    '''Arbitrary well-typed callable intentionally called incorrectly.'''

    return str(but_what_art_thou)


# ....................{ MAIN                               }....................
if __name__ == '__main__':
    print(swallowed_in_vastness(argv[1]), end='')
