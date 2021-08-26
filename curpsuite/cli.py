#!/usr/bin/env python3

import argparse
from .curp import CURP, CURPValueError


def main() -> int:
    parser = argparse.ArgumentParser(
        'curp',
        description='Extraer datos de una CURP y validarla.')

    parser.add_argument('curp', help='la curp a analizar')
    parser.add_argument('-n', '--nombre', help='nombre de pila para validar la CURP')
    parser.add_argument('-p', '--primer-apellido', help='primer apellido para validar la CURP')
    parser.add_argument('-s', '--segundo-apellido', help='segundo apellido para validar la CURP')
    parser.add_argument('-c', '--nombre-completo', help='nombre completo para validar la CURP')

    args = parser.parse_args()

    if args.curp is not None:
        try:
            c = CURP(
                args.curp,
                nombre=args.nombre,
                primer_apellido=args.primer_apellido,
                segundo_apellido=args.segundo_apellido,
                nombre_completo=args.nombre_completo
            )
        except CURPValueError as e:
            print(e)
        else:
            print(c.json())
    return 0


if __name__ == '__main__':
    exit(main())
