.. _contributing:

Contribuciones
==============

Gracias por contribuir a CURP Suite.

Antes de hacer una *pull request* asegúrate de que tu contribución
sea adecuada para este proyecto. Si en duda, abre un *issue* en el
repositorio y pregunta.


Proceso de contribución
-----------------------

Para contribuir al projecto:

* Crea un *fork* del repositorio en GitHub.
* Clona tu repositorio localmente.
* Crea una rama (*branch*) para contener los cambios que hagas.
* Cuando termines, sube tus cambios con ``git push``.
* Finalmente, crea una *pull request* para integrar tus cambios
  con el proyecto.

Si estás intentando arreglar algo menor, como un *typo*, es recomendado
hacer la edición sin dejar GitHub.


Pruebas (Tests)
---------------

Una vez hayas hecho modificaciones al proyecto, es importante
asegurarse de que no hayan alterado la funcionalidad existente.

Para esto, debes ejecutar las pruebas con el comando ``tox``.
::

    $ tox

Si estás agregando algo nuevo, también debes escribir
una prueba correspondiente.

CURP Suite utiliza :py:mod:`unittest` para correr las pruebas,
y :std:doc:`hypothesis <hypothesis:index>` para generar datos de prueba.

También puedes contribuir al proyecto mejorando las pruebas
y estrategias de generación de datos existentes.


Documentación
-------------

Si tus modificaciones necesitan que cambie la documentación,
por favor házlo así.

Mejoras a la documentación existente también serán apreciadas.


Licencia
--------

Al contribuir al proyecto CURP Suite, aceptas que
cualquier código o material que produzcas estará bajo la licencia
GPL v2.


TODO's (pendientes)
-------------------

Esta es una lista de las tareas que posiblemente necesiten
atención.

.. todolist::

