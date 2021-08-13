#!/usr/bin/env python3

import unittest
from curp.curp import CURPValidator
from curp.features import WordFeatures


class TestWordFeatures(unittest.TestCase):
    """Pruebas de la clase WordFeatures."""

    def test_word_features(self):
        """Probar la extracción correcta de características de palabras."""
        words = [
            ('ALVIRDE', 'A', 'I', 'L'),
            ('Álvaro', 'A', 'A', 'L'),
            ('JAUREGUI', 'J', 'A', 'R'),
            ('DEL CASTILLO', 'C', 'A', 'S'),
            ('DE ANDA', 'A', 'A', 'N'),
            ('VAN DER PLAS', 'P', 'A', 'L'),
            ('MC GREGOR', 'G', 'E', 'R'),
            ('RIVA PALACIO', 'R', 'I', 'V'),
            ('ARGÜELLO', 'A', 'U', 'R'),
            ('ESTRADA', 'E', 'A', 'S'),
            ('maría', 'M', 'A', 'R'),
            ('DUEÑAS', 'D', 'U', 'X'),
            ('MUÑOZ', 'M', 'U', 'X'),
            ('LI', 'L', 'I', 'X'),
            ('ÑANDO', 'X', 'A', 'N'),
            ('D/AMICO', 'D', 'X', 'X'),
            ("D'ARCO", 'D', 'X', 'X'),
            ('AL-SHAMI', 'A', 'X', 'L'),
            ('H. LUZ', 'H', 'X', 'X'),
            ('', 'X', 'X', 'X')]

        for w in words:
            with self.subTest(w=w[0]):
                ft = WordFeatures(
                    w[0],
                    CURPValidator._ignored_words,
                    CURPValidator._special_chars
                )
                self.assertEqual(w[1], ft.char)
                self.assertEqual(w[2], ft.vowel)
                self.assertEqual(w[3], ft.consonant)


if __name__ == '__main__':
    unittest.main()
