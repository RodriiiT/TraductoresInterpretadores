# analizador_sintactico_completo.py
from graphviz import Digraph
from analizador_lexico import analizar_lexicamente
import re

def generar_arbol_sintactico(codigo: str):
    """
    Genera un árbol sintáctico completo para código Java.
    """
    # Obtener la lista de tokens del código
    tokens = analizar_lexicamente(codigo)
    
    # Crear el grafo
    dot = Digraph(comment='Árbol Sintáctico')
    dot.attr(rankdir='TB')  # Top to Bottom layout
    dot.attr('node', shape='ellipse', style='filled', fillcolor='lightblue')
    
    # Nodo raíz
    dot.node('A', 'Programa')
    
    # Determinar si el código está dentro de una clase o son métodos sueltos
    tiene_clase = False
    for token in tokens:
        if token[0] == "class":
            tiene_clase = True
            break
    
    if tiene_clase:
        # Procesar como código con clases
        procesar_clases(dot, tokens, 'A')
    else:
        # Procesar como métodos sueltos
        procesar_metodos_sueltos(dot, tokens, 'A')
    
    # Guardamos y generamos la imagen del árbol en formato PNG
    try:
        dot.render('arbol_sintactico', format='png', cleanup=True)
        print("Árbol sintáctico generado correctamente: arbol_sintactico.png")
    except Exception as e:
        print(f"Error al generar el árbol: {e}")
        # Intentar guardar el DOT para depuración
        with open('arbol_sintactico.dot', 'w') as f:
            f.write(dot.source)
        print("Se ha guardado el archivo DOT para depuración: arbol_sintactico.dot")
    
    return dot

def procesar_clases(dot, tokens, nodo_padre):
    """
    Procesa las definiciones de clases en el código.
    """
    # ID para las clases
    id_clase = 0
    
    i = 0
    while i < len(tokens):
        if tokens[i][0] == "class":
            id_clase += 1
            nodo_id = f'C{id_clase}'
            
            # Obtener el nombre de la clase
            if i + 1 < len(tokens):
                nombre_clase = tokens[i+1][0]
                dot.node(nodo_id, f'Clase: {nombre_clase}')
                dot.edge(nodo_padre, nodo_id)
                
                # Buscar el cuerpo de la clase (entre llaves)
                j = i + 2
                while j < len(tokens) and tokens[j][0] != "{":
                    j += 1
                
                if j < len(tokens):
                    # Encontramos la llave de apertura, ahora buscamos la de cierre
                    inicio_clase = j
                    llaves_abiertas = 1
                    j += 1
                    
                    while j < len(tokens) and llaves_abiertas > 0:
                        if tokens[j][0] == "{":
                            llaves_abiertas += 1
                        elif tokens[j][0] == "}":
                            llaves_abiertas -= 1
                        j += 1
                    
                    if llaves_abiertas == 0:
                        # Procesar el contenido de la clase
                        fin_clase = j - 1
                        procesar_contenido_clase(dot, tokens[inicio_clase+1:fin_clase], nodo_id)
                
                i = j  # Avanzar al final de la clase
            else:
                i += 1
        else:
            i += 1

def procesar_contenido_clase(dot, tokens, nodo_padre):
    """
    Procesa el contenido de una clase (atributos y métodos).
    """
    # Procesar atributos
    procesar_atributos(dot, tokens, nodo_padre)
    
    # Procesar métodos
    procesar_metodos(dot, tokens, nodo_padre)

def procesar_atributos(dot, tokens, nodo_padre):
    """
    Procesa las declaraciones de atributos de clase.
    """
    # Tipos de datos comunes en Java
    tipos_datos = ["int", "double", "String", "boolean", "float", "char", "long"]
    
    # ID para los atributos
    id_atributo = 0
    
    i = 0
    while i < len(tokens):
        # Buscar patrones de declaración de atributos
        # Ejemplo: private int x;
        if (tokens[i][0] in ["private", "public", "protected"] or tokens[i][0] in tipos_datos) and i + 2 < len(tokens):
            # Verificar si es un método o un atributo
            j = i
            while j < len(tokens) and tokens[j][0] != "(" and tokens[j][0] != ";" and tokens[j][0] != "{":
                j += 1
            
            if j < len(tokens) and tokens[j][0] == ";":
                # Es un atributo
                id_atributo += 1
                nodo_id = f'A{id_atributo}'
                
                # Construir la declaración del atributo
                declaracion = " ".join([tokens[k][0] for k in range(i, j+1)])
                dot.node(nodo_id, f'Atributo: {declaracion}')
                dot.edge(nodo_padre, nodo_id)
                
                i = j + 1
            else:
                i += 1
        else:
            i += 1

