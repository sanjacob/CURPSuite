#!/usr/bin/env python3

"""CURP Suite Tests"""

# Copyright (C) 2021, Jacob Sánchez Pérez

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
from hypothesis import given, assume
from hypothesis import strategies as st
from .strategies import NameGen

import string
from datetime import date
from unidecode import unidecode
from curp.curp import CURP, WordFeatures
from curp import estados, altisonantes
from curp import (CURPValueError, CURPLengthError,
                  CURPVerificationError, CURPNameError,
                  CURPFirstSurnameError, CURPSecondSurnameError,
                  CURPDateError, CURPSexError, CURPRegionError)


def fix_verification(curp: str) -> str:
    """Corregir dígito de verificación de una CURP."""
    cs = CURP._verification_sum(curp)
    d = CURP._sum_to_verify_digit(cs)
    return f"{curp[:-1]}{d}"

def normalise_word(word: str) -> str:
    """Capitalizar una palabra, reemplazar Ñ con X y remover acentos y diéresis."""
    return unidecode(word.upper().replace("Ñ", "X"))


class TestCURP(unittest.TestCase):
    _template = "AAAA000101MDFBBBHV"

    @given(st.text(max_size=17))
    def test_curp_too_short(self, curp: str):
        """Probar que una CURP muy corta genere error."""
        with self.assertRaises(CURPLengthError):
            CURP(curp)

    @given(st.text(min_size=19))
    def test_curp_too_long(self, curp: str):
        """Probar que una CURP muy larga genere error."""
        with self.assertRaises(CURPLengthError):
            CURP(curp)

    @given(NameGen.names())
    def test_name_validation(self, n: str) -> None:
        """Prueba la comprobación de CURP con un nombre de pila aleatorio.
        """
        # Procesar nombre
        name = normalise_word(n)

        # Modificar CURP
        curp = self._template
        curp = curp.replace("AAAA", f"AAA{name[0]}")
        curp = curp.replace("BBB", f"BB{name[2]}")
        curp = fix_verification(curp)

        # Probar clase CURP
        c = CURP(curp)
        self.assertTrue(c.nombre_valido(n))

    @given(NameGen.names())
    def test_compound_name_validation(self, n: str) -> None:
        """Prueba la comprobación de CURP con un nombre de pila compuesto
        aleatorio.
        """
        # Procesar nombre
        name = normalise_word(n)

        # Modificar CURP
        curp = self._template
        curp = curp.replace("AAAA", f"AAA{name[0]}")
        curp = curp.replace("BBB", f"BB{name[2]}")
        curp = fix_verification(curp)

        c = CURP(curp)

        # Probar con todos los nombres ignorados
        for i in CURP._ignored_names + ('JOSÉ', 'MARÍA', 'JÖSË', 'MÄRÍÁ'):
            self.assertTrue(c.nombre_valido(f"{i} {n}"))
            self.assertTrue(c.nombre_valido(f"{i.title()} {n}"))
            self.assertTrue(c.nombre_valido(f"{i.lower()} {n}"))

    def test_ignored_name_validation(self) -> None:
        """Probar la comprobación de la CURP con nombres comunes cuando el
        nombre no es compuesto."""
        for i in CURP._ignored_names:
            with self.subTest(i=i):
                wf = WordFeatures(i, CURP._ignored_words, CURP._special_chars)

                curp = self._template
                curp = curp.replace("AAAA", f"AAA{wf.char}")
                curp = curp.replace("BBB", f"BB{wf.consonant}")
                curp = fix_verification(curp)

                c = CURP(curp)
                self.assertTrue(c.nombre_valido(i))

    @given(NameGen.names())
    def test_first_surname_validation(self, n: str) -> None:
        """Prueba la comprobación de CURP con un primer apellido aleatorio.
        """
        name = normalise_word(n)

        curp = self._template
        curp = curp.replace("AAAA", f"{name[0]}{name[1]}AA")
        curp = curp.replace("BBB", f"{name[2]}BB")
        curp = fix_verification(curp)

        c = CURP(curp)
        self.assertTrue(c.primer_apellido_valido(n))

    def test_first_surname_inconvenient(self):
        """Probar la comprobación del apellido cuando la CURP contiene una
        palabra inconveniente."""
        rude = altisonantes.altisonantes

        for r, vowels in rude.items():
            curp = self._template.replace("AAAA", r)
            curp = fix_verification(curp)
            c = CURP(curp)

            for v in vowels:
                with self.subTest(r=r, v=v):
                    a = f"{r[0]}{v}B"
                    self.assertTrue(c.primer_apellido_valido(a))

    @given(NameGen.names())
    def test_second_surname_validation(self, n: str) -> None:
        """Prueba la comprobación de CURP con un segundo apellido aleatorio.
        """
        name = normalise_word(n)

        curp = self._template
        curp = curp.replace("AAAA", f"AA{name[0]}A")
        curp = curp.replace("BBB", f"B{name[2]}B")
        curp = fix_verification(curp)

        c = CURP(curp)
        self.assertTrue(c.segundo_apellido_valido(n))

    @given(st.dates(min_value=date(1900, 1, 1), max_value=date(2099, 1, 1)),
           st.integers(0, 25))
    def test_date_parse(self, d: date, v: int) -> None:
        """Probar la extracción correcta de fechas de la CURP."""
        curp = self._template

        if d.year <= 1999:
            # Insertar dígito como homoclave
            curp = curp.replace("H", str(v % 10))
        else:
            # Insertar letra como homoclave
            curp = curp.replace("H", chr(ord('A')+v))

        curp = curp.replace("000101", d.strftime("%y%m%d"))
        curp = fix_verification(curp)

        c = CURP(curp)
        self.assertEqual(c.fecha_nacimiento, d)

    @given(st.integers(0, 99), st.integers(13, 99), st.integers(1, 30))
    def test_date_parse_wrong_month(self, y: int, m: int, d: int):
        """Probar que fechas incorrectas provoquen una excepción."""
        curp = self._template.replace("000101", f"{y:02}{m}{d:02}")
        curp = fix_verification(curp)

        with self.assertRaises(CURPDateError):
            CURP(curp)

    @given(st.integers(0, 99), st.integers(1, 12), st.integers(32, 99))
    def test_date_parse_wrong_day(self, y, m, d):
        """Probar que fechas incorrectas provoquen una excepción."""
        curp = self._template.replace("000101", f"{y:02}{m:02}{d}")
        curp = fix_verification(curp)

        with self.assertRaises(CURPDateError):
            CURP(curp)

    def test_sex_parse(self) -> None:
        """Probar la extracción correcta del sexo de la CURP."""
        # Parametros correctos y su valor esperado de retorno
        curp_items = ((self._template.replace('M', 'H'), 1),
                      (self._template.replace('M', 'M'), 2))

        for i in curp_items:
            with self.subTest(i=i):
                curp = fix_verification(i[0])
                c = CURP(curp)
                self.assertEqual(c.sexo, i[1])

    @given(st.characters(blacklist_characters=('H', 'M')))
    def test_sex_parse_error(self, c: str) -> None:
        """Probar que caracteres incorrectos en sexo provoquen un error."""
        curp = self._template.replace('M', c)
        error = CURPSexError

        # Si el carácter es alfanumérico, cambiar dígito y
        # verificar que CURPSexError sea alzada.
        # De lo contrario, verificar que CURPValueError sea
        # alzada (No CURPVerificationError).

        try:
            int(c, 36)
        except ValueError:
            error = CURPValueError
        else:
            curp = fix_verification(curp)

        with self.assertRaises(error) as cm:
            CURP(curp)

        e = cm.exception
        self.assertNotEqual(type(e), CURPVerificationError)

    def test_region_parse(self) -> None:
        """Probar la extracción correcta de la entidad federativa de la CURP."""
        # Parametros correctos y su valor esperado de retorno
        regiones = estados.estados

        for k, v in regiones.items():
            curp = self._template.replace("DF", k)
            c = CURP(fix_verification(curp))
            self.assertEqual(c.entidad, v['name'])
            self.assertEqual(c.entidad_iso, v['iso'])

    @given(st.text(min_size=2, max_size=2))
    def test_region_parse_error(self, r: str) -> None:
        """Probar que códigos incorrectos de región provoquen un error."""
        assume(r not in estados.estados)
        curp = self._template.replace('DF', r)
        error = CURPRegionError

        # Si el carácter es alfanumérico, cambiar dígito y
        # verificar que CURPRegionError sea alzada.
        # De lo contrario, verificar que CURPValueError sea
        # alzada (No CURPVerificationError).

        try:
            [int(x, 36) for x in r]
        except ValueError:
            error = CURPValueError
        else:
            curp = fix_verification(curp)

        with self.assertRaises(error) as cm:
            CURP(curp)

        e = cm.exception
        self.assertNotEqual(type(e), CURPVerificationError)

    def test_verification_sum(self):
        """Probar la comprobación correcta del dígito de verificación."""
        charset = string.digits + string.ascii_uppercase

        # Probar cada carácter válido de la CURP en cada posición.
        for c in charset:
            b36 = int(c, 36)
            if b36 > 23:
                b36 += 1

            for n in range(2, 19):
                with self.subTest(c=c, n=n):
                    # La suma sólo tendrá un elemento.
                    sm = b36 * n

                    # Convertir a dígito
                    d = sm % 10
                    d = 10 - d if d else d

                    # Crear CURP
                    curp = ("0" * (18 - n)) + c + ("0" * (n - 2)) + str(d)
                    cs = CURP._verification_sum(curp)
                    vd = CURP._sum_to_verify_digit(cs)

                    self.assertEqual(sm, cs)
                    self.assertEqual(str(d), vd)

    @given(st.integers(0))
    def test_sum_to_digit(self, s: int):
        """Probar método para convertir suma en dígito verificador."""
        d = CURP._sum_to_verify_digit(s)
        self.assertEqual(len(d), 1)
        self.assertTrue(d.isdigit())

        # Alternativa a mod
        m = int(str(s)[-1])
        m = 10 - m if m else m
        self.assertEqual(str(m), d)


if __name__ == '__main__':
    unittest.main()
