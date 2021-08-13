#!/usr/bin/env python3

import unittest
from unidecode import unidecode


class TestUnidecode(unittest.TestCase):
    """Probar el método unidecode para remover acentos y diéresis de palabras."""

    def test_accents_removal(self):
        """Probar la remoción de acentos/diéresis de vocales."""
        vowels = {'A': ('Á', 'Ä'), 'E': ('É', 'Ë'), 'I': ('Í', 'Ī'),
                  'O': ('Ó', 'Ö'), 'U': ('Ú', 'Ü')}
        for k, v in vowels.items():
            for c in v:
                self.assertEqual(k, unidecode(c))


if __name__ == '__main__':
    unittest.main()