def procesar_metodos(dot, tokens, nodo_padre):
    """
    Procesa las definiciones de métodos en la clase.
    """
    # Modificadores de acceso y tipos de retorno
    modificadores = ["public", "private", "protected", "static", "final", "abstract"]
    tipos_retorno = ["void", "int", "double", "String", "boolean", "float", "char", "long"]
    
    # ID para los métodos
    id_metodo = 0
    
    i = 0
    while i < len(tokens):
        # Buscar patrones de declaración de métodos
        # Ejemplo: public void metodo() { ... }
        if (tokens[i][0] in modificadores or tokens[i][0] in tipos_retorno):
            # Verificar si es un método
            j = i
            while j < len(tokens) and tokens[j][0] != "(":
                j += 1
            
            if j < len(tokens) and tokens[j][0] == "(":
                # Es un método
                id_metodo += 1
                nodo_id = f'M{id_metodo}'
                
                # Obtener el nombre del método
                nombre_metodo = tokens[j-1][0]
                
                # Obtener el tipo de retorno y modificadores
                tipo_retorno = None
                for k in range(i, j-1):
                    if tokens[k][0] in tipos_retorno:
                        tipo_retorno = tokens[k][0]
                        break
                
                mods = []
                for k in range(i, j-1):
                    if tokens[k][0] in modificadores and tokens[k][0] != tipo_retorno:
                        mods.append(tokens[k][0])
                
                # Construir la etiqueta del método
                if tipo_retorno:
                    if mods:
                        etiqueta = f'Método: {" ".join(mods)} {tipo_retorno} {nombre_metodo}'
                    else:
                        etiqueta = f'Método: {tipo_retorno} {nombre_metodo}'
                else:
                    if mods:
                        etiqueta = f'Método: {" ".join(mods)} {nombre_metodo}'
                    else:
                        etiqueta = f'Método: {nombre_metodo}'
                
                dot.node(nodo_id, etiqueta)
                dot.edge(nodo_padre, nodo_id)
                
                # Buscar el cuerpo del método
                # Primero encontrar el paréntesis de cierre
                k = j + 1
                parentesis_abiertos = 1
                while k < len(tokens) and parentesis_abiertos > 0:
                    if tokens[k][0] == "(":
                        parentesis_abiertos += 1
                    elif tokens[k][0] == ")":
                        parentesis_abiertos -= 1
                    k += 1
                
                # Luego buscar la llave de apertura
                while k < len(tokens) and tokens[k][0] != "{":
                    k += 1
                
                if k < len(tokens):
                    # Encontramos la llave de apertura, ahora buscamos la de cierre
                    inicio_metodo = k
                    llaves_abiertas = 1
                    k += 1
                    
                    while k < len(tokens) and llaves_abiertas > 0:
                        if tokens[k][0] == "{":
                            llaves_abiertas += 1
                        elif tokens[k][0] == "}":
                            llaves_abiertas -= 1
                        k += 1
                    
                    if llaves_abiertas == 0:
                        # Procesar el contenido del método
                        fin_metodo = k - 1
                        procesar_contenido_metodo(dot, tokens[inicio_metodo+1:fin_metodo], nodo_id)
                
                i = k  # Avanzar al final del método
            else:
                i += 1
        else:
            i += 1

