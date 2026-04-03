#!/usr/bin/env python3
# --------------------( LICENSE                            )--------------------
# Copyright (c) 2014-2026 Beartype authors.
# See "LICENSE" for further details.

'''
Top-level :mod:`beartype` command-line interface (CLI).

This executable submodule currently supports one command:

.. code-block:: console

   $ python -m beartype /path/to/script.py [script-args...]

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
from collections.abc import Iterator as _Iterator
from contextlib import contextmanager as _contextmanager
from os import (
    chdir as _os_chdir,
    getcwd as _os_getcwd,
)
from pathlib import Path as _Path
from runpy import run_module as _run_module
from sys import (
    argv as _argv,
    path as _sys_path,
)

# ....................{ PRIVATE ~ contextmanagers          }....................
@_contextmanager
def _chdir(dirname: str) -> _Iterator[None]:
    '''
    Temporarily change the current working directory (CWD) to ``dirname``.

    This private fallback intentionally avoids :func:`contextlib.chdir`, which
    only exists under Python >= 3.11, while preserving equivalent semantics for
    all Python versions currently supported by :mod:`beartype`.
    '''

    dirname_prior = _os_getcwd()

    try:
        _os_chdir(dirname)
        yield
    finally:
        _os_chdir(dirname_prior)


# ....................{ PRIVATE ~ runners                  }....................
def _run_script() -> None:
    '''
    Type-check and run the Python script passed on the command line.

    This runner preserves script-like semantics by forwarding all remaining
    command-line arguments and executing the script under ``__main__``.

    Raises
    ------
    ValueError
        If the caller passed an invalid argument count *or* script basename.
    FileNotFoundError
        If the passed script filename does *not* exist.
    '''

    # If the caller failed to pass at least one script filename, raise an
    # exception with a terse usage message.
    if len(_argv) < 2:
        raise ValueError(
            '"python -m beartype" passed invalid command-line arguments. '
            'Expected one Python script filename followed by optional '
            'script arguments.'
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

    # Absolute filename and optional arguments of this script. Assigning this
    # list to "sys.argv" preserves common script CLI expectations, including
    # shebang style invocation.
    _argv[:] = [str(script_file), *_argv[2:]]

    # Temporarily change the current working directory (CWD) to this directory.
    with _chdir(script_dirname):
        # Prepend this directory to the current Python path, enabling this
        # script to be transparently imported as if it were a top-level module.
        _sys_path.insert(0, '.')

        # Register this script for type-checking as if it were a package.
        _beartype_package(script_basename)

        # Run this script as if from command line under "__main__" semantics.
        _run_module(script_basename, run_name='__main__', alter_sys=True)


# ....................{ MAIN                               }....................
if __name__ == '__main__':
    _run_script()
