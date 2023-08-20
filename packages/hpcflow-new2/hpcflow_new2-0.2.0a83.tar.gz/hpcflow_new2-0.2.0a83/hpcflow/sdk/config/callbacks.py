"""Module that defines built-in callback functions for configuration item values."""


import os
import re
import fsspec
from hpcflow.sdk.core.errors import UnsupportedSchedulerError, UnsupportedShellError

from hpcflow.sdk.submission.shells import get_supported_shells


def callback_vars(config, value):
    """Substitute configuration variables."""

    def vars_repl(match_obj):
        var_name = match_obj.groups()[0]
        return config._variables[var_name]

    vars_join = "|".join(list(config._variables.keys()))
    vars_regex = r"\<\<(" + vars_join + r")\>\>"
    value = re.sub(
        pattern=vars_regex,
        repl=vars_repl,
        string=str(value),
    )
    return value


def callback_file_paths(config, file_path):
    if isinstance(file_path, list):
        return [config._resolve_path(i) for i in file_path]
    else:
        return config._resolve_path(file_path)


def callback_bool(config, value):
    if not isinstance(value, bool):
        if value.lower() == "true":
            return True
        elif value.lower() == "false":
            return False
        else:
            raise TypeError(f"Cannot cast {value!r} to a bool type.")
    return value


def callback_lowercase(config, value):
    if isinstance(value, list):
        return [i.lower() for i in value]
    elif isinstance(value, dict):
        return {k.lower(): v for k, v in value.items()}
    else:
        return value.lower()


def exists_in_schedulers(config, value):
    if value not in config.schedulers:
        raise ValueError(
            f"Cannot set default scheduler; {value!r} is not a supported scheduler "
            f"according to the config file, which lists these schedulers as available "
            f"on this machine: {config.schedulers!r}."
        )
    return value


def callback_supported_schedulers(config, schedulers):
    # validate against supported schedulers according to the OS - this won't validate that
    # a particular scheduler actually exists on this system:
    available = config._app.get_OS_supported_schedulers()
    for k in schedulers:
        if k not in available:
            raise UnsupportedSchedulerError(scheduler=k, available=available)

    return schedulers


def callback_supported_shells(config, shell_name):
    supported = get_supported_shells(os.name)
    if shell_name not in supported:
        raise UnsupportedShellError(shell=shell_name, supported=supported)
    return shell_name


def set_callback_file_paths(config, value):
    """Check the file(s) is/are accessible. This is only done on `config.set` (and not on
    `config.get` or `config._validate`) because it could be expensive in the case of remote
    files."""
    value = callback_file_paths(config, value)

    to_check = value
    if not isinstance(value, list):
        to_check = [value]

    for file_path in to_check:
        with fsspec.open(file_path, mode="rt") as fh:
            pass
            # TODO: also check something in it?
        print(f"Checked access to: {file_path}")


def check_load_data_files(config, value):
    """Check data files (e.g. task schema files) can be loaded successfully. This is only
    done on `config.set` (and not on `config.get` or `config._validate`) because it could
    be expensive in the case of remote files."""
    config._app.reload_template_components(warn=False)


def callback_update_log_console_level(config, value):
    config._app.log.update_console_level(value)