def procesar_metodos_sueltos(dot, tokens, nodo_padre):
    """
    Procesa métodos que no están dentro de una clase.
    """
    # Modificadores de acceso y tipos de retorno
    modificadores = ["public", "private", "protected", "static", "final", "abstract"]
    tipos_retorno = ["void", "int", "double", "String", "boolean", "float", "char", "long"]
    
    # ID para los métodos
    id_metodo = 0
    
    i = 0
    while i < len(tokens):
        # Buscar patrones de declaración de métodos
        if (tokens[i][0] in modificadores or tokens[i][0] in tipos_retorno):
            # Verificar si es un método
            j = i
            while j < len(tokens) and tokens[j][0] != "(":
                j += 1
            
            if j < len(tokens) and tokens[j][0] == "(":
                # Es un método
                id_metodo += 1
                nodo_id = f'M{id_metodo}'
                
                # Obtener el nombre del método
                nombre_metodo = tokens[j-1][0]
                
                # Obtener el tipo de retorno y modificadores
                tipo_retorno = None
                for k in range(i, j-1):
                    if tokens[k][0] in tipos_retorno:
                        tipo_retorno = tokens[k][0]
                        break
                
                mods = []
                for k in range(i, j-1):
                    if tokens[k][0] in modificadores and tokens[k][0] != tipo_retorno:
                        mods.append(tokens[k][0])
                
                # Construir la etiqueta del método
                if tipo_retorno:
                    if mods:
                        etiqueta = f'Método: {" ".join(mods)} {tipo_retorno} {nombre_metodo}'
                    else:
                        etiqueta = f'Método: {tipo_retorno} {nombre_metodo}'
                else:
                    if mods:
                        etiqueta = f'Método: {" ".join(mods)} {nombre_metodo}'
                    else:
                        etiqueta = f'Método: {nombre_metodo}'
                
                dot.node(nodo_id, etiqueta)
                dot.edge(nodo_padre, nodo_id)
                
                # Buscar el cuerpo del método
                # Primero encontrar el paréntesis de cierre
                k = j + 1
                parentesis_abiertos = 1
                while k < len(tokens) and parentesis_abiertos > 0:
                    if tokens[k][0] == "(":
                        parentesis_abiertos += 1
                    elif tokens[k][0] == ")":
                        parentesis_abiertos -= 1
                    k += 1
                
                # Luego buscar la llave de apertura
                while k < len(tokens) and tokens[k][0] != "{":
                    k += 1
                
                if k < len(tokens):
                    # Encontramos la llave de apertura, ahora buscamos la de cierre
                    inicio_metodo = k
                    llaves_abiertas = 1
                    k += 1
                    
                    while k < len(tokens) and llaves_abiertas > 0:
                        if tokens[k][0] == "{":
                            llaves_abiertas += 1
                        elif tokens[k][0] == "}":
                            llaves_abiertas -= 1
                        k += 1
                    
                    if llaves_abiertas == 0:
                        # Procesar el contenido del método
                        fin_metodo = k - 1
                        procesar_contenido_metodo(dot, tokens[inicio_metodo+1:fin_metodo], nodo_id)
                
                i = k  # Avanzar al final del método
            else:
                i += 1
        else:
            i += 1

def procesar_contenido_metodo(dot, tokens, nodo_padre):
    """
    Procesa el contenido de un método (declaraciones, sentencias, etc.).
    """
    # Procesar declaraciones de variables
    procesar_declaraciones_variables(dot, tokens, nodo_padre)
    
    # Procesar sentencias if
    procesar_sentencias_if(dot, tokens, nodo_padre)
    
    # Procesar bucles for
    procesar_bucles_for(dot, tokens, nodo_padre)
    
    # Procesar llamadas a System.out
    procesar_llamadas_system_out(dot, tokens, nodo_padre)
    
    # Procesar sentencias return
    procesar_sentencias_return(dot, tokens, nodo_padre)
    
    # Procesar asignaciones
    procesar_asignaciones(dot, tokens, nodo_padre)

