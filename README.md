# Validación de CURP y Nombre (CURPValidator)

CURPValidator es una sencilla clase en Python para comparar una **CURP** y un **nombre completo**, y determinar si coinciden. Con la ayuda del CURP, **se obtiene información de que palabras en el nombre corresponden** a los nombres de pila, apellido paterno, y apellido materno.

**Atención**: La clase no toma en cuenta si otras partes de la CURP, como estado, o fecha de nacimiento son válidas, sin embargo, esto no es difícil de incluir.

```python
>>> from CURPValidator import CURPValidator
>>> CURPValidator.validate('POPC990709MGTSRL02', 'CLAUDIA LEONOR POSADA PEREZ')
{'nombre': 'CLAUDIA LEONOR', 'apellido': 'POSADA', 'apellido_m': 'PEREZ'}
	
# Funciona con prefijos como Del, De la, De los, etc
>>> CURPValidator.validate('MAGE981117MMNCRS05', 'ESTEFANIA DE LOS DOLORES MACIAS GARCIA')
{'nombre': 'ESTEFANIA DE LOS DOLORES', 'apellido': 'MACIAS', 'apellido_m': 'GARCIA'}

>>> CURPValidator.validate('MAPS991116MOCRZN07', 'SANDRA DEL CARMEN MARTINEZ DE LA PAZ')
{'nombre': 'SANDRA DEL CARMEN', 'apellido': 'MARTINEZ', 'apellido_m': 'DE LA PAZ'}
	
# Detecta ausencia de un segundo apellido
>>> CURPValidator.validate('TAXA990915MNEMXM06', 'AMBER NICOLE TAMAYO')
{'nombre': 'AMBER NICOLE', 'apellido': 'TAMAYO', 'apellido_m': ''}
	
# Detección de CURPs con palabras altisonantes
>>> CURPValidator.validate('MXME991209MGRRSS07', 'ESMERALDA MARTINEZ MASTACHE ')
{'nombre': 'ESMERALDA', 'apellido': 'MARTINEZ', 'apellido_m': 'MASTACHE'}

# Regresa False en caso de no coincidir el nombre y la curp
>>> CURPValidator.validate('MACD990727MMMCRRN0', 'DANIELA IVETTE MARTINEZ CRUZ')
False
```
	 

Este programa se distribuye bajo la licencia GNU 2.0, más información en el sitio de la [Free Software Foundation](https://www.gnu.org/licenses/old-licenses/gpl-2.0.html) 

