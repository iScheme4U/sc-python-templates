.. image:: https://badge.fury.io/py/sc-python-templates.svg
    :target: https://badge.fury.io/py/sc-python-templates
.. image:: https://img.shields.io/pypi/pyversions/sc-python-templates
    :alt: PyPI - Python Version

A simple Python project sample structure
========================================

This project provides a sample structure for creating python project.


Installation
------------

It is possible to install the tool with `pip`::

    pip install sc-python-templates

Configuration
-------------

Configuration files reading in this order, the first is the top most priority:

#. production.xml in current directory,
#. production.xml in <project_name> directory under User directory,
#. production.xml in <project_name> directory under /var/opt/sc/ directory,
#. default.xml in <project_name> directory under /var/opt/sc/ directory.

The default configuration file looks like this::

    dev:
      # whether this program is running is development mode
      dev_mode: False

License
-------

The script is released under the MIT License.  The MIT License is registered
with and approved by the Open Source Initiative [1]_.

.. [1] https://opensource.org/licenses/MIT
