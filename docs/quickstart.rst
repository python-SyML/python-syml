.. image:: ./source/img/narrow_banner.png

################
Quickstart Guide
################

In this guide, we will explain how to use this package.

1. Loading the data in Python-SyML
=================================
.. warning::
    The current implementation does not support multiple data files nor data files that are not csv or parquet files.

Within the cloned repository, put in the folder name "data" a data file. It **must** be **one single CSV or parquet** file.
SyML will automatically detect the file and load it one you run it.

2. Running SyML's interface
===========================

SyML comes with an integrated CLI (Command-Line Interface) in order to facilitate basic script executions.
To launch SyML's interface, execute the following command in a terminal window within the directory "python-syml"

.. code-block:: bash

    >> syml run
