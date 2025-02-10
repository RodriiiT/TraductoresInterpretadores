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
            errores.append(f"Error: Símbolo desconocido '{palabra}'")
            tokens.append((palabra, "Símbolo Desconocido"))


    return tokens

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