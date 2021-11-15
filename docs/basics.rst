.. _basic:

Uso Básico de CURP Suite
========================

.. image:: https://live.staticflickr.com/65535/51403951610_b6c029e619_b.jpg

Analizar una CURP con CURP Suite es muy simple.

Empieza importando la clase CURP

.. doctest::

    >>> from curp import CURP

Ahora, intentemos analizar una CURP. Para este ejemplo, usaremos la CURP de una
mujer hipotética llamada Concepción Salgado Briseño, nacida el 26 de Junio de 1956,
en México, Ciudad de México.

.. doctest::

    >>> c = CURP("SABC560626MDFLRN01")

Ahora, tenemos un objeto :class:`CURP <curp.CURP>` llamado ``c``.
Los datos que haya tenido la CURP pueden ser accesados como propiedades del objeto:

.. doctest::

    >>> c.fecha_nacimiento
    datetime.date(1956, 6, 26)
    >>> c.sexo
    <Sexo.MUJER: 2>
    >>> c.entidad
    'Ciudad de México'
    >>> c.entidad_iso
    'MX-CMX'

La fecha de nacimiento será convertida a un objeto :class:`datetime.date`.
Mientras que el sexo será representado por un :class:`IntEnum <enum.IntEnum>` compatible
con `ISO/IEC 5218`_, es decir, ``1`` para sexo masculino, ``2`` para sexo femenino.

Se puede comparar el sexo de la siguiente forma.

.. doctest::

   >>> from curp import Sexo
   >>> c.sexo is Sexo.MUJER
   True
   >>> str(c.sexo)
   'M'

Por último, la entidad federativa de nacimiento
podrá ser obtenida tanto como nombre común o como clave `ISO 3166-2`_.

Representación JSON
-------------------

Tal vez resulte conveniente obtener los datos de la CURP de forma rápida, en
cuyo caso es posible obtener una representación JSON de la CURP:

.. doctest::

    >>> c.json()
    '{"curp": "SABC560626MDFLRN01", "sexo": 2, "fecha_nacimiento": "1956-06-26", "entidad_nacimiento": {"name": "Ciudad de México", "iso": "MX-CMX"}}'


Validación de Nombres
---------------------

Podemos validar que una CURP corresponde a cierto nombre:

.. doctest::

    >>> c.nombre_valido("Concepción")
    True
    >>> c.nombre_valido("María Concepción")
    True
    >>> c.nombre_valido("Luisa Concepción")
    False
    >>> c.nombre_valido("Pedro")
    False

Alternativamente, también se puede pasar el nombre como un argumento al
crear el objeto.

.. doctest::

    >>> c = CURP("SABC560626MDFLRN01", nombre="Concepción")

En este caso, se alzará una excepción si el nombre no corresponde a la CURP.
Una vez creado el objeto puede obtenerse el nombre con el que fue creado.

.. doctest::

    >>> c.nombre
    'CONCEPCIÓN'


Validación de Apellidos
-----------------------

De forma similar, también podemos validar una CURP con respecto a los apellidos:

.. doctest::

    >>> c.primer_apellido_valido("Salgado")
    True
    >>> c.primer_apellido_valido("Salgado Junior")
    True
    >>> c.primer_apellido_valido("Junior Salgado")
    False
    >>> c.primer_apellido_valido("De Salgado")
    True

.. doctest::

    >>> c.segundo_apellido_valido("Briseño")
    True
    >>> c.segundo_apellido_valido("Rodríguez")
    False


También se puede pasar alguno de los apellidos como argumento al crear el objeto.
Se alzará una excepción si el apellido no corresponde a la CURP.

.. doctest::

    >>> c = CURP("SABC560626MDFLRN01", primer_apellido="Salgado", segundo_apellido="Briseño")

Una vez creado el objeto se pueden obtener los apellidos con los que fue creado.

.. doctest::

    >>> c.primer_apellido
    'SALGADO'
    >>> c.segundo_apellido
    'BRISEÑO'


Validación de Nombre Completo
-----------------------------

