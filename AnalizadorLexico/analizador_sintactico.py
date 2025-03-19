from analizador_lexico import analizar_lexicamente, obtener_errores

def analizar_sintactico(codigo):
    """
    Esta función realiza un análisis sintáctico muy simplificado del código.
    Se espera que el código tenga la siguiente estructura:
    
      public class NombreClase {
          public static void main(String[] args) {
              // declaraciones: ejemplo: int x = 10;
              // if (condición) { ... }
              // asignaciones: ejemplo: x += 2;
          }
      }
    """
    tokens = analizar_lexicamente(codigo)
    pos = 0
    errores = []

    def current():
        nonlocal pos
        if pos < len(tokens):
            return tokens[pos][0]  # retornar la cadena del token
        return None

    def consume(expected):
        nonlocal pos
        if pos < len(tokens) and tokens[pos][0] == expected:
            pos += 1
            return True
        else:
            linea = tokens[pos][1] if pos < len(tokens) else "EOF"
            encontrado = tokens[pos][0] if pos < len(tokens) else "EOF"
            errores.append(f"Error en {linea}: se esperaba '{expected}', encontrado '{encontrado}'")
            return False

    # --- Inicio del análisis sintáctico ---
    # Se espera: public class <Identificador> {
    if current() == "public":
        consume("public")
    else:
        errores.append("Se esperaba 'public' al inicio de la clase")
    if current() == "class":
        consume("class")
    else:
        errores.append("Se esperaba 'class' después de 'public'")
    # Se espera el nombre de la clase (identificador)
    if pos < len(tokens) and tokens[pos][2] == "Identificador":
        consume(tokens[pos][0])
    else:
        errores.append("Se esperaba el nombre de la clase (identificador)")
    if current() == "{":
        consume("{")
    else:
        errores.append("Se esperaba '{' para abrir la clase")

    # Buscar el método main dentro de la clase
    found_main = False
    while pos < len(tokens) and current() != "}":
        # Si se detecta el inicio de un método con 'public'
        if current() == "public":
            consume("public")
            if current() == "static":
                consume("static")
            else:
                errores.append("Se esperaba 'static' en la declaración del método")
            if current() == "void":
                consume("void")
            else:
                errores.append("Se esperaba 'void' en la declaración del método")
            if current() == "main":
                consume("main")
                found_main = True
            else:
                errores.append("Se esperaba 'main' como nombre del método")
            if current() == "(":
                consume("(")
            else:
                errores.append("Se esperaba '(' en la declaración del método")
            # Se espera la declaración de parámetros: String [ ] identificador
            if current() == "String":
                consume("String")
            else:
                errores.append("Se esperaba 'String' en la declaración de parámetros")
            if current() == "[":
                consume("[")
            else:
                errores.append("Se esperaba '[' en la declaración de parámetros")
            if current() == "]":
                consume("]")
            else:
                errores.append("Se esperaba ']' en la declaración de parámetros")
            if pos < len(tokens) and tokens[pos][2] == "Identificador":
                consume(tokens[pos][0])
            else:
                errores.append("Se esperaba un identificador como nombre del parámetro")
            if current() == ")":
                consume(")")
            else:
                errores.append("Se esperaba ')' al cerrar la declaración de parámetros")
            # Se espera la apertura del cuerpo del método
            if current() == "{":
                consume("{")
                # Analizar las declaraciones/instrucciones del método main
                while pos < len(tokens) and current() != "}":
                    # Declaración de variable: int identificador = número ;
                    if current() == "int":
                        consume("int")
                        if pos < len(tokens) and tokens[pos][2] == "Identificador":
                            consume(tokens[pos][0])
                        else:
                            errores.append("Se esperaba un identificador en la declaración de variable")
                        if current() == "=":
                            consume("=")
                        else:
                            errores.append("Se esperaba '=' en la declaración de variable")
                        if pos < len(tokens) and tokens[pos][2] == "Número":
                            consume(tokens[pos][0])
                        else:
                            errores.append("Se esperaba un número en la asignación de variable")
                        if current() == ";":
                            consume(";")
                        else:
                            errores.append("Se esperaba ';' al final de la declaración de variable")
                    # Sentencia if: if ( condición ) { ... } [else { ... }]
                    elif current() == "if":
                        consume("if")
                        if current() == "(":
                            consume("(")
                        else:
                            errores.append("Se esperaba '(' en la sentencia if")
                        # Para la condición se espera: identificador, operador relacional, número o identificador
                        if pos < len(tokens) and tokens[pos][2] == "Identificador":
                            consume(tokens[pos][0])
                        else:
                            errores.append("Se esperaba un identificador en la condición del if")
                        if current() in {">=", "<=", ">", "<", "==", "!="}:
                            consume(current())
                        else:
                            errores.append("Se esperaba un operador relacional en el if")
                        if pos < len(tokens) and (tokens[pos][2] == "Número" or tokens[pos][2] == "Identificador"):
                            consume(tokens[pos][0])
                        else:
                            errores.append("Se esperaba un número o identificador en la condición del if")
                        if current() == ")":
                            consume(")")
                        else:
                            errores.append("Se esperaba ')' en la sentencia if")
                        if current() == "{":
                            consume("{")
                            # Sentencias dentro del bloque del if (se espera asignación: identificador (+=, etc.) número ;)
                            while pos < len(tokens) and current() != "}":
                                if pos < len(tokens) and tokens[pos][2] == "Identificador":
                                    consume(tokens[pos][0])
                                    if current() in {"+=", "-=", "*=", "/=", "="}:
                                        consume(current())
                                    else:
                                        errores.append("Se esperaba un operador de asignación en la sentencia del if")
                                    if pos < len(tokens) and tokens[pos][2] == "Número":
                                        consume(tokens[pos][0])
                                    else:
                                        errores.append("Se esperaba un número en la asignación dentro del if")
                                    if current() == ";":
                                        consume(";")
                                    else:
                                        errores.append("Se esperaba ';' al final de la instrucción dentro del if")
                                else:
                                    errores.append(f"Instrucción no reconocida en el bloque del if: {current()}")
                                    pos += 1
                            if current() == "}":
                                consume("}")
                            else:
                                errores.append("Se esperaba '}' para cerrar el bloque del if")
                        else:
                            errores.append("Se esperaba '{' para abrir el bloque del if")
                        # Opcionalmente se puede reconocer un bloque else (se omite el análisis detallado)
                        if current() == "else":
                            consume("else")
                            if current() == "{":
                                consume("{")
                                # Se omiten detalles; simplemente se salta hasta la '}'
                                while pos < len(tokens) and current() != "}":
                                    pos += 1
                                if current() == "}":
                                    consume("}")
                                else:
                                    errores.append("Se esperaba '}' para cerrar el bloque del else")
                            else:
                                errores.append("Se esperaba '{' para abrir el bloque del else")
                    # Asignación fuera del if: identificador (+=, etc.) número ;
                    elif pos < len(tokens) and tokens[pos][2] == "Identificador":
                        consume(tokens[pos][0])
                        if current() in {"+=", "-=", "*=", "/=", "="}:
                            consume(current())
                        else:
                            errores.append("Se esperaba un operador de asignación en la instrucción")
                        if pos < len(tokens) and tokens[pos][2] == "Número":
                            consume(tokens[pos][0])
                        else:
                            errores.append("Se esperaba un número en la asignación")
                        if current() == ";":
                            consume(";")
                        else:
                            errores.append("Se esperaba ';' al final de la asignación")
                    else:
                        errores.append(f"Instrucción no reconocida: {current()}")
                        pos += 1
                if current() == "}":
                    consume("}")
                else:
                    errores.append("Se esperaba '}' para cerrar el cuerpo del método main")
            else:
                errores.append("Se esperaba '{' para abrir el cuerpo del método")
        else:
            # Si no se reconoce una declaración de método, se avanza
            pos += 1

    if current() == "}":
        consume("}")
    else:
        errores.append("Se esperaba '}' para cerrar la clase")

    if not found_main:
        errores.append("No se encontró el método main")

    return errores if errores else ["Análisis sintáctico exitoso"]