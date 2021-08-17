#!/usr/bin/env python3

from hypothesis import given
from hypothesis.strategies import sampled_from, composite, tuples


class NameGen():
    """Contiene estrategias de `hypothesis` para probar la clase CURP."""

    # Charsets
    _consonants = 'BCDFGHJKLMNÑPQRSTVWXYZ'
    _vowels = 'AÁÄEÉËIÍÏOÓÖUÚÜ'

    # Duplicar los charsets ahora en minúscula
    _consonants += _consonants.lower()
    _vowels += _vowels.lower()
    _alphabet = _vowels + _consonants

    @classmethod
    @composite
    def names(draw, cls):
        """Palabras de 3 carácteres, una letra, una vocal y una consonante en ese orden."""
        return draw(tuples(cls.letters(), cls.vowels(), cls.consonants()).map("".join))

    @classmethod
    @composite
    def letters(draw, cls):
        """Letras del alfabeto Mexicano."""
        return draw(sampled_from(cls._alphabet))

    @classmethod
    @composite
    def vowels(draw, cls):
        """Vocales del alfabeto Mexicano."""
        return draw(sampled_from(cls._vowels))

    @classmethod
    @composite
    def consonants(draw, cls):
        """Consonantes del alfabeto Mexicano."""
        return draw(sampled_from(cls._consonants))