Finalmente, se puede validar una CURP con un nombre completo, en caso de
que no se cuente con los nombres y apellidos por separado. Esto tiene un
propósito doble, ya que también es útil para obtener las partes de un nombre,
si solo se cuenta con un nombre completo y una CURP.

.. doctest::

    >>> c.nombre_completo_valido("Concepción Salgado Briseño")
    ('Concepción', 'Salgado', 'Briseño')

Como en los casos anteriores, podemos usar el nombre completo como argumento
al crear el objeto. En caso de no coincidir, se alzará una excepción.

.. doctest::

    >>> c = CURP("SABC560626MDFLRN01", nombre_completo="Concepción Salgado Briseño")

El nombre y apellidos son obtenibles en el objeto como visto previamente.


Errores y Excepciones
---------------------

CURP Suite levanta una excepción distinta dependiendo de que aspecto
de la validación falla.

+------------------------------+--------------------------------------------+
| Excepción                    | Lanzada Cuando                             |
+==============================+============================================+
| CURPValueError [2]_          | La composición de la CURP es incorrecta.   |
+------------------------------+--------------------------------------------+
| CURPLengthError              | CURP no tiene 18 carácteres.               |
+------------------------------+--------------------------------------------+
| CURPVerificationError        | Dígito verificador no es correcto.         |
+------------------------------+--------------------------------------------+
| CURPNameError [1]_           | Nombre no corresponde a la CURP.           |
+------------------------------+--------------------------------------------+
| CURPFirstSurnameError [1]_   | Primer apellido no corresponde a la CURP.  |
+------------------------------+--------------------------------------------+
| CURPSecondSurnameError [1]_  | Segundo apellido no corresponde a la CURP. |
+------------------------------+--------------------------------------------+
| CURPFullNameError [1]_       | Nombre completo no corresponde a la CURP.  |
+------------------------------+--------------------------------------------+
| CURPDateError                | Fecha es numérica pero incorrecta.         |
+------------------------------+--------------------------------------------+
| CURPSexError                 | Sexo no es `H` o `M`.                      |
+------------------------------+--------------------------------------------+
| CURPRegionError              | Entidad Federativa no es válida.           |
+------------------------------+--------------------------------------------+

Todas las excepciones que CURP Suite levanta intencionalmente derivan de
CURPValueError.

Para atrapar cualquier excepción:


.. doctest::

    >>> from curp import CURP, CURPValueError
    >>> try:
    ...     c = CURP("SABC560626MDFLRN01")
    ... except CURPValueError:
    ...     print("Error al validar CURP")


.. [1] Solo levantadas si se crea la CURP con nombres/apellidos como argumentos.
.. [2] Levantada por múltiples motivos, dentro de los cuales están:

   - La CURP contiene caracteres no alfanuméricos.
   - Uno de los caracteres correspondientes al nombre / apellidos
     contiene un valor inapropiado (e.g. vocal cuando debe ser consonante).
   - La CURP contiene una palabra altisonante cuando no debería.
   - La fecha contiene al menos un carácter que no es numérico.

Interfaz de Línea de Comandos
-----------------------------

También es posible utilizar CURP Suite desde la terminal::

    $ curp -h
    usage: curp [-h] [-n NOMBRE] [-p PRIMER_APELLIDO] [-s SEGUNDO_APELLIDO] [-c NOMBRE_COMPLETO]
                curp

    Extraer datos de una CURP y validarla.

    positional arguments:
      curp                  la curp a analizar

    optional arguments:
      -h, --help            show this help message and exit
      -n NOMBRE, --nombre NOMBRE
                            nombre de pila para validar la CURP
      -p PRIMER_APELLIDO, --primer-apellido PRIMER_APELLIDO
                            primer apellido para validar la CURP
      -s SEGUNDO_APELLIDO, --segundo-apellido SEGUNDO_APELLIDO
                            segundo apellido para validar la CURP
      -c NOMBRE_COMPLETO, --nombre-completo NOMBRE_COMPLETO
                            nombre completo para validar la CURP


.. _ISO/IEC 5218: https://en.wikipedia.org/wiki/ISO/IEC_5218
.. _ISO 3166-2: https://www.iso.org/obp/ui/#iso:code:3166:MX
