#!/usr/bin/env python3
# --------------------( LICENSE                            )--------------------
# Copyright (c) 2014-2026 Beartype authors.
# See "LICENSE" for further details.

'''
Data script failing runtime type-checking under ``python -m beartype``.
'''

# ....................{ CALLABLES                          }....................
def swallowed_in_vastness(but_what_art_thou: int) -> str:
    '''Arbitrary well-typed callable intentionally called incorrectly.'''

    return str(but_what_art_thou)


# ....................{ MAIN                               }....................
print(swallowed_in_vastness('A chaos of hard clay and glittering sand.'), end='')
