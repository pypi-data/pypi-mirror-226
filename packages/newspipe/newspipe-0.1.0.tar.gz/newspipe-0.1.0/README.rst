########
NewsPipe
########

.. image:: https://img.shields.io/pypi/v/newspipe.svg?style=flat-square
  :target: https://pypi.org/project/newspipe/
  :alt: Latest PyPI version

.. image:: https://img.shields.io/pypi/pyversions/newspipe.svg?style=flat-square
  :target: https://pypi.org/project/newspipe/
  :alt: Python versions

.. image:: https://img.shields.io/codeclimate/maintainability/Nekmo/newspipe.svg?style=flat-square
  :target: https://codeclimate.com/github/Nekmo/newspipe
  :alt: Code Climate

.. image:: https://img.shields.io/codecov/c/github/Nekmo/newspipe/master.svg?style=flat-square
  :target: https://codecov.io/github/Nekmo/newspipe
  :alt: Test coverage

.. image:: https://img.shields.io/requires/github/Nekmo/newspipe.svg?style=flat-square
  :target: https://requires.io/github/Nekmo/newspipe/requirements/?branch=master
  :alt: Requirements Status


A web news aggregator with visualization improvements and powered by Artificial Intelligence (IA)

Development commands
====================

Type checks
-----------

Running type checks with mypy::

  $ mypy newspipe


Test coverage
-------------

To run the tests, check your test coverage, and generate an HTML coverage report::

    $ coverage run -m pytest
    $ coverage html
    $ open htmlcov/index.html


Celery
------

This app comes with Celery. To run a celery worker:

.. code-block:: bash

    celery -A newspipe worker -l info
