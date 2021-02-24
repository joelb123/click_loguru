# -*- coding: utf-8 -*-
"""Nox sessions."""

# third-party imports
import nox
from nox_poetry import session

CODE_LOCATIONS = (
    "click_loguru",
    "tests",
)

@nox.session
def tests(session):
    """Run tests with pytest and pytest-cov."""
    args = session.posargs or []
    session.install("coverage[toml]", "pytest", "pytest-cov", ".")
    session.run("pytest", *args)


@nox.session
def lint_pylint(session):
    """Run lint on all code."""
    args = session.posargs or CODE_LOCATIONS
    session.install("pylint", ".")
    session.run("pylint", *args)
