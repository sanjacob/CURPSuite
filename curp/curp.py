#!/usr/bin/env python3

import re
from enum import IntEnum
from datetime import date
from functools import partialmethod
from unidecode import unidecode

"""
CURP: Un sistema orientado a objetos de
validación y extracción de datos de la CURP

Jacob Sánchez Pérez
Copyright (C) 2020
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


# CURP Tuplas:

_valid_sexes = {'H': 1, 'M': 2}

# Abreviaciones de los estados en la CURP
_valid_regions = ('AS', 'BC', 'BS', 'CC',
                  'CL', 'CM', 'CS', 'CH',
                  'DF', 'DG', 'GT', 'GR',
                  'HG', 'JC', 'MC', 'MN',
                  'MS', 'NT', 'NL', 'OC',
                  'PL', 'QT', 'QR', 'SP',
                  'SL', 'SR', 'TC', 'TS',
                  'TL', 'VZ', 'YN', 'ZS',
                  'NE')

# Palabras inconvenientes de la CURP
# (Prefijos prohibidos)
_inconvenient = {
    "BXCA": ("BACA"),
    "BXKA": ("BAKA"),
    "BXEI": ("BUEI"),
    "BXEY": ("BUEY"),
    "CXCA": ("CACA"),
    "CXCO": ("CACO"),
    "CXGA": ("CAGA"),
    "CXGO": ("CAGO"),
    "CXKA": ("CAKA"),
    "CXKO": ("CAKO"),
    "CXGE": ("COGE"),
    "CXGI": ("COGI"),
    "CXJA": ("COJA"),
    "CXJE": ("COJE"),
    "CXJI": ("COJI"),
    "CXJO": ("COJO"),
    "CXLA": ("COLA"),
    "CXLO": ("CULO"),
    "FXLO": ("FALO"),
    "FXTO": ("FETO"),
    "GXTA": ("GETA"),
    "GXEI": ("GUEI"),
    "GXEY": ("GUEY"),
    "JXTA": ("JETA"),
    "JXTO": ("JOTO"),
    "KXCA": ("KACA"),
    "KXCO": ("KACO"),
    "KXGA": ("KAGA"),
    "KXGO": ("KAGO"),
    "KXKA": ("KAKA"),
    "KXKO": ("KAKO"),
    "KXGE": ("KOGE"),
    "KXGI": ("KOGI"),
    "KXJA": ("KOJA"),
    "KXJE": ("KOJE"),
    "KXJI": ("KOJI"),
    "KXJO": ("KOJO"),
    "KXLA": ("KOLA"),
    "KXLO": ("KULO"),
    "LXLO": ("LILO"),
    "LXCA": ("LOCA"),
    "LXCO": ("LOCO"),
    "LXKA": ("LOKA"),
    "LXKO": ("LOKO"),
    "MXME": ("MAME"),
    "MXMO": ("MAMO"),
    "MXAR": ("MEAR", "MIAR"),
    "MXAS": ("MEAS"),
    "MXON": ("MEON", "MION"),
    "MXCO": ("MOCO"),
    "MXKO": ("MOKO"),
    "MXLA": ("MULA"),
    "MXLO": ("MULO"),
    "NXCA": ("NACA"),
    "NXCO": ("NACO"),
    "PXDA": ("PEDA"),
    "PXDO": ("PEDO"),
    "PXNE": ("PENE"),
    "PXPI": ("PIPI"),
    "PXTO": ("PITO", "PUTO"),
    "PXPO": ("POPO"),
    "PXTA": ("PUTA"),
    "QXLO": ("QULO"),
    "RXTA": ("RATA"),
    "RXBA": ("ROBA"),
    "RXBE": ("ROBE"),
    "RXBO": ("ROBO"),
    "RXIN": ("RUIN"),
    "SXNO": ("SENO"),
    "TXTA": ("TETA"),
    "VXCA": ("VACA"),
    "VXGA": ("VAGA"),
    "VXGO": ("VAGO"),
    "VXKA": ("VAKA"),
    "VXEI": ("VUEI"),
    "VXEY": ("VUEY"),
    "WXEI": ("WUEI"),
    "WXEY": ("WUEY")
}


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
    def __init__(self, curp : str, full_name : str = None, given_name : str = None,
                 surname : str = None, second_surname : str = None, birth_date : date = None , sex : int = None):
        """
        Representa una CURP
        Parámetros adicionales serán comparados con los datos de la CURP
        y se regresará un error si éstos no coinciden

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
        second_millenia = False

        # Homonímia
        # R
        homonymy = curp[CURPChar.HOMONYMY]

        # Código de verificación
        verify = curp[CURPChar.VERIFICATION]

        try:
            int(homonymy)
        except ValueError:
            #



        # Día de nacimiento
        day = int(curp[CURPChar.DAY_ONE] + curp[CURPChar.DAY_TWO])
        month = int(curp[CURPChar.MONTH_ONE] + curp[CURPChar.MONTH_TWO])

        #
        year = curp[CURPChar.YEAR_ONE] + curp[CURPChar.YEAR_TWO]

        today = date.today()
        current_year = today.strftime("%y")
        century = today.strftime("%Y")[:-2]

        if int(year) > int(current_year):
            century = str(int(century) - 1)

        year = century + year

        # Regresar con error si la fecha es incorrecta
        try:
            self._birth_date = date(int(year), month, day)
        except ValueError as e:
            raise ValueError("Birth date is incorrect")


        # Sexo
        curp_sex = curp[CURPChar.SEX]
        self._sex = _valid_sexes.get(curp_sex, 0)

        if not self._sex or (sex is not None and self._sex != sex):
            raise ValueError("Sex is incorrect")


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

        # Código de verificación
        verify = curp[CURPChar.VERIFICATION]

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


