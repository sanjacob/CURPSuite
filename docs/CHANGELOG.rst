.. _changelog:

Changelog
=========

CURP Suite 2.7.0 (2026-11-16)
-----------------------------

Features
^^^^^^^^

- Soporte para Python 3.13, 3.14 y 3.15.
- Dependencias actualizadas.

Bugfixes
^^^^^^^^

- Corregir el ejemplo de uso del paquete (``entidad`` y ``entidad_iso``).

Misc
^^^^

- Se requiere Python 3.13 o superior. Se elimina el soporte para Python 3.8 a 3.12.
- Se elimina el extra opcional ``[test]``.
- Las dependencias de desarrollo se gestionan con uv (``uv.lock``) en lugar de Pipenv.
- Metadatos del paquete actualizados (licencia en formato SPDX y URLs del repositorio).

CURP Suite 2.6.1 (2023-10-04)
-----------------------------

Features
^^^^^^^^

- Soporte para pyproject.toml en lugar de setup.py o setup.cfg
- Dependencias actualizadas

Bugfixes
^^^^^^^^

- Build de documentación corregida
- Ahora los tests tienen un timeout mayor

CURP Suite 2.6.0 (2021-11-19)
-----------------------------

Features
^^^^^^^^

- Agregar soporte para Python 3.10.

Bugfixes
^^^^^^^^

- Corregir error menor en test por cambios en la versión anterior.

CURP Suite 2.5.1 (2021-11-19)
-----------------------------

Features
^^^^^^^^

- Sexo es ahora un IntEnum.
- Activar Dependabot.
- Actualizar algunas dependencias.
- Mejoras al Changelog.

Bugfixes
^^^^^^^^

- Arreglar problema con el test de validación de nombre completo.
- Mejoras a tests.

CURP Suite 2.4.2 (2021-08-27)
-----------------------------

Misc
^^^^

- Link de documentación actualizado.

CURP Suite 2.4.1 (2021-08-27)
-----------------------------

Features
^^^^^^^^

- Agregar soporte para Python 3.8.
- Agregar escudos al README y documentación.

Bugfixes
^^^^^^^^

- Ahora un primer apellido no se considera vacío si un segundo apellido existe.
- Corregir integración con GitHub Actions y readthedocs.

CURP Suite 2.3.0 (2021-08-27)
-----------------------------

Features
^^^^^^^^

- Cambiar a una API más orientada a objetos.
- Ahora es posible obtener atributos de la CURP después de la validación.
- Agregar validación más estricta.
- Agregar suite de pruebas con Hypothesis.

Misc
^^^^

- Cambiar nombre a CURP Suite.

CURPValidator 1.2.1 (2021-02-09)
--------------------------------

Features
^^^^^^^^

- Agregar licencia GPLv2.


CURPValidator 1.1.0 (2020-10-05)
--------------------------------

Bugfixes
^^^^^^^^

- Arreglar problema con palabras inconvenientes.

CURPValidator 1.0.0 (2020-08-06)
--------------------------------

Features
^^^^^^^^

- Funcionalidad básica.
