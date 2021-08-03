#!/usr/bin/env python3

import re
from enum import IntEnum
from datetime import date
from functools import partialmethod
from unidecode import unidecode
from curp import _altisonantes, _estados

"""
CURP: Un sistema orientado a objetos de
validación y extracción de datos de la CURP

Jacob Sánchez Pérez
Copyright (C) 2021
"""

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
# Also available at https://www.gnu.org/licenses/old-licenses/gpl-2.0.html


class CURPChar(IntEnum):
    """Guarda las posiciones de los datos de la CURP"""
    NAME_FIRST_LETTER = 3
    NAME_NEXT_CSNT = 15

    SURNAME_FIRST_LETTER = 0
    SURNAME_FIRST_VOWEL = 1
    SURNAME_NEXT_CSNT = 13

    SURNAME_M_FIRST_LETTER = 2
    SURNAME_M_NEXT_CSNT = 14

    YEAR_ONE = 4
    YEAR_TWO = 5
    MONTH_ONE = 6
    MONTH_TWO = 7
    DAY_ONE = 8
    DAY_TWO = 9

    SEX = 10
    REGION_ONE = 11
    REGION_TWO = 12

    HOMONYMY = 16
    VERIFICATION = 17


class WordFeatures:
    """
    Extrae ciertos carácteres de una palabra:

    - Primer carácter
    - Primera vocal (después del 1er char)
    - Primera consonante (después del 1er char)

    Si no se encuentra una vocal o consonante,
    una "X" tomará su lugar

    Cualquier "Ñ" será reemplazada con una "X"
    """

    _vowels = "[AEIOU]"
    _consonants = "[BCDFGHJKLMNÑPQRSTVWXYZ]"

    def __init__(self, word):
        word = word.split()[-1]
        x = lambda c : c if c != "Ñ" else "X"

        self._l = x(word[0])
        self._v = self._find_vowel(word[1:])
        self._c = x(self._find_consonant(word[1:]))

    @staticmethod
    def _find_char(charset, word, pos=0):
        i = re.findall(charset, word)
        return "X" if len(i) <= pos else i[pos]

    _find_vowel = partialmethod(_find_char, _vowels)
    _find_consonant = partialmethod(_find_char, _consonants)

    @property
    def char(self):
        return self._l

    @property
    def vowel(self):
        return self._v

    @property
    def consonant(self):
        return self._c


class CURP():
    """
    Realizar extracción de datos y verificación a partir de una CURP
    ('Clave Única de Registro de Población')
    """
    __LENGTH = 18

    def __init__(self, curp : str, full_name : str = None, given_name : str = None,
                 surname : str = None, second_surname : str = None):
        """
        Representa una CURP

        Si sólo se proporciona un nombre completo, se dividirá de acuerdo a la CURP.
        Si se proporciona el nombre por partes, se usarán en lugar del nombre completo.

        :param str curp: Una CURP de 18 carácteres
        :param str full_name: Nombre completo de la persona
        :param str given_name: Nombre de pila de la persona
        :param str surname: Apellido de la persona
        :param str second_surname: Apellido materno de la persona
        :param date birth_date: Fecha de nacimiento de la persona
        :param int sex: Sexo de la persona como un int (1 para Hombre, 2 para Mujer)
        """

        if len(curp) != self.__LENGTH:
            raise ValueError("La CURP no tiene el tamaño correcto")

        # Fecha de nacimiento
        self._birth_date = CURPValidator.validate_birth_date(curp)

        # Sexo
        self._sex = CURPValidator.validate_sex(curp)

        # Estado de la república
        self._birth_place = CURPValidator.validate_region(curp)

        if not CURPValidator.validate_verify(curp):
            raise ValueError("El dígito verificador no coincide con la CURP")

        # Nombre
        if not given_name is surname is second_surname is None:
            if given_name is not None:
                pass
            if surname is not None:
                pass
            if second_surname is not None:
                pass
        else:
            if full_name is not None:
                pass

    def json(self):
        json_data = {
            'sex': self.sex,
            'birth_date': self.birth_date
        }
        return json.dumps(json_data)

    @property
    def sex(self) -> int:
        return self._sex

    @property
    def birth_date(self) -> date:
        return self._birth_date

    @property
    def birth_place_iso(self) -> str:
        return self._birth_place['iso']

    @property
    def birth_place_name(self) -> str:
        return self._birth_place['name']