class CURPValidator:
    _word_regex = r'((?:DEL? )?(?:L(?:A|O)S? )?(?:\w|-)+\'?\b)'

    @classmethod
    def _create_map(cls, name):
        name_map = {}

        piece_index = 0

        for piece in re.findall(cls._word_regex, name):
            word = piece.split()[-1]
            name_map[piece_index] = {}

            name_map[piece_index]["v"] = cls._find_vowel(word[1:])
            name_map[piece_index]["c"] = cls._find_cons(word[1:])
            name_map[piece_index]["l"] = word[:1]

            piece_index += 1
        return name_map

    @staticmethod
    def _remove_accents(word):
        return unidecode(word)

    @staticmethod
    def _matches_name(curp, name_map):
        matches = ((curp[CURP.NAME_FIRST_LETTER] == name_map["l"]) and
            (curp[CURP.NAME_NEXT_CSNT] == name_map["c"]))

        return matches

    @staticmethod
    def _matches_f_surname(curp, name_map):

        matches = ((curp[CURP.SURNAME_FIRST_LETTER] == name_map["l"])
                   and (curp[CURP.SURNAME_FIRST_VOWEL] == name_map["v"])
                   and (curp[CURP.SURNAME_NEXT_CSNT] == name_map["c"]))

        # Match instead against what the uncensored letter would be,
        # according to our own mapping

        if not matches and curp[:CURP.NAME_FIRST_LETTER + 1] in censored:
            for i_word in inconvenient[curp[:CURP.NAME_FIRST_LETTER + 1]]:
                if not matches:
                    matches = ((curp[CURP.SURNAME_FIRST_LETTER] == name_map["l"])
                               and (i_word[CURP.SURNAME_FIRST_VOWEL] == name_map["v"])
                               and (curp[CURP.SURNAME_NEXT_CSNT] == name_map["c"]))

        return matches

    @staticmethod
    def _matches_m_surname(curp, name_map):
        matches = ((curp[CURP.SURNAME_M_FIRST_LETTER] == name_map["l"]) and
            (curp[CURP.SURNAME_M_NEXT_CSNT] == name_map["c"]))

        return matches

    @staticmethod
    def validate_region(curp):

        return (curp[CURP.REGION_ONE:CURP.REGION_TWO + 1] in valid_regions)

    @staticmethod
    def validate_gender(curp):
        return (curp[CURP.GENDER] == 'H' or curp[CURP.GENDER] == 'M')

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
