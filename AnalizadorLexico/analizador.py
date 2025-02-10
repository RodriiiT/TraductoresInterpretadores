import re

def analizar_lexicamente(codigo):
    palabras_reservadas = {"class", "public", "static", "void", "int", "String", "if", "else", "for", "while", "return"}
    operadores_aritmeticos = {"+", "-", "*", "/", "%"}
    operadores_asignacion = {"=", "+=", "-=", "*=", "/=", "%="}
    operadores_comparacion = {"==", "!=", "<", ">", "<=", ">="}
    operadores_logicos = {"&&", "||", "!"}
    delimitadores = {";", "{", "}", "(", ")", "[", "]", ","}
    
    comentarios = re.compile(r'//.*|/\*.*?\*/', re.DOTALL)
    
    tokens = []
    codigo = re.sub(comentarios, '', codigo)  # Eliminar comentarios
    
    # Expresión regular para identificar palabras, números y operadores
    patron = r'[a-zA-Z_][a-zA-Z_0-9]*|\d+|==|!=|<=|>=|&&|\|\||[+\-*/%<>=!;{}()\[\],]'

    lineas = codigo.split("\n")  # Dividir el código en líneas
    for num_linea, linea in enumerate(lineas, start=1):
        coincidencias = re.findall(patron, linea)
        for palabra in coincidencias:
            if palabra in palabras_reservadas:
                categoria = "Palabra Reservada"
            elif palabra in operadores_aritmeticos:
                categoria = "Operador Aritmético"
            elif palabra in operadores_asignacion:
                categoria = "Operador de Asignación"
            elif palabra in operadores_comparacion:
                categoria = "Operador de Comparación"
            elif palabra in operadores_logicos:
                categoria = "Operador Lógico"
            elif palabra in delimitadores:
                categoria = "Delimitador"
            elif palabra.isdigit():
                categoria = "Número"
            elif re.match(r'^[a-zA-Z_][a-zA-Z_0-9]*$', palabra):
                categoria = "Identificador"
            else:
                categoria = "Símbolo Desconocido"

            tokens.append((palabra, f"Línea {num_linea}", categoria))

    return tokens

def obtener_errores(codigo):
    errores = []
    palabras_reservadas = {"class", "public", "static", "void", "int", "String", "if", "else", "for", "while", "return"}
    operadores_aritmeticos = {"+", "-", "*", "/", "%"}
    operadores_asignacion = {"=", "+=", "-=", "*=", "/=", "%="}
    operadores_comparacion = {"==", "!=", "<", ">", "<=", ">="}
    operadores_logicos = {"&&", "||", "!"}
    delimitadores = {";", "{", "}", "(", ")", "[", "]", ","}

    patron = r'[a-zA-Z_][a-zA-Z_0-9]*|\d+|==|!=|<=|>=|&&|\|\||[+\-*/%<>=!;{}()\[\],]'
    coincidencias = re.findall(patron, codigo)

    # Detectar palabras clave mal escritas
    for palabra in coincidencias:
        if palabra not in palabras_reservadas and len(palabra) > 1:
            for res in palabras_reservadas:
                if res.startswith(palabra):  # Si la palabra está incompleta, como 'in' -> 'int'
                    errores.append(f"Error: Palabra clave mal escrita '{palabra}' (posiblemente debería ser '{res}')")

    # Detectar errores de declaración incompleta como 'int x 10'
    for palabra in coincidencias:
        if palabra == "int":
            if len(coincidencias) > 1 and "int" in coincidencias and "=" not in coincidencias:
                errores.append("Error: Falta el operador de asignación '=' en la declaración")

    # Verificar errores de operadores y sintaxis
    for palabra in coincidencias:
        if palabra == "=":
            # Verificar si hay una asignación sin un valor a la derecha
            index = coincidencias.index("=")
            if index + 1 >= len(coincidencias) or not coincidencias[index + 1].isdigit():
                errores.append("Error: Asignación incompleta, falta valor a la derecha del '='")

    # Verificar si faltan paréntesis o llaves
    abrir_llave = codigo.count("{")
    cerrar_llave = codigo.count("}")
    abrir_parentesis = codigo.count("(")
    cerrar_parentesis = codigo.count(")")

    if abrir_llave != cerrar_llave:
        errores.append("Error: Faltan llaves de cierre o apertura")
    if abrir_parentesis != cerrar_parentesis:
        errores.append("Error: Faltan paréntesis de cierre o apertura")

    # Verificar bloques vacíos
    # Comprobar si después de un paréntesis o llave hay un bloque vacío (como en "(){ }")
    if re.search(r'\(\s*\)', codigo):  # Paréntesis vacíos
        errores.append("Error: Paréntesis vacíos encontrados")

    if re.search(r'\{\s*\}', codigo):  # Llaves vacías
        errores.append("Error: Llaves vacías encontradas")

    return errores

# Ejemplo de uso
codigo_ejemplo = """
public class Prueba {
    public static void main(String[] args) {
        int x = 10;
        if (x >= 5) {
            x += 2;
        }
    }
}
"""

tokens = analizar_lexicamente(codigo_ejemplo)
for palabra, linea, categoria in tokens:
    print(f"{palabra} -> {linea}, {categoria}")
print("\n")