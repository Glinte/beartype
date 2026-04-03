#!/usr/bin/env python3
# --------------------( LICENSE                            )--------------------
# Copyright (c) 2014-2026 Beartype authors.
# See "LICENSE" for further details.

'''
Data script passing runtime type-checking under ``python -m beartype``.
'''

# ....................{ CALLABLES                          }....................
def count_yet_still(i_returned: int) -> str:
    '''Arbitrary well-typed callable exercised by this script.'''

    return str(i_returned)


# ....................{ MAIN                               }....................
print(count_yet_still(23), end='')
