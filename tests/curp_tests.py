#!/usr/bin/env python3

"""
CURPValidator Tests
Copyright (C) 2021
Jacob Sánchez Pérez
"""

# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.

import unittest
from datetime import date
from unidecode import unidecode
from hypothesis import given, assume
from hypothesis import strategies as st
from curp.curp import WordFeatures, CURP, CURPValidator
from curp import _estados


class TestUnidecode(unittest.TestCase):

    def test_accents_removal(self):
        vowels = {'A': ('Á', 'Ä'), 'E': ('É', 'Ë'), 'I': ('Í', 'Ī'),
                  'O': ('Ó', 'Ö'), 'U': ('Ú', 'Ü')}
        for k, v in vowels.items():
            for c in v:
                self.assertEqual(k, unidecode(c))


class TestWordFeatures(unittest.TestCase):

    def test_word_features(self):
        """
        Test that extracted word features are correct and follow CURP rules.
        """
        words = [
            ('ALVIRDE', 'A', 'I', 'L'),
            ('JAUREGUI', 'J', 'A', 'R'),
            ('DEL CASTILLO', 'C', 'A', 'S'),
            ('DE ANDA', 'A', 'A', 'N'),
            ('VAN DER PLAS', 'P', 'A', 'L'),
            ('MC GREGOR', 'G', 'E', 'R'),
            ('RIVA PALACIO', 'R', 'I', 'V'),
            ('ARGÜELLO', 'A', 'U', 'R'),
            ('ESTRADA', 'E', 'A', 'S'),
            ('DUEÑAS', 'D', 'U', 'X'),
            ('MUÑOZ', 'M', 'U', 'X'),
            ('LI', 'L', 'I', 'X'),
            ('ÑANDO', 'X', 'A', 'N'),
            ('', 'X', 'X', 'X')]

        for w in words:
            with self.subTest(w=w[0]):
                ft = WordFeatures(w[0])
                self.assertEqual(w[1], ft.char)
                self.assertEqual(w[2], ft.vowel)
                self.assertEqual(w[3], ft.consonant)


class TestCURP(unittest.TestCase):

    def test_wrong_len(self):
        """Test wrong CURP length"""
        curp = ("0123456789ABCDEFGHJ", "0123456789ABCDEFG", "")

        for c in curp:
            with self.subTest(c=c):
                with self.assertRaises(ValueError):
                    CURP(c)

    def test_dates(self):
        """Test date extraction"""
        dates = (("AARL981224MGTLJS03", "1998-12-24"), ("PERT220904MMSXZR01", "1922-09-04"),
                 ("FOTS990610HPLLPB01", "1999-06-10"), ("FOTS210610HPLLPB08", "2021-06-10"))

        for d in dates:
            with self.subTest(d=d):
                c = CURP(d[0])
                self.assertEqual(c.birth_date.isoformat(), d[1])

    def test_wrong_dates(self):
        """Test erroneous dates error raising"""
        dates = ("AARL980231MGTLJS01",
                 "AARL981331MGTLJS01", "AARL980532MGTLJS01")

        for d in dates:
            with self.subTest(d=d):
                with self.assertRaises(ValueError):
                    CURP(d)

    def test_sex(self):
        """Test sex extraction"""
        sexes = (("AARL981224MGTLJS03", 2), ("PERT220904MMSXZR01", 2),
                 ("FOTS990610HPLLPB01", 1), ("FOTS210610HPLLPB08", 1))

        for s in sexes:
            with self.subTest(s=s):
                c = CURP(s[0])
                self.assertEqual(c.sex, s[1])

    def test_wrong_sex(self):
        """Test invalid sex error raising"""
        sexes = ("AARL981224AGTLJS01", "PERT2209040MSXZR05",
                 "FOTS990610YPLLPB05", "FOTS210610@PLLPB05")

        for s in sexes:
            with self.subTest(s=s):
                with self.assertRaises(ValueError):
                    CURP(s)


