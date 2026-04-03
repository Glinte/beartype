#!/usr/bin/env -S python -m beartype
# --------------------( LICENSE                            )--------------------
# Copyright (c) 2014-2026 Beartype authors.
# See "LICENSE" for further details.

'''
Data script passing runtime type-checking under ``python -m beartype``.
'''

# ....................{ IMPORTS                            }....................
from sys import argv

# ....................{ CALLABLES                          }....................
def count_yet_still(i_returned: int) -> str:
    '''Arbitrary well-typed callable exercised by this script.'''

    return str(i_returned)


# ....................{ MAIN                               }....................
if __name__ == '__main__':
    print(count_yet_still(int(argv[1])), end='')
