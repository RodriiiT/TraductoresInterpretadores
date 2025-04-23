# analizador_sintactico.py
from graphviz import Digraph
from analizador_lexico import analizar_lexicamente

def generar_arbol_sintactico(codigo: str):
    """
    Genera un árbol sintáctico a modo de ejemplo, utilizando los tokens obtenidos 
    del análisis léxico para construir una estructura sencilla.
    """
    # Obtener la lista de tokens del código
    tokens = analizar_lexicamente(codigo)
    
    dot = Digraph(comment='Árbol Sintáctico')
    dot.node('A', 'Programa')

    # --- Nodo para la definición de la clase ---
    # Buscamos la palabra reservada "class" y asumimos que el siguiente token es el nombre de la clase.
    clase_index = None
    for i, token in enumerate(tokens):
        if token[0] == "class":
            clase_index = i
            break
    if clase_index is not None and clase_index + 1 < len(tokens):
        nombre_clase = tokens[clase_index + 1][0]
        dot.node('B', f'Clase: {nombre_clase}')
    else:
        dot.node('B', 'Clase: Desconocida')
    dot.edge('A', 'B')

    # --- Nodo para el método main ---
    # Buscamos el token "main" para identificar el método principal.
    main_index = None
    for i, token in enumerate(tokens):
        if token[0] == "main":
            main_index = i
            break
    if main_index is not None:
        dot.node('C', 'Método: main')
    else:
        dot.node('C', 'Método: Desconocido')
    dot.edge('B', 'C')

    # --- Nodo para una declaración de variable ---
    # Buscamos el token "int" y asumimos la siguiente secuencia: int, identificador, '=', valor, ';'
    int_index = None
    for i, token in enumerate(tokens):
        if token[0] == "int":
            int_index = i
            break
    if int_index is not None and int_index + 4 < len(tokens):
        var = tokens[int_index + 1][0]
        valor = tokens[int_index + 3][0]
        dot.node('D', f'Declaración: int {var} = {valor};')
    else:
        dot.node('D', 'Declaración: No encontrada')
    dot.edge('C', 'D')

    # --- Nodo para la sentencia if ---
    # Buscamos el token "if"
    if_index = None
    for i, token in enumerate(tokens):
        if token[0] == "if":
            if_index = i
            break
    if if_index is not None:
        # En una implementación real, se analizaría la condición. Aquí usamos un ejemplo simplificado.
        dot.node('E', 'Condición: if (x >= 5)')
    else:
        dot.node('E', 'Condición: No encontrada')
    dot.edge('C', 'E')

    # --- Nodo para la sentencia dentro del if ---
    # Buscamos el operador "+=" para identificar la sentencia
    plus_index = None
    for i, token in enumerate(tokens):
        if token[0] == "+=":
            plus_index = i
            break
    if plus_index is not None and plus_index - 1 >= 0 and plus_index + 1 < len(tokens):
        var = tokens[plus_index - 1][0]
        valor = tokens[plus_index + 1][0]
        dot.node('F', f'Sentencia: {var} += {valor};')
    else:
        dot.node('F', 'Sentencia: No encontrada')
    dot.edge('E', 'F')

    # Guardamos y generamos la imagen del árbol en formato PNG.
    dot.render('arbol_sintactico', format='png', cleanup=True)