class TestCURPValidator(unittest.TestCase):
    _template = "XXXXYYMMDDSRRXXXV0"

    @given(st.dates(min_value=date(1900, 1, 1), max_value=date(2099, 1, 1)),
           st.integers(0, 25))
    def test_birth_date_parsing(self, d: date, v: int) -> None:
        curp = self._template

        if d.year <= 1999:
            curp = curp.replace("V", str(v % 10))
        else:
            curp = curp.replace("V", chr(ord('A')+v))

        curp = curp.replace("YYMMDD", d.strftime("%y%m%d"))
        self.assertEqual(CURPValidator.parse_birth_date(curp), d)

    @given(st.integers(0, 99), st.integers(13, 99), st.integers(32, 99))
    def test_birth_date_parsing_error(self, y, m, d):
        curp = self._template.replace("YYMMDD", f"{y:02}{m}{d}")

        with self.assertRaises(ValueError):
            CURPValidator.parse_birth_date(curp)

    def test_sex_parsing(self) -> None:
        # Parametros correctos y su valor esperado de retorno
        curp_items = ((self._template.replace('S', 'H'), 1),
                      (self._template.replace('S', 'M'), 2))

        for i in curp_items:
            with self.subTest(i=i):
                self.assertEqual(CURPValidator.parse_sex(i[0]), i[1])

    @given(st.characters(blacklist_characters=('H', 'M')))
    def test_sex_parsing_error(self, c: str) -> None:
        # Deben alzar excepciones
        with self.assertRaises(ValueError):
            CURPValidator.parse_sex(self._template.replace('S', c))

    def test_region_parsing(self) -> None:
        # Parametros correctos y su valor esperado de retorno
        regiones = _estados._estados

        for k, v in regiones.items():
            curp = self._template.replace("RR", k)
            self.assertEqual(CURPValidator.parse_region(curp), v)

    @given(st.text(min_size=2, max_size=2))
    def test_region_parsing_error(self, r: str) -> None:
        assume(r not in _estados._estados)
        # Deben alzar excepciones
        with self.assertRaises(ValueError):
            CURPValidator.parse_sex(self._template.replace("RR", r))

    @unittest.skip("")
    def test_verify(self):
        CURPValidator.validate_verify("")
    # def test_name_splitting(self):
    #     curp_items = [
    #         {'curp': 'POPC990709MGTSRL02',
    #          'name': 'CLAUDIA LEONOR POSADA PEREZ',
    #          'result': {'nombre': 'CLAUDIA LEONOR', 'apellido': 'POSADA', 'apellido_m': 'PEREZ'}
    #         },
    #         {'curp': 'MAGE981117MMNCRS05',
    #          'name': 'ESTEFANIA DE LOS DOLORES MACIAS GARCIA',
    #          'result': {'nombre': 'ESTEFANIA DE LOS DOLORES', 'apellido': 'MACIAS', 'apellido_m': 'GARCIA'}
    #         },
    #         {'curp': 'MAPS991116MOCRZN07',
    #          'name': 'SANDRA DEL CARMEN MARTINEZ DE LA PAZ',
    #          'result': {'nombre': 'SANDRA DEL CARMEN', 'apellido': 'MARTINEZ', 'apellido_m': 'DE LA PAZ'}
    #         },
    #         {'curp': 'TAXA990915MNEMXM06',
    #          'name': 'AMBER NICOLE TAMAYO',
    #          'result': {'nombre': 'AMBER NICOLE', 'apellido': 'TAMAYO', 'apellido_m': ''}
    #         },
    #         {'curp': 'MXME991209MGRRSS07',
    #          'name': 'ESMERALDA MARTINEZ MASTACHE',
    #          'result': {'nombre': 'ESMERALDA', 'apellido': 'MARTINEZ', 'apellido_m': 'MASTACHE'}
    #         },
    #         {'curp': 'MACD990727MMMCRRN0',
    #          'name': 'DANIELA IVETTE MARTINEZ CRUZ',
    #          'result': False
    #         }
    #     ]
    #
    #     for i in curp_items:
    #         with self.subTest(i=i):
    #             r = CURPValidator.validate(i['curp'], i['name'])
    #             self.assertEqual(r, i['result'])


if __name__ == '__main__':
    unittest.main()
