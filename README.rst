=========================
Repo Health Information
=========================

.. start-badges

.. list-table::
    :stub-columns: 1

    * - docs
      - |docs|
    * - tests
      - |github-actions| |coverage| |codacy|
    * - package
      - |version| |wheel| |supported-versions| |supported-implementations| |commits-since|
.. |docs| image:: https://readthedocs.org/projects/python-syml/badge/?style=flat
    :target: https://readthedocs.org/projects/python-syml/
    :alt: Documentation Status

.. |github-actions| image:: https://github.com/KillianVar/python-syml/actions/workflows/github-actions.yml/badge.svg
    :alt: GitHub Actions Build Status
    :target: https://github.com/KillianVar/python-syml/actions

.. |coverage| image:: https://app.codacy.com/project/badge/Coverage/011ba7fa745b4a3083ea714909699110
    :alt: Coverage Build Status
    :target: https://app.codacy.com/gh/KillianVar/python-syml/dashboard?utm_source=gh&utm_medium=referral&utm_content=&utm_campaign=Badge_coverage

.. |codacy| image:: https://app.codacy.com/project/badge/Grade/011ba7fa745b4a3083ea714909699110
    :target: https://app.codacy.com/gh/KillianVar/python-syml/dashboard
    :alt: Codacy Code Quality Status

.. |version| image:: https://img.shields.io/pypi/v/syml.svg
    :alt: PyPI Package latest release
    :target: https://pypi.org/project/syml

.. |wheel| image:: https://img.shields.io/pypi/wheel/syml.svg
    :alt: PyPI Wheel
    :target: https://pypi.org/project/syml

.. |supported-versions| image:: https://img.shields.io/pypi/pyversions/syml.svg
    :alt: Supported versions
    :target: https://pypi.org/project/syml

.. |supported-implementations| image:: https://img.shields.io/pypi/implementation/syml.svg
    :alt: Supported implementations
    :target: https://pypi.org/project/syml

.. |commits-since| image:: https://img.shields.io/github/commits-since/KillianVar/python-syml/v0.7.5.svg
    :alt: Commits since latest release
    :target: https://github.com/KillianVar/python-syml/compare/v0.7.5...main



.. end-badges

|SyML-Logo|

.. |SyML-Logo| image:: https://github.com/KillianVar/python-syml/raw/dev/docs/source/img/banner.png



SyML (Systematic Machine Learning) is a library built to make Machine Learning simpler, by using SOTA ML, xAI and
vizualisation methods.

* Free software: MIT license

Installation
============

::

    pip install syml

You can also install the in-development version with::

    pip install https://github.com/KillianVar/python-syml/archive/main.zip


Documentation
=============


https://python-syml.readthedocs.io/


Development
===========

To run all the tests run::

    tox

Note, to combine the coverage data from all the tox environments run:

.. list-table::
    :widths: 10 90
    :stub-columns: 1

    - - Windows
      - ::

            set PYTEST_ADDOPTS=--cov-append
            tox

    - - Other
      - ::

            PYTEST_ADDOPTS=--cov-append tox
