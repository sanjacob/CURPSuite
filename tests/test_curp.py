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
from hypothesis import given, assume, example
from hypothesis import strategies as st
from .utils import CURPSkeleton, FeaturedWord, change_curp
from .strategies import WordStrats, CURPStrats, ASCIIStrats

import json
import string
from datetime import date
from unidecode import unidecode
from curp.curp import CURP, WordFeatures
from curp import estados, altisonantes
from curp import (CURPValueError, CURPLengthError,
                  CURPVerificationError, CURPNameError,
                  CURPFirstSurnameError, CURPSecondSurnameError,
                  CURPDateError, CURPSexError, CURPRegionError)


class TestCURP(unittest.TestCase):
    """Pruebas de la clase CURP."""

    _common_names = (
        'MARIA', 'MA', 'MA.', 'JOSE', 'J', 'J.',
        'JOSÉ', 'MARÍA', 'JÖSË', 'MÄRÍÁ'
    )

    _charset = string.digits + string.ascii_uppercase

    # Pruebas que requieren que la construcción del objeto falle

    @given(st.text(max_size=17))
    def test_creation_curp_too_short(self, curp: str) -> None:
        """Probar que una CURP muy corta genere error."""
        with self.assertRaises(CURPLengthError):
            CURP(curp)

    @given(st.text(min_size=19))
    def test_creation_curp_too_long(self, curp: str) -> None:
        """Probar que una CURP muy larga genere error."""
        with self.assertRaises(CURPLengthError):
            CURP(curp)

    @given(CURPStrats.curps())
    def test_creation_verification_digit_check(self, sk: CURPSkeleton) -> None:
        """Probar que sólo un dígito de verificación sea válido para cada CURP."""
        d = int(sk.curp[-1])
        for i in range(10):
            if i != d:
                with self.assertRaises(CURPVerificationError):
                    CURP(f"{sk.curp[:-1]}{i}")
            else:
                CURP(sk.curp)

    @given(CURPStrats.curps(), WordStrats.words())
    def test_creation_name_error(self, sk: CURPSkeleton, fake_name: FeaturedWord) -> None:
        """Prueba la creación de una CURP con un nombre de pila incorrecto."""
        # Asumir que el nombre falso no tenga la misma letra inicial
        # y primera consonante interna que el nombre real
        assume(fake_name.loosely_not_equal(sk.features[0]))

        with self.assertRaises(CURPNameError):
            c = CURP(sk.curp, nombre=fake_name.word)

    @given(CURPStrats.curps(), WordStrats.words())
    def test_creation_first_surname_error(self, sk: CURPSkeleton, fake_name: FeaturedWord) -> None:
        """Prueba la creación de una CURP con un primer apellido incorrecto."""
        # Asumir que el nombre falso no tenga
        # las mismas caracteristicas que el nombre real
        assume(fake_name != sk.features[1])

        with self.assertRaises(CURPFirstSurnameError):
            c = CURP(sk.curp, primer_apellido=fake_name.word)

    @given(CURPStrats.curps(), WordStrats.words())
    def test_creation_second_surname_error(self, sk: CURPSkeleton, fake_name: FeaturedWord) -> None:
        """Prueba la creación de una CURP con un primer apellido incorrecto."""
        # Asumir que el nombre falso no tenga la misma letra inicial
        # y primera consonante interna que el nombre real
        assume(fake_name.loosely_not_equal(sk.features[2]))

        with self.assertRaises(CURPSecondSurnameError):
            c = CURP(sk.curp, segundo_apellido=fake_name.word)

    @given(CURPStrats.curps(), ASCIIStrats.text(min_size=6, max_size=6, lowercase=False))
    def test_creation_date_error(self, sk: CURPSkeleton, d: str)-> None:
        """Prueba la creacion de una CURP con una fecha con caracteres no numericos. """
        assume(any(c not in string.digits for c in d))

        curp = change_curp(sk.curp, date=d)

        with self.assertRaises(CURPValueError) as cm:
            CURP(curp)
        
        self.assertNotIsInstance(cm.exception, CURPDateError)
        self.assertNotIsInstance(cm.exception, CURPVerificationError)

    @given(CURPStrats.curps(), st.integers(0, 99), st.integers(0, 99), st.integers(0, 99))
    def test_creation_date_error_nonexistent_dates(self, sk: CURPSkeleton, y: int, m: int, d: int) -> None:
        """Probar que fechas incorrectas provoquen un error."""
        date_is_valid = False
        century = '19' if sk.curp[-2].isdigit() else '20' 
        
        try:
            date(int(f"{century}{y:02}"), m, d)
        except ValueError:
            pass
        else:
            date_is_valid = True

        assume(not date_is_valid)

        fake_date = f"{y:02}{m:02}{d:02}"
        curp = change_curp(sk.curp, date=fake_date)
        
        with self.assertRaises(CURPDateError):
            CURP(curp)

    @given(CURPStrats.curps(), ASCIIStrats.characters(lowercase=False))
    def test_creation_sex_error(self, sk: CURPSkeleton, s: str) -> None:
        """Probar que códigos incorrectos de sexo provoquen un error."""
        # Solo probar códigos alfanuméricos incorrectos
        assume(s != 'H' and s != 'M')

        curp = change_curp(sk.curp, sex=s)

        with self.assertRaises(CURPSexError):
            CURP(curp)

    @given(CURPStrats.curps(), ASCIIStrats.text(min_size=2, max_size=2, lowercase=False))
    def test_creation_region_error(self, sk: CURPSkeleton, r: str) -> None:
        """Probar que códigos incorrectos de región provoquen un error."""
        # Solo probar códigos alfanuméricos incorrectos
        assume(r not in estados.estados)
    
        curp = change_curp(sk.curp, region=r)
    
        with self.assertRaises(CURPRegionError):
            CURP(curp)
    
    @given(st.text(min_size=18, max_size=18))
    def test_creation_invalid_characters(self, curp: str):
        """Probar que caracteres que no son validos en la CURP provoquen un error. """
        assume(any(c not in self._charset for c in curp))

        with self.assertRaises(CURPValueError) as cm:
            CURP(curp)

        self.assertNotIsInstance(cm.exception, CURPVerificationError)
        self.assertNotIsInstance(cm.exception, CURPLengthError)

    # Pruebas que requieren que el objeto sea construido exitosamente

    @given(CURPStrats.curps())
    def test_curp_property(self, sk: CURPSkeleton) -> None:
        """Prueba que la propiedad CURP sea la correcta."""
        c = CURP(sk.curp)
        self.assertEqual(c.curp, sk.curp)

    @given(CURPStrats.curps())
    def test_default_names_are_null(self, sk: CURPSkeleton) -> None:
        """Prueba que los nombres por defecto sean None."""
        c = CURP(sk.curp)
        self.assertIsNone(c.nombre)
        self.assertIsNone(c.primer_apellido)
        self.assertIsNone(c.segundo_apellido)

    @given(CURPStrats.curps())
    def test_name_property(self, sk: CURPSkeleton) -> None:
        """Prueba la creación de una CURP con un nombre de pila."""
        c = CURP(sk.curp, nombre=sk.name)
        self.assertEqual(c.nombre, sk.name.upper())

    @given(CURPStrats.curps())
    def test_first_surname_property(self, sk: CURPSkeleton) -> None:
        """Prueba la creación de una CURP con primer apellido."""
        c = CURP(sk.curp, primer_apellido=sk.first_surname)
        self.assertEqual(c.primer_apellido, sk.first_surname.upper())

    @given(CURPStrats.curps())
    def test_second_surname_property(self, sk: CURPSkeleton) -> None:
        """Prueba la creación de una CURP con segundo apellido."""
        c = CURP(sk.curp, segundo_apellido=sk.second_surname)
        self.assertEqual(c.segundo_apellido, sk.second_surname.upper())

    @given(CURPStrats.curps())
    def test_name_and_surnames_properties(self, sk: CURPSkeleton) -> None:
        """Prueba la creación de una CURP con nombres/apellidos en los argumentos."""
        c = CURP(
            sk.curp,
            nombre=sk.name,
            primer_apellido=sk.first_surname,
            segundo_apellido=sk.second_surname
        )

        self.assertEqual(c.nombre, sk.name.upper())
        self.assertEqual(c.primer_apellido, sk.first_surname.upper())
        self.assertEqual(c.segundo_apellido, sk.second_surname.upper())

    @given(CURPStrats.curps())
    def test_birth_date_property(self, sk: CURPSkeleton) -> None:
        """Prueba que la extracción de la fecha de nacimiento de la CURP funcione."""
        c = CURP(sk.curp)
        self.assertEqual(c.fecha_nacimiento, sk.birth_date)

    @given(CURPStrats.curps())
    def test_sex_property(self, sk: CURPSkeleton) -> None:
        """Prueba que la extracción del sexo de la CURP funcione."""
        c = CURP(sk.curp)
        self.assertEqual(c.sexo, sk.sex)

    @given(CURPStrats.curps())
    def test_region_properties(self, sk: CURPSkeleton) -> None:
        """Prueba que la extracción de la entidad federativa de la CURP funcione."""
        c = CURP(sk.curp)
        self.assertEqual(c.entidad, sk.region['name'])
        self.assertEqual(c.entidad_iso, sk.region['iso'])
        self.assertEqual(c.es_extranjero, not bool(sk.region['iso']))

    @given(CURPStrats.curps())
    def test_name_validation(self, sk: CURPSkeleton):
        """Prueba la validación del nombre de pila."""
        c = CURP(sk.curp)
        self.assertTrue(c.nombre_valido(sk.name))

    @given(CURPStrats.curps())
    def test_name_validation_with_compound_name(self, sk: str) -> None:
        """Prueba la comprobación de CURP con un nombre compuesto común."""
        c = CURP(sk.curp)

        # Probar con todos los nombres ignorados
        for n in self._common_names:
            self.assertTrue(c.nombre_valido(f"{n} {sk.name}"))
            self.assertTrue(c.nombre_valido(f"{n.title()} {sk.name}"))
            self.assertTrue(c.nombre_valido(f"{n.lower()} {sk.name}"))

    @given(CURPStrats.curps())
    def test_first_surname_validation(self, sk: CURPSkeleton):
        """Prueba la validación del primer apellido."""
        c = CURP(sk.curp)
        self.assertTrue(c.primer_apellido_valido(sk.first_surname))

    @given(CURPStrats.curps())
    def test_second_surname_validation(self, sk: CURPSkeleton):
        """Prueba la validación del segundo apellido."""
        c = CURP(sk.curp)
        self.assertTrue(c.segundo_apellido_valido(sk.second_surname))

    @given(CURPStrats.curps())
    def test_full_name_validation(self, sk: CURPSkeleton):
        """Prueba la validación del nombre completo."""
        c = CURP(sk.curp)
        self.assertTrue(c.nombre_completo_valido(sk.full_name))

    @given(CURPStrats.curps(), WordStrats.words())
    def test_name_validation_false(self, sk: CURPSkeleton, fake_name: FeaturedWord) -> None:
        """Prueba la creación de una CURP con un nombre de pila incorrecto."""
        # Asumir que el nombre falso no tenga la misma letra inicial
        # y primera consonante interna que el nombre real
        assume(fake_name.loosely_not_equal(sk.features[0]))
        c = CURP(sk.curp)
        self.assertFalse(c.nombre_valido(fake_name.word))

    @given(CURPStrats.curps(), WordStrats.words())
    def test_first_surname_validation_false(self, sk: CURPSkeleton, fake_name: FeaturedWord) -> None:
        """Prueba la creación de una CURP con un primer apellido incorrecto."""
        # Asumir que el nombre falso no tenga la misma letra inicial
        # y primera consonante interna que el nombre real
        assume(fake_name != sk.features[1])
        c = CURP(sk.curp)
        self.assertFalse(c.primer_apellido_valido(fake_name.word))

    @given(CURPStrats.curps(), WordStrats.words())
    def test_second_surname_validation_false(self, sk: CURPSkeleton, fake_name: FeaturedWord) -> None:
        """Prueba la creación de una CURP con un primer apellido incorrecto."""
        # Asumir que el nombre falso no tenga la misma letra inicial
        # y primera consonante interna que el nombre real
        assume(fake_name.loosely_not_equal(sk.features[2]))
        c = CURP(sk.curp)
        self.assertFalse(c.segundo_apellido_valido(fake_name.word))

    @given(CURPStrats.curps())
    def test_json_dump(self, sk: CURPSkeleton):
        """Prueba el método json."""
        c = CURP(sk.curp)

        j = json.loads(c.json())
        self.assertEqual(c.curp, j['curp'])
        self.assertEqual(str(c.fecha_nacimiento), j['fecha_nacimiento'])
        self.assertEqual(c.sexo, j['sexo'])
        self.assertEqual(c.entidad, j['entidad_nacimiento']['name'])
        self.assertEqual(c.entidad_iso, j['entidad_nacimiento']['iso'])

        n = any([x in j for x in ('nombre', 'primer_apellido', 'segundo_apellido')])
        self.assertFalse(n)

    @given(CURPStrats.curps())
    def test_json_dump_name_and_surnames(self, sk: CURPSkeleton):
        """Prueba el método json."""
        c = CURP(
            sk.curp,
            nombre=sk.name,
            primer_apellido=sk.first_surname,
            segundo_apellido=sk.second_surname
        )

        j = json.loads(c.json())
        self.assertEqual(c.nombre, j['nombre'])
        self.assertEqual(c.primer_apellido, j['primer_apellido'])
        self.assertEqual(c.segundo_apellido, j['segundo_apellido'])

    # Pruebas de clase

    @given(st.integers(0))
    def test_static_sum_to_digit(self, s: int):
        """Probar método para convertir suma en dígito verificador."""
        d = CURP._sum_to_verify_digit(s)
        self.assertEqual(len(d), 1)
        self.assertTrue(d.isdigit())

        # Alternativa a mod
        m = int(str(s)[-1])
        m = 10 - m if m else m
        self.assertEqual(str(m), d)

    def test_static_verification_sum(self):
        """Probar la comprobación correcta del dígito de verificación
        cuando la CURP contiene sólo un carácter distinto a cero."""
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

                    # Crear CURP
                    curp = ("0" * (18 - n)) + c + ("0" * (n - 1))
                    cs = CURP._verification_sum(curp)
                    self.assertEqual(sm, cs)

    # Otras pruebas

    # @given(CURPStrats.curps())
    # def test_example(self, g):
    #     print(g)

    # def test_name_validation_with_common_name(self) -> None:
    #     """Probar la comprobación de la CURP con nombres comunes que normalmente
    #     son ignorados cuando el nombre es compuesto."""
    #
    #     for i in CURP._ignored_names:
    #         with self.subTest(i=i):
    #             wf = WordFeatures(i, CURP._ignored_words, CURP._special_chars)
    #
    #             curp = self._template
    #             curp = curp.replace("AAAA", f"AAA{wf.char}")
    #             curp = curp.replace("BBB", f"BB{wf.consonant}")
    #             curp = fix_verification(curp)
    #
    #             c = CURP(curp)
    #             self.assertTrue(c.nombre_valido(i))

    # @given(CURPStrats.curps())
    # def test_creation_with_full_name(self, sk: CURPSkeleton) -> None:
    #     """Prueba la creación con nombre completo como argumento."""
    #     c = CURP(sk.curp, nombre_completo=sk.full_name)
    #     self.assertEqual(c.fecha_nacimiento, sk.birth_date)
    #     self.assertEqual(c.sexo, sk.sex)
    #     self.assertEqual(c.entidad, sk.region['name'])
    #     self.assertEqual(c.entidad_iso, sk.region['iso'])
    #     self.assertEqual(c.es_extranjero, not bool(sk.region['iso']))
    #
    #     self.assertEqual(c.nombre, sk.name.upper())
    #     self.assertEqual(c.primer_apellido, sk.first_surname.upper())
    #     self.assertEqual(c.segundo_apellido, sk.second_surname.upper())
    #


if __name__ == '__main__':
    unittest.main()
