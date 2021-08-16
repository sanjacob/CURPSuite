#!/usr/bin/env python3

"""
CURP Suite:
Un sistema de extracción de datos y validación de la CURP
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


import json
from datetime import date
from typing import Optional
from enum import Enum, auto
from unidecode import unidecode

from .chars import CURPChar
from .features import WordFeatures
from . import altisonantes, estados
from .exceptions import (CURPValueError, CURPLengthError,
                         CURPVerificationError, CURPNameError,
                         CURPFirstSurnameError, CURPSecondSurnameError,
                         CURPDateError, CURPSexError, CURPRegionError)

__all__ = ["CURP"]


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
    _ignored_words = ('DA', 'DAS', 'DE', 'DEL', 'DER', 'DI', 'DIE', 'DD',
                      'EL', 'LA', 'LOS', 'LAS', 'LE', 'LES', 'MAC', 'MC',
                      'VAN', 'VON', 'Y')
    _special_chars = ('/', '-', '.', "'", '’')
    _ignored_names = ('MARIA', 'MA.', 'MA', 'JOSE', 'J', 'J.')

    # Sexes
    _sexes = {'H': 1, 'M': 2}

    # Abreviaciones de los estados en la CURP
    _regions = estados.estados

    # Palabras inconvenientes de la CURP
    _inconvenient = altisonantes.altisonantes

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

        if nombre is not None:
            if self.nombre_valido(nombre):
                self._name = nombre.upper()
            else:
                raise CURPNameError("El nombre de pila no coincide con la CURP")

        if primer_apellido is not None:
            if self.primer_apellido_valido(primer_apellido):
                self._first_surname = primer_apellido.upper()
            else:
                raise CURPFirstSurnameError("El primer apellido no coincide con la CURP")

        if segundo_apellido is not None:
            if self.segundo_apellido_valido(segundo_apellido):
                self._second_surname = segundo_apellido.upper()
            else:
                raise CURPSecondSurnameError("El segundo apellido no coincide con la CURP")

        if (nombre is primer_apellido is segundo_apellido is None
            and nombre_completo is not None):
            names = self.nombre_completo_valido(nombre_completo)

            if names:
                self._name, self._first_surname, self._second_surname = names

    def nombre_valido(self, name: str) -> bool:
        """Verifica que una CURP sea válida para cierto nombre de pila.

        :param str name: Nombre de pila para validar.
        """
        # Remover primer nombre si este es muy común
        pieces = name.upper().split()

        if len(pieces) > 1 and unidecode(pieces[0]) in self._ignored_names:
            pieces.pop(0)

        wf = WordFeatures(' '.join(pieces),
                          self._ignored_words,
                          self._special_chars)

        valid = ((self.curp[CURPChar.NAME_CHAR] == wf.char)
                 and (self.curp[CURPChar.NAME_CONSONANT] == wf.consonant))
        return valid

    def __repr__(self):
        return f"<CURP [{self.curp[:CURPChar.NAME_CHAR + 1]}]>"

    def primer_apellido_valido(self, primer_apellido: str) -> bool:
        """Verifica que una CURP sea válida para cierto primer apellido.

        :param str primer_apellido: Primer apellido (comúnmente paterno) para validar.
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

        :param str segundo_apellido: Segundo apellido (comúnmente materno) para validar.
        """
        wf = WordFeatures(segundo_apellido,
                          self._ignored_words,
                          self._special_chars)

        valid = ((self.curp[CURPChar.SURNAME_B_CHAR] == wf.char)
                 and (self.curp[CURPChar.SURNAME_B_CONSONANT] == wf.consonant))
        return valid

    def nombre_completo_valido(self, nombre_completo: str) -> Optional[tuple[str]]:
        """Utiliza un nombre completo para validar la CURP.

        :param str nombre_completo: Nombre completo para validar.
        :return: Una tupla con el nombre por partes.
        :rtype: tuple or False
        """
        name_parts = ([], [], [])
        state = self._NameParseState.NONE

        # "VEGR/010517/H/MC/NTS/A5": "RUSSELL NATAHEL VENEGAS GUTIERREZ"
        current_part = 0

        for word in nombre_completo.split():
            if word not in self._ignored_words:
                if state is self._NameParseState.NONE:
                    if self.nombre_valido(word):
                        state = self._NameParseState.GIVEN_NAMES
                elif state is self._NameParseState.GIVEN_NAMES:
                    if self.primer_apellido_valido(word):
                        state = self._NameParseState.FIRST_SURNAME
                        current_part += 1
                elif state is self._NameParseState.FIRST_SURNAME:
                    if self.segundo_apellido_valido(word):
                        state = self._NameParseState.SECOND_SURNAME
                        current_part += 1

                name_parts[current_part].append(word)
            else:
                append_to = current_part
                if state is not self._NameParseState.SECOND_SURNAME:
                    append_to += 1
                name_parts[append_to].append(word)

        no_second_surname = self.segundo_apellido_valido('')

        if (state is self._NameParseState.SECOND_SURNAME
            or (state is self._NameParseState.FIRST_SURNAME and no_second_surname)):

            names_tuple = tuple([' '.join(x) for x in name_parts])
            return names_tuple
        else:
            return False

    def _parse_birth_date(self) -> date:
        """Obtiene la fecha de nacimiento de la CURP.

        :raises ValueError: La fecha de nacimiento no pudo ser construída
        :return: La fecha de nacimiento indicada en la CURP
        :rtype: datetime.date
        """
        # Homonímia
        # [1-9] para personas nacidas hasta el 1999
        # [A-Z] para personas nacidas desde el 2000
        homonymy = self.curp[CURPChar.HOMONYMY]
        before_2k = homonymy.isdigit()

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

    def _parse_sex(self) -> int:
        """Obtiene el sexo de la CURP.

        :raises ValueError: El sexo en la CURP es incorrecto.
        :return: El sexo de acuerdo a ISO/IEC 5218.
        :rtype: int
        """
        curp_sex = self.curp[CURPChar.SEX]
        sex = self._sexes.get(curp_sex, 0)

        if not sex:
            raise CURPSexError("El sexo de la CURP no es válido")

        self._sex = sex
        return sex

    def _parse_region(self) -> dict[str, str]:
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

    @staticmethod
    def _verification_sum(curp: str) -> int:
        """Suma de verificación de la CURP."""
        # Convertir curp de base 36 a base 10
        # Se asume que la homoclave de la curp no puede contener "Ñ"
        try:
            b36_list = [int(c, 36) for c in curp]
        except ValueError:
            raise CURPValueError("La CURP contiene caracteres no válidos.")
        # Ajustar elementos después de la Ñ (por diseño)
        b37_list = [x+1 if x > 23 else x for x in b36_list]

        # Sumar la multiplicación de cada elemento con su índice inverso
        # (empezando en 1), a excepción del último carácter,
        # pues este es el de verificación
        b37_sum = sum([i*x for i, x in enumerate(b37_list[-2::-1], 2)])
        return b37_sum

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
        """Nombre que acompaña a la CURP."""
        return self._name

    @property
    def primer_apellido(self) -> Optional[str]:
        """Primer apellido que acompaña a la CURP."""
        return self._first_surname

    @property
    def segundo_apellido(self) -> Optional[str]:
        """Segundo apellido que acompaña a la CURP."""
        return self._second_surname

    @property
    def fecha_nacimiento(self) -> date:
        """Fecha de nacimiento extraída de la CURP."""
        return self._birth_date

    @property
    def sexo(self) -> int:
        """Sexo extraído de la CURP."""
        return self._sex

    @property
    def entidad(self) -> str:
        """Entidad federativa de nacimiento de la CURP."""
        return self._birth_place['name']

    @property
    def entidad_iso(self) -> str:
        """Código ISO de la entidad federativa de nacimiento de la CURP."""
        return self._birth_place['iso']

    @property
    def es_extranjero(self) -> bool:
        """Booleano que indica si CURP pertenece a alguien nacido en el extranjero."""
        return self._birth_place['iso'] == ""


def main():
    import argparse
    parser = argparse.ArgumentParser(
        'curp',
        description='Extraer datos de una CURP y validarla.')

    parser.add_argument('curp', help='la curp a analizar')
    parser.add_argument('-n', '--nombre', help='nombre de pila para validar la CURP')
    parser.add_argument('-p', '--primer-apellido', help='primer apellido para validar la CURP')
    parser.add_argument('-s', '--segundo-apellido', help='segundo apellido para validar la CURP')
    parser.add_argument('-c', '--nombre-completo', help='nombre completo para validar la CURP')

    args = parser.parse_args()

    if args.curp is not None:
        c = CURP(
            args.curp,
            nombre=args.nombre,
            primer_apellido=args.primer_apellido,
            segundo_apellido=args.segundo_apellido,
            nombre_completo=args.nombre_completo
        )

    return c.json()


if __name__ == '__main__':
    exit(main())
