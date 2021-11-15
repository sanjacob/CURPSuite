.. CURP Suite documentation master file, created by
   sphinx-quickstart on Fri Aug 13 21:17:12 2021.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

CURP Suite: CURP para Humanos
================================

.. image:: https://img.shields.io/pypi/v/CURPSuite
    :target: https://pypi.org/project/CURPSuite

.. image:: https://img.shields.io/pypi/pyversions/CURPSuite
    :target: https://pypi.org/project/CURPSuite

.. image:: https://img.shields.io/github/license/jacobszpz/CURPSuite
    :target: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html

.. image:: https://img.shields.io/github/workflow/status/jacobszpz/CURPSuite/Python%20CI/master
    :target: https://github.com/jacobszpz/CURPSuite/actions

.. image:: https://img.shields.io/readthedocs/curpsuite
    :target: https://curpsuite.readthedocs.io

.. image:: https://img.shields.io/pypi/dm/curpsuite
    :target: https://pypistats.org/packages/curpsuite


**CURP Suite** es una librería de análisis y validación de la
:abbr:`CURP (Clave Única de Registro de Población)` Mexicana para Python.

---------------

.. doctest::

    >>> from curp import CURP
    >>> c = CURP("SABC560626MDFLRN01")
    >>> c.fecha_nacimiento
    datetime.date(1956, 6, 26)
    >>> c.sexo
    <Sexo.MUJER: 2>
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
  - Sexo compatible con `ISO/IEC 5218`_
  - Nombre y clave `ISO 3166-2`_ de la entidad federativa de nacimiento

- Representación JSON de datos extraídos
- Validación con nombres y apellidos
- Validación con nombre completo
- Interfaz de Línea de Comandos


Manual De Uso
-------------

Una explicación de como empezar a usar CURP Suite.

.. toctree::
   :maxdepth: 2

   install
   basics


Documentación de API
--------------------

Documentación de la interfaz pública de CURP Suite.

.. toctree::
   :maxdepth: 2

   curp_class


Contribuciones
--------------

Si quieres contribuir al proyecto, empieza aquí.

.. toctree::
   :maxdepth: 3

   CHANGELOG
   dev/contributing


.. _ISO/IEC 5218: https://en.wikipedia.org/wiki/ISO/IEC_5218
.. _ISO 3166-2: https://www.iso.org/obp/ui/#iso:code:3166:MX
