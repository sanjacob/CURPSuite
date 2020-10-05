#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import re

# CURPValidator, una función para comprobar una curp contra un
# nombre completo y obtener las partes de este
# Copyright (C) 2020  Jacob Sánchez Pérez

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


class CURPValidator:
    _word_regex = r'((?:DEL? )?(?:L(?:A|O)S? )?(?:\w|-)+\'?\b)'

    @staticmethod
    def _find_vowel(word, pos=0):
        i = re.findall("[AEIOU]", word)
        return "X" if len(i) <= pos else i[pos]

    @staticmethod
    def _find_cons(word, pos=0):
        i = re.findall("[BCDFGHJKLMNÑPQRSTVWXYZ]", word)

        consonant = "X" if len(i) <= pos else i[pos]

        if consonant == "Ñ":
            consonant = "X"

        return consonant

    @staticmethod
    def _removeAccents(word):
        accentless = word.replace("Á", "A")
        accentless = accentless.replace("É", "E")
        accentless = accentless.replace("Í", "I")
        accentless = accentless.replace("Ó", "O")
        accentless = accentless.replace("Ú", "U")
        accentless = accentless.replace("Ü", "U")
        accentless = accentless.replace("Ö", "O")

        return accentless

    @classmethod
    def _createMap(cls, name):
        curp_map = {}

        piece_index = 0

        for piece in re.findall(cls._word_regex, name):
            word = piece.split()[-1]
            curp_map[piece_index] = {}

            curp_map[piece_index]["v"] = cls._find_vowel(word[1:])
            curp_map[piece_index]["c"] = cls._find_cons(word[1:])
            curp_map[piece_index]["l"] = word[:1]

            piece_index += 1
        return curp_map

    @staticmethod
    def _matchesName(curp, name_map):
        matches = ((curp[3] == name_map["l"]) and (curp[15] == name_map["c"]))

        return matches

    @staticmethod
    def _matchesFSurname(curp, name_map):
        censored = ["RXBE", "RXTA", "CXGA", "MXME",
                    "LXCA", "CXCA", "VXGA", "MXAR",
                    "CXGO", "RXBA", "VXCA", "BXCA",
                    "CXGE", "PXNE", "FXLO", "LXCO",
                    "TXTA", "MXAS", "NXCA", "NXCO",
                    "CXGI", "CXLA", "CXLO", "MXMO",
                    "PXTA", "FXJE", "CXJE", "MXLO",
                    "MXLA", "PXTO", "CXLA", "CXCO",
                    "VXGO", "CXJA", "MXCO", "MXON",
                    "QXLO", "PXDA", "MXAR", "CXKA",
                    "VXKA", "RXBO", "CXJI", "CXJO",
                    "SXNO", "SXXO", "GXEI", "GXEY",
                    "MXKO", "KXGA", "MXON", "KXGE",
                    "LXLO", "LXLO", "GXTA", "PXTO"]

        bad_words = ["ROBE", "RATA", "CAGA", "MAME",
                     "LOCA", "CACA", "VAGA", "MEAR",
                     "CAGO", "ROBA", "VACA", "BACA",
                     "COGE", "PENE", "FALO", "LOCO",
                     "TETA", "MEAS", "NACA", "NACO",
                     "COGI", "COLA", "CULO", "MAMO",
                     "PUTA", "FAJE", "COJE", "MULO",
                     "MULA", "PUTO", "CULA", "CACO",
                     "VAGO", "COJA", "MOCO", "MEON",
                     "QULO", "PEDA", "MIAR", "CAKA",
                     "VAKA", "ROBO", "COJI", "COJO",
                     "SENO", "SEXO", "GUEI", "GUEY",
                     "MOKO", "KAGA", "MION", "KOGE",
                     "LILO", "LELO", "GETA", "PITO"]

        matches = ((curp[0] == name_map["l"])
                   and (curp[1] == name_map["v"])
                   and (curp[13] == name_map["c"]))

        # Match instead against what the uncensored letter would be,
        # according to our own mapping

        if not matches and curp[:4] in censored:
            indices = [i for i, x in enumerate(censored) if x == curp[:4]]

            for index in indices:
                if not matches:
                    matches = ((curp[0] == name_map["l"])
                               and (bad_words[index][1] == name_map["v"])
                               and (curp[13] == name_map["c"]))

        return matches

    @staticmethod
    def _matchesMSurname(curp, name_map):
        matches = ((curp[2] == name_map["l"]) and (curp[14] == name_map["c"]))

        return matches

    @classmethod
    def validate(cls, curp, full_name):
        given_names = []
        f_surname = []
        m_surname = []

        names_obtained = False
        f_surn_obtained = False
        m_surn_obtained = False

        name_split = re.findall(cls._word_regex, full_name)
        al_name = cls._removeAccents(full_name)

        # "VEGR/010517/H/MC/NTS/A5": "RUSSELL NATAHEL VENEGAS GUTIERREZ"
        curp_map = cls._createMap(al_name)
        alien = (curp[11:13] == "NE")

        name_index = 0

        current_word = given_names

        for word in curp_map:
            if not names_obtained and cls._matchesName(curp, curp_map[word]):
                names_obtained = True
            elif (not f_surn_obtained and names_obtained
                  and cls._matchesFSurname(curp, curp_map[word])):
                current_word = f_surname
                f_surn_obtained = True
            elif (not m_surn_obtained and f_surn_obtained
                  and cls._matchesMSurname(curp, curp_map[word])):
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
