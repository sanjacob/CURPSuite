# CURP Suite

[![PyPI Version][version-badge]][pypi] [![Python versions][python-version-badge]][pypi] [![License: GPL  v2][license-badge]][gnu] [![Build][build-badge]][actions] [![ReadTheDocs][docs-badge]][rtd] [![Total downloads][downloads-badge]][pepy]

**CURP Suite** es una librería de análisis y validación de la CURP Mexicana.

```python
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

```



CURP Suite te permite extraer toda la información que contiene una CURP de forma conveniente. Además, toda la validación es automática. CURP Suite está diseñado para dar soporte a toda la especificación oficial de la CURP.

También puede ser invocada desde la terminal

```bash
$ curp SABC560626MDFLRN01
{"curp": "SABC560626MDFLRN01", "sexo": 2, "fecha_nacimiento": "1956-06-26", "entidad_nacimiento": {"name": "Ciudad de México", "iso": "MX-CMX"}}
```





## Instalación

##### Desde PyPI

```bash
$ python3 -m pip install CURPSuite
```

CURP Suite soporta Python 3.8+.



## Características

- Extracción de datos
  - Fecha de nacimiento como objeto `datetime.date`
  - Sexo compatible con [ISO/IEC 5218][iso5218]
  - Nombre y clave [ISO 3166-2][iso3166] de la entidad federativa de nacimiento
- Representación JSON de datos extraídos
- Validación con nombres y apellidos
- Validación con nombre completo
- Interfaz de Línea de Comandos



## Documentación

Disponible en https://curpsuite.readthedocs.io.



## Licencia

Este programa se distribuye bajo la licencia [GPLv2.0][license], más información en el sitio de la [Free Software Foundation][gnu].



<!-- MARKDOWN LINK REFERENCES -->

[iso5218]: https://en.wikipedia.org/wiki/ISO/IEC_5218 "ISO/IEC 5218"
[iso3166]: https://es.wikipedia.org/wiki/ISO_3166-2 "ISO 3166-2"
[git]: https://git-scm.com/	"Git"
[python]: https://www.python.org/ "Python.org"
[pipenv]: https://pipenv.pypa.io/en/latest/ "Pipenv"
[license]: LICENSE "General Public License"
[gnu]: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html "Free Software Foundation"
[pypi]: https://pypi.org/project/CURPSuite
[license-badge]: https://img.shields.io/github/license/jacobszpz/CURPSuite
[version-badge]: https://img.shields.io/pypi/v/CURPSuite
[python-version-badge]: https://img.shields.io/pypi/pyversions/CURPSuite
[build-badge]: https://img.shields.io/github/actions/workflow/status/jacobszpz/CURPSuite/integration.yml?branch=master
[actions]: https://github.com/jacobszpz/CURPSuite/actions
[docs-badge]: https://img.shields.io/readthedocs/curpsuite
[rtd]: https://curpsuite.readthedocs.io
[rtd-changelog]: https://curpsuite.readthedocs.io/es/latest/CHANGELOG.html
[downloads-badge]: https://static.pepy.tech/badge/curpsuite
[pepy]: https://pepy.tech/project/curpsuite
[pypi-stats]: https://pypistats.org/packages/curpsuite