class CURPValidator:
    _word_regex = r'((?:DEL? )?(?:L(?:A|O)S? )?(?:\w|-)+\'?\b)'

    _valid_sexes = {'H': 1, 'M': 2}

    # Abreviaciones de los estados en la CURP
    _valid_regions = _estados._estados

    # Palabras inconvenientes de la CURP
    _inconvenient = _altisonantes._altisonantes

    @staticmethod
    def validate_name(curp : str, name : str):
        """Verifica que una CURP sea compatible con cierto nombre de pila."""
        wf = WordFeatures(name)
        matches = ((curp[CURP.NAME_FIRST_LETTER] == wf.char) and
            (curp[CURP.NAME_NEXT_CSNT] == wf.consonant))

        return matches

    @staticmethod
    def validate_surname(curp : str, f):
        # Buscar principio de la CURP en la lista de palabras inconvenientes
        if curp[:CURP.NAME_FIRST_LETTER + 1] in _inconvenient:
            pass

        curp[CURP.SURNAME_FIRST_VOWEL] == f.vowel

        matches = ((curp[CURP.SURNAME_FIRST_LETTER] == f.char)
                   and (curp[CURP.SURNAME_NEXT_CSNT] == f.consonant))

        # Match instead against what the uncensored letter would be,
        # according to our own mapping

        if not matches and False:
            for i_word in inconvenient[curp[:CURP.NAME_FIRST_LETTER + 1]]:
                if not matches:
                    matches = i_word[CURP.SURNAME_FIRST_VOWEL] == f.vowel


        return matches

    @staticmethod
    def validate_m_surname(curp : str, surname : str):
        wf = WordFeatures(surname)
        matches = ((curp[CURP.SURNAME_M_FIRST_LETTER] == wf.char) and
            (curp[CURP.SURNAME_M_NEXT_CSNT] == wf.consonant))

        return matches

    @staticmethod
    def validate_birth_date(curp : str):
        """Obtiene la fecha de nacimiento de la CURP como un objeto date
        :raises ValueError: La fecha de nacimiento no pudo ser construída
        :return: La fecha de nacimiento indicada en la CURP
        :rtype: datetime.date
        """
        # Homonímia
        # [1-9] para personas nacidas hasta el 1999
        # [A-Z] para personas nacidas desde el 2000
        homonymy = curp[CURPChar.HOMONYMY]
        twentieth_century = homonymy.isdigit()

        # Día y mes de nacimiento
        day = int(curp[CURPChar.DAY_ONE] + curp[CURPChar.DAY_TWO])
        month = int(curp[CURPChar.MONTH_ONE] + curp[CURPChar.MONTH_TWO])

        # Año de nacimiento en dos dígitos
        year = curp[CURPChar.YEAR_ONE] + curp[CURPChar.YEAR_TWO]

        # TODO: Usar dígito diferenciador de homonímia para conseguir
        # un año de nacimiento más preciso
        today = date.today()
        current_year = today.strftime("%y")
        century = today.strftime("%Y")[:-2]

        # Asume que cualquier año mayor al actual
        # es en realidad del siglo pasado
        if int(year) > int(current_year):
            century = str(int(century) - 1)

        # Aunque no necesariamente cierto,
        # es probablemente la mejor opción
        if twentieth_century:
            century = '19'

        year = century + year

        # Regresar con error si la fecha es incorrecta
        try:
            birth_date = date(int(year), month, day)
        except ValueError as e:
            raise ValueError("La fecha de nacimiento es incorrecta")

        return birth_date

    @classmethod
    def validate_sex(cls, curp : str) -> int:
        """Compara el sexo indicado en la CURP con valores válidos (H/M).
        :raises ValueError: El sexo en la CURP es incorrecto.
        :return: El sexo de acuerdo a ISO/IEC 5218.
        """
        curp_sex = curp[CURPChar.SEX]
        sex = cls._valid_sexes.get(curp_sex, 0)

        if not sex:
            raise ValueError("El sexo de la CURP no es válido")
        return sex

    @classmethod
    def validate_region(cls, curp : str) -> dict:
        """Valida la entidad federativa de nacimiento de una CURP.
        :raises ValueError: La CURP contiene un código de entidad incorrecto.
        :return: El nombre y código ISO 3166-2 de la entidad federativa
        de nacimiento.
        :rtype: dict
        """
        curp_region = curp[CURPChar.REGION_ONE] + curp[CURPChar.REGION_TWO]
        region = cls._valid_regions.get(curp_region, None)

        if not region:
            raise ValueError("La entidad de nacimiento es incorrecta")
        return region

    @staticmethod
    def validate_verify(curp : str) -> bool:
        """Usa el último carácter de la CURP para verificar la misma
        de acuerdo un algoritmo.
        """
        # Código de verificación
        verify = curp[CURPChar.VERIFICATION]

        # Convertir lista de base 36 a base 10
        b36_list = [int(c, 36) for c in curp]
        # Ajustar elementos después de la Ñ (por diseño)
        b37_list = [x+1 if x >= 23 else x for x in b36_list]

        # Sumar la multiplicación de cada elemento con su índice inverso
        # (empezando en 1), a excepción del último carácter, pues este es el de verificación
        b37_sum = sum([i*x for i,x in enumerate(b37_list[-2::-1], 1)])

        # Crear función lambda para hacer las operaciones finales
        m = lambda x : abs(x % 10 - 10)
        print(m(b37_sum))
        return m(b37_sum) == verify

    @classmethod
    def _create_map(cls, name):
        name_map = {}

        piece_index = 0

        for piece in re.findall(cls._word_regex, name):
            word = piece.split()[-1]
            name_map[piece_index] = {}

            # name_map[piece_index]["v"] = cls._find_vowel(word[1:])
            # name_map[piece_index]["c"] = cls._find_cons(word[1:])
            # name_map[piece_index]["l"] = word[:1]

            piece_index += 1
        return name_map

    @staticmethod
    def _remove_accents(word):
        return unidecode(word)


    @classmethod
    def validate(cls, curp, full_name):
        given_names = []
        f_surname = []
        m_surname = []

        names_obtained = False
        f_surn_obtained = False
        m_surn_obtained = False

        name_split = re.findall(cls._word_regex, full_name)
        al_name = cls._remove_accents(full_name)

        # "VEGR/010517/H/MC/NTS/A5": "RUSSELL NATAHEL VENEGAS GUTIERREZ"
        name_map = cls._create_map(al_name)
        alien = (curp[CURP.REGION_ONE:CURP.REGION_TWO + 1] == "NE")

        name_index = 0

        current_word = given_names

        for word in name_map:
            if not names_obtained and cls._matches_name(curp, name_map[word]):
                names_obtained = True
            elif (not f_surn_obtained and names_obtained
                  and cls._matches_f_surname(curp, name_map[word])):
                current_word = f_surname
                f_surn_obtained = True
            elif (not m_surn_obtained and f_surn_obtained
                  and cls._matches_m_surname(curp, name_map[word])):
                current_word = m_surname
                m_surn_obtained = True

            current_word.append(name_split[word])
            name_index += 1

        no_surn = (curp[2] == "X" and curp[14] == "X")

        if (names_obtained and f_surn_obtained
                and (m_surn_obtained or no_surn or alien)):

            return {"nombre": ' '.join(given_names),
                    "apellido": ' '.join(f_surname),
                    "apellido_m": ' '.join(m_surname)}

        else:
            return False
