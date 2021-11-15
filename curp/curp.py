"""
CURP Suite
Análisis y validación de la CURP mexicana.
"""

# Copyright (C) 2021, Jacob Sánchez Pérez

# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor,
# Boston, MA  02110-1301, USA.

from __future__ import annotations

import json
import string
from datetime import date
from enum import Enum, IntEnum, auto
from unidecode import unidecode
from typing import Optional, Union, Literal

from .chars import CURPChar
from .features import WordFeatures
from . import altisonantes, estados
from .exceptions import (CURPValueError, CURPLengthError,
                         CURPVerificationError, CURPNameError,
                         CURPFirstSurnameError, CURPSecondSurnameError,
                         CURPFullNameError, CURPDateError, CURPSexError,
                         CURPRegionError)

__all__ = ["CURP"]


class Sexo(IntEnum):
    DESCONOCIDO = 0
    HOMBRE = 1
    MUJER = 2

    def __str__(self) -> str:
        return self.name[0]


class CURP():
    """
    Realiza extracción de datos y validación de una CURP
    (Clave Única de Registro de Población).

    Uso::

        >>> from curp import CURP
        >>> c = CURP("SABC560626MDFLRN01")
        >>> c
        <CURP [SABC]>
    """
    _LENGTH = 18
    # str.index solo regresa la primera coincidencia
    _CHARSET = f"{string.digits}{string.ascii_uppercase[:14]}"
    _CHARSET += f"N{string.ascii_uppercase[14:]}"

    _ignored_words = ('DA', 'DAS', 'DE', 'DEL', 'DER', 'DI', 'DIE', 'DD',
                      'EL', 'LA', 'LOS', 'LAS', 'LE', 'LES', 'MAC', 'MC',
                      'VAN', 'VON', 'Y')
    _special_chars = ('/', '-', '.', "'", '’')
    _ignored_names = ('MARIA', 'MA', 'MA.', 'JOSE', 'J', 'J.')

    # Sexos
    _sexes: dict[str, Sexo] = {'H': Sexo.HOMBRE, 'M': Sexo.MUJER}

    # Abreviaciones de los estados en la CURP
    _regions = estados.estados

    # Palabras inconvenientes de la CURP
    _inconvenient = altisonantes.altisonantes

    # Para detectar si una CURP es inválida debido a estar sin censura,
    # crear lista de palabras sin censura
    _inc_uncensored = [f"{k[0]}{vowel}{k[2:]}"
                       for k, vowels in _inconvenient.items() for vowel in vowels]

    class _NameParseState(Enum):
        """Indica el progreso al comparar un nombre completo con una CURP."""
        NONE = auto()
        GIVEN_NAMES = auto()
        FIRST_SURNAME = auto()
        SECOND_SURNAME = auto()

    def __init__(self, curp: str, nombre: str = None,
                 primer_apellido: str = None, segundo_apellido: str = None,
                 nombre_completo: str = None):
        """
        Construye una CURP.

        Si sólo se proporciona un nombre completo, se dividirá de acuerdo a la CURP.
        Si se proporciona el nombre por partes, se usarán en lugar del nombre completo.
        Sólo se validarán las partes que se proporcionen.

        :param str curp: Una CURP de 18 caracteres.
        :param str nombre: Nombre de pila de la persona.
        :param str primer_apellido: Primer apellido (paterno) de la persona.
        :param str segundo_apellido: Segundo apellido (materno) de la persona.
        :param str nombre_completo: Nombre completo de la persona.
        """
        self._curp = curp

        if len(curp) != self._LENGTH:
            raise CURPLengthError("La CURP no tiene el tamaño correcto")

        if not self._validate_verify():
            raise CURPVerificationError("El dígito verificador no "
                                        "coincide con la CURP")

        # Fecha de nacimiento
        self._parse_birth_date()
        # Sexo
        self._parse_sex()
        # Estado de la república
        self._parse_region()

        # Nombre
        self._name = self._first_surname = self._second_surname = None

        # Validar caracteres restantes
        if not self._validate_name_chars():
            raise CURPValueError('Los caracteres del nombre/apellidos contienen errores')

        if nombre is not None:
            if self.nombre_valido(nombre):
                self._name = nombre.upper()
            else:
                raise CURPNameError('El nombre de pila no coincide con la CURP')

        if primer_apellido is not None:
            if self.primer_apellido_valido(primer_apellido):
                self._first_surname = primer_apellido.upper()
            else:
                raise CURPFirstSurnameError('El primer apellido no coincide con la CURP')

        if segundo_apellido is not None:
            if self.segundo_apellido_valido(segundo_apellido):
                self._second_surname = segundo_apellido.upper()
            else:
                raise CURPSecondSurnameError('El segundo apellido no coincide con la CURP')

        no_pieces = nombre is primer_apellido is segundo_apellido is None

        if no_pieces and nombre_completo is not None:
            names = self.nombre_completo_valido(nombre_completo)

            if names:
                capital_names = [n.upper() for n in names]
                self._name, self._first_surname, self._second_surname = capital_names
            else:
                raise CURPFullNameError('El nombre completo no parece coincidir con la CURP')

    def __repr__(self) -> str:
        return f"<CURP [{self.curp[:CURPChar.NAME_CHAR + 1]}]>"

    def nombre_valido(self, name: str) -> bool:
        """Verifica que una CURP sea válida para cierto nombre de pila.

        :param str name: Nombre de pila para validar.

        .. todo::

            Averiguar si la regla de los nombres comunes aplica aún si hay palabras
            ignoradas antes de ellos.
        """
        # Remover primer nombre si este es muy común
        pieces = name.upper().split()

        # TODO: Tal vez sea necesario omitir palabras ignoradas (De, Del, Etc.)
        if len(pieces) > 1 and unidecode(pieces[0]) in self._ignored_names:
            pieces.pop(0)

        wf = WordFeatures(' '.join(pieces),
                          self._ignored_words,
                          self._special_chars)

        valid = ((self.curp[CURPChar.NAME_CHAR] == wf.char)
                 and (self.curp[CURPChar.NAME_CONSONANT] == wf.consonant))
        return valid

    def primer_apellido_valido(self, primer_apellido: str) -> bool:
        """Verifica que una CURP sea válida para cierto primer apellido.

        :param str primer_apellido: Primer apellido (usualmente paterno) para validar.
        """
        curp_start = self.curp[:CURPChar.NAME_CHAR + 1]

        wf = WordFeatures(primer_apellido, self._ignored_words, self._special_chars)

        valid = ((self.curp[CURPChar.SURNAME_A_CHAR] == wf.char)
                 and (self.curp[CURPChar.SURNAME_A_CONSONANT] == wf.consonant))

        if valid:
            valid = self.curp[CURPChar.SURNAME_A_VOWEL] == wf.vowel

            # Buscar principio de la CURP en la lista de palabras inconvenientes
            if curp_start in self._inconvenient:
                # Usar las vocales reales para determinar si la CURP
                # corresponde al apellido
                for vowel in self._inconvenient[curp_start]:
                    valid = valid or (vowel == wf.vowel)

        return valid

    def segundo_apellido_valido(self, segundo_apellido: str) -> bool:
        """Verifica que una CURP sea válida para cierto segundo apellido.

        :param str segundo_apellido: Segundo apellido (usualmente materno) para validar.
        """
        wf = WordFeatures(segundo_apellido,
                          self._ignored_words,
                          self._special_chars)

        valid = ((self.curp[CURPChar.SURNAME_B_CHAR] == wf.char)
                 and (self.curp[CURPChar.SURNAME_B_CONSONANT] == wf.consonant))
        return valid

    def nombre_completo_valido(self, nombre_completo: str) -> Union[tuple[str, ...], Literal[False]]:
        """Utiliza un nombre completo para validar la CURP.

        :param str nombre_completo: Nombre completo para validar.
        :return: Una tupla con el nombre por partes, o False si el nombre no corresponde.
        :rtype: tuple or False
        """
        NameParseState = self._NameParseState

        names: dict[CURP._NameParseState, list[str]] = {k: [] for k in list(NameParseState)}
        state_gen = (s for s in NameParseState)
        state = next(state_gen)
        validation = {NameParseState.NONE: self.nombre_valido,
                      NameParseState.GIVEN_NAMES: self.primer_apellido_valido,
                      NameParseState.FIRST_SURNAME: self.segundo_apellido_valido,
                      NameParseState.SECOND_SURNAME: lambda n: False}

        # Guarda preposiciones y otras palabras ignoradas
        # hasta encontrar siguiente palabra normal
        ignored_buffer: list[str] = []

        for word in nombre_completo.split():
            if unidecode(word.upper()) not in self._ignored_words:
                if validation[state](word):
                    state = next(state_gen)
                elif state is NameParseState.NONE:
                    if unidecode(word.upper()) not in self._ignored_names:
                        return False

                # Agregar palabras ignoradas guardadas a la parte actual
                if len(ignored_buffer):
                    names[state].extend(ignored_buffer)
                    ignored_buffer.clear()
                names[state].append(word)

            else:
                ignored_buffer.append(word)

        names[state].extend(ignored_buffer)

        valid = state is NameParseState.SECOND_SURNAME

        if state is NameParseState.FIRST_SURNAME:
            valid = self.segundo_apellido_vacio
        elif state is NameParseState.GIVEN_NAMES:
            valid = self.primer_apellido_vacio

        if valid:
            names_list = [names[n] for n in NameParseState]
            names_list[0:2] = [names_list[0] + names_list[1]]
            names_tuple = tuple([' '.join(x) for x in names_list])
            return names_tuple

        return False

    def _validate_name_chars(self) -> bool:
        """Valida que los caracteres correspondientes al nombre y apellidos
        estén dentro del espacio correcto."""

        consonants = WordFeatures._consonants
        vowels = WordFeatures._vowels + 'X'

        name_chars = ((CURPChar.NAME_CHAR, CURPChar.NAME_CONSONANT),
                      (CURPChar.SURNAME_A_CHAR, CURPChar.SURNAME_A_CONSONANT),
                      (CURPChar.SURNAME_B_CHAR, CURPChar.SURNAME_B_CONSONANT))

        valid = self.curp[CURPChar.SURNAME_A_VOWEL] in vowels

        for char, consonant in name_chars:
            valid = valid and (self.curp[char] in string.ascii_uppercase and
                               self.curp[consonant] in consonants)

        if self.curp[:CURPChar.NAME_CHAR + 1] in self._inc_uncensored:
            valid = False

        return valid

    def _parse_birth_date(self) -> date:
        """Obtiene la fecha de nacimiento de la CURP.

        :raises ValueError: La fecha de nacimiento no pudo ser construída
        :return: La fecha de nacimiento indicada en la CURP
        :rtype: datetime.date
        """
        # Homonímia
        # [0-9] para personas nacidas hasta el 1999
        # [A-Z] para personas nacidas desde el 2000
        homonymy = self.curp[CURPChar.HOMONYMY]
        before_2k = homonymy in string.digits

        # Día y mes de nacimiento
        try:
            day = int(self.curp[CURPChar.DAY_0] + self.curp[CURPChar.DAY_1])
            month = int(self.curp[CURPChar.MONTH_0] + self.curp[CURPChar.MONTH_1])
            year = int(self.curp[CURPChar.YEAR_0] + self.curp[CURPChar.YEAR_1])
        except ValueError:
            raise CURPValueError(
                "La fecha de nacimiento contiene caracteres no numéricos")

        # Año y siglo actual
        current_year = date.today().year
        century = int(current_year / 100)

        # Asume que cualquier año mayor al actual
        # es en realidad del siglo pasado
        if year > (current_year % 100):
            century -= 1

        # Aunque no necesariamente cierto,
        # es probablemente la mejor opción
        if before_2k:
            century = 19
        elif century == 19:
            century = 20

        year += (century * 100)

        # Regresar con error si la fecha es incorrecta
        try:
            birth_date = date(year, month, day)
        except ValueError:
            raise CURPDateError("La fecha de nacimiento es incorrecta")

        self._birth_date = birth_date
        return birth_date

    def _parse_sex(self) -> Sexo:
        """Obtiene el sexo de la CURP.

        :raises ValueError: El sexo en la CURP es incorrecto.
        :return: El sexo de acuerdo a ISO/IEC 5218.
        :rtype: int
        """
        curp_sex = self.curp[CURPChar.SEX]
        sex: Sexo = self._sexes.get(curp_sex, Sexo.DESCONOCIDO)

        if not sex:
            raise CURPSexError("El sexo de la CURP no es válido")

        self._sex = sex
        return sex

    def _parse_region(self) -> estados.RegionData:
        """Obtiene la entidad federativa de nacimiento de la CURP.

        :raises ValueError: La CURP contiene un código de entidad incorrecto.
        :return: El nombre y código ISO 3166-2 de la entidad federativa
        de nacimiento.
        :rtype: dict
        """
        curp_region = self.curp[CURPChar.REGION_0] + self.curp[CURPChar.REGION_1]
        region = self._regions.get(curp_region, None)

        if not region:
            raise CURPRegionError("La entidad de nacimiento es incorrecta")

        self._birth_place = region
        return region

    def _validate_verify(self) -> bool:
        """Usa el último carácter de la CURP para verificar la misma
        de acuerdo al algoritmo oficial.
        """
        # Código de verificación
        verify = self.curp[CURPChar.VERIFICATION]
        b37_sum = self._verification_sum(self.curp)
        # Hacer las operaciones finales
        return self._sum_to_verify_digit(b37_sum) == verify

    @classmethod
    def _verification_sum(cls, curp: str) -> int:
        """Suma de verificación de la CURP."""
        try:
            r = sum([i * cls._CHARSET.index(x) for i, x in enumerate(curp[-2::-1], 2)])
            # Asegurarse de que el dígito de verificación sea válido
            cls._CHARSET.index(curp[-1])
        except ValueError:
            raise CURPValueError("La CURP contiene caracteres no válidos.")
        else:
            return r

    @staticmethod
    def _sum_to_verify_digit(sm: int) -> str:
        d = sm % 10
        d = 10 - d if d else d
        return str(d)

    def json(self) -> str:
        """Objeto JSON conteniendo los datos extraídos de la CURP."""
        json_data = {
            'curp': self.curp,
            'sexo': self.sexo,
            'fecha_nacimiento': str(self.fecha_nacimiento),
            'entidad_nacimiento': self._birth_place
        }

        if self._name is not None:
            json_data['nombre'] = self._name

        if self._first_surname is not None:
            json_data['primer_apellido'] = self._first_surname

        if self._second_surname is not None:
            json_data['segundo_apellido'] = self._second_surname
        return json.dumps(json_data, ensure_ascii=False)

    # Properties

    @property
    def curp(self) -> str:
        """CURP con la que se construyó el objeto."""
        return self._curp

    @property
    def nombre(self) -> Optional[str]:
        """Nombre con el que se construyó el objeto."""
        return self._name

    @property
    def primer_apellido(self) -> Optional[str]:
        """Primer apellido con el que se construyó el objeto."""
        return self._first_surname

    @property
    def segundo_apellido(self) -> Optional[str]:
        """Segundo apellido con el que se construyó el objeto."""
        return self._second_surname

    @property
    def fecha_nacimiento(self) -> date:
        """Fecha de nacimiento extraída de la CURP."""
        return self._birth_date

    @property
    def sexo(self) -> Sexo:
        """Sexo extraído de la CURP."""
        return self._sex

    @property
    def entidad(self) -> str:
        """Entidad federativa de nacimiento de la CURP."""
        return self._birth_place['name']

    @property
    def entidad_iso(self) -> Optional[str]:
        """Código ISO de la entidad federativa de nacimiento de la CURP."""
        return self._birth_place['iso']

    @property
    def es_extranjero(self) -> bool:
        """True si la CURP pertenece a alguien nacido en el extranjero."""
        return not self._birth_place['iso']

    @property
    def primer_apellido_vacio(self) -> bool:
        """True si la CURP puede corresponder a un primer apellido vacio."""
        # Asumir que si existe un segundo apellido, el primero también debe
        # existir, incluso si aparenta no hacerlo
        segundo_vacio = self.segundo_apellido_vacio
        return segundo_vacio and self.primer_apellido_valido('')

    @property
    def segundo_apellido_vacio(self) -> bool:
        """True si la CURP puede corresponder a un segundo apellido vacio."""
        return self.segundo_apellido_valido('')
