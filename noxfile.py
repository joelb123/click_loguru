# -*- coding: utf-8 -*-
"""Nox testing environment defs."""
# cribbed from https://cjolowicz.github.io/posts/hypermodern-python-03-linting/

# standard library imports
import tempfile

# third-party imports
import nox

CODE_LOCATIONS = (
    "click_loguru",
    "tests",
    "noxfile.py",
)


def install_with_constraints(session, *args, **kwargs):
    """Get dependencies from poetry."""
    with tempfile.NamedTemporaryFile() as requirements:
        session.run(
            "poetry",
            "export",
            "--without-hashes",
            "--dev",
            "--format=requirements.txt",
            f"--output={requirements.name}",
            external=True,
        )
        session.install(f"--constraint={requirements.name}", *args, **kwargs)


@nox.session(python=["3.8", "3.9"])
def tests(session):
    """Run tests with pytest and pytest-cov."""
    args = session.posargs or ["--cov=click_loguru"]
    session.run("poetry", "install", "--no-dev", external=True)
    install_with_constraints(session, "coverage[toml]", "pytest", "pytest-cov")
    session.run("pytest", *args)


@nox.session(python=["3.8"])
def lint_pylint(session):
    """Run lint on all code"""
    args = session.posargs or CODE_LOCATIONS
    session.run("poetry", "install", "--no-dev", external=True)
    install_with_constraints(session, "pylint", "nox")
    session.run("pylint", *args)
