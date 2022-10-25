[![License](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)
<p align="center">
    <img src="img/quetzal_logo.png" alt="logo_quetzal">
</p>

## Compilador Quetzal (TC3048) <!-- omit in toc --> 
## Version: 1.2.3 <!-- omit in toc --> 
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
Antes de hacer uso del compilador, asegurate de instalar las librerias de:
- "tabulate" ``` pip install tabulate```
- "pandas" ``` pip install pandas```

Para ejecutar el compilador, ejecuta el comando: 

- ``` py quetzal_compiler.py [OPTIONS]``` en **Windows**
- ``` python3 quetzal_compiler.py [OPTIONS] ``` en **Mac/GNU Linux**

## Comandos:
Uso: quetzal_compiler.py [OPTIONS]

Options:

  -f, --file PATH  La ruta al archivo a compilar [requerido si el modo de **test** no esta activado]

  -t, --test PATH  Ejecuta el compilador con todos los archivos de prueba en esta carpeta [requerido si el modo **file** no esta activado]

  -d, --debug      Activa el modo debug para mostrar informacion detallada del proceso

  -v, --version    Muestra la version actual del compilador

  --help           Muestra los comandos disponibles

## Procedimiento

Pasos que sigue el proyecto para compilar un programa en Quetzal:
1. Analizar el programa en Quetzal y generar una tabla de sintaxis. Para eso se realizan los siguientes pasos mediante el código lexical_reader.py (El orden es importante):
    1. Leer el archivo de entrada y separarlo en filas y se mandan a la función de separación de tokens.
    2. Se verifica que la linea ingresada no sea una linea vacia. Si lo es, se ignora.
    3. Se verifica, en el siguiente orden, si la linea es un token de tipo y se sustituye por una variable temporal: 
        * Escaped Character
        * Unicode Character
        * Character
        * String
        * Double operator
    4. Se buscan comentarios en la linea y se eliminan.
    5. Se separa la linea analizada por espacios en blanco y se guardan en una lista.
    6. Se separa la lista anterior por caracteres especiales y se guarda en una lista.
    7. Se recorre la lista anterior y se verifica uno por uno el tipo de token que es. Creando una lista de tokens con su respectivo tipo y valor

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