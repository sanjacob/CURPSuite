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

# Copyright (C) 2021, Jacob Sánchez Pérez

from __future__ import annotations

from unidecode import unidecode
from functools import partialmethod


class WordFeatures:
    """
    Extrae ciertos caracteres de una palabra:

    - Primer carácter
    - Primera vocal interna
    - Primera consonante interna

    Si no se encuentra alguna de las anteriores,
    una "X" tomará su lugar

    Cualquier "Ñ" será reemplazada con una "X"

    :param str word: Palabra a analizar
    :param tuple[str] ignored_words: Tupla de palabras que no se usarán
    para el análisis si no es absolutamente necesario
    :param tuple[str] special_chars: Caracteres que sirven como separador de
    palabras
    """

    _vowels = "AEIOU"
    _consonants = "BCDFGHJKLMNÑPQRSTVWXYZ"

    def __init__(self, word: str, ignored_words: tuple[str, ...] = (),
                 special_chars: tuple[str, ...] = ()):
        self._char = "X"

        # Reemplazar Ñ's
        word = unidecode(word.upper().replace("Ñ", "X"))

        for c in special_chars:
            word = word.replace(c, " ")

        # Remover preposiciones, conjunciones, etc.
        pieces = word.split()

        if pieces:
            # Preservar última palabra
            pieces = [w for w in pieces[:-1]
                      if w not in ignored_words] + [pieces[-1]]

            # Usar primera palabra del apellido
            word = pieces[0]
            self._char = word[0]

        self._vowel = self._find_vowel(word[1:])
        self._consonant = self._find_consonant(word[1:])

    @staticmethod
    def _find_char(charset: str, word: str, pos: int = 0) -> str:
        """Encuentra cualquier carácter de un set regex en una palabra."""
        # Más rápido que regex para este caso
        for char in word[pos:]:
            if char in charset:
                return char
        return "X"

    _find_vowel = partialmethod(_find_char, _vowels)
    _find_consonant = partialmethod(_find_char, _consonants)

    @property
    def char(self) -> str:
        """Primer carácter."""
        return self._char

    @property
    def vowel(self) -> str:
        """Primera vocal interna."""
        return self._vowel

    @property
    def consonant(self) -> str:
        """Primera consonante interna."""
        return self._consonant
