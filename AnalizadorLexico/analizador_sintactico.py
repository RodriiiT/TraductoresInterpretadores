# analizador_sintactico.py
from graphviz import Digraph

def generar_arbol_sintactico(codigo: str):
    """
    Función que recibe un código Java y genera un árbol sintáctico a modo de ejemplo.
    Aquí podrías implementar la lógica de análisis sintáctico real.
    """
    dot = Digraph(comment='Árbol Sintáctico')

    # Nodo raíz (por ejemplo, el programa completo)
    dot.node('A', 'Programa')

    # Suponiendo que el código se compone de una clase, un método y algunas sentencias:
    dot.node('B', 'Clase: Prueba')
    dot.edge('A', 'B')

    dot.node('C', 'Método: main')
    dot.edge('B', 'C')

    dot.node('D', 'Declaración: int x = 10;')
    dot.edge('C', 'D')

    dot.node('E', 'Condición: if (x >= 5)')
    dot.edge('C', 'E')

    dot.node('F', 'Sentencia: x += 2;')
    dot.edge('E', 'F')

    # Aquí podrías parsear el código real para generar un árbol más detallado,
    # usando el input en "codigo". Este ejemplo es estático.
    
    # Guardar el gráfico en un archivo PNG
    dot.render('arbol_sintactico', format='png', cleanup=True)
