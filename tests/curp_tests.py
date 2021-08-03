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
from curp.curp import WordFeatures, CURP, CURPValidator


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
            ('ESTRADA', 'E', 'A', 'S'),
            ('DUEÑAS', 'D', 'U', 'X'),
            ('MUÑOZ', 'M', 'U', 'X'),
            ('LI', 'L', 'I', 'X'),
            ('ÑANDEZ', 'X', 'A', 'N')]

        for w in words:
            with self.subTest(w=w[0]):
                ft = WordFeatures(w[0])
                self.assertEqual(w[1], ft.char)
                self.assertEqual(w[2], ft.vowel)
                self.assertEqual(w[3], ft.consonant)

class TestCURP(unittest.TestCase):

    def test_dates(self):
        """Test date extraction"""
        dates = (("AARL981224MGTLJS01", "1998-12-24"), ("PERT220904MMSXZR05", "1922-09-04"),
                 ("FOTS990610HPLLPB05", "1999-06-10"), ("FOTS210610HPLLPB05", "2021-06-10"))

        for d in dates:
            with self.subTest(d=d):
                c = CURP(d[0])
                self.assertEqual(c.birth_date.isoformat(), d[1])

    def test_wrong_dates(self):
        """Test erroneous dates error raising"""
        dates = ("AARL980231MGTLJS01", "AARL981331MGTLJS01", "AARL980532MGTLJS01")

        for d in dates:
            with self.subTest(d=d):
                with self.assertRaises(ValueError):
                    CURP(d)

    def test_sex(self):
        """Test sex extraction"""
        sexes = (("AARL981224MGTLJS01", 2), ("PERT220904MMSXZR05", 2),
                 ("FOTS990610HPLLPB05", 1), ("FOTS210610HPLLPB05", 1))

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

    def test_name_splitting(self):
        curp_items = [
            {'curp': 'POPC990709MGTSRL02',
             'name': 'CLAUDIA LEONOR POSADA PEREZ',
             'result': {'nombre': 'CLAUDIA LEONOR', 'apellido': 'POSADA', 'apellido_m': 'PEREZ'}
            },
            {'curp': 'MAGE981117MMNCRS05',
             'name': 'ESTEFANIA DE LOS DOLORES MACIAS GARCIA',
             'result': {'nombre': 'ESTEFANIA DE LOS DOLORES', 'apellido': 'MACIAS', 'apellido_m': 'GARCIA'}
            },
            {'curp': 'MAPS991116MOCRZN07',
             'name': 'SANDRA DEL CARMEN MARTINEZ DE LA PAZ',
             'result': {'nombre': 'SANDRA DEL CARMEN', 'apellido': 'MARTINEZ', 'apellido_m': 'DE LA PAZ'}
            },
            {'curp': 'TAXA990915MNEMXM06',
             'name': 'AMBER NICOLE TAMAYO',
             'result': {'nombre': 'AMBER NICOLE', 'apellido': 'TAMAYO', 'apellido_m': ''}
            },
            {'curp': 'MXME991209MGRRSS07',
             'name': 'ESMERALDA MARTINEZ MASTACHE',
             'result': {'nombre': 'ESMERALDA', 'apellido': 'MARTINEZ', 'apellido_m': 'MASTACHE'}
            },
            {'curp': 'MACD990727MMMCRRN0',
             'name': 'DANIELA IVETTE MARTINEZ CRUZ',
             'result': False
            }
        ]

        for i in curp_items:
            with self.subTest(i=i):
                r = CURPValidator.validate(i['curp'], i['name'])
                self.assertEqual(r, i['result'])


if __name__ == '__main__':
    unittest.main()
