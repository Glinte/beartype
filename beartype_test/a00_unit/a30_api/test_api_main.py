#!/usr/bin/env python3
# --------------------( LICENSE                            )--------------------
# Copyright (c) 2014-2026 Beartype authors.
# See "LICENSE" for further details.

'''
Top-level :mod:`beartype` CLI unit tests.
'''

# ....................{ IMPORTS                            }....................
#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
# WARNING: To raise human-readable test errors, avoid importing from
# package-specific submodules at module scope.
#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

# ....................{ TESTS                              }....................
def test_api_main_script_pass() -> None:
    '''
    Test that ``python -m beartype`` type-checks and successfully runs a script
    with valid runtime usage.
    '''

    # ....................{ IMPORTS                        }....................
    # Defer test-specific imports.
    from beartype._util.py.utilpyinterpreter import (
        get_interpreter_command_words)
    from beartype_test._util.command.pytcmdrun import (
        run_command_forward_stderr_return_stdout)
    from beartype_test._util.path.pytpathtest import get_test_unit_data_dir

    # ....................{ LOCALS                         }....................
    # Absolute dirname containing the data scripts exercised by this test.
    script_dir = get_test_unit_data_dir() / 'api' / 'standard' / 'main'

    # Absolute filename of the passing script exercised by this test.
    script_filename = str(script_dir / 'script_pass.py')

    # ....................{ PASS                           }....................
    # Assert this command emits the expected script output.
    assert run_command_forward_stderr_return_stdout(
        command_words=(
            get_interpreter_command_words() +
            ('-m', 'beartype', script_filename)
        )) == '23'


def test_api_main_script_fail() -> None:
    '''
    Test that ``python -m beartype`` fails when a script violates a type hint.
    '''

    # ....................{ IMPORTS                        }....................
    # Defer test-specific imports.
    from beartype._util.py.utilpyinterpreter import (
        get_interpreter_command_words)
    from beartype_test._util.command.pytcmdrun import (
        run_command_return_stdout_stderr)
    from beartype_test._util.path.pytpathtest import get_test_unit_data_dir
    from pytest import raises
    from subprocess import CalledProcessError

    # ....................{ LOCALS                         }....................
    # Absolute dirname containing the data scripts exercised by this test.
    script_dir = get_test_unit_data_dir() / 'api' / 'standard' / 'main'

    # Absolute filename of the failing script exercised by this test.
    script_filename = str(script_dir / 'script_fail.py')

    # ....................{ FAIL                           }....................
    # Assert this command fails with the expected violation in captured stderr.
    with raises(CalledProcessError) as exception_info:
        run_command_return_stdout_stderr(command_words=(
            get_interpreter_command_words() +
            ('-m', 'beartype', script_filename)
        ))

    assert 'BeartypeCallHintParamViolation' in exception_info.value.stderr
