.. CURP Suite documentation master file, created by
   sphinx-quickstart on Fri Aug 13 21:17:12 2021.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

CURP Suite: CURPs para Humanos
==============================

.. image:: https://img.shields.io/badge/License-GPL%20v2-blue.svg
    :target: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html

**CURP Suite** es una librería de análisis y validación de la CURP Mexicana para Python.

---------------

.. doctest::

    >>> from curp import CURP
    >>> c = CURP("SABC560626MDFLRN01")
    >>> c.fecha_nacimiento
    datetime.date(1956, 6, 26)
    >>> c.sexo
    2
    >>> c.entidad
    'Ciudad de México'
    >>> c.nombre_valido("CONCEPCIÓN")
    True


Guia
----

.. toctree::
   :maxdepth: 2
   :caption: Contents:

   curp_class



Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
