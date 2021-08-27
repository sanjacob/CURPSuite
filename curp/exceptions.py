"""
Clases de excepciones de CURP Suite
"""


# Clase base
class CURPValueError(ValueError):
    """Indica que la validación de la CURP presentó errores."""


class CURPLengthError(CURPValueError):
    """La CURP no tiene la longitud correcta de 18 caracteres."""


class CURPVerificationError(CURPValueError):
    """El dígito verificador de la CURP no es el calculado."""


class CURPNameError(CURPValueError):
    """El nombre provisto no corresponde a la CURP."""


class CURPFirstSurnameError(CURPValueError):
    """El primer apellido provisto no corresponde a la CURP."""


class CURPSecondSurnameError(CURPValueError):
    """El segundo apellido provisto no corresponde a la CURP."""


class CURPFullNameError(CURPValueError):
    """El nombre completo provisto no corresponde a la CURP."""


class CURPDateError(CURPValueError):
    """La fecha indicada en la CURP es incorrecta."""


class CURPSexError(CURPValueError):
    """El sexo indicado en la CURP no es válido."""


class CURPRegionError(CURPValueError):
    """La entidad federativa indicada en la CURP no es válida."""
