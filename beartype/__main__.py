#!/usr/bin/env python3
# --------------------( LICENSE                            )--------------------
# Copyright (c) 2014-2026 Beartype authors.
# See "LICENSE" for further details.

'''
Top-level :mod:`beartype` command-line interface (CLI).

This executable submodule currently supports one command:

.. code-block:: console

   $ python -m beartype /path/to/script.py

which import-hook type-checks and then runs that script in-process.
'''

# ....................{ IMPORTS                            }....................
#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
# WARNING: To avoid polluting the public module namespace, external attributes
# should be locally imported at module scope *ONLY* under alternate private
# names (e.g., "from argparse import ArgumentParser as _ArgumentParser" rather
# than merely "from argparse import ArgumentParser").
#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
from beartype.claw import beartype_package as _beartype_package
from contextlib import chdir as _chdir
from importlib import import_module as _import_module
from pathlib import Path as _Path
from sys import (
    argv as _argv,
    path as _sys_path,
)

# ....................{ PRIVATE ~ runners                  }....................
def _run_script() -> None:
    '''
    Type-check and run the Python script passed on the command line.

    Raises
    ------
    ValueError
        If the caller passed an invalid argument count *or* script basename.
    FileNotFoundError
        If the passed script filename does *not* exist.
    '''

    # If the caller failed to pass exactly one script filename, raise an
    # exception with a terse usage message.
    if len(_argv) != 2:
        raise ValueError(
            '"python -m beartype" passed invalid command-line arguments. '
            'Expected exactly one Python script filename.'
        )

    # Relative or absolute filename of the script to be run under runtime type
    # checking.
    script_filename = _argv[1]

    # "Path" object encapsulating this script, canonicalized into an absolute
    # filename if this script exists *OR* raising a "FileNotFoundError"
    # exception otherwise.
    script_file = _Path(script_filename).resolve(strict=True)

    # Unqualified basename of this script excluding trailing filetype(s).
    script_basename = script_file.stem

    # If this basename is *NOT* a valid Python identifier, fail early with a
    # human-readable exception.
    if not script_basename.isidentifier():
        raise ValueError(
            f'Script filename "{script_file}" has basename '
            f'"{script_basename}" that is not a valid Python identifier.'
        )

    # Absolute dirname of the directory directly containing this script.
    script_dirname = str(script_file.parent)

    # Temporarily change the current working directory (CWD) to this directory.
    with _chdir(script_dirname):
        # Append this directory to the current Python path, enabling this
        # script to be transparently imported as if it were a top-level module.
        _sys_path.append('.')

        # Register this script for type-checking as if it were a package.
        _beartype_package(script_basename)

        # Import this script as a module, running all module scope code.
        _import_module(script_basename)


# ....................{ MAIN                               }....................
if __name__ == '__main__':
    _run_script()
