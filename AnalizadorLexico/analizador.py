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
    errores = []
    codigo = re.sub(comentarios, '', codigo)  # Eliminar comentarios
    
    # Expresión regular para identificar palabras, números y símbolos
    patron = r'[a-zA-Z_][a-zA-Z_0-9]*|\d+|==|!=|<=|>=|&&|\|\||[+\-*/%<>=!;{}()\[\],]'
    coincidencias = re.findall(patron, codigo)

    for palabra in coincidencias:
        if palabra in palabras_reservadas:
            tokens.append((palabra, "Palabra Reservada"))
        elif palabra in operadores_aritmeticos:
            tokens.append((palabra, "Operador Aritmético"))
        elif palabra in operadores_asignacion:
            tokens.append((palabra, "Operador de Asignación"))
        elif palabra in operadores_comparacion:
            tokens.append((palabra, "Operador de Comparación"))
        elif palabra in operadores_logicos:
            tokens.append((palabra, "Operador Lógico"))
        elif palabra in delimitadores:
            tokens.append((palabra, "Delimitador"))
        elif palabra.isdigit():
            tokens.append((palabra, "Número"))
        elif re.match(r'^[a-zA-Z_][a-zA-Z_0-9]*$', palabra):
            tokens.append((palabra, "Identificador"))
        else:
            tokens.append((palabra, "Símbolo Desconocido"))

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

resultado = analizar_lexicamente(codigo_ejemplo)
for token in resultado:
    print(token)