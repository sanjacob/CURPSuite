#!/usr/bin/env python3

"""
CURP Suite
~~~~~~~~~~

CURP Suite es una librería para el análisis y validación de la CURP,
o Clave Única de Registro de Población.

Uso básico:
    >>> from curp import CURP
    >>> c = CURP("SABC560626MDFLRN01")
    >>> c.fecha_nacimiento
    datetime.date(1956, 6, 26)
    >>> c.sexo
    2
    >>> c.entidad_nacimiento
    'Ciudad de México'
    >>> c.entidad_nacimiento_iso
    'MX-CMX'

La documentación completa se encuentra en <https://curpsuite.readthedocs.io>.

:copyright: (c) 2021, Jacob Sánchez Pérez.
:license: GPL v2.0, ver LICENSE para más detalles.
"""

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
# Also available at https://www.gnu.org/licenses/old-licenses/gpl-2.0.html

from .__about__ import __title__, __summary__, __uri__, __version__
from .__about__ import __author__, __email__, __license__
from .__about__ import __copyright__
from .curp import CURP, Sexo
from .exceptions import (CURPValueError, CURPLengthError,
                         CURPVerificationError, CURPNameError,
                         CURPFirstSurnameError, CURPSecondSurnameError,
                         CURPFullNameError, CURPDateError, CURPSexError, CURPRegionError)

__all__ = ['__title__', '__summary__', '__uri__', '__version__',
           '__author__', '__email__', '__license__', '__copyright__',
           'CURP', 'Sexo', 'CURPValueError', 'CURPLengthError', 'CURPVerificationError',
           'CURPNameError', 'CURPFirstSurnameError', 'CURPSecondSurnameError',
           'CURPFullNameError', 'CURPDateError', 'CURPSexError', 'CURPRegionError']
