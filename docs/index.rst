.. CURP Suite documentation master file, created by
   sphinx-quickstart on Fri Aug 13 21:17:12 2021.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

CURP Suite: CURP para Humanos
================================

.. image:: https://img.shields.io/badge/License-GPL%20v2-blue.svg
    :target: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html

**CURP Suite** es una librería de análisis y validación de la
:abbr:`CURP (Clave Única de Registro de Población)` Mexicana para Python.

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
    >>> c.nombre_valido("Concepción")
    True


**CURP Suite** te permite extraer toda la información que contiene una CURP
de forma conveniente. Además, toda la validación es automática.
CURP Suite está diseñado para dar soporte a toda la especificación oficial de la CURP.


Características
---------------

- Extracción de datos

  - Fecha de nacimiento como objeto :class:`datetime.date`
  - Sexo de acuerdo a `ISO/IEC 5218`_
  - Nombre y clave `ISO 3166-2`_ de la entidad federativa de nacimiento

- Representación JSON de datos extraídos
- Validación con nombres y apellidos
- Validación con nombre completo
- Interfaz de Línea de Comandos


Manual De Uso
-------------

.. toctree::
   :maxdepth: 2
   :caption: Contents:

   install
   basics
   curp_class


.. _ISO/IEC 5218: https://en.wikipedia.org/wiki/ISO/IEC_5218
.. _ISO 3166-2: https://www.iso.org/obp/ui/#iso:code:3166:MX