def procesar_declaraciones_variables(dot, tokens, nodo_padre):
    """
    Procesa las declaraciones de variables y las añade al árbol.
    """
    # Tipos de datos comunes en Java
    tipos_datos = ["int", "double", "String", "boolean", "float", "char", "long"]
    
    # ID para los nodos de declaración
    id_declaracion = 0
    
    i = 0
    while i < len(tokens):
        if tokens[i][0] in tipos_datos:
            # Verificar si es una declaración de variable
            j = i + 1
            while j < len(tokens) and tokens[j][0] != ";" and tokens[j][0] != "{":
                j += 1
            
            if j < len(tokens) and tokens[j][0] == ";":
                # Es una declaración de variable
                id_declaracion += 1
                nodo_id = f'D{id_declaracion}'
                
                # Construir la declaración
                declaracion = " ".join([tokens[k][0] for k in range(i, j+1)])
                dot.node(nodo_id, f'Declaración: {declaracion}')
                dot.edge(nodo_padre, nodo_id)
            
            i = j + 1
        else:
            i += 1

def procesar_sentencias_if(dot, tokens, nodo_padre):
    """
    Procesa las sentencias if y las añade al árbol.
    """
    # ID para los nodos if
    id_if = 0
    
    i = 0
    while i < len(tokens):
        if tokens[i][0] == "if":
            id_if += 1
            nodo_id = f'IF{id_if}'
            
            # Buscar la condición entre paréntesis
            j = i + 1
            while j < len(tokens) and tokens[j][0] != "(":
                j += 1
            
            if j < len(tokens):
                # Encontramos el paréntesis de apertura, ahora buscamos el de cierre
                inicio_condicion = j + 1
                parentesis_abiertos = 1
                j += 1
                
                while j < len(tokens) and parentesis_abiertos > 0:
                    if tokens[j][0] == "(":
                        parentesis_abiertos += 1
                    elif tokens[j][0] == ")":
                        parentesis_abiertos -= 1
                    j += 1
                
                if parentesis_abiertos == 0:
                    # Construir la condición
                    fin_condicion = j - 1
                    condicion = " ".join([tokens[k][0] for k in range(inicio_condicion, fin_condicion)])
                    dot.node(nodo_id, f'Condición: if ({condicion})')
                    dot.edge(nodo_padre, nodo_id)
                    
                    # Buscar el bloque del if
                    k = j
                    while k < len(tokens) and tokens[k][0] != "{":
                        k += 1
                    
                    if k < len(tokens):
                        # Encontramos la llave de apertura, ahora buscamos la de cierre
                        inicio_bloque = k + 1
                        llaves_abiertas = 1
                        k += 1
                        
                        while k < len(tokens) and llaves_abiertas > 0:
                            if tokens[k][0] == "{":
                                llaves_abiertas += 1
                            elif tokens[k][0] == "}":
                                llaves_abiertas -= 1
                            k += 1
                        
                        if llaves_abiertas == 0:
                            # Procesar el bloque del if
                            fin_bloque = k - 1
                            bloque_if_id = f'IF_BLOCK{id_if}'
                            dot.node(bloque_if_id, 'Bloque If')
                            dot.edge(nodo_id, bloque_if_id)
                            procesar_contenido_metodo(dot, tokens[inicio_bloque:fin_bloque], bloque_if_id)
                            
                            # Buscar el else si existe
                            l = k
                            while l < len(tokens) and tokens[l][0] != "else":
                                l += 1
                            
                            if l < len(tokens) and tokens[l][0] == "else":
                                # Encontramos un else
                                else_id = f'ELSE{id_if}'
                                dot.node(else_id, 'Else')
                                dot.edge(nodo_id, else_id)
                                
                                # Buscar el bloque del else
                                m = l + 1
                                while m < len(tokens) and tokens[m][0] != "{":
                                    m += 1
                                
                                if m < len(tokens):
                                    # Encontramos la llave de apertura, ahora buscamos la de cierre
                                    inicio_else = m + 1
                                    llaves_abiertas = 1
                                    m += 1
                                    
                                    while m < len(tokens) and llaves_abiertas > 0:
                                        if tokens[m][0] == "{":
                                            llaves_abiertas += 1
                                        elif tokens[m][0] == "}":
                                            llaves_abiertas -= 1
                                        m += 1
                                    
                                    if llaves_abiertas == 0:
                                        # Procesar el bloque del else
                                        fin_else = m - 1
                                        bloque_else_id = f'ELSE_BLOCK{id_if}'
                                        dot.node(bloque_else_id, 'Bloque Else')
                                        dot.edge(else_id, bloque_else_id)
                                        procesar_contenido_metodo(dot, tokens[inicio_else:fin_else], bloque_else_id)
                                        
                                        i = m  # Avanzar al final del else
                                else:
                                    i = l + 1
                            else:
                                i = k  # Avanzar al final del if
                        else:
                            i = k
                    else:
                        i = j
                else:
                    i = j
            else:
                i += 1
        else:
            i += 1

