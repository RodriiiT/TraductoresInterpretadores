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
    codigo = re.sub(comentarios, '', codigo)  #Eliminar comentarios
    
    #Expresión regular para identificar palabras, números y operadores
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
    # Otras colecciones para validación (se pueden usar en el futuro)
    operadores_aritmeticos = {"+", "-", "*", "/", "%"}
    operadores_asignacion = {"=", "+=", "-=", "*=", "/=", "%="}
    operadores_comparacion = {"==", "!=", "<", ">", "<=", ">="}
    operadores_logicos = {"&&", "||", "!"}
    delimitadores = {";", "{", "}", "(", ")", "[", "]", ","}

    # Procesar el código línea a línea
    lineas = codigo.split("\n")
    patron = r'[a-zA-Z_][a-zA-Z_0-9]*|\d+|==|!=|<=|>=|&&|\|\||[+\-*/%<>=!;{}()\[\],]'
    
    for num_linea, linea in enumerate(lineas, start=1):
        tokens_line = re.findall(patron, linea)
        
        # 1. Palabras clave mal escritas
        for token in tokens_line:
            if token not in palabras_reservadas and len(token) > 1:
                for r in palabras_reservadas:
                    if r.startswith(token) and token != r:
                        errores.append((num_linea, f"Palabra clave mal escrita '{token}' (posiblemente debería ser '{r}')"))
        
        # 2. Declaración incompleta (por ejemplo: 'int x 10' sin el operador '=')
        if "int" in tokens_line:
            # Si después de 'int' no se encuentra un '=' en la misma línea
            int_indices = [i for i, t in enumerate(tokens_line) if t == "int"]
            for idx in int_indices:
                # Se asume que debe venir un identificador y luego '='
                if idx + 2 < len(tokens_line) and tokens_line[idx+2] != "=":
                    errores.append((num_linea, "Falta el operador de asignación '=' en la declaración"))
        
        # 3. Asignación incompleta: si aparece '=' y el siguiente token no es un número ni un identificador válido
        for i, token in enumerate(tokens_line):
            if token == "=":
                if i+1 >= len(tokens_line):
                    errores.append((num_linea, "Asignación incompleta: falta valor a la derecha del '='"))
                else:
                    siguiente = tokens_line[i+1]
                    if not (siguiente.isdigit() or re.match(r'^[a-zA-Z_][a-zA-Z_0-9]*$', siguiente)):
                        errores.append((num_linea, f"Asignación incompleta: '{siguiente}' no es un valor válido"))
    
    # 4. Comprobación global de llaves y paréntesis
    if codigo.count("{") != codigo.count("}"):
        errores.append((0, "Error: Faltan llaves de cierre o apertura"))
    if codigo.count("(") != codigo.count(")"):
        errores.append((0, "Error: Faltan paréntesis de cierre o apertura"))
    
    # 5. Bloques vacíos (se asume que no se desean)
    if re.search(r'\(\s*\)', codigo):
        errores.append((0, "Error: Paréntesis vacíos encontrados"))
    if re.search(r'\{\s*\}', codigo):
        errores.append((0, "Error: Llaves vacías encontradas"))
    
    return errores