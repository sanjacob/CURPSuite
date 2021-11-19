#!/usr/bin/env python3

from __future__ import annotations

import string
from datetime import date
from unidecode import unidecode
from curp import CURP
from curp import estados, altisonantes
from .utils import normalise_word, build_curp, FeaturedWord, CURPSkeleton
from hypothesis import given
from hypothesis.strategies import (sampled_from, composite, tuples,
                                   integers, dates, lists, booleans)


class ASCIIStrats:
    """Contiene estrategias de :class:`hypothesis` para generar texto ascii."""

    @classmethod
    @composite
    def text(draw, cls, min_size: int = 0, max_size: int = None,
             lowercase: bool = True, uppercase: bool = True, digits: bool = True) -> str:
        """Genera texto ascii."""
        charset = ""

        if digits:
            charset += string.digits
        if lowercase:
            charset += string.ascii_lowercase
        if uppercase:
            charset += string.ascii_uppercase

        t = ''.join(draw(lists(sampled_from(charset), min_size=min_size, max_size=max_size)))
        return t

    @classmethod
    @composite
    def characters(draw, cls, lowercase: bool = True, uppercase: bool = True, digits: bool = True):
        return draw(cls.text(min_size=1, max_size=1, lowercase=lowercase, uppercase=uppercase, digits=digits))


class WordStrats:
    """Contiene estrategias de :class:`hypothesis` para generar palabras."""

    # Charsets
    _consonants = 'BCDFGHJKLMNÑPQRSTVWXYZ'
    _vowels = 'AÁÄEÉËIÍÏOÓÖUÚÜ'

    # Duplicar los charsets ahora en minúscula
    _consonants += _consonants.lower()
    _vowels += _vowels.lower()
    _alphabet = _vowels + _consonants

    @classmethod
    @composite
    def words(draw, cls, min_size: int = 0, max_size: int = None) -> FeaturedWord:
        """Estrategia para generar palabras con características
        (1ra letra, vocal interna y consonante interna).

        :param min_size: Longitud mínima de palabra, por defecto es 0.
        :param max_size: Longitud máxima de palabra.
        :return: Objeto que contiene palabra y sus características.
        :rtype: :class:`FeaturedWord`
        """

        # Empezar por generar una lista de booleanos
        bool_list = draw(lists(booleans(), min_size=min_size, max_size=max_size))
        # Convertir booleanos a vocales/consonantes, creando así una palabra
        word = [draw(cls.vowels()) if x else draw(cls.consonants()) for x in bool_list]

        # Obtener posiciones de primera consonante y vocal internas
        try:
            first_consonant = bool_list[1:].index(False) + 1
        except ValueError:
            first_consonant = -1
        try:
            first_vowel = bool_list[1:].index(True) + 1
        except ValueError:
            first_vowel = -1

        fw = FeaturedWord(
            word=''.join(word), vowel=first_vowel, consonant=first_consonant
        )
        return fw

    @classmethod
    @composite
    def letters(draw, cls) -> str:
        """Letras del alfabeto español."""
        return draw(sampled_from(cls._alphabet))

    @classmethod
    @composite
    def vowels(draw, cls) -> str:
        """Vocales del alfabeto español. Incluye versiones con acentos y diéresis."""
        return draw(sampled_from(cls._vowels))

    @classmethod
    @composite
    def consonants(draw, cls) -> str:
        """Consonantes del alfabeto español."""
        return draw(sampled_from(cls._consonants))


class CURPStrats:
    """Estrategias de :class:`hypothesis` para generar la CURP Mexicana
    y sus atributos."""

    _regions = estados.estados
    _altisonantes = altisonantes.altisonantes
    _sexes = ('H', 'M')
    _consonants = 'BCDFGHJKLMNPQRSTVWXYZ'
    _vowels = 'AEIOUX'

    @classmethod
    @composite
    def curps(draw, cls) -> CURPSkeleton:
        """Estrategia que genera Claves Únicas de Registro de Población.
        :return: Dataclass que contiene la CURP y los datos de la misma."""

        surnames = []

        # Generar nombre y dos apellidos
        w = draw(WordStrats.words(min_size=1))
        given_name = w

        for _ in range(2):
            w = draw(WordStrats.words())
            surnames.append(w)

        # Asegurar que no existan casos en los que
        # el primer apellido este vacío y el segundo no
        surnames.sort(reverse=True)

        sex = draw(cls.sexes())
        date = draw(cls.birth_dates())
        region = draw(cls.mexican_states())

        curp = build_curp(
            name=given_name,
            first_surname=surnames[0],
            second_surname=surnames[1],
            date=date,
            sex=sex[0],
            region=region[0]
        )

        sk = CURPSkeleton(
            curp=curp,
            name=given_name,
            first_surname=surnames[0],
            second_surname=surnames[1],
            birth_date=date,
            sex=sex[1],
            region=region[1]

        )

        return sk

    @classmethod
    @composite
    def birth_dates(draw, cls) -> date:
        """Estrategia que genera objetos :class:`datetime.date` entre
        1900-01-01 y 2099-12-31."""
        return draw(dates(min_value=date(1900, 1, 1), max_value=date(2099, 12, 31)))

    @classmethod
    @composite
    def sexes(draw, cls) -> tuple[str, int]:
        """Estrategia que genera claves de sexo válidas para la CURP.
        :return: Tupla conteniendo la clave de sexo y su valor numérico.
        """
        i = draw(integers(1, len(cls._sexes)))
        return (cls._sexes[i - 1], i)

    @classmethod
    @composite
    def mexican_states(draw, cls) -> tuple[str, dict[str, str]]:
        """Estrategia que genera claves de entidad federativa válidas para la CURP.
        :return: Tupla conteniendo la clave de entidad federativa y
            un diccionario de datos de la entidad.
        """
        a = sampled_from(sorted(cls._regions.keys()))
        k = draw(a)
        v = cls._regions[k]
        return (k, v)

    @classmethod
    @composite
    def ignored_words(draw, cls) -> str:
        """Palabras ignoradas en la CURP."""
        return draw(sampled_from(CURP._ignored_words))

    @classmethod
    @composite
    def ignored_names(draw, cls) -> str:
        """Palabras ignoradas en la CURP."""
        return draw(sampled_from(CURP._ignored_names))

    @classmethod
    @composite
    def ignored_strings(draw, cls, min_size=0, max_size=None) -> str:
        """Cadena de palabras ignoradas."""
        return draw(lists(cls.ignored_words(), min_size=min_size, max_size=max_size).map(' '.join))

    @classmethod
    @composite
    def inconvenient(draw, cls) -> str:
        """Palabras inconvenientes de la CURP."""
        k = draw(sampled_from(sorted(cls._altisonantes.keys())))
        v = draw(sampled_from(cls._altisonantes[k]))
        return f"{k[0]}{v}{k[2:]}"

    @classmethod
    @composite
    def vowels(draw, cls) -> str:
        """Vocales que pueden aparecer en la CURP."""
        return draw(sampled_from(cls._vowels))

    @classmethod
    @composite
    def consonants(draw, cls) -> str:
        """Consonantes que pueden aparecer en la CURP."""
        return draw(sampled_from(cls._consonants))