def procesar_bucles_for(dot, tokens, nodo_padre):
    """
    Procesa los bucles for y los añade al árbol.
    """
    # ID para los nodos for
    id_for = 0
    
    i = 0
    while i < len(tokens):
        if tokens[i][0] == "for":
            id_for += 1
            nodo_id = f'FOR{id_for}'
            
            # Buscar la configuración del for entre paréntesis
            j = i + 1
            while j < len(tokens) and tokens[j][0] != "(":
                j += 1
            
            if j < len(tokens):
                # Encontramos el paréntesis de apertura, ahora buscamos el de cierre
                inicio_config = j + 1
                parentesis_abiertos = 1
                j += 1
                
                while j < len(tokens) and parentesis_abiertos > 0:
                    if tokens[j][0] == "(":
                        parentesis_abiertos += 1
                    elif tokens[j][0] == ")":
                        parentesis_abiertos -= 1
                    j += 1
                
                if parentesis_abiertos == 0:
                    # Construir la configuración
                    fin_config = j - 1
                    config = " ".join([tokens[k][0] for k in range(inicio_config, fin_config)])
                    dot.node(nodo_id, f'Bucle: for ({config})')
                    dot.edge(nodo_padre, nodo_id)
                    
                    # Buscar el bloque del for
                    k = j
                    while k < len(tokens) and tokens[k][0] != "{":
                        k += 1
                    
                    if k < len(tokens):
                        # Encontramos la llave de apertura, ahora buscamos la de cierre
                        inicio_bloque = k + 1
                        llaves_abiertas = 1
                        k += 1
                        
                        while k < len(tokens) and llaves_abiertas > 0:
                            if tokens[k][0] == "{":
                                llaves_abiertas += 1
                            elif tokens[k][0] == "}":
                                llaves_abiertas -= 1
                            k += 1
                        
                        if llaves_abiertas == 0:
                            # Procesar el bloque del for
                            fin_bloque = k - 1
                            bloque_for_id = f'FOR_BLOCK{id_for}'
                            dot.node(bloque_for_id, 'Bloque For')
                            dot.edge(nodo_id, bloque_for_id)
                            procesar_contenido_metodo(dot, tokens[inicio_bloque:fin_bloque], bloque_for_id)
                            
                            i = k  # Avanzar al final del for
                        else:
                            i = k
                    else:
                        i = j
                else:
                    i = j
            else:
                i += 1
        else:
            i += 1

def procesar_llamadas_system_out(dot, tokens, nodo_padre):
    """
    Procesa las llamadas a System.out y las añade al árbol.
    """
    # ID para los nodos de System.out
    id_sysout = 0
    
    i = 0
    while i < len(tokens):
        if i + 2 < len(tokens) and tokens[i][0] == "System" and tokens[i+1][0] == "." and tokens[i+2][0] == "out":
            id_sysout += 1
            nodo_id = f'SYSOUT{id_sysout}'
            
            # Buscar el método (println, printf, etc.)
            j = i + 3
            if j < len(tokens) and tokens[j][0] == ".":
                j += 1
                if j < len(tokens):
                    metodo = tokens[j][0]
                    
                    # Buscar los argumentos entre paréntesis
                    k = j + 1
                    while k < len(tokens) and tokens[k][0] != "(":
                        k += 1
                    
                    if k < len(tokens):
                        # Encontramos el paréntesis de apertura, ahora buscamos el de cierre
                        inicio_args = k + 1
                        parentesis_abiertos = 1
                        k += 1
                        
                        while k < len(tokens) and parentesis_abiertos > 0:
                            if tokens[k][0] == "(":
                                parentesis_abiertos += 1
                            elif tokens[k][0] == ")":
                                parentesis_abiertos -= 1
                            k += 1
                        
                        if parentesis_abiertos == 0:
                            # Construir los argumentos
                            fin_args = k - 1
                            args = " ".join([tokens[l][0] for l in range(inicio_args, fin_args)])
                            dot.node(nodo_id, f'System.out.{metodo}({args})')
                            dot.edge(nodo_padre, nodo_id)
                            
                            # Buscar el punto y coma
                            while k < len(tokens) and tokens[k][0] != ";":
                                k += 1
                            
                            i = k + 1  # Avanzar después del punto y coma
                        else:
                            i = k
                    else:
                        i = j + 1
                else:
                    i = j
            else:
                i += 1
        else:
            i += 1

