[![License](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)
<p align="center">
    <img src="img/quetzal_logo.png" alt="logo_quetzal">
</p>

## Compilador Quetzal (TC3048) <!-- omit in toc --> 
## Version: 1.2.1 <!-- omit in toc --> 
## Tabla de contenidos <!-- omit in toc --> 
- [Introduccion](#introduccion)
- [Modo de uso](#modo-de-uso)
- [Procedimiento](#procedimiento)
- [Licencia](#licencia)
- [Autores](#autores)


## Introduccion
Compilador para el lenguaje quetzal como parte de la materia **Desarrollo de compiladores (TC3048)** del Tecnol&oacute;gico de Monterrey campus Cuernavaca en el semestre de agosto diciembre de 2022. 
Lenguaje consultado en: https://arielortiz.info/s202211/tc3048/quetzal/quetzal_language_spec.html 
El compilador esta implementado en Python 3.10.4

## Modo de uso
Antes de hacer uso del compilador, asegurate de instalar la libreria de "tabulate" ``` pip install tabulate```
Para ejecutar el compilador, ejecuta el comando: 

- ``` py main.py ``` en **Windows**
- ``` python3 main.py ``` en **Mac/GNU Linux**

Para mostrar una version detallada del procedimiento interno del compilador añade el parametro "debug" al comando anterior:

- ``` py main.py debug ``` en **Windows**
- ``` python3 main.py debug ``` en **Mac/GNU Linux**

## Procedimiento

Pasos que sigue el proyecto para compilar un programa en Quetzal:
1. Analizar el programa en Quetzal y generar una tabla de sintaxis.
    Para eso se realizan los siguientes pasos mediante el código lexical_reader.py (El orden es importante):
    1.1.- Si la linea contiene un TP_STRING         lo remplaza por una palabra reservada con un espacio en blanco al inicio y al final 
    1.2.-            "            TP_CHAR                                                          "
    1.3.- Si la linea es un comentario, lo ignora y regresa una lista vacia para continuar con la siguiente linea
    1.4.- Se verifican todos los OPERADORES DOBLES y se remplazan por una palabra reservada con un espacio en blanco al inicio y al final
        NOTA: Todos los tokens cuentan con un espacio al inicio y al final para poder separarse correctamente en procesos posteriores
    1.7.- Separamos la linea en tokens, aprovechando los espacios en blanco que se agregaron en los pasos anteriores y obtenemos una lista de tokens
    1.8.- Se recorre la lista de tokens y se verifica si tienen un caracter especial, si es asi se separa en dos tokens diferentes
    1.9.- Se recorre nuevamente la lista de tokens y se detecta el tipo de token al que pertenece cada uno
    1.10.- Se regresa la lista de tokens_type que genera la tabla de sintaxis que contiene la informacion de cada token y su tipo -> {token, token_type}

## Licencia
``` 
   Copyright 2022, KRI-EIGHT. 

   Licensed under the Apache License, Version 2.0 (the "License");
   you may not use this file except in compliance with the License.
   You may obtain a copy of the License at

       https://www.apache.org/licenses/LICENSE-2.0

   Unless required by applicable law or agreed to in writing, software
   distributed under the License is distributed on an "AS IS" BASIS,
   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   See the License for the specific language governing permissions and
   limitations under the License.
```
## Autores
- Rodrigo Sebasti&aacute;n de la Rosa Andr&eacute;s <a href="https://github.com/RodrigoSebastian"><img src="img/git.png" height="15rem" style="margin-left: 2rem;"></a>
- Israel Sanchez Hinojosa <a href="https://github.com/Isra-14"><img src="img/git.png" height="15rem" style="margin-left: 2rem;"></a>
- Antonio Misael Delgado Salmer&oacute;n <a href="https://github.com/MisaDelgado10"><img src="img/git.png" height="15rem" style="margin-left:2rem;"></a>