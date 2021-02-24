click_loguru
============
``click_loguru`` initializes `click <https://click.palletsprojects.com/>`_ CLI-based
programs for logging to stderr and (optionally) a log file via the
`loguru <https://github.com/Delgan/loguru/>`_ logger.  It can optionally log run time,
CPU use, and peak memory use of user functions.

Log file names will include the name of your program and (if your application uses
subcommands via ``@click.group()``), the name of the subcommand. Log files are 
(optionally) numbered, with a retention policy specified.  Log files can be
enabled or disabled per-subcommand and written to a subdirectory that your
application specifies.  

Global CLI options control verbose/quiet levels and log file creation.
The values of these global options are accessible, along with the path to the
log file, from your application.

Instantiation
-------------
``click_loguru`` objects are instantiated from the ``ClickLoguru`` class as::

      click_loguru = ClickLoguru(name,
                                 version,
                                 retention=4,
                                 stderr_format_func=None,
                                 log_dir_parent="./logs",
                                 file_log_level="DEBUG",
                                 stderr_log_level="INFO",
                                 timer_log_level="debug",
        )

where:

* **name** is the name of your application
* **version** is the version string of your application
* **retention** is the log file retention policy.  If set to a non-zero value, the
  log files will be given by ``logs/NAME[-SUBCOMMAND]_n.log`` where ```NAME`` is the name
  of your application, ``SUBCOMMAND`` is the group subcommand (if you are using
  click groups), and ``n`` is an integer number.  The value of ``retention`` specifies
  the number of log files to be kept.
* **stderr_format_func** is the format function to be used for messages to stderr, as
  defined by ``loguru``.  Default is very short, with ``INFO``-level messages having
  no level name printed.
* **log_dir_parent** sets the location of the log file directory.  This value may be
  overridden per-command.
* **file_log_level**  sets the level of logging to the log file.
* **stderr_log_level** sets the level of logging to stderr.  This value may be overridden
  by the ``--quiet`` or ``--verbose`` options.
* **timer_log_level** is the level at which ``elapsed_time`` results will be logged.


Methods
-------
The ``ClickLoguru`` class defines the following methods:

* **logging_options** is a decorator to be used for your application's CLI function.  This
  decorator defines the global options that allows control of ``quiet``, ``verbose``,
  and ``log file`` booleans.

* **stash_subcommand** is a  decorator to be used for the CLI method for applications
  which define subcommands.

* **init_logger** is  a decorator which must be used for each subcommand.   It allows
  override of the default ``log_dir_parent`` established at instantiation,
  as well as turning off file logging for that command by setting ``log file`` to ``False``.

* **log_elapsed_time** is a decorator which causes the elapsed wall-clock time and
  CPU time in seconds for the (sub)command
  to be emitted at the level specified by the ``level=`` argument (``debug`` by default).

* **get_global_options** is a method that returns the context object associated with the
  global options. The context object is printable.  The attributes of the context object are the booleans ``verbose``,
  ``quiet``, and ``log file``, the string ``subcommand`` showing the subcommand that was invoked,
  and ``log file_handler_id`` if your code wishes to manipulate the handler directly.

* **user_global_options_callback** is a method to be used as
  a callback when your code declares a global option.  Values
  of these global options will be stored in a user global
  options context dictionary.

* **get_user_global_options** is a method to retrieve a
  dictionary of values of user global options.

* **elapsed_timer** is a method that accepts a single argument, ``phase``.
  The next invocation of this method will produce a log entry at ``timer_log_level``
  showing the elapsed wall clock and CPU time.  If ``phase`` is ``None``, 
  the next invocation will not produce a message.

* **log_peak_memory_use** is a method that results in the peak memory usage for
  the function and children of the function to be emitted at a level specified
  by the ``level=`` keyword (``debug`` is default).  This functionality
  is somewhat expensive in that it requires an additional thread, so the global
  option ``--profile_mem`` must be enabled.


See the `simple test CLI application
<https://github.com/joelb123/click_loguru/blob/master/tests/__init__.py>`_
for usage examples.

Prerequisites
-------------
Python 3.6 or greater is required.
This package is tested under Linux using Python 3.8. Besides  ``click`` and ``loguru``
themselves, this package depends upon ``memory_profiler`` and ``attrs``.


Project Status
--------------
+-------------------+-------------+
| Latest Release    | |pypi|      |
+-------------------+-------------+
| Activity          | |repo|      |
+-------------------+-------------+
| Downloads         | |downloads| |
+-------------------+-------------+
| Download Rate     | |dlrate|    |
+-------------------+-------------+
| License           | |license|   |
+-------------------+-------------+
| Build             | |build|     |
+-------------------+-------------+
| Coverage          | |coverage|  |
+-------------------+-------------+
| Code Grade        | |codacy|    |
+-------------------+-------------+
| Issues            | |issues|    |
+-------------------+-------------+
| Code Style        | |black|     |
+-------------------+-------------+
| Pre-commit        | |precommit| |
+-------------------+-------------+

.. |pypi| image:: https://img.shields.io/pypi/v/click_loguru.svg
    :target: https://pypi.python.org/pypi/click_loguru
    :alt: Python package

.. |repo| image:: https://img.shields.io/github/last-commit/joelb123/click_loguru
    :target: https://github.com/joelb123/click_loguru
    :alt: GitHub repository

.. |license| image:: https://img.shields.io/badge/License-BSD%203--Clause-blue.svg
    :target: https://github.com/joelb123/click_loguru/blob/master/LICENSE.txt
    :alt: License terms

.. |build| image:: https://github.com/joelb123/click_loguru/workflows/tests/badge.svg
    :target:  https://github.com/joelb123/click_loguru/actions
    :alt: GitHub Actions

.. |codacy| image:: https://api.codacy.com/project/badge/Grade/83706d2404e3436d94494eb3bbfe467d
    :target: https://www.codacy.com/gh/joelb123/click_loguru?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=joelb123/click_loguru&amp;utm_campaign=Badge_Grade
    :alt: Codacy.io grade

.. |coverage| image:: https://codecov.io/gh/joelb123/click_loguru/branch/master/graph/badge.svg
    :target: https://codecov.io/gh/joelb123/click_loguru
    :alt: Codecov.io test coverage

.. |black| image:: https://img.shields.io/badge/code%20style-black-000000.svg?style=flat-square
    :target: https://github.com/psf/black
    :alt: Black is the uncompromising Python code formatter

.. |precommit| image:: https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white
    :target: https://github.com/pre-commit/pre-commit
    :alt: pre-commit

.. |issues| image:: https://img.shields.io/github/issues/joelb123/click_loguru.svg
    :target:  https://github.com/joelb123/click_loguru/issues
    :alt: Issues reported


.. |depend| image:: https://api.dependabot.com/badges/status?host=github&repo=joelb123/click_loguru
     :target: https://app.dependabot.com/accounts/joelb123/repos/236847525
     :alt: dependabot dependencies


.. |dlrate| image:: https://img.shields.io/pypi/dm/click_loguru
    :target: https://pypistats.org/packages/click_loguru
    :alt: Download stats

.. |downloads| image:: https://pepy.tech/badge/click_loguru
    :target: https://pepy.tech/project/click_loguru
    :alt: Download stats