def procesar_sentencias_return(dot, tokens, nodo_padre):
    """
    Procesa las sentencias return y las añade al árbol.
    """
    # ID para los nodos return
    id_return = 0
    
    i = 0
    while i < len(tokens):
        if tokens[i][0] == "return":
            id_return += 1
            nodo_id = f'RETURN{id_return}'
            
            # Buscar el punto y coma
            j = i + 1
            while j < len(tokens) and tokens[j][0] != ";":
                j += 1
            
            if j < len(tokens):
                # Construir la sentencia return
                valor_return = " ".join([tokens[k][0] for k in range(i+1, j)])
                dot.node(nodo_id, f'Return: {valor_return}')
                dot.edge(nodo_padre, nodo_id)
                
                i = j + 1  # Avanzar después del punto y coma
            else:
                i += 1
        else:
            i += 1

def procesar_asignaciones(dot, tokens, nodo_padre):
    """
    Procesa las asignaciones y las añade al árbol.
    """
    # ID para los nodos de asignación
    id_asignacion = 0
    
    # Operadores de asignación
    operadores_asignacion = ["=", "+=", "-=", "*=", "/=", "%="]
    
    i = 0
    while i < len(tokens):
        if i + 2 < len(tokens) and tokens[i+1][0] in operadores_asignacion:
            # Verificar que no es parte de una declaración de variable
            es_declaracion = False
            for j in range(i-1, max(0, i-3), -1):
                if j >= 0 and tokens[j][0] in ["int", "double", "String", "boolean", "float", "char", "long"]:
                    es_declaracion = True
                    break
            
            if not es_declaracion:
                id_asignacion += 1
                nodo_id = f'ASSIGN{id_asignacion}'
                
                # Buscar el punto y coma
                j = i + 2
                while j < len(tokens) and tokens[j][0] != ";":
                    j += 1
                
                if j < len(tokens):
                    # Construir la asignación
                    asignacion = " ".join([tokens[k][0] for k in range(i, j+1)])
                    dot.node(nodo_id, f'Asignación: {asignacion}')
                    dot.edge(nodo_padre, nodo_id)
                    
                    i = j + 1  # Avanzar después del punto y coma
                else:
                    i += 1
            else:
                i += 1
        else:
            i += 1

# Prueba rápida si se ejecuta como script
if __name__ == '__main__':
    codigo_prueba = """
    public class EjemploPatterns {
        public static void main(String[] args) {
            // Variables
            String nombre = "Juan";
            int edad = 30;
            double salario = 2500.75;

            // Imprimir mensaje con printf
            System.out.printf("Nombre: %s | Edad: %d | Salario: %.2f%n", nombre, edad, salario);

            // Condicional
            if (edad > 18) {
                System.out.println("Mayor de edad");
            } else {
                System.out.println("Menor de edad");
            }

            // Bucle for
            for (int i = 0; i < 3; i++) {
                System.out.println("Contador: " + i);
            }
        }
    }
    """
    
    try:
        generar_arbol_sintactico(codigo_prueba)
    except Exception as e:
        print(f"Error al generar el árbol: {e}")