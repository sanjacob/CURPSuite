# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor,
# Boston, MA  02110-1301, USA.

# Copyright (C) 2021, Jacob Sánchez Pérez

from enum import IntEnum


class CURPChar(IntEnum):
    """Guarda las posiciones de los datos de la CURP"""
    # Primer Apellido
    SURNAME_A_CHAR = 0
    SURNAME_A_VOWEL = 1
    SURNAME_A_CONSONANT = 13

    # Segundo Apellido
    SURNAME_B_CHAR = 2
    SURNAME_B_CONSONANT = 14

    # Nombre de Pila
    NAME_CHAR = 3
    NAME_CONSONANT = 15

    # Fecha de Nacimiento
    YEAR_0 = 4
    YEAR_1 = 5
    MONTH_0 = 6
    MONTH_1 = 7
    DAY_0 = 8
    DAY_1 = 9

    # Sexo y Entidad Federativa de Nacimiento
    SEX = 10
    REGION_0 = 11
    REGION_1 = 12

    # Homoclave
    HOMONYMY = 16
    VERIFICATION = 17
