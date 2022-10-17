[Insertar logo aquí]

## Proyecto de Compiladores
## Version: 1.0.0
### Autores:
### - Rodrigo Sebastián de la Rosa Andrés
### - Israel Sanchez Hinojosa
### - Antonio Misael Delgado Salmerón

Basado en: https://arielortiz.info/s202211/tc3048/quetzal/quetzal_language_spec.html

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