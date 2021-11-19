#!/usr/bin/env python3

import unittest
from hypothesis import given

from curp import CURP
from curp.features import WordFeatures
from .utils import FeaturedWord
from .strategies import WordStrats


class TestWordFeatures(unittest.TestCase):
    """Pruebas de la clase WordFeatures."""

    @given(WordStrats.words())
    def test_word_features_extraction(self, featured_word: FeaturedWord) -> None:
        """Usar generador de palabras para probar la clase :class:`WordFeatures`."""
        wf = WordFeatures(featured_word)
        self.assertEqual(featured_word.char, wf.char)
        self.assertEqual(featured_word.vowel, wf.vowel)
        self.assertEqual(featured_word.consonant, wf.consonant)

    def test_word_features_extraction_examples(self) -> None:
        """Probar la extracción correcta de características de palabras."""
        words = [
            # Generales
            ('ALVIRDE', 'A', 'I', 'L'),
            ('JAUREGUI', 'J', 'A', 'R'),
            ('ESTRADA', 'E', 'A', 'S'),

            # Minúscula
            ('anna', 'A', 'A', 'N'),
            ('marcial', 'M', 'A', 'R'),

            # Acentos
            ('Álvaro', 'A', 'A', 'L'),
            ('maría', 'M', 'A', 'R'),

            # Letra inicial Ñ
            ('ÑANDO', 'X', 'A', 'N'),

            # Carácteres especiales (/, -, ., ')
            ('D/AMICO', 'D', 'X', 'X'),
            ("d’Arc", 'D', 'X', 'X'),
            ("B'IVANNY", 'B', 'X', 'X'),
            ('AL-SHAMI', 'A', 'X', 'L'),
            ('H. LUZ', 'H', 'X', 'X'),

            # Diéresis
            ('ARGÜELLO', 'A', 'U', 'R'),
            ('MÄNNIG', 'M', 'A', 'N'),
            ('Gëzim', 'G', 'E', 'Z'),
            ('Ingrïd', 'I', 'I', 'N'),
            ('WÖRNE', 'W', 'O', 'R'),
            ('DÖNICKE', 'D', 'O', 'N'),

            # Primera palabra de apellido compuesto
            ('RIVA PALACIO', 'R', 'I', 'V'),
            ('CABEZA DE VACA', 'C', 'A', 'B'),
            ('PONCE DE LEON', 'P', 'O', 'N'),
            ('MONTES DE OCA', 'M', 'O', 'N'),

            # Nombre compuesto con preposición
            # (DA, DAS, DE, DEL, DER, DI, DIE, DD,
            # EL, LA, LOS, LAS, LE, LES, MAC, MC,
            # VAN, VON, Y)
            ('da Silva', 'S', 'I', 'L'),
            ('DAS', 'D', 'A', 'S'),
            ('DE ANDA', 'A', 'A', 'N'),
            ('De Niro', 'N', 'I', 'R'),
            ('de Haas', 'H', 'A', 'S'),
            ('DEL CASTILLO', 'C', 'A', 'S'),
            ('de La Motte', 'M', 'O', 'T'),
            ('DE LOS SANTOS', 'S', 'A', 'N'),
            ('DE LAS FUENTES', 'F', 'U', 'N'),
            ('DE LAS CUEVAS', 'C', 'U', 'V'),
            ('der Ältere', 'A', 'E', 'L'),
            ('Di María', 'M', 'A', 'R'),
            ('EL CARMEN', 'C', 'A', 'R'),
            ('EL GERGI', 'G', 'E', 'R'),
            ('EL ATI', 'A', 'I', 'T'),
            ('La Rose', 'R', 'O', 'S'),
            ('LE LOREC', 'L', 'O', 'R'),
            ('LE SOTO', 'S', 'O', 'T'),
            ('LE CLERCQ', 'C', 'E', 'L'),
            ('Mac Laren', 'L', 'A', 'R'),
            ('MC GREGOR', 'G', 'E', 'R'),
            ('van Leeuwen', 'L', 'E', 'W'),
            ('van der Waals', 'W', 'A', 'L'),
            ('VAN DER PLAS', 'P', 'A', 'L'),
            ('van Beethoven', 'B', 'E', 'T'),
            ('van der Rohe', 'R', 'O', 'H'),
            ('Von Doom', 'D', 'O', 'M'),
            ('von der Vogelweide', 'V', 'O', 'G'),
            ('Y LOPEZ', 'L', 'O', 'P'),
            ('Y VARGAS', 'V', 'A', 'R'),
            ('Y MONTIEL', 'M', 'O', 'N'),

            # Preposición sola
            ('DA', 'D', 'A', 'X'),
            ('DAS', 'D', 'A', 'S'),
            ('DE', 'D', 'E', 'X'),
            ('DEL', 'D', 'E', 'L'),
            ('DER', 'D', 'E', 'R'),
            ('DI', 'D', 'I', 'X'),
            ('DIE', 'D', 'I', 'X'),
            ('DD', 'D', 'X', 'D'),
            ('EL', 'E', 'X', 'L'),
            ('LA', 'L', 'A', 'X'),
            ('LOS', 'L', 'O', 'S'),
            ('LAS', 'L', 'A', 'S'),
            ('LE', 'L', 'E', 'X'),
            ('LES', 'L', 'E', 'S'),
            ('MAC', 'M', 'A', 'C'),
            ('MC', 'M', 'X', 'C'),
            ('VAN', 'V', 'A', 'N'),
            ('VON', 'V', 'O', 'N'),
            ('Y', 'Y', 'X', 'X'),

            # No son preposición
            ('DU SOLIER', 'D', 'U', 'X'),
            ('van den Berg', 'D', 'E', 'N'),

            # Sin vocal interna
            ('ICH', 'I', 'X', 'C'),
            ('ALF', 'A', 'X', 'L'),
            ('ANN', 'A', 'X', 'N'),
            ('AXL', 'A', 'X', 'X'),
            ('IVY', 'I', 'X', 'V'),

            # Consonante interna es Ñ
            ('OÑATE', 'O', 'A', 'X'),
            ('PEÑA', 'P', 'E', 'X'),
            ('IÑIGO', 'I', 'I', 'X'),
            ('NUÑO', 'N', 'U', 'X'),
            ('MUÑOZ', 'M', 'U', 'X'),

            # Sin consonante interna
            ('PO', 'P', 'O', 'X'),
            ('LE', 'L', 'E', 'X'),
            ('HO', 'H', 'O', 'X'),
            ('YU', 'Y', 'U', 'X'),
            ('WU', 'W', 'U', 'X'),
            ('LI', 'L', 'I', 'X'),
            ('LEE', 'L', 'E', 'X'),
            ('DEE', 'D', 'E', 'X'),

            # Sin apellido
            ('', 'X', 'X', 'X')
        ]

        for w in words:
            with self.subTest(w=w[0]):
                ft = WordFeatures(
                    w[0],
                    CURP._ignored_words,
                    CURP._special_chars
                )
                self.assertEqual(w[1], ft.char)
                self.assertEqual(w[2], ft.vowel)
                self.assertEqual(w[3], ft.consonant)


if __name__ == '__main__':
    unittest.main()
