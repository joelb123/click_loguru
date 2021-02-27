# -*- coding: utf-8 -*-
"""Test click_loguru via the simple.py app."""
import functools
import os
from pathlib import Path

from click.testing import CliRunner
from . import cli

MEMORY_QUANTUM_MB = 25


def print_docstring():
    """Decorator to print a docstring."""

    def decorator(func):
        """Define decorator"""

        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            """Print docstring and call function"""
            print(func.__doc__)
            return func(*args, **kwargs)

        return wrapper

    return decorator


def level_checker(logfile_path):
    """Check for expected messages at different log levels."""
    with logfile_path.open("r") as filehandle:
        line_no = 0
        for line in filehandle.read().split("\n"):
            if line_no == 3:
                assert "debug message" in line
            elif line_no == 4:
                assert "info message" in line
            elif line_no == 5:
                assert "warning message" in line
            elif line_no == 6:
                assert "error message" in line
            line_no += 1


@print_docstring()
def test_help():
    """Test help command."""
    runner = CliRunner()
    result = runner.invoke(cli, [])
    assert result.exit_code == 0
    print(result.output)


@print_docstring()
def test_version():
    """Test show_context command."""
    runner = CliRunner()
    result = runner.invoke(cli, ["--version"])
    assert result.exit_code == 0


@print_docstring()
def test_show_context():
    """Test show_context command."""
    runner = CliRunner()
    result = runner.invoke(cli, ["show-context"])
    assert result.exit_code == 0


@print_docstring()
def test_levels(tmp_path):
    """Test logging to a data file."""
    runner = CliRunner()
    os.chdir(tmp_path)
    result = runner.invoke(cli, ["levels"])
    logfile_path = Path(result.output.split("\n")[-2].split()[1])
    assert result.exit_code == 0
    assert len(list(Path("tests/data/logs").glob("*"))) == 1
    level_checker(logfile_path)


@print_docstring()
def test_quiet(tmp_path):
    """Test query of global quiet option."""
    runner = CliRunner()
    os.chdir(tmp_path)
    result = runner.invoke(cli, ["quiet-value"])
    assert result.exit_code == 0
    assert not bool(int(result.output))
    result = runner.invoke(cli, ["-q", "quiet-value"])
    assert result.exit_code == 0
    assert bool(int(result.output))


@print_docstring()
def test_retention(tmp_path):
    """Test keeping copies of the log file."""
    runner = CliRunner()
    os.chdir(tmp_path)
    log_count = 0
    while log_count < 10:
        result = runner.invoke(cli, ["levels"])
        assert result.exit_code == 0
        log_count += 1
    assert len(list(Path("tests/data/logs").glob("*"))) == 4


@print_docstring()
def test_extra(tmp_path):
    """Test query of global quiet option."""
    runner = CliRunner()
    os.chdir(tmp_path)
    result = runner.invoke(cli, ["extra-value"])
    assert result.exit_code == 0
    assert not bool(int(result.output))
    result = runner.invoke(cli, ["-e", "extra-value"])
    assert result.exit_code == 0
    assert bool(int(result.output))


@print_docstring()
def test_other_module(tmp_path):
    """Test logging from another module."""
    runner = CliRunner()
    os.chdir(tmp_path)
    result = runner.invoke(cli, ["other-module"])
    logfile_path = Path(result.output.split("\n")[-2].split()[1])
    assert result.exit_code == 0
    assert len(list(Path("tests/data/logs").glob("*"))) == 1
    level_checker(logfile_path)


@print_docstring()
def test_elapsed_timing(tmp_path):
    """Test elapsed-time functions."""
    runner = CliRunner()
    os.chdir(tmp_path)
    result = runner.invoke(cli, ["log-elapsed-time"])
    for i, line in enumerate(result.output.split("\n")):
        if i == 0:
            assert "First elapsed time" in line
        elif i == 1:
            assert "Second elapsed time" in line
        elif i == 2:
            assert "Total elapsed time" in line


def get_mem_use_from_logstring(logstring):
    """Parse peak memory use from log string."""
    return int(logstring.split()[5])


@print_docstring()
def test_memory_profiling(tmp_path):
    """Test peak memory use logging."""
    runner = CliRunner()
    os.chdir(tmp_path)
    mem_inc_mb = 10
    result = runner.invoke(cli, ["--profile_mem", "log-memory-use", "0"])
    assert "Peak total memory use" in result.output
    base_mem_size = get_mem_use_from_logstring(result.output)
    result = runner.invoke(
        cli, ["--profile_mem", "log-memory-use", str(mem_inc_mb)]
    )
    inc_mem_size = get_mem_use_from_logstring(result.output)
    assert (inc_mem_size - base_mem_size - mem_inc_mb) <= MEMORY_QUANTUM_MB
