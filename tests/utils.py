#!/usr/bin/env python3

from __future__ import annotations

from datetime import date
from unidecode import unidecode
from dataclasses import dataclass
from curp import CURP
from curp.chars import CURPChar
from curp.altisonantes import altisonantes


class FeaturedWord(str):
    """Similar a :class:`WordFeatures` pero las posiciones de las características
    son especificadas al crear el objeto.

    :param word: Palabra
    :param char: Posición del primer carácter.
    :param vowel: Posición de la primera vocal.
    :param consonant: Posición de la primera consonante.

    Si alguna de las posiciones es -1 la característica asignada será "X"
    """

    def __new__(cls, word="", char: int = 0, vowel: int = 1, consonant: int = 2):
        obj = str.__new__(cls, word)
        w = normalise_word(word)
        assert len(w) > max(vowel, consonant)
        obj._char = w[char] if w else "X"
        obj._vowel = w[vowel] if vowel != -1 else "X"
        obj._consonant = w[consonant] if consonant != -1 else "X"
        return obj

    @property
    def char(self) -> str:
        return self._char

    @property
    def vowel(self) -> str:
        return self._vowel

    @property
    def consonant(self) -> str:
        return self._consonant

    def loosely_eq(self, other: 'FeaturedWord') -> bool:
        """Compara aproximadamente si tiene las mismas características que otra palabra."""
        diff = (self.char == other.char and
                self.consonant == other.consonant)
        return diff

    def __eq__(self, other: Any) -> bool:
        if isinstance(other, FeaturedWord):
            diff = (self.char == other.char and
                    self.vowel == other.vowel and
                    self.consonant == other.consonant)
            return diff
        elif isinstance(other, str):
            return str(self) == other
        else:
            return NotImplemented

    def __ne__(self, other: Any) -> bool:
        return not self == other

    def __repr__(self) -> str:
        return f"<FeaturedWord [{self}]>"


@dataclass(frozen=True)
class CURPSkeleton:
    """Holds data that belongs to a CURP."""
    curp: str
    name: FeaturedWord
    first_surname: FeaturedWord
    second_surname: FeaturedWord
    birth_date: date
    sex: int
    region: dict[str, str]

    @property
    def full_name(self) -> str:
        return f"{self.name} {self.first_surname} {self.second_surname}"


def fix_verification(curp: str) -> str:
    """Corregir dígito de verificación de una CURP."""
    cs = CURP._verification_sum(curp)
    d = CURP._sum_to_verify_digit(cs)
    return f"{curp[:-1]}{d}"

def normalise_word(word: str) -> str:
    """Procesar palabra para eliminar peculiaridades y volverla mayúscula."""
    return unidecode(word.upper().replace("Ñ", "X"))

def build_curp(name: FeaturedWord = None, first_surname: FeaturedWord = None,
               second_surname: FeaturedWord = None, date: date = date(2000, 1, 1),
               sex: str = 'M', region: str = 'DF', fix_digit: bool = True) -> str:
    """Ensambla una CURP a partir de parámetros."""
    n, f, s = name, first_surname, second_surname
    hc = '0' if date.year <= 1999 else 'A'
    curp = f"{f.char}{f.vowel}{s.char}{n.char}"

    # Si la CURP forma palabra inconveniente, censurar
    censored = f"{curp[0]}X{curp[2:]}"
    if censored in altisonantes:
        if curp[1] in altisonantes[censored]:
            curp = censored

    curp += f"{date:%y%m%d}{sex}{region}"
    curp += f"{f.consonant}{s.consonant}{n.consonant}{hc}V"

    if fix_digit:
        curp = fix_verification(curp)

    return curp

def insert_in_word(word: str, c: str, i: int):
    """Reemplaza cierta sección de una string con otra string."""
    return f"{word[:i]}{c}{word[i + len(c):]}"

def change_curp(curp: str, c: str = None, i: int = None, chars: str = None, consonants: str = None,
                date: str = None, sex: str = None, region: str = None):
    """Permite el reemplazo de un elemento de una CURP."""
    if c is not None and i is not None:
        curp = insert_in_word(curp, c, i)

    if chars is not None:
        curp = insert_in_word(curp, chars, CURPChar.SURNAME_A_CHAR)

    if consonants is not None:
        curp = insert_in_word(curp, consonants, CURPChar.SURNAME_A_CONSONANT)

    if date is not None:
        curp = insert_in_word(curp, date, CURPChar.YEAR_0)

    if sex is not None:
        curp = insert_in_word(curp, sex, CURPChar.SEX)

    if region is not None:
        curp = insert_in_word(curp, region, CURPChar.REGION_0)

    # Si es posible, arreglar dígito de verificación
    if curp.isalnum():
        curp = fix_verification(curp)

    return curp
